# from tqdm import tqdm
import os
from data_handles import remove_comments, remove_spaces, create_tokenised
from difflib import ndiff
import sys
import re
import pickle
import string


def process_comments(comment_list):
    processed_comments = []
    for comment in comment_list:
        for char in comment:
            if char not in string.ascii_letters:
                comment = comment.replace(char, " ")
        comment = ' '.join(comment.lower().split())
        processed_comments.append(comment)

    return processed_comments



def retrieve_data(data_dir):
    # Retrieve training data from disk
    with open(data_dir + 'bigfix.test.diff', 'r', encoding='utf-8') as df:
        train_diff_lines = df.read().split('\n')[:-1]
    with open(data_dir + 'nngen.bigfix.test.msg', 'r', encoding='utf-8') as mf:
        train_messages = mf.read().split('\n')[:-1]

    # readable_diffs = ["\n".join(diff.split(" <nl> ")[:-1]) for diff in train_diff_lines]
    readable_diffs = [diff.split(" <nl> ")[:-1] for diff in train_diff_lines]  # -1 is for the extra space at the end of the line
    # Remove first two metadata lines
    cleaned_diffs = [diff[2:] for diff in readable_diffs]

    # Separate debt code and repaid code
    train_debt, train_repaid = [], []
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
        train_debt.append("\n".join(before))
        train_repaid.append("\n".join(after))

    # Retrieve testing data from disk
    with open(data_dir + 'satd_repayment.pkl', 'rb') as pklf:
        df_satd_repayment = pickle.load(pklf)

    # Separate comments, debt, and repaid
    test_comments, test_debt, test_repaid = [], [], []
    for i, row in df_satd_repayment.iterrows():
        test_comments.append(row['SATD_Comment'])
        test_debt.append(row['Before'])
        test_repaid.append(row['After'])

    # Process comments: Keep English letters only, remove spaces, and lowercase
    processed_train_messages = process_comments(train_messages)
    processed_test_comments = process_comments(test_comments)

    # Remove java comments from code
    train_debt_no_comments = [remove_comments(x) for x in train_debt]
    train_repaid_no_comments = [remove_comments(x) for x in train_repaid]
    test_debt_no_comments = [remove_comments(x) for x in test_debt]
    test_repaid_no_comments = [remove_comments(x) for x in test_repaid]

    # Keep in-between spaces, strip lines, and remove empty lines
    train_debt_no_spaces = [remove_spaces(x) for x in train_debt_no_comments]
    train_repaid_no_spaces = [remove_spaces(x) for x in train_repaid_no_comments]
    test_debt_no_spaces = [remove_spaces(x) for x in test_debt_no_comments]
    test_repaid_no_spaces = [remove_spaces(x) for x in test_repaid_no_comments]

    # Aggregate data into a training group and a testing group
    training_data = [(msg, debt, repaid) for msg, debt, repaid in
                  zip(processed_train_messages, train_debt_no_spaces, train_repaid_no_spaces)]
    testing_data = [(cmt, debt, repaid) for cmt, debt, repaid in
                 zip(processed_test_comments, test_debt_no_spaces, test_repaid_no_spaces)]

    return training_data, testing_data