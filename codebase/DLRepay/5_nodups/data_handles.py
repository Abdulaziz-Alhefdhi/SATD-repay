import re
import javalang
import sys
import numpy as np


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

    return '\n'.join(result)
    # code = code.splitlines()  # Split lines
    # result = []
    # for line in code:
    #     line = line.split()
    #     line = ' '.join(line)
    #     if len(line) > 0:  # Remove empty lines
    #         result.append(line)
    #
    # return '\n'.join(result)


def create_tokenised(code_lines, fixed=False):
    code_streams = [javalang.tokenizer.tokenize(x, ignore_errors=True) for x in code_lines]
    code_tokenised = []
    for code in code_streams:
        code_tokenised.append([x.value for x in code])
    if fixed:
        return [['<sol>'] + x + ['<eol>'] for x in code_tokenised]
    else:
        return code_tokenised


def create_parsed(buggy_lines, fixed_lines):
    buggy_trees, fixed_trees = [], []
    err_c = 0
    for buggy_line, fixed_line in zip(buggy_lines, fixed_lines):
        try:
            buggy_tree = javalang.parse.parse(
                "class WrappaerClass { public void wrapperMethod() { " + buggy_line + " } }")
            fixed_tree = javalang.parse.parse(
                "class WrappaerClass { public void wrapperMethod() { " + fixed_line + " } }")
            buggy_trees.append(buggy_tree)
            fixed_trees.append(fixed_tree)
            # print(i)
            # print("Success!")
            # print(cand)
            # print('==========')
        except javalang.parser.JavaSyntaxError as stx_er:
            err_c += 1
            print("Error " + str(err_c) + " (JavaSyntaxError): " + str(stx_er))
            print(buggy_line)
            print(fixed_line)
            print('==========')
        except javalang.tokenizer.LexerError as lex_er:
            err_c += 1
            print("Error " + str(err_c) + " (LexerError): " + str(lex_er))
            print(buggy_line)
            print(fixed_line)
            print('==========')
        except TypeError as tp_er:
            err_c += 1
            print("Error " + str(err_c) + " (TypeError): " + str(tp_er))
            print(buggy_line)
            print(fixed_line)
            print('==========')

    return buggy_trees, fixed_trees


def build_dictionary(corpus):
    vocabulary = set([x for y in corpus for x in y])
    token_to_int = dict([(token, i + 1) for i, token in enumerate(vocabulary)])
    vocabulary.add('<unk/pad>')
    token_to_int['<unk/pad>'] = 0
    int_to_token = dict((i, token) for token, i in token_to_int.items())

    return vocabulary, token_to_int, int_to_token


def data_shapes(cm_vocab, cd_vocab, train_bugs, train_fixes, test_bugs, test_fixes):
    cmv_size = len(cm_vocab)
    cdv_size = len(cd_vocab)
    max_bug_len_train = max([len(txt) for txt in train_bugs])
    max_fix_len_train = max([len(txt) for txt in train_fixes])
    num_train_dps = len(train_bugs)
    max_bug_len_test = max([len(txt) for txt in test_bugs])
    max_fix_len_test = max([len(txt) for txt in test_fixes])
    num_test_dps = len(test_bugs)

    return cmv_size, cdv_size, max_bug_len_train, max_fix_len_train, num_train_dps, max_bug_len_test, max_fix_len_test, num_test_dps


def prepare_model_data(num_dps, max_bug_len, max_fix_len, data_type, cmv_size, cdv_size, buggy_tokenised, fixed_tokenised, w2i, c2i):
    # Prepare model data containers
    input_bugs = np.zeros((num_dps, max_bug_len), dtype='int32')
    input_fixes = np.zeros((num_dps, max_fix_len), dtype='int32')
    if data_type == "train":
        output_fixes = np.zeros((num_dps, max_fix_len, cdv_size), dtype='float32')
        # Fill out model data containers
        for i, (buggy, fixed) in enumerate(zip(buggy_tokenised, fixed_tokenised)):
            for w, word in enumerate(buggy):
                input_bugs[i, w] = w2i[word]
            for t, token in enumerate(fixed):
                int_value = c2i[token]
                input_fixes[i, t] = int_value
                if t > 0:
                    output_fixes[i, t - 1, int_value] = 1.
            output_fixes[i, t, 0] = 1.
        return input_bugs, input_fixes, output_fixes

    elif data_type == "test":
        for i, (buggy, fixed) in enumerate(zip(buggy_tokenised, fixed_tokenised)):
            for w, word in enumerate(buggy):
                if word not in list(w2i.keys()):
                    input_bugs[i, w] = w2i['<unk/pad>']
                else:
                    # print(token_to_int[token])
                    input_bugs[i, w] = w2i[word]
            for t, token in enumerate(fixed):
                if token not in list(c2i.keys()):
                    input_fixes[i, t] = c2i['<unk/pad>']
                else:
                    input_fixes[i, t] = c2i[token]
        return input_bugs, input_fixes

    else:
        sys.exit("Specified data model type not recognised!")
