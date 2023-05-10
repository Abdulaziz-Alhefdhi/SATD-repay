import pickle
import string
import re
import sys
import javalang
import json


def read_files(diff_fname, msg_fname):
    with open(diff_fname, 'r', encoding='utf-8') as df:
        diff_lines = df.read().split('\n')[:-1]
    with open(msg_fname, 'r', encoding='utf-8') as mf:
        messages = mf.read().split('\n')[:-1]

    return diff_lines, messages


def separate_debt_repaid(cleaned_diffs):
    debt, repaid = [], []
    for diff in cleaned_diffs:
        before, after = [], []
        for line in diff:
            if line.startswith("-"):
                before.append(line[2:])
            elif line.startswith("+"):
                after.append(line[2:])
            else:
                before.append(line)
                after.append(line)
        debt.append("\n".join(before))
        repaid.append("\n".join(after))

    return debt, repaid


def process_comments(comment_list):
    processed_comments = []
    for comment in comment_list:
        for char in comment:
            if char not in string.digits+string.ascii_letters:
                comment = comment.replace(char, " ")
        comment = ' '.join(comment.lower().split())
        processed_comments.append(comment)

    return processed_comments


def remove_comments(code, d4j=False):
    code = re.sub('(?s)/\*.*?\*/', '', code)
    code = re.sub('(//[^\n]*)', '', code)

    if not d4j:
        return code
    else:
        code = remove_spaces(code)
        code = code.splitlines()
        no_comments = []
        for line in code:
            if not line.startswith("*"):
                no_comments.append(line)
        return no_comments


def remove_spaces(code):
    """This function removes excessive spaces and keeps necessary ones"""
    code = code.splitlines()  # Split lines
    result = []
    for line in code:
        line = line.strip()
        if len(line) > 0:  # Remove empty lines
            result.append(line)

    return ' '.join(result)


def create_tokenised(code_lines):
    code_streams = [javalang.tokenizer.tokenize(x, ignore_errors=True) for x in code_lines]
    code_tokenised = []
    for code in code_streams:
        code_tokenised.append(" ".join([x.value for x in code]))

    return code_tokenised


def retrieve_data(data_dir):
    # Retrieve BigFix data from disk
    bigfix_diff_lines, bigfix_messages = read_files(f'{data_dir}bigfix.test.diff', f'{data_dir}nngen.bigfix.test.msg')

    # Retrieve NNGen data from disk
    nngen_dir = f"{data_dir}nngen_data/"
    nngen_diff_files = ['cleaned.train.diff', 'cleaned.valid.diff', 'cleaned.test.diff']
    nngen_msg_files = ['cleaned.train.msg', 'cleaned.valid.msg', 'cleaned.test.msg']
    nngen_diff_groups, nngen_msg_groups = [], []
    for diff_file, msg_file in zip(nngen_diff_files, nngen_msg_files):
        diff_lines, messages = read_files(nngen_dir+diff_file, nngen_dir+msg_file)
        nngen_diff_groups.append(diff_lines)
        nngen_msg_groups.append(messages)
    # Ungroup
    nngen_diff_lines_raw = [x for y in nngen_diff_groups for x in y]
    nngen_messages_raw = [x for y in nngen_msg_groups for x in y]
    # Keep only changed files
    nngen_diff_lines, nngen_messages = [], []
    for diff, msg in zip(nngen_diff_lines_raw, nngen_messages_raw):
        if diff.startswith("mmm "):
            nngen_diff_lines.append(diff)
            nngen_messages.append(msg)
    print(f'# NNGen dps with no code changed thus removed: {len(nngen_messages_raw) - len(nngen_messages)}')

    # From <nl> to lines
    bigfix_readable_diffs = [diff.split(" <nl> ")[:-1] for diff in bigfix_diff_lines]  # -1 is for the extra space at the end of the line
    nngen_readable_diffs = [diff.split(" <nl> ")[:-1] for diff in nngen_diff_lines]  # -1 is for the extra space at the end of the line

    # Remove first two metadata lines from each diff
    bigfix_cleaned_diffs = [diff[2:] for diff in bigfix_readable_diffs]
    nngen_cleaned_diffs = [diff[2:] for diff in nngen_readable_diffs]

    # Separate debt code and repaid code
    bigfix_debt, bigfix_repaid = separate_debt_repaid(bigfix_cleaned_diffs)
    nngen_debt, nngen_repaid = separate_debt_repaid(nngen_cleaned_diffs)

    # Retrieve satd_repay data from disk
    with open(data_dir + 'satd_repayment.pkl', 'rb') as pklf:
        df_satd_repayment = pickle.load(pklf)
    # Separate comments, debt, and repaid
    satdr_comments, satdr_debt, satdr_repaid = [], [], []
    for i, row in df_satd_repayment.iterrows():
        satdr_comments.append(row['SATD_Comment'])
        satdr_debt.append(row['Before'])
        satdr_repaid.append(row['After'])

    # Remove java comments from code
    bigfix_debt_no_comments = [remove_comments(x) for x in bigfix_debt]
    bigfix_repaid_no_comments = [remove_comments(x) for x in bigfix_repaid]
    nngen_debt_no_comments = [remove_comments(x) for x in nngen_debt]
    nngen_repaid_no_comments = [remove_comments(x) for x in nngen_repaid]
    satdr_debt_no_comments = [remove_comments(x) for x in satdr_debt]
    satdr_repaid_no_comments = [remove_comments(x) for x in satdr_repaid]

    # Keep in-between spaces, strip lines, remove empty lines, and make one-liners
    bigfix_debt_no_spaces = [remove_spaces(x) for x in bigfix_debt_no_comments]
    bigfix_repaid_no_spaces = [remove_spaces(x) for x in bigfix_repaid_no_comments]
    nngen_debt_no_spaces = [remove_spaces(x) for x in nngen_debt_no_comments]
    nngen_repaid_no_spaces = [remove_spaces(x) for x in nngen_repaid_no_comments]
    satdr_debt_no_spaces = [remove_spaces(x) for x in satdr_debt_no_comments]
    satdr_repaid_no_spaces = [remove_spaces(x) for x in satdr_repaid_no_comments]

    # SATDR codes need tokenisation
    satdr_debt_tokenised = create_tokenised(satdr_debt_no_spaces)
    satdr_repaid_tokenised = create_tokenised(satdr_repaid_no_spaces)

    # Fix quotation issue with BigFix
    bigfix_debt_lq = [x.replace('``', '"') for x in bigfix_debt_no_spaces]
    bigfix_debt_rq = [x.replace("''", '"') for x in bigfix_debt_lq]
    bigfix_repaid_lq = [x.replace('``', '"') for x in bigfix_repaid_no_spaces]
    bigfix_repaid_rq = [x.replace("''", '"') for x in bigfix_repaid_lq]

    # Process comments: Keep only English letters and numbers, remove spaces, and lowercase
    processed_bigfix_messages = process_comments(bigfix_messages)
    processed_nngen_messages = process_comments(nngen_messages)
    processed_satdr_comments = process_comments(satdr_comments)

    # Prepare data for json files
    bigfix_dicts = [{"code": x, "nl": y} for x, y in zip(bigfix_repaid_rq, processed_bigfix_messages)]
    nngen_dicts = [{"code": x, "nl": y} for x, y in zip(nngen_repaid_no_spaces, processed_nngen_messages)]
    satdr_dicts = [{"code": x, "nl": y} for x, y in zip(satdr_repaid_tokenised, processed_satdr_comments)]

    # Prepair code-nl pairs
    # bigfix_tuples = [(x, y) for x, y in zip(bigfix_repaid_rq, processed_bigfix_messages)]
    # nngen_tuples = [(x, y) for x, y in zip(nngen_repaid_no_spaces, processed_nngen_messages)]
    # satdr_tuples = [(x, y) for x, y in zip(satdr_repaid_tokenised, processed_satdr_comments)]

    return bigfix_dicts, satdr_dicts


    # for item in satdr_dicts:
    #     if '"' in item['code'] and "'" in item['code']:
    #         print("=====================")
    #         print(item)

    # with open('data.json', 'w', encoding='utf-8') as data_file:
    #     json.dump(data, data_file, ensure_ascii=False, indent=4)
    # with open("mydata.json", "w") as final:
    #     json.dump(data, final)

    # sys.exit()


    # c, i = 0, 0
    # for item1, item2 in zip(satdr_repaid_no_comments, satdr_repaid_no_spaces):
    #     i += 1
    #     if item1 == item2:
    #         c += 1
    #         print("========================")
    #         print(item1)
    #         print("+++++++++")
    #         print(item2)
    # print("========================")
    # print(f"{c}/{i}")
    # sys.exit()

    # Aggregate data into a training group and a testing group
    # training_data = [(msg, debt, repaid) for msg, debt, repaid in
    #               zip(processed_train_messages, train_debt_no_spaces, train_repaid_no_spaces)]
    # testing_data = [(cmt, debt, repaid) for cmt, debt, repaid in
    #              zip(processed_test_comments, test_debt_no_spaces, test_repaid_no_spaces)]

    # return training_data, testing_data