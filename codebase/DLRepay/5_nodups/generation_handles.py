import os
import sys
import subprocess
import data_handles
import pair_patterns
# from train_bigfix_test_defects4j.correct_defects4j_data.encdec_5_abstract_ids import pair_patterns
from tqdm import tqdm
sys.path.append('/home/aziz/experiments/problems/gans_for_apr/')
import model_handles
import beam_search_v2


def generate_fixes(buggy_tokenised, fixed_tokenised, cand_num, enc_dec, test_buggy_inputs, max_fixed_len_test, token_int_map, int_token_map, d4j_localised, vocab_size, itrn, gen_dir):
    if cand_num == 1:
        generated_ints = model_handles.generate_fixed_ints_enc_dec(enc_dec, test_buggy_inputs, max_fixed_len_test,
                                                                   token_int_map, int_token_map)
        generated_codes = model_handles.decode_ints_enc_dec(generated_ints, int_token_map)
        generated_codes = pair_patterns.interpret_ids(generated_codes, d4j_localised, True)
        test_buggy_tokenised = pair_patterns.interpret_ids(buggy_tokenised, d4j_localised)
        test_fixed_tokenised = pair_patterns.interpret_ids(fixed_tokenised, d4j_localised)
        write_to_file(itrn, cand_num, gen_dir, test_buggy_tokenised, test_fixed_tokenised, generated_codes)
        # for i, (buggy, fixed, gnrtd) in enumerate(zip(test_buggy_tokenised, test_fixed_tokenised, generated_codes)):
        #     print('=============')
        #     print('=============')
        #     print('SATD comment:', ' '.join(buggy))
        #     print('---')
        #     print('Repaid code: ', ' '.join(fixed[1:-1]))
        #     print('Candidate:   ', ' '.join(gnrtd[1:-1]))

            # Chart 1 & Chart 7 have weird patch files. Skip them
            # if (d4j_meta[i][0] != "Chart" or d4j_meta[i][1] != 1) and (
            #         d4j_meta[i][0] != "Chart" or d4j_meta[i][1] != 7):
            #     compile_d4j(data_dir, d4j_meta, i, ' '.join(gnrtd[1:-1]))
            # if d4j_meta[i][0] == "Chart" and d4j_meta[i][1] == 8:
            #     sys.exit("Terminate")
    else:
        generated_probs = beam_search_v2.generate_fixed_ints(enc_dec, test_buggy_inputs, max_fixed_len_test,
                                                             token_int_map, int_token_map, test=True, v_size=vocab_size)
        gnrtd_cands = [beam_search_v2.cand_gnrtr_beam(test_dp, cand_num, token_int_map) for test_dp in
                       tqdm(generated_probs)]
        cand_codes = [beam_search_v2.decode_ints(cand, int_token_map) for cand in gnrtd_cands]
        cand_patches = []
        for i in range(cand_num):
            patch_slice = []
            for cand_group in cand_codes:
                patch_slice.append(cand_group[i])
            cand_patches.append(patch_slice)
        cand_patches = [pair_patterns.interpret_ids(cand_slice, d4j_localised, True) for cand_slice in cand_patches]
        cand_codes = []
        for i in range(len(buggy_tokenised)):
            cand_group = []
            for patch_slice in cand_patches:
                cand_group.append(patch_slice[i])
            cand_codes.append(cand_group)
        test_buggy_tokenised = pair_patterns.interpret_ids(buggy_tokenised, d4j_localised)
        test_fixed_tokenised = pair_patterns.interpret_ids(fixed_tokenised, d4j_localised)
        write_to_file(itrn, cand_num, gen_dir, test_buggy_tokenised, test_fixed_tokenised, cand_codes)
        # for i, (buggy, fixed, cand_group) in enumerate(zip(test_buggy_tokenised, test_fixed_tokenised, cand_codes)):
        #     print('=============')
        #     print('=============')
        #     print('SATD comment:', ' '.join(buggy))
        #     print('Repaid code: ', ' '.join(fixed[1:-1]))
        #     for cand in cand_group:
        #         print('Candidate:   ', ' '.join(cand[1:-1]))


def compile_d4j(data_path, d4j_md, j, gnrtd_cand):
    # Declare vars
    proj_id, bid = d4j_md[j][0], d4j_md[j][1]
    proj_dir = data_path + "defects4j-1.2.0-bfvs/{}/{}/buggy".format(proj_id.lower(), bid)
    patch_path = data_path + "defects4j-1.2.0/framework/projects/{}/patches/{}.src.patch".format(proj_id, bid)
    # test_dir = "/tmp/test_{}_{}".format(proj_id.lower(), bid)
    test_dir = "test_syntax/test_{}_{}".format(proj_id.lower(), bid)
    cwd = os.getcwd()  # Current working directory (round-trip)

    c = 0
    try:
        # Retrieve buggy project and patch file
        subprocess.run("cp -r {} {}".format(proj_dir, test_dir).split())
        subprocess.run("cp {} {}".format(patch_path, test_dir).split())
        # Read in patch file
        with open("{}/{}.src.patch".format(test_dir, bid), 'r', encoding='utf-8') as f:
            patch_lines = f.read().split('\n')[:-1]

        # Apply fix in the patch file
        new_patch = []
        for i, line in enumerate(patch_lines):
            if line.startswith("- ") and patch_lines[i + 1].startswith("+ ") and not patch_lines[i - 1].startswith(
                    "- ") and not patch_lines[i + 2].startswith("+ "):
                buggy_tokenised = data_handles.create_tokenised([patch_lines[i + 1][1:].strip()])
                fixed_tokenised = data_handles.create_tokenised([line[1:].strip()], True)
                if buggy_tokenised[0] == d4j_md[j][3][0] and fixed_tokenised[0] == d4j_md[j][3][1]:
                    new_patch.append("- {}".format(gnrtd_cand))
                else:
                    new_patch.append(line)
            else:
                new_patch.append(line)

        # Write patch file again
        with open("{}/{}.src.patch".format(test_dir, bid), 'w', encoding='utf-8') as f:
            for line in new_patch:
                f.write(line + "\n")

        # Examine the patch
        os.chdir(test_dir)  # cd to testing dir
        # subprocess.run("unix2dos {}.src.patch".format(bid).split())  # Convert to dos format!
        # p_file = open("{}.src.patch".format(bid))
        # subprocess.run("patch -Rp1 --binary".format(bid).split(), stdin=p_file)
        p_file = open("{}.src.patch".format(bid))
        subprocess.run("patch -Rp1".format(bid).split(), stdin=p_file)
        subprocess.run("defects4j compile".split())

    except Exception as ex:
        print(ex)
    finally:
        # Clean testing directory
        os.chdir(cwd)  # Return to CWD
        subprocess.run("rm -rf {}".format(test_dir).split())

    # # Create testing directory
    # subprocess.run("cp -r {} {}".format(proj_dir, test_dir).split())
    # subprocess.run("cp {} {}".format(patch_path, test_dir).split())
    # # Compile testing directory
    # os.chdir(test_dir)  # cd to testing dir
    # subprocess.run("defects4j test".split())
    # # Examine the patch
    # p_file = open("{}.src.patch".format(bid))
    # subprocess.run("patch -Rp1".format(bid).split(), stdin=p_file)
    # subprocess.run("defects4j test".split())
    # # Clean testing directory
    # os.chdir(cwd)  # Return to CWD
    # subprocess.run("rm -rf {}".format(test_dir).split())

    return c


def write_to_file(epo, num_of_cands, gen_fldr_name, test_buggy, test_fixed, generated):
    with open("{}/iter_{}_generation.java".format(gen_fldr_name, epo), "w", encoding='utf-8') as f:
        for i, (buggy, fixed, gnrtd) in enumerate(zip(test_buggy, test_fixed, generated)):
            f.write("SATD comment: {}\n".format(' '.join(buggy)))
            f.write("Repaid code:  {}\n".format(' '.join(fixed[1:-1])))
            if num_of_cands == 1:
                f.write("Candidate:    {}\n".format(' '.join(gnrtd[1:-1])))
            else:
                for cand in gnrtd:
                    f.write("Candidate:    {}\n".format(' '.join(cand[1:-1])))
            f.write("=============\n")
            f.write("=============\n")
            # for i, (buggy, fixed, cand_group) in enumerate(zip(test_buggy, test_fixed, generated)):
            #     f.write("SATD comment: {}\n".format(' '.join(buggy)))
            #     f.write("Repaid code:  {}\n".format(' '.join(fixed[1:-1])))
            #     for cand in cand_group:
            #         f.write("Candidate:    {}\n".format(' '.join(cand[1:-1])))
            #     f.write("=============\n")
            #     f.write("=============\n")
