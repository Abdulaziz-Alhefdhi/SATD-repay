import json
import sys

from nltk.translate.bleu_score import sentence_bleu, corpus_bleu


def calculate_bleu(references, candidates):
    b1 = corpus_bleu(references, candidates, weights=(1., 0., 0., 0.))
    b2 = corpus_bleu(references, candidates, weights=(1/2, 1/2, 0., 0.))
    b3 = corpus_bleu(references, candidates, weights=(1/3, 1/3, 1/3, 0.))
    b4 = corpus_bleu(references, candidates, weights=(1/4, 1/4, 1/4, 1/4))
    b = corpus_bleu(references, candidates)
    print("Bleu-1 Score: %.3f" % b1, " Bleu-2 Score: %.3f" % b2, " Bleu-3 Score: %.3f" % b3, " Bleu-4 Score: %.3f" % b4, " Bleu Score: %.3f" % b)

    return b1, b2, b3, b4, b


# Retrieve data from disk
# Target data
with open('dataset/target.json', 'r') as target_file:
    target_set = target_file.read().split('\n')[:-1]
# Make dicts to read codes and comments
target_json = [json.loads(x) for x in target_set]
# Generation
with open('saved_models/predictions.txt', 'r') as pred_file:
    predictions = pred_file.read().split('\n')[:-1]

target_codes = [x['code'] for x in target_json]
test_inputs = [x['nl'] for x in target_json]

good, c = 0, 0
for target, pred in zip(target_codes, predictions):
    c += 1
    if target == pred:
        good += 1
        print("================")
        print(target)
        print("++++++")
        print(pred)
print("================")
print(good, c)

target_lists = [[x.split()] for x in target_codes]
pred_lists = [x.split() for x in predictions]
# paired = [([x], y) for x, y in zip(target_lists, pred_lists)]

bleu1, bleu2, bleu3, bleu4, bleu = calculate_bleu(target_lists, pred_lists)
sys.exit()

scores = [sentence_bleu(ref, cand) for ref, cand in zip(target_lists, pred_lists)]

combined = [(score, tin, " ".join(target[0]), " ".join(pred)) for score, tin, target, pred in zip(scores, test_inputs, target_lists, pred_lists)]
x = sorted(combined, reverse=True)
for item in x:
    print("===================")
    print(item[1])
    print("++++++")
    print(item[2])
    print("++++++")
    print(item[3])
    print("++++++")
    print(item[0])
