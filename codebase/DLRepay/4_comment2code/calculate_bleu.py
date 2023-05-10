import sys

from nltk.translate.bleu_score import corpus_bleu


def calculate_bleu(target_lists, predicted_lists):
    references = []
    for a_list in target_lists:
        references.append([a_list])

    b1 = corpus_bleu(references, predicted_lists, weights=(1/1, 0., 0., 0.))
    b2 = corpus_bleu(references, predicted_lists, weights=(1/2, 1/2, 0., 0.))
    b3 = corpus_bleu(references, predicted_lists, weights=(1/3, 1/3, 1/3, 0.))
    b4 = corpus_bleu(references, predicted_lists, weights=(1/4, 1/4, 1/4, 1/4))

    return b1, b2, b3, b4


def extract_refs_cands(file_path):
    with open(file_path, 'r', encoding='utf-8') as ff:
        file_lines = ff.read().split("\n")

    references, candidates = [], []
    for line in file_lines:
        if 'Fixed code: ' in line:
            references.append(line.split("Fixed code: ", 1)[1].split())
        if 'Generation: ' in line:
            candidates.append(line.split("Generation: ", 1)[1].split())

    return references, candidates

# generation_path = "train_bigfix_test_defects4j/train_bigfix_100_test_defects4j_10.java"
# generation_path = "train_bigfix_test_defects4j/1000_train_dp_generation.java"
# generation_path = "train_bigfix_test_defects4j/iter_20_generation.java"
# generation_path = "train_bigfix_test_defects4j/train_bigfix_test_defects4j_generation.java"

# generation_path = "train_test_defects4j/3_metadata/iter_10_generation.java"
# generation_path = "train_test_defects4j/3_metadata/iter_20_generation.java"
# generation_path = "train_test_defects4j/3_metadata/train_test_defects4j_generation.java"

# generation_path = "train_bigfix_test_defects4j/correct_defects4j_data/encdec_5_abstraction/no_beam/iter_10_generation.java"
# generation_path = "train_bigfix_test_defects4j/correct_defects4j_data/encdec_5_abstraction/no_beam/iter_20_generation.java"
# generation_path = "train_bigfix_test_defects4j/correct_defects4j_data/encdec_5_abstraction/no_beam/train_bigfix_test_defects4j_generation.java"
generation_path = "train_bigfix_test_defects4j/correct_defects4j_data/encdec_13_cmplr_short_fix/beam1/iter_30_generation.java"


refs, cands = extract_refs_cands(generation_path)
bleu1, bleu2, bleu3, bleu4 = calculate_bleu(refs, cands)

c = 0
for ref, cand in zip(refs, cands):
    if ref == cand:
        c += 1
        print(" ".join(ref))
        print(" ".join(cand))
        print('==========')

if len(refs) == len(cands):
    print("# pairs:", len(cands))
else:
    exit("There is something wrong!")
print("Bleu-1 Score: %.2f" % bleu1, " Bleu-2 Score: %.2f" % bleu2, " Bleu-3 Score: %.2f" % bleu3, " Bleu-4 Score: %.2f" % bleu4)
print("# identical pairs:", c)
iden_per = "%.2f" % (c/len(refs)*100)
print("Percentage of identical pairs:", iden_per+"%")
