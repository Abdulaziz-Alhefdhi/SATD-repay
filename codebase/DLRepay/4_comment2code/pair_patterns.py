import sys
import javalang
from collections import Counter
from tqdm import tqdm


def extract_patterns(repaid):
    print("This function abstracts IDs and constants")
    # Tokenise (types & values)
    repaid_tokenised = []
    for rp in repaid:
        # for line in bug:
        #     buggy_tokenised.append(list(javalang.tokenizer.tokenize(line, ignore_errors=True)))
        # debt_tokenised.append(list(javalang.tokenizer.tokenize(dt, ignore_errors=True)))
        # debt_tokenised.append(list(javalang.tokenizer.tokenize(dt)))
        # for line in fix:
        #     fixed_tokenised.append(list(javalang.tokenizer.tokenize(line, ignore_errors=True)))
        repaid_tokenised.append(list(javalang.tokenizer.tokenize(rp, ignore_errors=True)))
        # repaid_tokenised.append(list(javalang.tokenizer.tokenize(rp)))

    # test_code = "public class TestClass { public void testMethod(int i) { int j = 3; x = j + i; } }"
    # # test_code = "package javalang.brewtab.com; class Test {}"
    # test_tree = javalang.parse.parse(test_code)
    # print("=============")
    # for path, node in test_tree: #.filter(javalang.tree.MethodDeclaration):
    #     # print(path)
    #     # print(path, node)
    #     print(node)
    #     print("---")
    # print(test_tree.package.name)
    # print("---")

    # print(test_tree.types[0])
    # print("---")
    # print(test_tree.types[0].name)
    #
    # print("=============")
    # print("=============")
    # print("=============")
    #
    # for a_type in test_tree.types:
    #     print(a_type)
    #     print("---")
    # print(len(test_tree.types))
    # print(type(test_tree.types[0]))

    # tokens = javalang.tokenizer.tokenize('System.out.println("Hello " + "world");')
    # tokens = javalang.tokenizer.tokenize(test_code)
    # parser = javalang.parser.Parser(tokens)
    # print(parser.parse_expression())

    # sys.exit()

    # print("=======")
    # print(" ".join([x.value for x in buggy_tokenised[0]]))
    # print(" ".join([type(x).__name__ for x in buggy_tokenised[0]]))

    # Recognise pair patterns (and modify fixed patterns)
    repaid_patterns = []
    # buggy_fixed_patterns = []
    for i, repaid_code in enumerate(repaid_tokenised):
        # dtpat = [(type(token).__name__, token.value) for token in debt_code]
        rppat = [(type(token).__name__, token.value) for token in repaid_code]
        # for code in debt_code:
        #     dtpat.append([(type(token).__name__, token.value) for token in code])
        # debt_patterns.append(dtpat)
        # for code in repaid_code:
        #     rppat.append([(type(token).__name__, token.value) for token in code])
        repaid_patterns.append(rppat)



    # buggy_context_v1 = [bp[:-1] for bp in buggy_patterns]
    # debt_patterns = [dtp[-1] for dtp in debt_patterns]
    # fixed_context_v1 = [fp[:-1] for fp in fixed_patterns]
    # repaid_patterns = [rpp[-1] for rpp in repaid_patterns]

    # print(debt_patterns[0])
    # print(repaid_patterns[0])
    # sys.exit()

    # buggy_context = []
    # for i, context in enumerate(buggy_context_v1):
    #     new_context = []
    #     for line in context:
    #         for item in buggy_actual[i]:
    #             if item[0] == "Identifier":
    #                 if item in line:
    #                     new_context.append(line)
    #                     break
    #     buggy_context.append([x for y in new_context for x in y])
        # buggy_context.append(new_context)
    # fixed_context = []
    # for i, context in enumerate(fixed_context_v1):
    #     new_context = []
    #     for line in context:
    #         for item in fixed_actual[i]:
    #             if item[0] == "Identifier":
    #                 if item in line:
    #                     new_context.append(line)
    #                     break
    #     fixed_context.append([x for y in new_context for x in y])
        # fixed_context.append(new_context)

    # print("=============")
    # for bug, fix, cv1, cv2 in zip(buggy_actual, fixed_actual, buggy_context_v1, buggy_context):
    #     print("==========================")
    #     for line in cv1:
    #         print(" ".join([x[1] for x in line]))
    #     print("=============")
    #     for line in cv2:
    #         print(" ".join([x[1] for x in line]))
    #     print("=============")
    #     print(" ".join([x[1] for x in bug]))
    #     print("=============")
    #     print(" ".join([x[1] for x in fix]))
    #     print("==========================")
    #     print("==========================")
    # sys.exit()

    # c = 0
    # for bc, bcv1 in zip(buggy_context, buggy_context_v1):
    #     if len(bc) != len(bcv1):
    #         c += 1
    # print(c)
    # c = 0
    # for fc, fcv1 in zip(fixed_context, fixed_context_v1):
    #     if len(fc) != len(fcv1):
    #         c += 1
    # print(c)

    # print(len(buggy_context_v1), len(buggy_context))
    # print(len(fixed_context_v1), len(fixed_context))
    # sys.exit()

    # c = 0
    # for v1, v2 in zip(fixed_context_v1, fixed_context):
    #     if len(v1) == len(v2):
    #         c += 1
    #         print("=======")
    #         print(v1)
    #         print("=======")
    #         print(v2)
    #         print("=======")
    # print(c)

    # for context, actual in zip(buggy_context, buggy_actual):
    #     print("=========")
    #     print([x[1] for x in context])
    #     print("-----")
    #     print([x[1] for x in actual])
    #     print("=========")

    # print(len(fixed_context_v1), len(fixed_context))
    # print(len(buggy_context_v1), len(buggy_context))
    # print(len(buggy_actual), len(fixed_actual))

    # sys.exit()


    # debt_patterns = [x for x in debt_actual]
    # repaid_patterns = [x for x in repaid_actual]

    # for i, item in enumerate(buggy_patterns):
    #     print(i+1)
    #     print(item)
    #     print("======")
    # for i, item in enumerate(fixed_patterns):
    #     print(i+1)
    #     print(item)
    #     print("======")
    # sys.exit()

    # debt_repaid_patterns = [(dt, rp) for dt, rp in zip(debt_patterns, repaid_patterns)]

        # buggy_fixed_patterns.append((buggy_pattern, fixed_pattern))

    # aggregate_buggy = [x for pattern in buggy_patterns for x in pattern]
    # aggregate_fixed = [x for pattern in fixed_patterns for x in pattern]
    # aggregate_buggy_fixed = aggregate_buggy + aggregate_fixed

    # aggregate_types = [x[0] for x in aggregate_buggy_fixed]

    # aggregate_separators = [x for x in aggregate_buggy_fixed if x[0] == "Separator"]
    # aggregate_ids = [x for x in aggregate_buggy_fixed if x[0] == "Identifier"]
    # aggregate_ops = [x for x in aggregate_buggy_fixed if x[0] == "Operator"]
    # aggregate_keywords = [x for x in aggregate_buggy_fixed if x[0] == "Keyword"]
    # aggregate_strs = [x for x in aggregate_buggy_fixed if x[0] == "String"]
    # aggregate_decints = [x for x in aggregate_buggy_fixed if x[0] == "DecimalInteger"]
    # aggregate_nulls = [x for x in aggregate_buggy_fixed if x[0] == "Null"]
    # aggregate_bools = [x for x in aggregate_buggy_fixed if x[0] == "Boolean"]
    # aggregate_mods = [x for x in aggregate_buggy_fixed if x[0] == "Modifier"]
    # aggregate_bts = [x for x in aggregate_buggy_fixed if x[0] == "BasicType"]
    # aggregate_decfloats = [x for x in aggregate_buggy_fixed if x[0] == "DecimalFloatingPoint"]
    # aggregate_annots = [x for x in aggregate_buggy_fixed if x[0] == "Annotation"]
    # aggregate_hexints = [x for x in aggregate_buggy_fixed if x[0] == "HexInteger"]
    # aggregate_octints = [x for x in aggregate_buggy_fixed if x[0] == "OctalInteger"]

    # print(Counter(aggregate_separators))
    # print(Counter(aggregate_ids))
    # print(Counter(aggregate_ops))
    # print(Counter(aggregate_keywords))
    # print(Counter(aggregate_strs))
    # print(Counter(aggregate_decints))
    # print(Counter(aggregate_nulls))
    # print(Counter(aggregate_bools))
    # print(Counter(aggregate_mods))
    # print(Counter(aggregate_bts))
    # print(Counter(aggregate_decfloats))
    # print(Counter(aggregate_annots))
    # print(Counter(aggregate_hexints))
    # print(Counter(aggregate_octints))

    # print(Counter(aggregate_types))
    # print(len(Counter(aggregate_types)))

    # no_id_change = 0
    # for i, pair in enumerate(buggy_fixed_patterns):
    #     buggy_ids = set([x for x in pair[0] if x[0] == "Identifier"])
    #     fixed_ids = set([x for x in pair[1] if x[0] == "Identifier"])
    #     if buggy_ids == fixed_ids:
    #         print("=======")
    #         print(buggy_lines[i])
    #         print(fixed_lines[i])
    #         no_id_change += 1
    # print("=======")
    # print(no_id_change)



    ########################################################################################

    constant_types = {"String", "DecimalInteger", "Null", "DecimalFloatingPoint", "HexInteger", "OctalInteger"}
    localised_data = []
    for i, pattern in enumerate(repaid_patterns):
        local_token_dict = dict()
        id_c, c_c = 1, 1
        for token in pattern:
            if token[0] == "Identifier":
                if token[1] not in local_token_dict.keys():
                    local_token_dict[token[1]] = "<id>_"+str(id_c)
                    id_c += 1
            elif token[0] in constant_types:
                if token[1] not in local_token_dict.keys():
                    local_token_dict[token[1]] = "<c>_"+str(c_c)
                    c_c += 1
        # for token in pair[1]:
        #     if token[0] == "Identifier":
        #         if token[1] not in local_token_dict.keys():
        #             local_token_dict[token[1]] = "<id>_"+str(id_c)
        #             id_c += 1
        #     elif token[0] in constant_types:
        #         if token[1] not in local_token_dict.keys():
        #             local_token_dict[token[1]] = "<c>_"+str(c_c)
        #             c_c += 1
        # new_debt = [x[1] if x[0] != "Identifier" and x[0] not in constant_types else local_token_dict[x[1]] for x in
        #              pair[0]]
        old_repaid = [x[1] for x in pattern]
        new_repaid = [x[1] if x[0] != "Identifier" and x[0] not in constant_types else local_token_dict[x[1]] for x in
                      pattern]
        localised_data.append((local_token_dict, ['<sol>'] + new_repaid + ['<eol>'], old_repaid))

    ########################################################################################





        # print("=======")
        # print(buggy_lines[i])
        # print(fixed_lines[i])
        # print(" ".join(new_buggy))
        # print(" ".join(new_fixed))




    # sys.exit()

    # types = set(aggregate_types)

    # bpc = Counter(aggregate_buggy)
    # fpc = Counter(aggregate_fixed)

    # print("=======")
    # print(set(aggregate_buggy_fixed))
    # print(len(set(aggregate_buggy_fixed)), len(aggregate_buggy_fixed))
    # print(set(aggregate_types))
    # print(len(set(aggregate_types)), len(aggregate_types))





    # Extract pair patterns
    # print("# pair pairs:", len(buggy_fixed_patterns))
    # buggy_fixed_patterns = sorted(set(buggy_fixed_patterns))
    # print("# pair patterns:", len(buggy_fixed_patterns))


    return localised_data
    # return buggy_fixed_patterns


# def interpret_ids(codes, localised, gnrtd=False):
#     results = []
#     for i in range(len(localised)):
#         local_dict = dict((id_no, token) for token, id_no in localised[i][0].items())
#         if gnrtd:
#             results.append(
#                 [local_dict[id_no] if id_no in local_dict.keys() and id_no in localised[i][1] else id_no for id_no in
#                  codes[i]])
#         else:
#             results.append([local_dict[id_no] if id_no in local_dict.keys() else id_no for id_no in codes[i]])
#
#     return results


def interpret_ids(codes, localised, gnrtd=False):
    results = []
    for i in range(len(localised)):
        local_dict = dict((id_no, token) for token, id_no in localised[i].items())
        results.append([local_dict[id_no] if id_no in local_dict.keys() else id_no for id_no in codes[i]])

    return results

