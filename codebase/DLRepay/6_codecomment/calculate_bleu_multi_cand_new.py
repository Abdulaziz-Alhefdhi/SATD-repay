import sys

from nltk.translate.bleu_score import corpus_bleu, sentence_bleu


def calculate_bleu(references, candidates):
    b1 = corpus_bleu(references, candidates, weights=(1., 0., 0., 0.))
    b2 = corpus_bleu(references, candidates, weights=(1/2, 1/2, 0., 0.))
    b3 = corpus_bleu(references, candidates, weights=(1/3, 1/3, 1/3, 0.))
    b4 = corpus_bleu(references, candidates, weights=(1/4, 1/4, 1/4, 1/4))
    b = corpus_bleu(references, candidates)
    print("Bleu-1 Score: %.3f" % b1, " Bleu-2 Score: %.3f" % b2, " Bleu-3 Score: %.3f" % b3, " Bleu-4 Score: %.3f" % b4, " Bleu Score: %.3f" % b)

    return b1, b2, b3, b4, b


def extract_refs_cands(file_path):
    with open(file_path, 'r', encoding='utf-8') as ff:
        file_lines = ff.read().split("\n")

    references, candidates = [], []
    for line in file_lines:
        if 'Repaid code:  ' in line:
            references.append(line.split("Repaid code:  ", 1)[1].split())
        if 'Candidate:    ' in line:
            candidates.append(line.split("Candidate:    ", 1)[1].split())

    return references, candidates


k = 10
folder_name = "output"
iter = 60
generation_path = "{}/iter_{}_generation.java".format(folder_name, iter)

refs, all_cands = extract_refs_cands(generation_path)
cands = [all_cands[i:i+k] for i in range(0, len(all_cands), k)]


# bleu1, bleu2, bleu3, bleu4 = calculate_bleu(refs, cands)
print('==========')
c = 0
perfect = []
for ref, group in zip(refs, cands):
    for cand in group:
        if ref == cand:
            c += 1
            read_ref, read_cand = " ".join(ref), " ".join(cand)
            # print(read_old)
            print(read_ref)
            print(read_cand)
            print('==========')
            perfect.append((read_ref, read_cand))
            break

print("Results folder name:", folder_name)
print("Iteration:", iter)
print("# candidates per reference:", k)
print('==========')
if len(refs) == len(cands):
    print("# testing dps:", len(cands))
else:
    exit("Something went wrong!")

# print("Bleu-1 Score: %.2f" % bleu1, " Bleu-2 Score: %.2f" % bleu2, " Bleu-3 Score: %.2f" % bleu3, " Bleu-4 Score: %.2f" % bleu4)


print("# perfect fixes:", c)
iden_per = "%.2f" % (c/len(refs)*100)
print("Percentage of perfect fixs:", iden_per+"%")
print("# perfect fixes after removing duplicate dps:", len(set(perfect)))
print('==========')

# Calculate sentence bleu for each candidate


bleus = []
for ref, c_group in zip(refs, cands):
    scores = [sentence_bleu([ref], cand, weights=(1/1, 0., 0., 0.)) for cand in c_group]
    # scores = [sentence_bleu([ref], cand) for cand in c_group]
    bleus.append(scores)

best_cands = []
# counter = 0
for ref, c_group, b_scores in zip(refs, cands, bleus):
    score_cand = [(s, c) for s, c in zip(b_scores, c_group)]
    sorted_score_cand = sorted(score_cand, reverse=True)
    best_cands.append(sorted(score_cand, reverse=True)[0][1])
    # print('==========')
    # sorted_scores = [pair[0] for pair in sorted_score_cand]
    # print(sorted_scores)
    # if sorted_score_cand[0][0] == 1:
    #     print('==========')
    #     print(ref)
    #     print(sorted_score_cand[0][1])
    #     counter += 1
print('==========')
# print(len(best_cands), len(refs))
# c = 0
# for ref, cand in zip(refs, best_cands):
#     if ref == cand:
#         c += 1
#         print('==========')
#         print(ref)
#         print(cand)
# print(c)

target_lists = [[ref] for ref in refs]


bleu1, bleu2, bleu3, bleu4, bleu = calculate_bleu(target_lists, best_cands)

