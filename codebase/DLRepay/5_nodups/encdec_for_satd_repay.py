import sys
from random import seed, sample
import datetime
from retrieve_data import retrieve_data
import data_handles
import pair_patterns
from generation_handles import generate_fixes
import model_handles


# Specify data paths
data_dir = "../"
output_dir = "output"
# Specify random seed value
rsv = 30
# Model hyper-parameters
latent_dim = 1024
dropout = 0.2
epochs = 60
# k for beam search (# patch candidates)
num_cands = 10
num_train_dps = 1000000
num_test_dps = 40
max_comment_length = 1000000
max_code_length = 120
seed(rsv)

print("====================")
print("Collecting data...")
comments, repaid_codes = retrieve_data(data_dir)

print("Create localised abstraction...")
localised_no_comment = pair_patterns.extract_patterns(repaid_codes)
# Tokenise comments
satd_comments = [x.split() for x in comments]
localised = [(x[0], x[1], x[2], y) for x, y in zip(localised_no_comment, satd_comments)]

# Don't take too-long comments/codes
trimmed = [x for x in localised if len(x[1]) <= max_code_length and len(x[3]) <= max_comment_length]
# Remove duplicates
hashable_trimmed = [(tuple(x[0].items()), tuple(x[1]), tuple(x[2]), tuple(x[3])) for x in trimmed]
no_dups = sorted(set(hashable_trimmed))
clean_localised = [(dict(x[0]), list(x[1]), list(x[2]), list(x[3])) for x in no_dups]
# Radomise
shuf_localised = sample(clean_localised, k=len(clean_localised))
# Testing set
test_localised = shuf_localised[:num_test_dps]
test_comments_tokenised = [x[3] for x in test_localised]
test_codes_tokenised = [x[1] for x in test_localised]
# Training set
train_localised = shuf_localised[num_test_dps:]
train_localised = train_localised[:num_train_dps]
train_comments_tokenised = [x[3] for x in train_localised]
train_codes_tokenised = [x[1] for x in train_localised]


for localised in shuf_localised:
    comment = ' '.join(localised[3])
    code = ' '.join(localised[2])
    if code == '} else if ( out instanceof ThreadsDefinition ) { renderThreads ( buffer , out ) ; } else if ( out instanceof TransactedDefinition ) {':
        print("===========")
        print(comment)
        print(code)
sys.exit()



# Build dictionary and token-integer mapping
comment_tokenised = train_comments_tokenised + test_comments_tokenised
code_tokenised = train_codes_tokenised + test_codes_tokenised
comment_vocab, word_int_map, int_word_map = data_handles.build_dictionary(comment_tokenised)
code_vocab, code_int_map, int_code_map = data_handles.build_dictionary(code_tokenised)
print("====================")

# Data shapes
comment_vocab_size, code_vocab_size, max_comment_len_train, max_code_len_train, num_dps_train, \
max_comment_len_test, max_code_len_test, num_dps_test = \
    data_handles.data_shapes(comment_vocab, code_vocab, train_comments_tokenised, train_codes_tokenised,
                             test_comments_tokenised, test_codes_tokenised)
print("====================")
print('# training data points:', num_dps_train)
print('# testing data points:', num_dps_test)
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

# For interpreting IDs and constants during generation
id_c_test_lookup = [x[0] for x in test_localised]

# Model training and patch generation
start_time = datetime.datetime.now().replace(microsecond=0)
print("Training started at:", start_time)
for e in range(1, epochs+1):
    print('Iteration', str(e) + '/' + str(epochs) + ':-')
    enc_dec.fit([train_comment_inputs, train_code_inputs], train_code_outputs)
    if (e) % 10 == 0:
        generate_fixes(test_comments_tokenised, test_codes_tokenised, num_cands, enc_dec, test_comment_inputs,
                       max_code_len_test, code_int_map, int_code_map, id_c_test_lookup, code_vocab_size, e, output_dir)

end_time = datetime.datetime.now().replace(microsecond=0)
print('=============')
print('=============')
print("Training completed at:", end_time)
print("Training took (h:mm:ss)", end_time - start_time)

