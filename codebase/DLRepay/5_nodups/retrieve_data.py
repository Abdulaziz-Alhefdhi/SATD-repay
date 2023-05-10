# from tqdm import tqdm
import os
from data_handles import remove_comments, remove_spaces, create_tokenised
from difflib import ndiff
import sys
import re
import pickle
import string


def retrieve_data(data_dir):
    # file_paths = [root+'/'+name for root, dirs, files in os.walk(data_dir) for name in files]
    # debt_paths = [f_path for f_path in file_paths if 'Before' in f_path]
    # repaid_paths = [f_path for f_path in file_paths if 'After' in f_path]
    with open(data_dir + 'satd_repayment.pkl', 'rb') as pklf:
        df_satd_repayment = pickle.load(pklf)

    # debt_data = []
    # for path in debt_paths:
    #     with open(path, 'r', encoding='utf-8') as f:
    #         debt_data.append(f.read())
    # repaid_data = []
    # for path in repaid_paths:
    #     with open(path, 'r', encoding='utf-8') as f:
    #         repaid_data.append(f.read())

    satd_data, repaid_data = [], []
    for i, row in df_satd_repayment.iterrows():
        satd_data.append(row['SATD_Comment'])
        repaid_data.append(row['After'])

    # Process comments. Keep English letters only, remove spaces, and lowercase
    processed_comments = []
    for comment in satd_data:
        for char in comment:
            if char not in string.ascii_letters:
                comment = comment.replace(char, " ")
        comment = ' '.join(comment.lower().split())
        processed_comments.append(comment)

    # Remove java comments from code
    # debt_no_comments = [remove_comments(x) for x in debt_data]
    repaid_no_comments = [remove_comments(x) for x in repaid_data]

    # Keep in-between spaces, strip lines, and remove empty lines
    # debt_no_spaces = [remove_spaces(x) for x in debt_no_comments]
    repaid_no_spaces = [remove_spaces(x) for x in repaid_no_comments]


    # debt_line_groups = [x.split("\n") for x in debt_no_spaces]
    # debt_lines = [" ".join(x) for x in debt_line_groups]

    # One-liners
    # debt_lines = [x.replace("\n", " ") for x in debt_no_spaces]
    # repaid_lines = [x.replace("\n", " ") for x in repaid_no_spaces]

    # for i, item in enumerate(debt_lines):
    #     print(debt_no_spaces[i])
    #     print("+++++")
    #     print(item)
    #     print("======")
    #     print("======")
    #
    # sys.exit()
    # print("# buggy-fixed files processed:", str(len(buggy_no_spaces))+"*2")

    # for item in debt_no_spaces:
    #     print(item)
    #     print("+++")
    # print("===========")
    # print("===========")
    # for item in repaid_no_spaces:
    #     print(item)
    #     print("+++")
    # sys.exit()

    # Calculate diffs between bugs and fixes
    # initial_diffs = [list(ndiff(x.splitlines(), y.splitlines())) for x, y in tqdm(zip(buggy_texts, fixed_texts))]

    # Restrict to one-line difference
    # one_line_diffs = []
    # for diff in tqdm(initial_diffs):
    #     if sum([1 for x in diff if x.startswith('-')]) > 1 or sum([1 for x in diff if x.startswith('+')]) > 1:
    #         continue
    #     one_line_diffs.append(diff)
    # print(len(initial_diffs)-len(one_line_diffs), 'pairs with more than one-line-diff have been removed')
    # print('Current # data points:', len(one_line_diffs))

    # Restrict to modified lines (exclude added/deleted lines)
    # diffs = []
    # for j, diff in enumerate(tqdm(one_line_diffs)):
    #     plus_found, minus_found = False, False
    #     context, minus_line, plus_line = [], "", ""
    #     for i, x in enumerate(diff):
    #         if x.startswith('+'):
    #             plus_found = True
    #             plus_line = x[2:]
    #         elif x.startswith('-'):
    #             minus_found = True
    #             minus_line = x[2:]
    #         elif not x.startswith('?'):
    #             context.append(x[2:])
    #         if plus_found and minus_found:
    #             diffs.append((minus_line, plus_line, context[-cl:]))
                # print("==============")
                # print("\n".join([line for line in one_line_diffs[j]]))
                # print("---")
                # print("Bug:-")
                # print(" ".join(context[-cl:]) + " " + minus_line)
                # print("Fix:-")
                # print(" ".join(context[-cl:]) + " " + plus_line)

                # print("Buggy line:", minus_line)
                # print("Fixed line:", plus_line)
                # print("Context:-")
                # print("\n".join([line for line in context[-cl:]]))
                # break
    # sys.exit()
    # print(sorted(set([len(x[2]) for x in diffs])))
    # c = 0
    # for diff in diffs:
    #     if len(diff[2]) == 2:
    #         print(diff)
    #         c += 1
    # print(c)
    # sys.exit()
    # print(len(one_line_diffs) - len(diffs), 'pairs with addition/deletion diffs have been removed')
    # print('Current # data points:', len(diffs))
    # sys.exit()

    # create tokenised pairs
    # Aggregate buggy lines and fixed lines separately first
    # buggy_lines = [diff[0] for diff in diffs]
    # fixed_lines = [diff[1] for diff in diffs]
    # Create tokenised codes
    # debt_tokenised = create_tokenised(debt_no_spaces)
    # repaid_tokenised = create_tokenised(repaid_no_spaces, True)



    # for i in range(4, len(repaid_dps), 4):
    #     print(repaid_dps[i])
    #     print("+++++")
    #     # print(repaid_dps[i])
    #     # print("=============")
    #     # print("=============")
    # sys.exit()



    # for i, item in enumerate(repaid_no_spaces):
    #     print(item)
    #     print("+++")
    #     print(repaid_tokenised[i])
    #     print("============")
    #     print("============")
    # sys.exit()

    # Add tokenised pairs to training data
    # bug_fix_data_draft = []
    # for i, diff in enumerate(diffs):  # tuple lists to prepare for duplicate removal
    #     bug_fix_data_draft.append((diff[0], tuple(buggy_tokenised[i]), diff[1], tuple(fixed_tokenised[i]), diff[2]))

    # Remove redundant data points, then sort
    # bug_fix_data = sorted(set(bug_fix_data_draft))
    # print(len(bug_fix_data_draft)-len(bug_fix_data), 'redundant data points have been removed')

    # list back tuples
    # return [(w, list(x), y, list(z)) for w, x, y, z in bug_fix_data]
    return processed_comments, repaid_no_spaces


# def retrieve_sequencer_data(data_dir):
#     with open(data_dir + 'tgt-train.txt', 'r', encoding='utf-8') as f:
#         train_fixed_lines = f.read().split('\n')[:-1]
#     with open(data_dir + 'tgt-test.txt', 'r', encoding='utf-8') as f:
#         test_fixed_lines = f.read().split('\n')[:-1]
#     with open(data_dir + 'tgt-val.txt', 'r', encoding='utf-8') as f:
#         val_fixed_lines = f.read().split('\n')[:-1]
#
#     print(len(train_fixed_lines), len(test_fixed_lines), len(val_fixed_lines))
#     sys.exit()
#     return "hi"


def retrieve_d4j_metadata(root_dir, release, cl):
    # Version check
    if release == "2.0.0":
        folder_name = "defects4j"
    elif release == "1.2.0":
        folder_name = "defects4j-1.2.0"
    else:
        sys.exit("defects4j version provided is not available")
    patch_dir = root_dir + folder_name + "/framework/projects/"

    # Collect project IDs (names)
    project_ids = [project for project in os.listdir(patch_dir) if
                   os.path.isdir(os.path.join(patch_dir, project)) and project != "lib"]

    # Collect project directories
    project_dirs = [os.path.join(patch_dir, pid+'/patches/') for pid in project_ids]

    # Collect bug IDs
    # First, collect file names
    file_names = []
    for pdir in project_dirs:
        file_paths = os.listdir(pdir)
        file_names.append([fpath for fpath in file_paths if "src" in fpath])
    # Then, extract bug IDs from file names
    bug_ids = []
    for fname in file_names:
        bug_ids.append([int(x.split(".")[0]) for x in fname])

    # Collect all text from all available patch files (line by line)
    project_contents = []
    err_c = 0
    for i, project in enumerate(project_dirs):
        file_contents = []
        for j, src_file in enumerate(file_names[i]):
            try:
                # Using 'ISO-8859-1' to avoid UnicodeDecodeError
                with open(project_dirs[i] + src_file, 'r', encoding='ISO-8859-1') as ff:
                    file_contents.append((bug_ids[i][j], ff.read().split("\n")[:-1]))
                # with open(project_dirs[i] + src_file, 'r', encoding='ISO-8859-1') as ff:
                #     file_content = ff.read()
                # print(file_content)
                # content_brushed = remove_comments(file_content, True)
                # print("=======")
                # print(content_brushed)
                # print("=======")
                # print("=======")
                # file_contents.append((bug_ids[i][j], content_brushed))
            except UnicodeDecodeError as unidecerr:
                print(unidecerr)
                err_c += 1
                print("Project name: "+project_ids[i]+"\nFile name: "+src_file)
                sys.exit("UnicodeDecodeError caught!")
        project_contents.append(file_contents)
    # sys.exit()
    # print("# UnicodeDecodeErrors:", err_c)

    # Collect bug/fixed lines and bug metadata (single-lined pairs)
    metadata_v1 = []
    # prohibited_in_context = ('+ ', '- ', '@@ -', 'Index:', '===', 'diff ', 'index ')
    for j, project in enumerate(project_contents):
        for content in project:
            bug_fix_path, con_sl = "", ""
            for i, line in enumerate(content[1]):
                if line.startswith('+++ '):
                    bug_fix_path = line.split('+++ b/')[1] if line.startswith('+++ b') else line.split()[1]
                    # print("Bug path:", bug_path)
                # elif line.startswith('--- '):
                #     fix_path = line.split('--- a/')[1] if line.startswith('--- a') else line.split()[1]
                    # print("Fix path:", fix_path)
                elif line.startswith('@@ -'):
                    con_info = re.search('@@ (.*) @@', line).group(1)
                    bug_sl = int(con_info.split()[1].split(",")[0][1:])
                    bug_con_size = int(con_info.split()[1].split(",")[1])
                    fix_sl = int(con_info.split()[0].split(",")[0][1:])
                    fix_con_size = int(con_info.split()[0].split(",")[1])
                # elif not line.startswith(prohibited_in_context):
                #     context.append(line)
                    # print("Context line:", line)
                elif 1 < i < len(content[1]) - 1 and line.startswith('+ ') and content[1][i - 1].startswith(
                    '- ') and not (
                            content[1][i + 1].startswith('+ ') or content[1][i + 1].startswith('- ')) and not (
                            content[1][i - 2].startswith('- ') or content[1][i - 2].startswith('+ ')):
                    metadata_v1.append((project_ids[j], content[0], (line[1:].strip(), content[1][i - 1][1:].strip()),
                                     bug_fix_path, (bug_sl, bug_con_size, fix_sl, fix_con_size)))
                    # print("metadata point:-")
                    # print(metadata[-1])

    # # Strip out +/- signs and white spaces
    # v2metadata = [(pid, bid, (x[1:].strip(), y[1:].strip()), (bp, fp)) for pid, bid, (x, y), (bp, fp) in v1metadata]

    # create tokenised pairs
    # Aggregate buggy lines and fixed lines separately first
    buggy_lines = [meta[2][0] for meta in metadata_v1]
    fixed_lines = [meta[2][1] for meta in metadata_v1]
    # Create tokenised codes
    buggy_tokenised = create_tokenised(buggy_lines)
    fixed_tokenised = create_tokenised(fixed_lines, True)

    # Add tokenised pairs to metadata
    metadata_tokens = []
    for i, meta in enumerate(metadata_v1):
        metadata_tokens.append((meta[0], meta[1], meta[2], (buggy_tokenised[i], fixed_tokenised[i]), meta[3], meta[4]))

    # Retrieve context
    metadata_context = []
    for i, meta in enumerate(metadata_tokens):
        # Define buggy-fixed paths
        buggy_path = root_dir + "defects4j-1.2.0-bfvs/{}/{}/buggy/{}".format(meta[0].lower(), meta[1], meta[4])
        fixed_path = root_dir + "defects4j-1.2.0-bfvs/{}/{}/fixed/{}".format(meta[0].lower(), meta[1], meta[4])
        # Retrieve files, remove last (empty) line, and restrict to context (previous and a few lines ahead)
        with open(buggy_path, 'r', encoding='ISO-8859-1') as ff:
            buggy_file = ff.read().split("\n")[:-1][:meta[5][0]+meta[5][1]-1]
        with open(fixed_path, 'r', encoding='ISO-8859-1') as ff:
            fixed_file = ff.read().split("\n")[:-1][:meta[5][2]+meta[5][3]-1]

        buggy_file_one_text = "\n".join(buggy_file)
        fixed_file_one_text = "\n".join(fixed_file)
        # Remove comments
        buggy_no_comments = remove_comments(buggy_file_one_text)
        fixed_no_comments = remove_comments(fixed_file_one_text)
        # Remove spaces
        buggy_no_spaces = remove_spaces(buggy_no_comments)
        fixed_no_spaces = remove_spaces(fixed_no_comments)

        buggy_lines = buggy_no_spaces.splitlines()
        fixed_lines = fixed_no_spaces.splitlines()
        # Reverse context
        buggy_rev = buggy_lines[::-1]
        fixed_rev = fixed_lines[::-1]

        # Restrict to previous context (from the bug/fix to the beginning of the file)
        for i, (bl, fl) in enumerate(zip(buggy_rev, fixed_rev)):
            if bl.strip() == meta[2][0] and fl.strip() == meta[2][1]:
                b_prefile_rev, f_prefile_rev = buggy_rev[i+1:], fixed_rev[i+1:]
                break

        # From the bug/fix to the containing function, extract the context
        if re.match("(public|protected|private|static|\s) +[\w\<\>\[\],\s]+\s+(\w+) *\([^\)]*\) *(\{?|[^;])",
                    metadata_tokens[2][0]):
        # if re.match(
        #         "(public|private|static|protected|abstract|native|synchronized) +([a-zA-Z0-9<>._?, ]+) +([a-zA-Z0-9_]+) *\\([a-zA-Z0-9<>\\[\\]._?, \n]*\\) *([a-zA-Z0-9_ ,\n]*) *\\{",
        #         metadata_tokens[2][0]):
            # If the bug/fix is actually a method declaration, then no context
            metadata_context.append((meta[0], meta[1], meta[2], meta[3], meta[4], meta[5], ([""], [""])))
        else:
            # If the bug/fix is NOT actually a method declaration
            bcon_rev, fcon_rev = [], []
            for line in b_prefile_rev:
                if not line.startswith("import") and not line.startswith("package"):
                    bcon_rev.append(line)
                if re.match("(public|protected|private|static|\s) +[\w\<\>\[\],\s]+\s+(\w+) *\([^\)]*\) *(\{?|[^;])", line):
                # if re.match("(public|private|static|protected|abstract|native|synchronized) +([a-zA-Z0-9<>._?, ]+) +([a-zA-Z0-9_]+) *\\([a-zA-Z0-9<>\\[\\]._?, \n]*\\) *([a-zA-Z0-9_ ,\n]*) *\\{", line):
                    break
            for line in f_prefile_rev:
                if not line.startswith("import") and not line.startswith("package"):
                    fcon_rev.append(line)
                if re.match("(public|protected|private|static|\s) +[\w\<\>\[\],\s]+\s+(\w+) *\([^\)]*\) *(\{?|[^;])", line):
                # if re.match("(public|private|static|protected|abstract|native|synchronized) +([a-zA-Z0-9<>._?, ]+) +([a-zA-Z0-9_]+) *\\([a-zA-Z0-9<>\\[\\]._?, \n]*\\) *([a-zA-Z0-9_ ,\n]*) *\\{", line):
                    break
            metadata_context.append(
                (meta[0], meta[1], meta[2], meta[3], meta[4], meta[5], (bcon_rev[:cl][::-1], fcon_rev[:cl][::-1])))

    # Return sorted list of metadata
    return sorted(metadata_context)
