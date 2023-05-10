from difflib import unified_diff
from posixpath import dirname
from nltk.tokenize import TreebankWordTokenizer, wordpunct_tokenize
import os

tokenizer = TreebankWordTokenizer()
skipped = 0
processed = 0
with open(f'data/bigfix.test.diff', "w", encoding="utf-8") as diffFile:
    dirName = '../bigfix'
    dirs = os.listdir(dirName)
    for i in sorted(dirs, key=int):
        buggyFileName = f'{i}_buggy.txt'
        fixedFileName = f'{i}_fixed.txt'
        with open(f'{dirName}/{i}/{buggyFileName}', encoding="utf-8") as buggyFile:
            with open(f'{dirName}/{i}/{fixedFileName}', encoding="utf-8") as fixedFile:
                diffIter = unified_diff(buggyFile.readlines(), fixedFile.readlines(),
                                        fromfile=fixedFileName, tofile=buggyFileName)
                lines = []
                tokenCount = 0
                for j in diffIter:
                    if j.startswith('---'):
                        tokens = tokenizer.tokenize(
                            j.replace('---', 'mmm a /', 1))
                        tokenCount += len(tokens)
                        tokens = wordpunct_tokenize(' '.join(tokens))
                        tokenCount += len(tokens)
                        lines.append(' '.join(tokens))
                    elif j.startswith('+++'):
                        tokens = tokenizer.tokenize(
                            j.replace('+++', 'ppp b /', 1))
                        tokenCount += len(tokens)
                        tokens = wordpunct_tokenize(' '.join(tokens))
                        tokenCount += len(tokens)
                        lines.append(' '.join(tokens))
                    elif not j.startswith('@@'):
                        tokens = tokenizer.tokenize(j)
                        tokenCount += len(tokens)
                        tokens = wordpunct_tokenize(' '.join(tokens))
                        tokenCount += len(tokens)
                        lines.append(' '.join(tokens))

                if(lines):
                    len_lim = 200
                    if tokenCount > len_lim:
                        print(f'Skipping {i}: Token count exceeds limit({len_lim})')
                        skipped += 1
                    else:
                        diffFile.write(f"{' <nl> '.join(lines)} <nl> \n")
                        processed += 1
                else:
                    print(f'Skipping {i}: No diff')
                    skipped += 1

print(f'\n\nSkipped: {skipped} | Processed: {processed}')
