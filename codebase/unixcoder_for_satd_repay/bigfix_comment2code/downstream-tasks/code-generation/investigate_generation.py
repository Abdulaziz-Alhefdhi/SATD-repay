import json
from nltk.translate.bleu_score import corpus_bleu


def calculate_bleu(target_lists, predicted_lists):
    # Cut out <sos> and <eos>
    references = []
    for a_list in target_lists:
        references.append([a_list[1:-1]])

    bleu1 = corpus_bleu(references, predicted_lists, weights=(1., 0., 0., 0.))
    bleu2 = corpus_bleu(references, predicted_lists, weights=(1/2, 1/2, 0., 0.))
    bleu3 = corpus_bleu(references, predicted_lists, weights=(1/3, 1/3, 1/3, 0.))
    bleu4 = corpus_bleu(references, predicted_lists, weights=(1/4, 1/4, 1/4, 1/4))
    bleu  = corpus_bleu(references, predicted_lists)
    print("Bleu-1 Score: %.3f" % bleu1, " Bleu-2 Score: %.3f" % bleu2, " Bleu-3 Score: %.3f" % bleu3, " Bleu-4 Score: %.3f" % bleu4, " Bleu Score: %.3f" % bleu)

    return bleu1, bleu2, bleu3, bleu4, bleu


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

for target, pred in zip(target_codes, predictions):
    print("================")
    print(target)
    print("++++++")
    print(pred)
