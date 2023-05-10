import re
import sys
from random import seed, sample
import datetime
# from tqdm import tqdm
# Choose between removing or keeping code (not pattern) duplicates
from retrieve_data import retrieve_data
import data_handles
# from train_bigfix_test_defects4j.correct_defects4j_data.encdec_5_abstract_ids import data_handles
# Choose between abstracting IDs only or IDs and constants
import pair_patterns
# from train_bigfix_test_defects4j.correct_defects4j_data.encdec_5_abstract_ids import pair_patterns
from generation_handles import generate_fixes
import model_handles


# Specify data paths
# data_dir = "/home/aziz/experiments/problems/satd_repayment/data/"
# data_dir = "/home/aziz/dsl/gpu/experiments/problems/satd_repayment/data/"
# data_dir = "data/"
data_dir = "../"
output_dir = "test"
# d4j_v = "2.0.0"
# d4j_v = "1.2.0"
# trained_model_name = "enc_dec_4_apr.h5"
# Specify random seed value
rsv = 30
# Model hyper-parameters
latent_dim = 1024
# latent_dim = 2048
dropout = 0.2
epochs = 60
# epochs = 20
# k for beam search (# patch candidates)
# num_cands = 50
num_cands = 10
num_train_dps = 1000000
# num_test_dps = 1000000
# num_train_dps = 100
num_test_dps = 40
# context_limit = 30
# test_perc = 10
max_code_length = 120
# max_comment_length = 2
# max_code_length = 1000000
max_comment_length = 1000000

seed(rsv)
# print("Collecting testing data (defects4j)...")
# print("defects4j version:", d4j_v)
# d4j_meta = retrieve_data(data_dir)

# b_con_lens = sorted([len(x[6][0]) for x in d4j_meta])
# f_con_lens = sorted([len(x[6][1]) for x in d4j_meta])

# d4j_sorted_size = []
# for item in sorted(set(b_con_lens), reverse=True):
#     for meta in d4j_meta:
#         if len(meta[6][0]) == item:
#             d4j_sorted_size.append(meta)
#
# c = 0
# for meta in d4j_sorted_size:
#     if len(meta[6][0]) == 30:
#         c += 1
#         print("====")
#         print(meta[0], meta[1], len(meta[6][0]))
#         print(meta[2][0])
#         print(meta[2][1])
#         print("====")
#         print("\n".join((meta[6][0])))
#         print("====")
#
# print(b_con_lens)
# print("=======")
# print(f_con_lens)
# print("=======")
# print(c, c*100/len(d4j_meta))
#
# print(len(d4j_meta))
# print(len(d4j_sorted_size))
#
# sys.exit()

# for meta in d4j_meta:
#     print("=======")
#     print(meta[0], "{}:-".format(meta[1]))
#     print("---")
#     print(meta[2][0])
#     print(meta[2][1])
#     print("---")
#     print("=======")

# sys.exit()

# If project ID, bug ID, and buggy-fixed pairs found identical, remove duplications
# d4j_meta_dict = {(x[0], x[1], tuple(x[3][0]), tuple(x[3][1])): (x[0], x[1], x[2], x[3], x[4]) for x in d4j_meta_dups}
# d4j_meta = sorted([(x[0], x[1], x[2], x[3], x[4]) for x in d4j_meta_dict.values()])

# d4j_meta_clean = sorted(set([(x[0], x[1], (x[2][0], x[2][1]), (tuple(x[3][0]), tuple(x[3][1])), (x[4][0], x[4][1]), x[5]) for x in d4j_meta]))
# d4j_meta_clean = [(x[0], x[1], (x[2][0], x[2][1]), (list(x[3][0]), list(x[3][1])), (x[4][0], x[4][1]), x[5]) for x in d4j_meta_clean]

# for i, item in enumerate(d4j_meta):
#     print("==============")
#     print(i + 1)
#     print("---")
#     print(item[2][0])
#     print(item[3][0])
#     print("---")
#     print(item[2][1])
#     print(item[3][1])
#
#
# print("==============")
# print("==============")
#
# for i, item in enumerate(d4j_meta):
#     splitted = item[-1].split()
#     splitted[0] = splitted[0][1:]
#     splitted[1] = splitted[1][1:]
#     if splitted[0] != splitted[1]:
#         print(i+1, splitted)
# print("==========")
# print("==========")
# for item in d4j_meta[308]:
#     print(item)
#     print("---")



# sys.exit()

# from collections import Counter
# d4j_count = dict(Counter(d4j_meta_clean))
# for k, v in d4j_count.items():
#     if v == 2:
#         print(k)
# print(len(d4j_meta))
# print(len(d4j_meta_clean))
# sys.exit()


# con_sls = [x[5] for x in d4j_meta_clean]
# print(len(d4j_meta))
# print(len(d4j_meta_clean))
# print(con_sls)
# print(len(con_sls))

# sys.exit()

# d4j_meta_clean = sorted(set([(x[0], x[1], (x[2][0], x[2][1]), (tuple(x[3][0]), tuple(x[3][1])), (x[4][0], x[4][1])) for x in d4j_meta_dups]))
# d4j_meta = [(x[0], x[1], (x[2][0], x[2][1]), (list(x[3][0]), list(x[3][1])), (x[4][0], x[4][1])) for x in d4j_meta_clean]
# print("# d4j dps before cleaning:", len(d4j_meta_dups))
# print(len(d4j_meta_dups) - len(d4j_meta), "duplicated d4j dps have been removed")

# sys.exit()
print("====================")
print("Collecting data...")
comments, repaid_codes = retrieve_data(data_dir)

# for comment, code in zip(satd_comments, repaid_codes):
#     print("====================")
#     print(comment)
#     print("++++")
#     print(code)
#     print("====================")


# print(len(satd_comments), len(repaid_codes))



# import pickle
# with open(data_dir + 'satd_repayment.pkl', 'rb') as pklf:
#     df_satd_repayment = pickle.load(pklf)
# for i, row in df_satd_repayment.iterrows():
#     print("====================")
#     print(row['After'])
#     print('+++++')
#     print(after[i])
# sys.exit()



# con_lens = sorted([len(x[4]) for x in bigfix_data], reverse=True)

# print("==================")
# print("==================")
#
# bigfix_sorted_size = []
# for item in sorted(set(con_lens), reverse=True):
#     for bf in bigfix_data:
#         if len(bf[4]) == item:
#             bigfix_sorted_size.append(bf)
#
# c = 0
# for bf in bigfix_sorted_size:
#     if len(bf[4]) == 30:
#         c += 1
#         print("====")
#         print(bf[0])
#         print(bf[2])
#         print("====")
#         print("\n".join((bf[4])))
#         print("====")
#
# print(con_lens)
# print("=======")
# print(c, c*100/len(bigfix_data))
#
# print(len(bigfix_data))
# print(len(bigfix_sorted_size))


# Shuffle training data (only if you are not using patterns)
# bigfix_shuf = sample(bigfix_data, k=len(bigfix_data))

# problematic_lines = ["Preconditions.checkArgument(outputFormatServicePort == 0",
#                      "while (remainingResultSize > 0 && countdown > 0",
#                      "&& (oldt.getSd().getLocation().compareTo(newt.getSd().getLocation()) == 0",
#                      "if (qbp.getAggregationExprsForClause(dest).size() != 0",
#                      "if (null == name || name.length() == 0",
#                      "while (bigTblRowContainer != null && bigTblRowContainer.rowCount() > 0"]
# bf_context = []
# for bfdp in bigfix_data:
#     dp_context = []
#     for line in bfdp[4]:
#         if len(dp_context) > 0 and dp_context[-1] in problematic_lines:
#             dp_context[-1] = dp_context[-1]+" "+line
#         else:
#             dp_context.append(line)
#     bf_context.append(dp_context)

# d4j_buggy_context = []
# for d4jdp in d4j_meta:
#     bug_context = []
#     for line in d4jdp[6][0]:
#         if len(bug_context) > 0 and bug_context[-1] in problematic_lines:
#             bug_context[-1] = bug_context[-1] + " " + line
#         else:
#             bug_context.append(line)
#     d4j_buggy_context.append(bug_context)

# d4j_fixed_context = []
# for d4jdp in d4j_meta:
#     fix_context = []
#     for line in d4jdp[6][1]:
#         if len(fix_context) > 0 and fix_context[-1] in problematic_lines:
#             fix_context[-1] = fix_context[-1] + " " + line
#         else:
#             fix_context.append(line)
#     d4j_fixed_context.append(fix_context)

# print("==============")
# print("hi")
# sys.exit()

# for bbb, aaa in zip(before, after):
#     print(bbb)
#     print("+++")
#     print(aaa)
#     print("===========")
#     print("===========")
#
# sys.exit()

# Extract lines only
# bf_buggy_lines = [x+[y[0]] if len(x) > 0 else [y[0]] for x, y in zip(bf_context, bigfix_data)]
# bf_fixed_lines = [x+[y[2]] if len(x) > 0 else [y[2]] for x, y in zip(bf_context, bigfix_data)]
# d4j_buggy_lines = [x[6][0]+[x[2][0]] if len(x[6][0]) > 0 else [x[2][0]] for x in d4j_meta]
# d4j_fixed_lines = [x[6][1]+[x[2][1]] if len(x[6][1]) > 0 else [x[2][1]] for x in d4j_meta]
# d4j_buggy_lines = [x[2][0] for x in d4j_meta_dups]
# d4j_fixed_lines = [x[2][1] for x in d4j_meta_dups]

# for bug in d4j_buggy_lines:
#     print("============")
#     print(bug)
# sys.exit()

# for i, (buggy, fixed) in enumerate(zip(bf_buggy_lines, bf_fixed_lines)):
#     print("==========")
#     print(i+1)
#     print("--")
#     print(buggy)
#     print("--")
#     print(fixed)
#     print("==========")
#     if i+1 == 10:
#         break
# for i, (buggy, fixed) in enumerate(zip(d4j_buggy_lines, d4j_fixed_lines)):
#     print("==========")
#     print(i+1)
#     print("--")
#     print(buggy)
#     print("--")
#     print(fixed)
#     print("==========")
#     if i+1 == 10:
#         break
# sys.exit()

print("Create localised abstraction...")
# before_v2 = [[b] for b in before]
# after_v2 = [[a] for a in after]
localised_no_comment = pair_patterns.extract_patterns(repaid_codes)
# Tokenise comments
satd_comments = [x.split() for x in comments]
localised = [(x[0], x[1], x[2], y) for x, y in zip(localised_no_comment, satd_comments)]


# lens = [len(x) for x in localised]
# print(lens)
# print(len(localised))
# sys.exit()

# for item in localised:
#     print("====================")
#     print(item[0])
#     print("++++++++++")
#     print(item[1])
#     print("++++++++++")
#     print(item[2])
#     print("++++++++++")
#     print(item[3])
#     print("====================")
# sys.exit()

# print("Retrieve localised abstraction from defects4j...")
# d4j_localised = pair_patterns.extract_patterns(d4j_buggy_lines, d4j_fixed_lines)

# test_bugs = [('Chart', 11), ('Closure', 86), ('Lang', 59), ('Math', 30), ('Mockito', 38), ('Time', 19), ('Chart', 1), ('Chart', 7), ('Closure', 113), ('Chart', 9)]
# for bug in test_bugs:
#     for i, item in enumerate(d4j_meta):
#         if item[0] == bug[0] and item[1] == bug[1]:
#             print("======")
#             print(item[0], item[1])
#             print("---")
#             print(item[2][0])
#             print(d4j_localised[i][1])
#             print("---")
#             print(item[2][1])
#             print(d4j_localised[i][2])
#             print("---")
#             print(d4j_localised[i][0])
#             print("---")
#             print(i + 1)
#             print("======")
# sys.exit()

# Remove duplicated patterns in training data (BigFix)
# bf_pair_patterns = sorted(set([(tuple(x[1]), tuple(y[2])) for x, y in zip(bf_localised, bf_localised)]))
# If you want to keep duplicated patterns, comment the previous line and uncomment the following line
# bf_pair_patterns = [(tuple(x[1]), tuple(y[2])) for x, y in zip(bf_localised, bf_localised)]
# print(len(bf_localised) - len(bf_pair_patterns), "redundant patterns have been removed")
# print("Current # training dps:", len(bf_pair_patterns))


# Separate training and testing data
# chunks = [shuf_templates[i:i + test_perc] for i in range(0, len(shuf_templates), test_perc)]
# train_chunk, test_chunk = chunks[:-1], chunks[-1:]
# train = [x for y in train_chunk for x in y]
# test = [x for y in test_chunk for x in y]
# Cut training and testing data to maxes
# train = train[:num_train_dps]
# test = test[:num_test_dps]

# Data duplication
# debt_dps, repaid_dps = [], []
# for i in range(25):
#     for debt in debt_no_spaces:
#         debt_dps.append(debt)
#     for repaid in repaid_no_spaces:
#         repaid_dps.append(repaid)


# Extra info
# occurr_c_d4j = 0
# for bf_pattern in bf_patterns_shuf:
#     for d4j_pattern in d4j_patterns_shuf:
#         if bf_pattern == d4j_pattern:
#             occurr_c_d4j += 1
# print("# times recognisable patterns found in D4J:", occurr_c_d4j)

# Extract training and testing patterns that are already tokenised
# train_buggy_tokenised = [list(x[0]) for x in bf_patterns_shuf]
# train_fixed_tokenised = [list(x[1]) for x in bf_patterns_shuf]

# print("======")
# print("Before:-")
# print(localised[3][1])
# print("======")
# print("After:-")
# print(localised[3][2])
# print("======")
# print("Lookup:-")
# print(localised[3][0])
# print("======")
# sys.exit()

# print("===============")
# blens = [len(x[2]) for x in localised]
# print(sorted(blens))
# sys.exit()

# Remove dps with too-long comments/codes
trimmed = [x for x in localised if len(x[1]) <= max_code_length and len(x[3]) <= max_comment_length]
# Radomise
shuf_localised = sample(trimmed, k=len(trimmed))
# Testing set
test_localised = shuf_localised[:num_test_dps]
test_comments_tokenised = [x[3] for x in test_localised]
test_codes_tokenised = [x[1] for x in test_localised]
# Training set
train_localised = shuf_localised[num_test_dps:]
train_localised = train_localised[:num_train_dps]
train_comments_tokenised = [x[3] for x in train_localised]
train_codes_tokenised = [x[1] for x in train_localised]

# test_thing = test_codes_tokenised
# for item in test_thing:
#     print("=======")
#     print(item)
# print(len(test_thing))
# sys.exit()

# train_localised = [x for i in range(25) for x in localised]
# Shuffle training patterns
# shuf_train = sample(train_localised, k=len(train_localised))

# for localised in shuf_localised:
#     comment = ' '.join(localised[3])
#     code = ' '.join(localised[2])
#     if comment == 'todo fix the test failure in no windows box' and code == '} public void testPollFileWhileSlowFileIsBeingWritten ( ) throws Exception { if ( ! ON_WINDOWS ) { return ; } deleteDirectory ( "./target/exclusiveread" ) ;':
#         print("===========")
#         print(comment)
#         print(code)
# sys.exit()

# Build dictionary and token-integer mapping
comment_tokenised = train_comments_tokenised + test_comments_tokenised
code_tokenised = train_codes_tokenised + test_codes_tokenised
comment_vocab, word_int_map, int_word_map = data_handles.build_dictionary(comment_tokenised)
code_vocab, code_int_map, int_code_map = data_handles.build_dictionary(code_tokenised)
print("====================")
# print("Int-token mapping:-")
# print(int_word_map)
# sys.exit()

# Data shapes
comment_vocab_size, code_vocab_size, max_comment_len_train, max_code_len_train, num_dps_train, \
max_comment_len_test, max_code_len_test, num_dps_test = \
    data_handles.data_shapes(comment_vocab, code_vocab, train_comments_tokenised, train_codes_tokenised,
                             test_comments_tokenised, test_codes_tokenised)
print("====================")
print('# training data points:', num_dps_train)
print('# testing data points:', num_dps_test)
# print("# collected testing bugs:", len(sorted({(x[0], x[1]) for x in d4j_meta})))
# print("# collected testing bugs:", len(sorted({(x[0], x[1]) for x in d4j_meta_dups})))
print('Comment vocabulary size:', comment_vocab_size)
print('Code vocabulary size:', code_vocab_size)
print('Max length in SATD comments in training data:', max_comment_len_train)
print('Max length in repaying code in training data:', max_code_len_train)
print('Max length in SATD comments in testing data:', max_comment_len_test)
print('Max length in repaying code in testing data:', max_code_len_test)
print('Beam width =', num_cands)
# print('# Context lines', context_limit)
print("====================")

# Prepare model training and testing data
train_comment_inputs, train_code_inputs, train_code_outputs = \
    data_handles.prepare_model_data(num_dps_train, max_comment_len_train, max_code_len_train, "train",
                                    comment_vocab_size, code_vocab_size, train_comments_tokenised,
                                    train_codes_tokenised, word_int_map, code_int_map)
test_comment_inputs, test_code_inputs = \
    data_handles.prepare_model_data(num_dps_test, max_comment_len_test, max_code_len_test, "test",
                                    comment_vocab_size, code_vocab_size, test_comments_tokenised,
                                    test_codes_tokenised, word_int_map, code_int_map)

# build encoder-decoder model
enc_dec = model_handles.build_enc_dec(latent_dim, comment_vocab_size, code_vocab_size, dropout)
enc_dec.summary()

# print("====================")
# for i in range(len(test_buggy_tokenised)):
#     bug_count = compile_d4j(data_dir, d4j_meta, i)
#     # print("bug", i+1)
#     if bug_count > 1:
#         print(d4j_meta[i][0], d4j_meta[i][1])
#         print(d4j_meta[i][2][0])
#         print(bug_count)
#         print('---')
# sys.exit()

# For interpreting IDs and constants during generation
id_c_test_lookup = [x[0] for x in test_localised]
# Model training and patch generation
start_time = datetime.datetime.now().replace(microsecond=0)
print("Training started at:", start_time)
for e in range(1, epochs+1):
    print('Iteration', str(e) + '/' + str(epochs) + ':-')
    enc_dec.fit([train_comment_inputs, train_code_inputs], train_code_outputs)
    # generator.save(trained_model_dir + trained_model_name)
    # print("The Model of this iteration has been saved to disk")
    if (e) % 10 == 0:
        generate_fixes(test_comments_tokenised, test_codes_tokenised, num_cands, enc_dec, test_comment_inputs,
                       max_code_len_test, code_int_map, int_code_map, id_c_test_lookup, code_vocab_size, e, output_dir)
    # generate_fixes(test_buggy_tokenised, test_fixed_tokenised, num_cands)




end_time = datetime.datetime.now().replace(microsecond=0)
print('=============')
print('=============')
print("Training completed at:", end_time)
print("Training took (h:mm:ss)", end_time - start_time)

