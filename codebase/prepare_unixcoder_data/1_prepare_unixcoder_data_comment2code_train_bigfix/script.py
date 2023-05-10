import sys
from random import seed, shuffle
import datetime
from retrieve_data import retrieve_data
import json
# import data_handles
# import pair_patterns
# from generation_handles import generate_fixes
# import model_handles
from pathlib import Path


def write_dataset_to_disk(dataset_folder, train_data, dev_data, target_data, test_data):
    Path(dataset_folder).mkdir(parents=True, exist_ok=True)
    with open(f'{dataset_folder}/train.json', 'w', encoding='utf-8') as train_file:
        for dp in train_data:
            train_file.write(f'{dp}\n')
    with open(f'{dataset_folder}/dev.json', 'w', encoding='utf-8') as dev_file:
        for dp in dev_data:
            dev_file.write(f'{dp}\n')
    with open(f'{dataset_folder}/target.json', 'w', encoding='utf-8') as target_file:
        for dp in target_data:
            target_file.write(f'{dp}\n')
    with open(f'{dataset_folder}/test.json', 'w', encoding='utf-8') as test_file:
        for dp in test_data:
            test_file.write(f'{dp}\n')


# Specify data paths
data_dir = "../"
dataset_dir = "dataset"
# output_dir = "gpu_output"
# Specify random seed value
rsv = 30
# Model hyper-parameters
# latent_dim = 1024
# dropout = 0.2
# epochs = 60
# k for beam search (# patch candidates)
# num_cands = 10
# num_train_dps = 1000000
# num_test_dps = 1000000
# max_comment_length = 1000000
# max_code_length = 200

seed(rsv)  # For consistent randomisation
print("====================")
print("Collecting data...")
bigfix_data, satdr_data = retrieve_data(data_dir)

print("Removing duplicates from training data...")
bigfix_nodups = []
for bfdp in bigfix_data:
    if bfdp not in bigfix_nodups:
        bigfix_nodups.append(bfdp)
# bigfix_nodups = sorted(set(bigfix_data))

# Randomise data
shuffled_bigfix = bigfix_nodups
target_set = satdr_data
shuffle(shuffled_bigfix)
shuffle(target_set)

# Make test set
test_set = [{"code": "", "nl": x["nl"]} for x in target_set]
# print(type(target_set), type(test_set))
# print(type(target_set[0]), type(test_set[0]))
# print(len(target_set), len(test_set))
# for x, y in zip(target_set, test_set):
#     print("=================")
#     print(x)
#     print("++++")
#     print(y)
# sys.exit()
print(shuffled_bigfix[-1])

# Make train and dev sets
train_set, dev_set = shuffled_bigfix[1000:], shuffled_bigfix[:1000]

# Serialise data
train_json = [json.dumps(x) for x in train_set]
dev_json = [json.dumps(x) for x in dev_set]
target_json = [json.dumps(x) for x in target_set]
test_json = [json.dumps(x) for x in test_set]

print(len(bigfix_data), len(shuffled_bigfix))
print(len(train_json), len(dev_json), len(target_json), len(test_json))
# print(json.dumps(test_set[:10]))
# sys.exit()
# test_json = json.dumps(test_set)

# for x, y in zip(target_json, test_json):
#     print("=================")
#     print(x)
#     print("++++")
#     print(y)

print("Writing json files to disk...")
write_dataset_to_disk(dataset_dir, train_json, dev_json, target_json, test_json)

sys.exit()


# with open('train.json', 'w', encoding='utf-8') as train_file:
#     json.dump(train_set, train_file)
# with open('dev.json', 'w', encoding='utf-8') as dev_file:
#     json.dump(dev_set, dev_file)
# with open('test.json', 'w', encoding='utf-8') as test_file:
#     json.dump(test_set, test_file)

# with open("mydata.json", "w") as final:
#     json.dump(data, final)

sys.exit()

# Specify data
train_comments = [item[0] for item in train_data]
train_debt_codes = [item[1] for item in train_data]
train_repaid_codes = [item[2] for item in train_data]
test_comments = [item[0] for item in test_data]
test_debt_codes = [item[1] for item in test_data]
test_repaid_codes = [item[2] for item in test_data]

for item in test_comments:
    print(item)
    print("========================")

sys.exit()

print("Creating localised abstraction...")
train_localised_no_comment = pair_patterns.extract_patterns(train_debt_codes, train_repaid_codes)
test_localised_no_comment = pair_patterns.extract_patterns(test_debt_codes, test_repaid_codes)

# Tokenise comments
train_satd_comments = [x.split() for x in train_comments]
test_satd_comments = [x.split() for x in test_comments]
# Combine
train_localised = [(x[0], x[1], x[2], x[3], x[4], y) for x, y in zip(train_localised_no_comment, train_satd_comments)]
test_localised = [(x[0], x[1], x[2], x[3], x[4], y) for x, y in zip(test_localised_no_comment, test_satd_comments)]

# Don't take too-long comments/codes
train_trimmed = [x for x in train_localised if len(x[1]) <= max_code_length and len(x[3]) <= max_code_length and len(x[5]) <= max_comment_length]
test_trimmed = [x for x in test_localised if len(x[1]) <= max_code_length and len(x[3]) <= max_code_length and len(x[5]) <= max_comment_length]

# Remove duplicates in training set
train_hashable_trimmed = [(tuple(x[0].items()), tuple(x[1]), tuple(x[2]), tuple(x[3]), tuple(x[4]), tuple(x[5])) for x in train_trimmed]
train_no_dups = sorted(set(train_hashable_trimmed))
# Back to non-hashable
train_clean_localised = [(dict(x[0]), list(x[1]), list(x[2]), list(x[3]), list(x[4]), list(x[5])) for x in train_no_dups]

# Radomise
shuf_train = sample(train_clean_localised, k=len(train_clean_localised))
# Testing set
test_input_tokenised = [x[5]+x[1] for x in test_trimmed]
test_output_tokenised = [x[3] for x in test_trimmed]
# Training set
train_input_tokenised = [x[5]+x[1] for x in shuf_train]
train_output_tokenised = [x[3] for x in shuf_train]

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
id_c_test_lookup = [x[0] for x in test_trimmed]
# Model training and patch generation
start_time = datetime.datetime.now().replace(microsecond=0)
print("Training started at:", start_time)
for e in range(1, epochs+1):
    print('Iteration', str(e) + '/' + str(epochs) + ':-')
    enc_dec.fit([train_comment_inputs, train_code_inputs], train_code_outputs)
    if (e) % 10 == 0:
        generate_fixes(test_input_tokenised, test_output_tokenised, num_cands, enc_dec, test_comment_inputs,
                       max_output_len_test, output_t2i_map, output_i2t_map, id_c_test_lookup, output_vocab_size, e,
                       output_dir, test_trimmed)

end_time = datetime.datetime.now().replace(microsecond=0)
print('=============')
print('=============')
print("Training completed at:", end_time)
print("Training took (h:mm:ss)", end_time - start_time)

