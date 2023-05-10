import sys
from random import seed, shuffle
from retrieve_data import retrieve_data
import json
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
output_dir = "dataset"
# Specify random seed value for consistent randomisation
rsv = 30
seed(rsv)
print("====================")
print("Collecting data...")
nngen_data, satdr_data = retrieve_data(data_dir)

# print("Removing duplicates from training data...")
# nngen_nodups = []
# for bfdp in nngen_data:
#     if bfdp not in nngen_nodups:
#         nngen_nodups.append(bfdp)

# Randomise data
shuffled_nngen = nngen_data
target_set = satdr_data
shuffle(shuffled_nngen)
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
print(shuffled_nngen[0])

# Make train and dev sets
train_set, dev_set = shuffled_nngen[2000:], shuffled_nngen[:2000]

# Serialise data
train_json = [json.dumps(x) for x in train_set]
dev_json = [json.dumps(x) for x in dev_set]
target_json = [json.dumps(x) for x in target_set]
test_json = [json.dumps(x) for x in test_set]

print(len(nngen_data), len(shuffled_nngen))
print(len(train_json), len(dev_json), len(target_json), len(test_json))
# print(json.dumps(test_set[:10]))

# for i in range(1000):
#     print("=============")
#     print(train_json[i])

# sys.exit()
# test_json = json.dumps(test_set)

# for x, y in zip(target_json, test_json):
#     print("=================")
#     print(x)
#     print("++++")
#     print(y)

print("Writing json files to disk...")
write_dataset_to_disk(output_dir, train_json, dev_json, target_json, test_json)
