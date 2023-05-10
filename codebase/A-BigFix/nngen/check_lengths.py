from collections import Counter


train_fp = "data/cleaned.train.diff"
bigfix_fp = "data/bigfix.test.diff"

with open(train_fp, 'r', encoding='utf-8') as tfp:
	train_lines = tfp.read().split('\n')

with open(bigfix_fp, 'r', encoding='utf-8') as tfp:
	bf_lines = tfp.read().split('\n')

train_lines = train_lines[:-1]
bf_lines = bf_lines[:-1]

# print(train_lines[-2])
# print(bf_lines[-2])

train_tokenised = [x.split() for x in train_lines]
train_lens = [len(x) for x in train_tokenised]
print(sorted(train_lens)[-1])

bf_tokenised = [x.split() for x in bf_lines]
bf_lens = [len(x) for x in bf_tokenised]
print(sorted(bf_lens)[-1])


for item in bf_tokenised:
	if len(item) == 153:
		print(" ".join(item))

