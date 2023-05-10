# from tqdm import tqdm
import os
from data_handles import remove_comments, remove_spaces, create_tokenised
from difflib import ndiff
import sys
import re
import pickle
import string


def retrieve_data(data_dir):
    # Retrieve data from disk
    with open(data_dir + 'satd_repayment.pkl', 'rb') as pklf:
        df_satd_repayment = pickle.load(pklf)

    # Separate comments, debt, and repaid
    comment_list, debt_list, repaid_list = [], [], []
    for i, row in df_satd_repayment.iterrows():
        comment_list.append(row['SATD_Comment'])
        debt_list.append(row['Before'])
        repaid_list.append(row['After'])

    # Process comments: Keep English letters only, remove spaces, and lowercase
    processed_comments = []
    for comment in comment_list:
        for char in comment:
            if char not in string.ascii_letters:
                comment = comment.replace(char, " ")
        comment = ' '.join(comment.lower().split())
        processed_comments.append(comment)

    # Remove java comments from code
    debt_no_comments = [remove_comments(x) for x in debt_list]
    repaid_no_comments = [remove_comments(x) for x in repaid_list]

    # Keep in-between spaces, strip lines, and remove empty lines
    debt_no_spaces = [remove_spaces(x) for x in debt_no_comments]
    repaid_no_spaces = [remove_spaces(x) for x in repaid_no_comments]


    return processed_comments, debt_no_spaces, repaid_no_spaces


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


# def retrieve_d4j_metadata(root_dir, release, cl):
#     # Version check
#     if release == "2.0.0":
#         folder_name = "defects4j"
#     elif release == "1.2.0":
#         folder_name = "defects4j-1.2.0"
#     else:
#         sys.exit("defects4j version provided is not available")
#     patch_dir = root_dir + folder_name + "/framework/projects/"
#
#     # Collect project IDs (names)
#     project_ids = [project for project in os.listdir(patch_dir) if
#                    os.path.isdir(os.path.join(patch_dir, project)) and project != "lib"]
#
#     # Collect project directories
#     project_dirs = [os.path.join(patch_dir, pid+'/patches/') for pid in project_ids]
#
#     # Collect bug IDs
#     # First, collect file names
#     file_names = []
#     for pdir in project_dirs:
#         file_paths = os.listdir(pdir)
#         file_names.append([fpath for fpath in file_paths if "src" in fpath])
#     # Then, extract bug IDs from file names
#     bug_ids = []
#     for fname in file_names:
#         bug_ids.append([int(x.split(".")[0]) for x in fname])
#
#     # Collect all text from all available patch files (line by line)
#     project_contents = []
#     err_c = 0
#     for i, project in enumerate(project_dirs):
#         file_contents = []
#         for j, src_file in enumerate(file_names[i]):
#             try:
#                 # Using 'ISO-8859-1' to avoid UnicodeDecodeError
#                 with open(project_dirs[i] + src_file, 'r', encoding='ISO-8859-1') as ff:
#                     file_contents.append((bug_ids[i][j], ff.read().split("\n")[:-1]))
#                 # with open(project_dirs[i] + src_file, 'r', encoding='ISO-8859-1') as ff:
#                 #     file_content = ff.read()
#                 # print(file_content)
#                 # content_brushed = remove_comments(file_content, True)
#                 # print("=======")
#                 # print(content_brushed)
#                 # print("=======")
#                 # print("=======")
#                 # file_contents.append((bug_ids[i][j], content_brushed))
#             except UnicodeDecodeError as unidecerr:
#                 print(unidecerr)
#                 err_c += 1
#                 print("Project name: "+project_ids[i]+"\nFile name: "+src_file)
#                 sys.exit("UnicodeDecodeError caught!")
#         project_contents.append(file_contents)
#     # sys.exit()
#     # print("# UnicodeDecodeErrors:", err_c)
#
#     # Collect bug/fixed lines and bug metadata (single-lined pairs)
#     metadata_v1 = []
#     # prohibited_in_context = ('+ ', '- ', '@@ -', 'Index:', '===', 'diff ', 'index ')
#     for j, project in enumerate(project_contents):
#         for content in project:
#             bug_fix_path, con_sl = "", ""
#             for i, line in enumerate(content[1]):
#                 if line.startswith('+++ '):
#                     bug_fix_path = line.split('+++ b/')[1] if line.startswith('+++ b') else line.split()[1]
#                     # print("Bug path:", bug_path)
#                 # elif line.startswith('--- '):
#                 #     fix_path = line.split('--- a/')[1] if line.startswith('--- a') else line.split()[1]
#                     # print("Fix path:", fix_path)
#                 elif line.startswith('@@ -'):
#                     con_info = re.search('@@ (.*) @@', line).group(1)
#                     bug_sl = int(con_info.split()[1].split(",")[0][1:])
#                     bug_con_size = int(con_info.split()[1].split(",")[1])
#                     fix_sl = int(con_info.split()[0].split(",")[0][1:])
#                     fix_con_size = int(con_info.split()[0].split(",")[1])
#                 # elif not line.startswith(prohibited_in_context):
#                 #     context.append(line)
#                     # print("Context line:", line)
#                 elif 1 < i < len(content[1]) - 1 and line.startswith('+ ') and content[1][i - 1].startswith(
#                     '- ') and not (
#                             content[1][i + 1].startswith('+ ') or content[1][i + 1].startswith('- ')) and not (
#                             content[1][i - 2].startswith('- ') or content[1][i - 2].startswith('+ ')):
#                     metadata_v1.append((project_ids[j], content[0], (line[1:].strip(), content[1][i - 1][1:].strip()),
#                                      bug_fix_path, (bug_sl, bug_con_size, fix_sl, fix_con_size)))
#                     # print("metadata point:-")
#                     # print(metadata[-1])
#
#     # # Strip out +/- signs and white spaces
#     # v2metadata = [(pid, bid, (x[1:].strip(), y[1:].strip()), (bp, fp)) for pid, bid, (x, y), (bp, fp) in v1metadata]
#
#     # create tokenised pairs
#     # Aggregate buggy lines and fixed lines separately first
#     buggy_lines = [meta[2][0] for meta in metadata_v1]
#     fixed_lines = [meta[2][1] for meta in metadata_v1]
#     # Create tokenised codes
#     buggy_tokenised = create_tokenised(buggy_lines)
#     fixed_tokenised = create_tokenised(fixed_lines, True)
#
#     # Add tokenised pairs to metadata
#     metadata_tokens = []
#     for i, meta in enumerate(metadata_v1):
#         metadata_tokens.append((meta[0], meta[1], meta[2], (buggy_tokenised[i], fixed_tokenised[i]), meta[3], meta[4]))
#
#     # Retrieve context
#     metadata_context = []
#     for i, meta in enumerate(metadata_tokens):
#         # Define buggy-fixed paths
#         buggy_path = root_dir + "defects4j-1.2.0-bfvs/{}/{}/buggy/{}".format(meta[0].lower(), meta[1], meta[4])
#         fixed_path = root_dir + "defects4j-1.2.0-bfvs/{}/{}/fixed/{}".format(meta[0].lower(), meta[1], meta[4])
#         # Retrieve files, remove last (empty) line, and restrict to context (previous and a few lines ahead)
#         with open(buggy_path, 'r', encoding='ISO-8859-1') as ff:
#             buggy_file = ff.read().split("\n")[:-1][:meta[5][0]+meta[5][1]-1]
#         with open(fixed_path, 'r', encoding='ISO-8859-1') as ff:
#             fixed_file = ff.read().split("\n")[:-1][:meta[5][2]+meta[5][3]-1]
#
#         buggy_file_one_text = "\n".join(buggy_file)
#         fixed_file_one_text = "\n".join(fixed_file)
#         # Remove comments
#         buggy_no_comments = remove_comments(buggy_file_one_text)
#         fixed_no_comments = remove_comments(fixed_file_one_text)
#         # Remove spaces
#         buggy_no_spaces = remove_spaces(buggy_no_comments)
#         fixed_no_spaces = remove_spaces(fixed_no_comments)
#
#         buggy_lines = buggy_no_spaces.splitlines()
#         fixed_lines = fixed_no_spaces.splitlines()
#         # Reverse context
#         buggy_rev = buggy_lines[::-1]
#         fixed_rev = fixed_lines[::-1]
#
#         # Restrict to previous context (from the bug/fix to the beginning of the file)
#         for i, (bl, fl) in enumerate(zip(buggy_rev, fixed_rev)):
#             if bl.strip() == meta[2][0] and fl.strip() == meta[2][1]:
#                 b_prefile_rev, f_prefile_rev = buggy_rev[i+1:], fixed_rev[i+1:]
#                 break
#
#         # From the bug/fix to the containing function, extract the context
#         if re.match("(public|protected|private|static|\s) +[\w\<\>\[\],\s]+\s+(\w+) *\([^\)]*\) *(\{?|[^;])",
#                     metadata_tokens[2][0]):
#         # if re.match(
#         #         "(public|private|static|protected|abstract|native|synchronized) +([a-zA-Z0-9<>._?, ]+) +([a-zA-Z0-9_]+) *\\([a-zA-Z0-9<>\\[\\]._?, \n]*\\) *([a-zA-Z0-9_ ,\n]*) *\\{",
#         #         metadata_tokens[2][0]):
#             # If the bug/fix is actually a method declaration, then no context
#             metadata_context.append((meta[0], meta[1], meta[2], meta[3], meta[4], meta[5], ([""], [""])))
#         else:
#             # If the bug/fix is NOT actually a method declaration
#             bcon_rev, fcon_rev = [], []
#             for line in b_prefile_rev:
#                 if not line.startswith("import") and not line.startswith("package"):
#                     bcon_rev.append(line)
#                 if re.match("(public|protected|private|static|\s) +[\w\<\>\[\],\s]+\s+(\w+) *\([^\)]*\) *(\{?|[^;])", line):
#                 # if re.match("(public|private|static|protected|abstract|native|synchronized) +([a-zA-Z0-9<>._?, ]+) +([a-zA-Z0-9_]+) *\\([a-zA-Z0-9<>\\[\\]._?, \n]*\\) *([a-zA-Z0-9_ ,\n]*) *\\{", line):
#                     break
#             for line in f_prefile_rev:
#                 if not line.startswith("import") and not line.startswith("package"):
#                     fcon_rev.append(line)
#                 if re.match("(public|protected|private|static|\s) +[\w\<\>\[\],\s]+\s+(\w+) *\([^\)]*\) *(\{?|[^;])", line):
#                 # if re.match("(public|private|static|protected|abstract|native|synchronized) +([a-zA-Z0-9<>._?, ]+) +([a-zA-Z0-9_]+) *\\([a-zA-Z0-9<>\\[\\]._?, \n]*\\) *([a-zA-Z0-9_ ,\n]*) *\\{", line):
#                     break
#             metadata_context.append(
#                 (meta[0], meta[1], meta[2], meta[3], meta[4], meta[5], (bcon_rev[:cl][::-1], fcon_rev[:cl][::-1])))
#
#     # Return sorted list of metadata
#     return sorted(metadata_context)
