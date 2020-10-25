import pandas as pd
import math
import numpy as np
import datetime

data_df = pd.read_csv("accident_data.csv")
# print(data_df.axes)
# print(data_df.columns)
# print(data_df['Local'].unique())
# print(data_df[(data_df['Local'] == 'Local_04')]['Accident Level'].value_counts())
# print(data_df[(data_df['Local'] == 'Local_04')]['Accident Level'].value_counts().max())


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
                # result_more_frequent = value_counts.idxmax()
                # frequency = value_counts.max()
                # prob = frequency / count

                for index in value_counts:
                    # print("index = ", index)
                    prob = index/count
                    # print("count = ", count, "count_rows = ",
                    #                                 count_rows, "prob = ", prob, end='\n\n')
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
    # print("best_entropy = ", best_entropy)
    # print("best_p = ", best_p)
    return best_p, best_entropy


# print(data_df)
# ['Countries', 'Local', 'Industry Sector',
#                                            'Potential Accident Level', 'Genre', 'Employee ou Terceiro',
#                                            'Risco Critico']
print(give_us_best_entropy_param(data_df, ['Countries', 'Local', 'Industry Sector',
                                           'Potential Accident Level', 'Genre', 'Employee ou Terceiro',
                                           'Risco Critico'], "Accident Level"))


class Connection_Sub_Tree(object):
    def __init__(self, value, entropy, data_frame, params, result, index = [0]):
        self.value = value

        self.sub_tree = Tree(data_frame, params, result, index)
        self.entropy = entropy
        if not self.sub_tree.leaf:
            if self.entropy > self.sub_tree.entropy:
                self.entropy = self.sub_tree.entropy
            else:
                self.sub_tree.leaf = True
                self.sub_tree.entropy = self.entropy
                self.sub_tree.sub_trees.clear()
        else:
            self.sub_tree.entropy = self.entropy


class Tree(object):
    def __init__(self, data_frame, params, result, index = [0]):
        if isinstance(data_frame, pd.DataFrame):
            self.data_frame = data_frame
            self.number_rows = self.data_frame[result].count()
            self.leaf = False
            self.index = index[0]
            index[0] += 1
            if isinstance(params, list) and (all(isinstance(n, str) for n in params)):
                self.params = params
            else:
                raise TypeError("Error, param has to be a list of strings")
            if isinstance(result, str):
                self.result = result
            else:
                raise TypeError("Error, result has to be string")
            value_counts = data_frame[result].value_counts()
            self.expected_result = value_counts.idxmax()
            if len(self.params) > 0:
                self.param, self.entropy = give_us_best_entropy_param(self.data_frame, self.params, self.result)
                self.sub_trees = []
                parameters_sub = self.params.copy()
                # print("parameters_sub = ", parameters_sub)
                # print("self.param = ", self.param)
                parameters_sub.remove(self.param)
                # print("parameters_sub = ", parameters_sub)
                values = data_frame[self.param].unique()
                for value in values:
                    # print("value = ", value)
                    # print(data_frame[data_frame[self.param] == value])
                    self.sub_trees.append(
                        Connection_Sub_Tree(value, self.entropy,
                                            data_frame[
                                                data_frame[self.param] == value
                                                ],
                                            parameters_sub,
                                            result,
                                            index
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

    def estimate_results(self, data):
        if isinstance(data, pd.DataFrame):
            data["estimated_result"] = "0"
            print(data)
            n = data["estimated_result"].count()
            index_list = data.index
            i = 0
            while i < n:
                #solve one
                data.loc[index_list[i], "estimated_result"] = self.calculate_estimation(df_testing.iloc[[i], :], self)
                # print("i = ", i, " estimated_result = ",  data["estimated_result"].values[i])
                i += 1
            return data
        else:
            raise TypeError("Error, error data_frame has to be a pandas' DataFrame")

    def calculate_estimation(self, data, tree):
        # found = False
        # print("data = \n", data)
        # print("data[0] = \n",data[tree.param].values[0])
        if isinstance(data, pd.DataFrame):
            if isinstance(tree, Tree):
                for sub in tree.sub_trees:
                    if data[tree.param].values[0] == sub.value:
                        # found = True
                        resultado = self.calculate_estimation(data, sub.sub_tree)
                        # print("resultado = ", resultado)
                        return resultado
                resultado = tree.expected_result
                # print("resultado = ", resultado)
                return resultado

data_size = data_df["Accident Level"].count()
chosen_idx = np.random.choice(data_size, replace=False, size=int(round(data_size*0.8)))
# print(data_df)
data_df
df_training = data_df.iloc[chosen_idx]
df_testing = data_df.drop(chosen_idx)

# print (pd.merge(data_df, df_training, indicator=True, how='outer')
#          .query('_merge=="left_only"')
#          .drop('_merge', axis=1))
# print(data_df['Data'][0] == '2016-01-01 00:00:00')
# print(data_df[data_df['Data'] == '2016-01-01 00:00:00'])

parameters = ['Countries', 'Local', 'Industry Sector',
               'Potential Accident Level', 'Genre', 'Employee ou Terceiro', 'Risco Critico']

# print(df_testing)
# print(df_training)
# print(df_training.iloc[0]["Local"])
# print(df_training['Potential Accident Level'][0])
# print(list(df_testing.columns).pop())

result = "Accident Level"
tree = Tree(df_training, parameters , result)

# print("tree.entropy = ", tree.entropy)
# print("tree.expected_result = ", tree.expected_result)
# print("tree.sub_trees[0].sub_tree.leaf = ", tree.sub_trees[0].sub_tree.leaf)
# print("tree.sub_trees[0].value = ", tree.sub_trees[0].value)

# data_df = data_df[['Countries', 'Local', 'Industry Sector',
#                'Potential Accident Level', 'Genre', 'Employee ou Terceiro', 'Risco Critico']]


import pydot
import os

G = pydot.Dot()
G.set_node_defaults(
    style='filled',
    shape='box',
    fontsize='10')


def create_tree_graph(tree_graph, graph):
    if isinstance(tree_graph, Tree):
        if isinstance(graph, pydot.Dot):
            # stack_tree = [tree]
            # stack_graph = []
            if tree_graph.index == 0:
                color = "green"

            elif tree_graph.leaf:
                color = "lightblue"
            else:
                color = "yellow"
            string1 = "{:^15}\n{}\n{:06.5f}\n{}".format(
                tree_graph.index,
                tree_graph.param,
                tree_graph.entropy,
                tree_graph.expected_result
            )
            node = pydot.Node(string1, fillcolor=color)
            #             if tree_graph.index == 0:
            # #                 string1 = "{:^15}\nparameter:{}\nentropy:{:06.5f}\nexpected_result:{}".format(
            # #                     tree_graph.index,
            # #                     tree_graph.param,
            # #                     tree_graph.entropy,
            # #                     tree_graph.expected_result,
            # #                     )
            # #                 string1 = "{:^15}\n{}".format(
            # #                     tree_graph.index,
            # #                     tree_graph.param
            # #                     )
            #                 string1 = "{:^15}\n{}\n{:06.5f}\n{}".format(
            #                     tree_graph.index,
            #                     tree_graph.param,
            #                     tree_graph.entropy,
            #                     tree_graph.expected_result
            #                     )
            # #                 string1 = "{:^15}".format(
            # #                     tree_graph.index,
            # # #                     tree_graph.param
            # #                     )
            # #                 print(string1)
            #                 node = pydot.Node(string1, fillcolor="green")
            #             else:
            # #                 string1 = "{:^15}\nparameter:{}\nentropy:{:06.5f}\nexpected_result:{}".format(
            # #                     tree_graph.index,
            # #                     tree_graph.param,
            # #                     tree_graph.entropy,
            # #                     tree_graph.expected_result
            # #                     )
            # #                 string1 = "{:^15}\n{}".format(
            # #                     tree_graph.index,
            # #                     tree_graph.param
            # #                     )
            #                 string1 = "{:^15}\n{}\n{:06.5f}\n{}".format(
            #                     tree_graph.index,
            #                     tree_graph.param,
            #                     tree_graph.entropy,
            #                     tree_graph.expected_result
            #                     )
            # #                 string1 = "{:^15}".format(
            # #                     tree_graph.index,
            # # #                     tree_graph.param
            # #                     )
            # #                 print(string1)
            #                 node = pydot.Node(string1, fillcolor="yellow")
            graph.add_node(node)

            for sub in tree_graph.sub_trees:
                #                 string2 = "{:^15}\nparameter:{}\nentropy:{:06.5f}\nexpected_result:{}".format(
                #                     sub.sub_tree.index,
                #                     sub.sub_tree.param,
                #                     sub.sub_tree.entropy,
                #                     sub.sub_tree.expected_result,
                #                 )
                #                 string2 = "{:^15}\n{}".format(
                #                     sub.sub_tree.index,
                #                     sub.sub_tree.param
                #                 )
                if sub.sub_tree.index == 0:
                    color = "green"
                elif sub.sub_tree.leaf:
                    color = "lightblue"
                else:
                    color = "yellow"

                string2 = "{:^15}\n{}\n{:06.5f}\n{}".format(
                    sub.sub_tree.index,
                    sub.sub_tree.param,
                    sub.sub_tree.entropy,
                    sub.sub_tree.expected_result
                )
                #                 string2 = "{:^15}".format(
                #                     sub.sub_tree.index,
                # #                     sub.sub_tree.param
                #                 )
                #                 node = pydot.Node(string2, style="filled", fillcolor="yellow")
                node = pydot.Node(string2, fillcolor=color)
                graph.add_node(node)
                edge = pydot.Edge(string1, string2, label=str(sub.value))
                graph.add_edge(edge)
                #                 print("EDGE:\n{:^15}\nparameter:{}\nentropy:{}\nexpected_result:{}\n{:^15}".format(
                #                     str(sub.value),
                #                     sub.sub_tree.param,
                #                     sub.sub_tree.entropy,
                #                     sub.sub_tree.expected_result,
                #                     sub.sub_tree.index
                #                 ))
                graph = create_tree_graph(sub.sub_tree, graph)

            return graph
        else:
            raise TypeError("'graph has to be 'pydot.Dot' object")

    else:
        raise TypeError("'create_tree_graph has to receive 'Tree' object!")


# G = create_tree_graph(tree, G)

# def function02(data_df):
#     return data_df[(data_df['Potential Accident Level'] == 'IV')]
# def function01(data_df):
#     dt = function02(data_df[(data_df['Countries'] == 'Country_01')])
#     print(dt['Countries'].count())

# count = dt[result].count()
# print(function01(data_df))

# data_df = data_df[(data_df['Countries'] == 'Country_01')]
# data_df = data_df[(data_df['Potential Accident Level'] == 'IV')]
# # data_df = data_df[(data_df['Employee ou Terceiro'] == 'Third Party')]
# # data_df = data_df[(data_df['Local'] == 'Local_01')]
# print(data_df)

# print(df_testing.iloc[[1], :])
# print(df_testing)
print(tree.estimate_results(df_testing))
# print(tree.estimate_results(df_training))
# df_testing["teste"] = 0
# df_testing.loc[3, "teste"] = 100
#
# print(df_testing)
# print(df_testing.index)
# df_testing["estimated_result"] = 'I'
print(df_testing)

i = 0
list_accident = ['I', 'II', 'III', 'IV', 'V']
n = len(list_accident)
# while i < n:
#     print("{:^4}".format(list_accident[i]))
#     i += 1
print(df_testing)
print(df_testing[(df_testing["estimated_result"] == list_accident[0])&(df_testing["Accident Level"] == list_accident[1])])

# while i < n:
#     j = 0
#     while j < n:
#         print("{:^4}".format(list_accident[j]))
#         j += 1
#     i += 1

matrix=[]

while i < n:
    j = 0
    matrix.append([])
    while j < n:
        # print(df_testing[(df_testing["estimated_result"] == list_accident[i])&
        #                             (df_testing["Accident Level"] == list_accident[j])]["Accident Level"].count())
        matrix[i].append(df_testing[(df_testing["estimated_result"] == list_accident[i])&
                                    (df_testing["Accident Level"] == list_accident[j])]["Accident Level"].count())
        j += 1
    i += 1

print(pd.DataFrame(matrix, index = list_accident, columns = list_accident))