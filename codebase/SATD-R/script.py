import pandas as pd
import sys
import os
import subprocess
import pickle


# Testing set
df = pd.read_csv("satd_removal.csv", sep=";")  # Read CSV file

for i, row in df.iterrows():
    if row['Project'] == "Log4j":
        df.at[i, 'Project'] = 'logging-log4j1'
    else:
        df.at[i, 'Project'] = row['Project'].lower()

cwd = os.getcwd()  # Current working directory (round-trip)

nc, yc, c = 0, 0, 0
comment_found = []

print("Extracting found SATD comments and their related data...")
for i, row in df.iterrows():
    os.chdir("{}".format(row['Project']))
    log_out = subprocess.run("git log --pretty=%P -n1 {}".format(row['Commit_Removal']).split(), capture_output=True,
                            text=True)
    cbid = log_out.stdout[:-1]
    diff_out = subprocess.run("git diff {} {} -- {}".format(cbid, row['Commit_Removal'], row['File_Path']).split(),
                            capture_output=True, text=True)
    diff = diff_out.stdout[:-1]

    if len(diff_out.stdout) > 0 and row['SATD_Comment'] not in diff:
        nc += 1
    elif len(diff_out.stdout) > 0 and row['SATD_Comment'] in diff:
        yc += 1
        comment_found.append([row['Project'], row['File_Path'], row['SATD_Comment'], cbid, row['Commit_Removal'], diff])
    else:
        c += 1

    os.chdir(cwd)


print(c, yc, nc, c+yc+nc)

df_comment_found = pd.DataFrame(comment_found, columns=['Project', 'File_Path', 'SATD_Comment', 'Commit_Before', 'Commit_Removal', 'Diff'])
print("============")
print(df_comment_found.head())
print(df_comment_found.shape)

c = 0
above_below_codes = []
for i, row in df_comment_found.iterrows():
    diff_lines = row['Diff'].split('\n')
    for i, line in enumerate(diff_lines):
        if row['SATD_Comment'] in line:
            c += 1
            above = '\n'.join(diff_lines[:i])
            below = '\n'.join(diff_lines[i:])
            above_below_codes.append(
                [row['Project'], row['File_Path'], row['SATD_Comment'], row['Commit_Before'], row['Commit_Removal'],
                 row['Diff'], above, below])
df_above_below_codes = pd.DataFrame(above_below_codes, columns=['Project', 'File_Path', 'SATD_Comment', 'Commit_Before', 'Commit_Removal', 'Diff', 'Above', 'Below'])
print(df_above_below_codes.head())
print(df_above_below_codes.shape)
print(c)
print("===================")
c = 0

special_chars = ["-", "+", "/", "*"]

below_codes, above_codes = [], []
for i, row in df_above_below_codes.iterrows():
    below_lines = row['Below'].split('\n')
    clean_below_lines = [' '.join(x.split()) for x in below_lines]
    below_code_and_context = []
    for line in clean_below_lines:
        if line.startswith("@@ "):
            break
        elif len(line) == 0 or line[0] in special_chars:
            below_code_and_context.append(line)
        else:
            below_code_and_context.append(line)
            break
    below_codes.append('\n'.join(below_code_and_context))

    above_lines = row['Above'].split('\n')
    clean_above_lines = [' '.join(x.split()) for x in above_lines]
    reversed_above_lines = list(reversed(clean_above_lines))
    above_code_and_context = []
    for line in reversed_above_lines:
        if line.startswith("@@ "):
            break
        elif len(line) == 0 or line[0] in special_chars:
            above_code_and_context.append(line)
        else:
            above_code_and_context.append(line)
            break
    above_codes.append('\n'.join(list(reversed(above_code_and_context))))

print(len(above_codes), len(below_codes))
print(df_above_below_codes.shape)

df_satd_repayment = df_above_below_codes[['Project', 'File_Path', 'SATD_Comment', 'Commit_Before', 'Commit_Removal', 'Diff']].copy()
df_satd_repayment['Above'] = above_codes
df_satd_repayment['Below'] = below_codes
print("===================")
print(df_satd_repayment.head())
print(df_satd_repayment.shape)

satd_code, repaid_code = [], []
for i, row in df_satd_repayment.iterrows():
    above_lines = row['Above'].split('\n')
    below_lines = row['Below'].split('\n')
    before, after = [], []
    for line in above_lines:
        if line.startswith('-'):
            before.append(line[1:])
        elif line.startswith('+'):
            after.append(line[1:])
        else:
            before.append(line)
            after.append(line)
    for line in below_lines:
        if line.startswith('-'):
            before.append(line[1:])
        elif line.startswith('+'):
            after.append(line[1:])
        else:
            before.append(line)
            after.append(line)
    satd_code.append('\n'.join(before))
    repaid_code.append('\n'.join(after))

df_satd_repayment['Before'] = satd_code
df_satd_repayment['After'] = repaid_code

print(df_satd_repayment.head())
print(df_satd_repayment.shape)
print(df_satd_repayment['Before'].shape)
print(df_satd_repayment['After'].shape)
print(df_satd_repayment.columns)

sys.exit()

df_satd_repayment.to_csv('satd_repayment.csv', sep='`')
with open('satd_repayment.pkl', 'wb') as pkl:
    pickle.dump(df_satd_repayment, pkl)
print("Dataset saved...")

