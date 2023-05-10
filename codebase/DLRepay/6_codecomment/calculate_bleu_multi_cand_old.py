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
        if 'Repaid code: ' in line:
            references.append(line.split("Repaid code: ", 1)[1].split())
        if 'Candidate:   ' in line:
            candidates.append(line.split("Candidate:   ", 1)[1].split())

    return references, candidates


k = 10
folder_name = "output3"
iter = 60
generation_path = "{}/iter_{}_generation.java".format(folder_name, iter)

refs, all_cands = extract_refs_cands(generation_path)
cands = [all_cands[i:i+k] for i in range(0, len(all_cands), k)]


# bleu1, bleu2, bleu3, bleu4 = calculate_bleu(refs, cands)
print('==========')
print("Results folder name:", folder_name)
print("Iteration:", iter)
print("# candidates:", k)
print('==========')
c = 0
for ref, group in zip(refs, cands):
    for cand in group:
        if ref == cand:
            c += 1
            print(" ".join(ref))
            print(" ".join(cand))
            print('==========')
            break

if len(refs) == len(cands):
    print("# pairs:", len(cands))
else:
    exit("Something went wrong!")
# print("Bleu-1 Score: %.2f" % bleu1, " Bleu-2 Score: %.2f" % bleu2, " Bleu-3 Score: %.2f" % bleu3, " Bleu-4 Score: %.2f" % bleu4)

print("# identical pairs:", c)
iden_per = "%.2f" % (c/len(refs)*100)
print("Percentage of identical pairs:", iden_per+"%")
