from math import log
from tqdm import tqdm
import numpy as np


def cand_gnrtr_beam(data, k, token_map):
    # Because we cannot calculate the log of 0
    data = data[1:]
    sequences = [[list(), 0.0]]
    # walk over each step in sequence
    for row in data:
        all_candidates = list()
        # expand each current candidate
        for i in range(len(sequences)):
            seq, score = sequences[i]
            for j in range(len(row)):
                if len(seq) > 0 and seq[-1] == token_map["<eol>"]:
                    candidate = [seq, score]
                else:
                    log_res = log(row[j]) if row[j] != 0 else float('-inf')
                    candidate = [list(seq) + [j], score - log_res]
                candidate = (tuple(candidate[0]), candidate[1])
                all_candidates.append(candidate)
        # Remove duplicated candidates
        all_candidates = list(set(all_candidates))
        # order all candidates by score
        ordered = sorted(all_candidates, key=lambda tup: tup[1])
        # Limit to best k
        sequences = ordered[:k]
    return [x[0] for x in sequences]


def generate_fixed_ints(gen, bugs, fixed_len, token_map, int_map, test=False, v_size=None):
    gntd_ints = np.zeros(shape=(len(bugs), fixed_len))
    gntd_ints[:, 0] = token_map["<sol>"]
    # For testing, we are returning probabilities instead of sequences
    if test:
        test_predictions = np.zeros(shape=(len(bugs), fixed_len, v_size), dtype='float32')
        test_predictions[:, 0, token_map["<sol>"]] = 1.
    j = 0
    # Loop all training/testing set
    for buggy, generated in tqdm(zip(bugs, gntd_ints), total=len(bugs)):
        buggy_input = buggy[np.newaxis]
        gntd_in_out = generated[np.newaxis]
        # Loop 1 sequence
        for i in range(1, fixed_len):
            predictions = gen.predict([buggy_input, gntd_in_out])
            prediction = predictions.argmax(axis=2)[:, i]
            if test:
                test_predictions[j, i] = predictions[:, i]
            generated[i] = prediction
            if (not test) and int_map[prediction[0]] == "<eol>":
                break
        j += 1
    if test:
        print('=============')
        print(test_predictions)
        print(test_predictions.shape)
        print(token_map["<sol>"])

    return gntd_ints if not test else test_predictions


def decode_ints(int_matrix, int_map):
    gntd_codes = []
    for ints in int_matrix:
        code = [int_map[x] for x in ints]
        truncated_code = ["<sol>"]
        for token in code:
            truncated_code.append(token)
            if token == "<eol>":
                break
        gntd_codes.append(truncated_code)

    return gntd_codes
