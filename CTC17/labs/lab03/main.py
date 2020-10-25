import pandas as pd
import math
import numpy as np
import random
import pydot

def give_us_best_entropy_param(data_frame=pd.DataFrame(), params=[], result=""):
    best_p = ""
    best_entropy = 0
    unchanged_entropy = True
    count_rows = data_frame[result].count()
    for p in params:
        if p != result:
            list_values = data_frame[p].unique()
            entropy = 0
            for value in list_values:
                dt = data_frame[(data_frame[p] == value)]
                value_counts = dt[result].value_counts()
                count = dt[result].count()

                for index in value_counts:
                    prob = index / count
                    if prob < 1 and prob > 0:
                        entropy -= (prob * math.log(prob, 2)) * (count / count_rows)
            if best_entropy > entropy or unchanged_entropy:
                best_entropy = entropy
                best_p = p
                unchanged_entropy = False
    # print("best_entropy = ", best_entropy)
    # print("best_p = ", best_p)
    return best_p, best_entropy

class Connection_Sub_Tree(object):
    def __init__(self, value, entropy, data_frame, params, result, index=[0]):
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
    def __init__(self, data_frame, params, result, index=[0]):
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
                parameters_sub.remove(self.param)
                values = data_frame[self.param].unique()
                for value in values:
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
                for sub in self.sub_trees:
                    self.entropy += sub.sub_tree.number_rows * sub.entropy / self.number_rows
            else:
                self.leaf = True

        else:
            raise TypeError("Error, error data_frame has to be a pandas' DataFrame")

    def estimate_results(self, data, list_choices=['I', 'II', 'III', 'IV', 'V']):
        if isinstance(data, pd.DataFrame):
            estimated = "estimated_result"
            data[estimated] = "0"
            # print(data)
            number_entries = data["estimated_result"].count()
            index_list = data.index
            i = 0
            while i < number_entries:
                data.loc[index_list[i], estimated] = \
                    self.calculate_estimation(data.iloc[[i]], self)
                i += 1

            i = 0

            n_list = len(list_choices)
            matrix = []
            precise_estimations = 0
            while i < n_list:
                j = 0
                matrix.append([])
                while j < n_list:
                    quant = data[(data[estimated] == list_choices[i]) &
                                 (data[self.result] == list_choices[j])][
                        self.result].count()
                    if i == j:
                        precise_estimations += quant
                    matrix[i].append(quant)
                    j += 1
                i += 1

            return pd.DataFrame(matrix, index=list_choices, columns=list_choices), precise_estimations, number_entries
        else:
            raise TypeError("Error, error data_frame has to be a pandas' DataFrame")

    def calculate_estimation(self, data, tree_go):
        if isinstance(data, pd.DataFrame):
            if isinstance(tree_go, Tree):
                for sub in tree_go.sub_trees:
                    if data[tree_go.param].values[0] == sub.value:
                        # found = True
                        resultado = self.calculate_estimation(data, sub.sub_tree)
                        return resultado
                resultado = tree_go.expected_result
                return resultado

def create_tree_graph(tree_graph, graph):
    if isinstance(tree_graph, Tree):
        if isinstance(graph, pydot.Dot):
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
            graph.add_node(node)

            for sub in tree_graph.sub_trees:
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
                node = pydot.Node(string2, fillcolor=color)
                graph.add_node(node)
                edge = pydot.Edge(string1, string2, label=str(sub.value))
                graph.add_edge(edge)
                graph = create_tree_graph(sub.sub_tree, graph)

            return graph
        else:
            raise TypeError("'graph has to be 'pydot.Dot' object")

    else:
        raise TypeError("'create_tree_graph has to receive 'Tree' object!")


def random_correct_guess(data, list_choices=['I', 'II', 'III', 'IV', 'V']):
    if isinstance(data, pd.DataFrame):
        number_entries = len(data)
        number_possibilities = len(list_choices)
        i = 0
        precise_estimations = 0
        index_data = data.index
        while i < number_entries:
            rand = random.randrange(0, number_possibilities)
            if data["Accident Level"][index_data[i]] == list_choices[rand]:
                precise_estimations += 1
            i += 1

        return precise_estimations, number_entries
    else:
        raise TypeError("Error, error data_frame has to be a pandas' DataFrame")

class AprioriModel(object):
    def __init__(self, training_model, result = "Accident Level"):
        if isinstance(training_model, pd.DataFrame):
            self.result = result
            self.expected_result = training_model[self.result].value_counts().idxmax()

    def estimate_results(self, data, list_choices=['I', 'II', 'III', 'IV', 'V']):
        if isinstance(data, pd.DataFrame):
            estimated = "estimated_result"
            number_entries = len(data)
            index_list = data.index

            i = 0

            n_list = len(list_choices)
            matrix = []
            precise_estimations = 0
            while i < n_list:
                j = 0
                matrix.append([])
                while j < n_list:
                    quant = data[(data[self.result] == list_choices[i]) &
                                 (self.expected_result == list_choices[j])][
                        self.result].count()
                    if i == j:
                        precise_estimations += quant
                    matrix[i].append(quant)
                    j += 1
                i += 1
            return pd.DataFrame(matrix, index=list_choices, columns=list_choices), precise_estimations, number_entries
        else:
            raise TypeError("Error, error data_frame has to be a pandas' DataFrame")

# apriori = AprioriModel(df_training)
#
# print(apriori.estimate_results(df_testing))
# seed = 3
# seed = 63
# seed = 76
# seed = 83
# seed = 86
# seed = 95
if __name__ == '__main__':
    seed = 100
    precise_estimations = 1
    precise_estimations_apriori = 2
    # while precise_estimations <= precise_estimations_apriori:
    random.seed(seed)
    data_df = pd.read_csv("accident_data.csv")
    data_size = len(data_df)
    df_training, df_testing = \
        np.split(data_df.sample(frac=1, random_state=seed),
                 [int(.8 * len(data_df))])

    parameters = ['Countries', 'Local', 'Industry Sector',
                  'Potential Accident Level', 'Genre', 'Employee ou Terceiro', 'Risco Critico']

    G = pydot.Dot()
    G.set_node_defaults(
        style='filled',
        shape='box',
        fontsize='10')

    result = "Accident Level"
    tree = Tree(df_training, parameters, result)
    matrix, precise_estimations, number_entries = tree.estimate_results(df_testing)
    print(precise_estimations / number_entries)
    print("precise_estimations = ", precise_estimations)
    print("matrix_training = \n", matrix)
    matrix, precise_estimations, number_entries = tree.estimate_results(df_training)

    print("precise_estimations = ", precise_estimations)
    print("matrix = \n", matrix)
    # print(tree.estimate_results(df_training))

    precise_estimations_random, number_entries = random_correct_guess(data=df_testing,
                                                               list_choices=['I', 'II', 'III', 'IV', 'V'])


    apriori = AprioriModel(df_training)
    matrix_apriori, precise_estimations_apriori, number_entris_apriori = apriori.estimate_results(df_testing)
    print(precise_estimations_apriori / number_entris_apriori)
    print("precise_estimations_apriori = ", precise_estimations_apriori)
    print("matrix_apriori = \n", matrix_apriori)

