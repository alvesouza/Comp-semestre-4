import pandas as pd
import math
import datetime

data_df = pd.read_csv("accident_data.csv")
print(data_df.axes)
print(data_df.columns)
print(data_df['Local'].unique())
print(data_df[(data_df['Local'] == 'Local_04')]['Accident Level'].value_counts())
print(data_df[(data_df['Local'] == 'Local_04')]['Accident Level'].value_counts().max())


# print(data_df[(data_df['Local'] == 'Local_04')]['Accident Level'].count())
# print(data_df[(data_df['Local'] == 'Local_04')]['Accident Level'].unique())
# print(data_df[(data_df['Local'] == 'Local_04')]['Accident Level'].max())
# print(datetime.datetime(data_df["Data"][1])-datetime.datetime(data_df["Data"][0]))
# print(data_df)

# def give_entropy_most_likely_result(data_frame=pd.DataFrame(), param="", result=""):
#     list_values = data_frame[param].unique()
#     entropy = 0
#     count_param = data_frame[result].count()
#     for value in list_values:
#         dt = data_df[(data_df[param] == value)]
#         value_counts = dt[result].value_counts()
#         # print(value_counts)
#         count = dt[result].count()
#         # result_more_frequent = value_counts.idxmax()
#         frequency = value_counts.max()
#         prob = frequency / count
#         # print("frequency = ", frequency, "count = ", count, "prob = ", prob)
#         if prob < 1:
#             entropy -= (prob * math.log(prob, 2) + (1 - prob) * math.log((1 - prob), 2)) * (count / count_param)


def give_us_best_entropy_param(data_frame=pd.DataFrame(), params=[], result=""):
    list_values = []
    best_p = ""
    best_entropy = 0
    unchanged_entropy = True
    # print("\nparams = ", params)
    # print("result = ", result, end='\n\n')
    count_rows = data_frame[result].count()
    # print("count_rows = ", count_rows)
    # print(data_frame)
    for p in params:
        if p != result:
            list_values = data_frame[p].unique()
            entropy = 0
            # print("p = ", p)
            # print("list_values = ", list_values)
            for value in list_values:
                # print("value = ", value)
                dt = data_frame[(data_frame[p] == value)]
                # print(dt)
                value_counts = dt[result].value_counts()
                # print("value_counts = ", value_counts, end='\n\n')
                count = dt[result].count()
                result_more_frequent = value_counts.idxmax()
                frequency = value_counts.max()
                # prob = frequency / count

                for index in value_counts:
                    print("index = ", index)
                    prob = index/count
                    print("count = ", count, "count_rows = ",
                                                    count_rows, "prob = ", prob, end='\n\n')
                    if prob < 1 and prob > 0:
                        # print("addedEntropy = ", -(prob * math.log(prob, 2)) * (count / count_rows))
                        entropy -= (prob * math.log(prob, 2)) * (count / count_rows)
                # if prob < 1:
                #     entropy -= (prob * math.log(prob, 2) + (1 - prob) * math.log((1 - prob), 2)) * (count / count_rows)
                # print("entropy = ", entropy)
            #
            # print("entropy = ", entropy)
            if best_entropy > entropy or unchanged_entropy:
                best_entropy = entropy
                best_p = p
                unchanged_entropy = False
    print("best_entropy = ", best_entropy)
    print("best_p = ", best_p)
    return best_p, best_entropy


# print(data_df)
# ['Countries', 'Local', 'Industry Sector',
#                                            'Potential Accident Level', 'Genre', 'Employee ou Terceiro',
#                                            'Risco Critico']
print(give_us_best_entropy_param(data_df, ['Countries', 'Local', 'Industry Sector',
                                           'Potential Accident Level', 'Genre', 'Employee ou Terceiro',
                                           'Risco Critico'], "Accident Level"))


class Connection_Sub_Tree(object):
    def __init__(self, value, entropy, data_frame, params, result):
        self.value = value
        value_counts = data_frame[result].value_counts()
        self.expected_result = value_counts.idxmax()
        self.sub_tree = Tree(data_frame, params, result)
        self.entropy = entropy
        if not self.sub_tree.leaf:
            if self.entropy > self.sub_tree.entropy:
                self.entropy = self.sub_tree.entropy
            else:
                self.sub_tree.leaf = True
                self.sub_tree.sub_trees.clear()


class Tree(object):
    def __init__(self, data_frame, params, result):
        if isinstance(data_frame, pd.DataFrame):
            self.data_frame = data_frame
            self.number_rows = self.data_frame[result].count()
            self.leaf = False
            if isinstance(params, list) and (all(isinstance(n, str) for n in params)):
                self.params = params
            else:
                raise TypeError("Error, param has to be a list of strings")
            if isinstance(result, str):
                self.result = result
            else:
                raise TypeError("Error, result has to be string")

            if len(self.params) > 0:
                self.param, self.entropy = give_us_best_entropy_param(self.data_frame, self.params, self.result)
                self.sub_trees = []
                parameters_sub = self.params.copy()
                # print("parameters_sub = ", parameters_sub)
                print("self.param = ", self.param)
                parameters_sub.remove(self.param)
                print("parameters_sub = ", parameters_sub)
                values = data_frame[self.param].unique()
                for value in values:
                    print("value = ", value)
                    # print(data_frame[data_frame[self.param] == value])
                    self.sub_trees.append(
                        Connection_Sub_Tree(value, self.entropy,
                                            data_frame[
                                                data_frame[self.param] == value
                                                ],
                                            parameters_sub,
                                            result
                                            )
                    )
                self.entropy = 0
                # print("teste ///////////////////////////////")
                for sub in self.sub_trees:
                    # print("sub.value = ", sub.value)
                    self.entropy += sub.sub_tree.number_rows*sub.entropy/self.number_rows
            else:
                self.leaf = True

        else:
            raise TypeError("Error, error data_frame has to be a pandas' DataFrame")

tree = Tree(data_df, ['Countries', 'Local', 'Industry Sector',
               'Potential Accident Level', 'Genre', 'Employee ou Terceiro', 'Risco Critico'], "Accident Level")

print(tree.entropy)
print(tree.sub_trees[0].sub_tree.leaf)
print(tree.sub_trees[0].value)

data_df = data_df[['Countries', 'Local', 'Industry Sector',
               'Potential Accident Level', 'Genre', 'Employee ou Terceiro', 'Risco Critico']]

# def function02(data_df):
#     return data_df[(data_df['Potential Accident Level'] == 'IV')]
# def function01(data_df):
#     dt = function02(data_df[(data_df['Countries'] == 'Country_01')])
#     print(dt['Countries'].count())

# count = dt[result].count()
# print(function01(data_df))

data_df = data_df[(data_df['Countries'] == 'Country_01')]
data_df = data_df[(data_df['Potential Accident Level'] == 'IV')]
# data_df = data_df[(data_df['Employee ou Terceiro'] == 'Third Party')]
# data_df = data_df[(data_df['Local'] == 'Local_01')]
print(data_df)