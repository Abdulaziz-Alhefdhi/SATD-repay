import sys
import javalang
from collections import Counter
from tqdm import tqdm


def extract_patterns(debt, repaid):
    # Tokenise (types & values)
    debt_tokenised, repaid_tokenised = [], []
    for dt, rp in zip(debt, repaid):
        debt_tokenised.append(list(javalang.tokenizer.tokenize(dt, ignore_errors=True)))
        repaid_tokenised.append(list(javalang.tokenizer.tokenize(rp, ignore_errors=True)))

    # Recognise pair patterns (and modify fixed patterns)
    debt_patterns, repaid_patterns = [], []
    for i, (debt_code, repaid_code) in enumerate(zip(debt_tokenised, repaid_tokenised)):
        dtpat = [(type(token).__name__, token.value) for token in debt_code]
        rppat = [(type(token).__name__, token.value) for token in repaid_code]
        debt_patterns.append(dtpat)
        repaid_patterns.append(rppat)

    debt_repaid_patterns = [(dt, rp) for dt, rp in zip(debt_patterns, repaid_patterns)]
    # Abstraction
    constant_types = {"String", "DecimalInteger", "Null", "DecimalFloatingPoint", "HexInteger", "OctalInteger"}
    localised_data = []
    for i, pair in enumerate(debt_repaid_patterns):
        local_token_dict = dict()
        id_c, c_c = 1, 1
        for token in pair[0]:
            if token[0] == "Identifier":
                if token[1] not in local_token_dict.keys():
                    local_token_dict[token[1]] = "<id>_"+str(id_c)
                    id_c += 1
            elif token[0] in constant_types:
                if token[1] not in local_token_dict.keys():
                    local_token_dict[token[1]] = "<c>_"+str(c_c)
                    c_c += 1
        for token in pair[1]:
            if token[0] == "Identifier":
                if token[1] not in local_token_dict.keys():
                    local_token_dict[token[1]] = "<id>_"+str(id_c)
                    id_c += 1
            elif token[0] in constant_types:
                if token[1] not in local_token_dict.keys():
                    local_token_dict[token[1]] = "<c>_"+str(c_c)
                    c_c += 1
        old_debt = [x[1] for x in pair[0]]
        new_debt = [x[1] if x[0] != "Identifier" and x[0] not in constant_types else local_token_dict[x[1]] for x in
                     pair[0]]
        old_repaid = [x[1] for x in pair[1]]
        new_repaid = [x[1] if x[0] != "Identifier" and x[0] not in constant_types else local_token_dict[x[1]] for x in
                     pair[1]]
        localised_data.append((local_token_dict, new_debt, old_debt, ['<sol>'] + new_repaid + ['<eol>'], old_repaid))


    return localised_data


def interpret_ids(codes, localised, gnrtd=False):
    results = []
    for i in range(len(localised)):
        local_dict = dict((id_no, token) for token, id_no in localised[i].items())
        results.append([local_dict[id_no] if id_no in local_dict.keys() else id_no for id_no in codes[i]])

    return results

