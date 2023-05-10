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
output_dir = "output3"
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
comments, debt_codes, repaid_codes = retrieve_data(data_dir)

print("Create localised abstraction...")
localised_no_comment = pair_patterns.extract_patterns(debt_codes, repaid_codes)

# Tokenise comments
satd_comments = [x.split() for x in comments]
# Combine
localised = [(x[0], x[1], x[2], x[3], x[4], y) for x, y in zip(localised_no_comment, satd_comments)]

# Don't take too-long comments/codes
trimmed = [x for x in localised if len(x[1]) <= max_code_length and len(x[3]) <= max_code_length and len(x[5]) <= max_comment_length]
# Remove duplicates
hashable_trimmed = [(tuple(x[0].items()), tuple(x[1]), tuple(x[2]), tuple(x[3]), tuple(x[4]), tuple(x[5])) for x in trimmed]
no_dups = sorted(set(hashable_trimmed))
clean_localised = [(dict(x[0]), list(x[1]), list(x[2]), list(x[3]), list(x[4]), list(x[5])) for x in no_dups]

# Radomise
shuf_localised = sample(clean_localised, k=len(clean_localised))
# Testing set
test_localised = shuf_localised[:num_test_dps]
test_input_tokenised = [x[5]+x[1] for x in test_localised]
test_output_tokenised = [x[3] for x in test_localised]
# Training set
train_localised = shuf_localised[num_test_dps:]
train_localised = train_localised[:num_train_dps]
train_input_tokenised = [x[5]+x[1] for x in train_localised]
train_output_tokenised = [x[3] for x in train_localised]

# for localised in shuf_localised:
#     comment = ' '.join(localised[3])
#     code = ' '.join(localised[2])
#     if code == '} else if ( out instanceof ThreadsDefinition ) { renderThreads ( buffer , out ) ; } else if ( out instanceof TransactedDefinition ) {':
#         print("===========")
#         print(comment)
#         print(code)
# sys.exit()

# Build dictionary and token-integer mapping
input_tokenised = train_input_tokenised + test_input_tokenised
output_tokenised = train_output_tokenised + test_output_tokenised
input_vocab, input_t2i_map, input_i2t_map = data_handles.build_dictionary(input_tokenised)
output_vocab, output_t2i_map, output_i2t_map = data_handles.build_dictionary(output_tokenised)

# Data shapes
input_vocab_size, output_vocab_size, max_input_len_train, max_output_len_train, num_dps_train, \
max_input_len_test, max_output_len_test, num_dps_test = \
    data_handles.data_shapes(input_vocab, output_vocab, train_input_tokenised, train_output_tokenised,
                             test_input_tokenised, test_output_tokenised)
print("====================")
print('# training data points:', num_dps_train)
print('# testing data points:', num_dps_test)
print('Input vocabulary size:', input_vocab_size)
print('Output vocabulary size:', output_vocab_size)
print('Max. input length in training data:', max_input_len_train)
print('Max. output length in training data:', max_output_len_train)
print('Max. input length in testing data:', max_input_len_test)
print('Max. output length in testing data:', max_output_len_test)
print('Beam width =', num_cands)
print("====================")

# Prepare model training and testing data
train_comment_inputs, train_code_inputs, train_code_outputs = \
    data_handles.prepare_model_data(num_dps_train, max_input_len_train, max_output_len_train, "train",
                                    input_vocab_size, output_vocab_size, train_input_tokenised,
                                    train_output_tokenised, input_t2i_map, output_t2i_map)
test_comment_inputs, test_code_inputs = \
    data_handles.prepare_model_data(num_dps_test, max_input_len_test, max_output_len_test, "test",
                                    input_vocab_size, output_vocab_size, test_input_tokenised,
                                    test_output_tokenised, input_t2i_map, output_t2i_map)

# build encoder-decoder model
enc_dec = model_handles.build_enc_dec(latent_dim, input_vocab_size, output_vocab_size, dropout)
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
        generate_fixes(test_input_tokenised, test_output_tokenised, num_cands, enc_dec, test_comment_inputs,
                       max_output_len_test, output_t2i_map, output_i2t_map, id_c_test_lookup, output_vocab_size, e,
                       output_dir, test_localised)

end_time = datetime.datetime.now().replace(microsecond=0)
print('=============')
print('=============')
print("Training completed at:", end_time)
print("Training took (h:mm:ss)", end_time - start_time)

