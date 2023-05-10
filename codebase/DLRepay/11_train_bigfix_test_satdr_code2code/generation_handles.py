import sys
import pair_patterns
from tqdm import tqdm
sys.path.append('/home/aziz/experiments/problems/gans_for_apr/')
import model_handles
import beam_search_v2


def generate_fixes(buggy_tokenised, fixed_tokenised, cand_num, enc_dec, test_buggy_inputs, max_fixed_len_test, token_int_map, int_token_map, d4j_localised, vocab_size, itrn, gen_dir, test_data):
    if cand_num == 1:
        generated_ints = model_handles.generate_fixed_ints_enc_dec(enc_dec, test_buggy_inputs, max_fixed_len_test,
                                                                   token_int_map, int_token_map)
        generated_codes = model_handles.decode_ints_enc_dec(generated_ints, int_token_map)
        generated_codes = pair_patterns.interpret_ids(generated_codes, d4j_localised, True)
        test_fixed_tokenised = pair_patterns.interpret_ids(fixed_tokenised, d4j_localised)
        write_to_file(itrn, cand_num, gen_dir, test_fixed_tokenised, generated_codes, test_data)
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
        test_fixed_tokenised = pair_patterns.interpret_ids(fixed_tokenised, d4j_localised)
        write_to_file(itrn, cand_num, gen_dir, test_fixed_tokenised, cand_codes, test_data)


def write_to_file(epo, num_of_cands, gen_fldr_name, test_fixed, generated, test_dps):
    # comments = [x[5] for x in test_dps]
    debt_codes = [x[2] for x in test_dps]
    with open("{}/iter_{}_generation.java".format(gen_fldr_name, epo), "w", encoding='utf-8') as f:
        for i, (debt, fixed, gnrtd) in enumerate(zip(debt_codes, test_fixed, generated)):
            # f.write("SATD comment: {}\n".format(' '.join(comment)))
            f.write("Debt code:   {}\n".format(' '.join(debt)))
            f.write("Repaid code: {}\n".format(' '.join(fixed[1:-1])))
            if num_of_cands == 1:
                f.write("Candidate:   {}\n".format(' '.join(gnrtd[1:-1])))
            else:
                for cand in gnrtd:
                    f.write("Candidate:   {}\n".format(' '.join(cand[1:-1])))
            f.write("=============\n")
            f.write("=============\n")
