# -*- coding: utf-8 -*-
"""causal_graph2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_zEDlijN-tq-IRX3t-psRwPq-FIHoM-g

Colab was used for the 'causal graph' because the the installation of the visualization libraries on Windows was not easy
"""

#!pip install causalnex

#!apt install libgraphviz-dev

#!pip install pygraphviz


import numpy as np
import pandas as pd

import pygraphviz
# silence warnings
import warnings
warnings.filterwarnings("ignore")

from sklearn.preprocessing import LabelEncoder


from causalnex.structure import StructureModel
from IPython.display import Image
from causalnex.structure.notears import from_pandas,from_pandas_lasso
from causalnex.plots import plot_structure, NODE_STYLE, EDGE_STYLE

df1  = pd.read_csv('data.csv')

#select the top 6 most important features according to the RandomForest Classifier

#df_c = df1[['diagnosis','area_worst','texture_worst','symmetry_worst','smoothness_worst','symmetry_mean','smoothness_worst','symmetry_mean',
#             'smoothness_mean','texture_mean']]

#df_c = df1 [[ 'area_worst','texture_worst','symmetry_worst','smoothness_worst','symmetry_mean','diagnosis']]

df_c = df1 [['diagnosis','area_mean', 'concavity_mean', 'concave points_mean', 'radius_worst','perimeter_worst',
             'area_worst', 'concavity_worst','concave points_worst']]

df = df_c.copy()

#check for non numeric columns in the DataFrame
non_numeric_columns = list(df.select_dtypes(exclude=[np.number]).columns)
print(non_numeric_columns)

#encode all non numeric columns using LabelEncoder
le = LabelEncoder()

for col in non_numeric_columns:
    df[col] = le.fit_transform(df[col])

#initialize the Structure model 
sm = StructureModel()

df

sm = from_pandas(df)

viz = plot_structure(
    sm,
    graph_attributes={"scale": "2"},
    all_node_attributes=NODE_STYLE.WEAK,
    all_edge_attributes=EDGE_STYLE.WEAK)
Image(viz.draw(format='png'))

#remove edges with threshold below 0.8
sm.remove_edges_below_threshold(0.8)
viz = plot_structure(
    sm,
    graph_attributes={"scale": "2"},
    all_node_attributes=NODE_STYLE.WEAK,
    all_edge_attributes=EDGE_STYLE.WEAK)
Image(viz.draw(format='png'))

"""'diagnosis' is having a direct effect on 'area_worst' and 'area_mean'. This does not make sense because 'diagnosis' is what we want the outcome to be."""

#we construct a new causal graph but this time,we put a constrain on 'diagnosis'
#sm.remove_edges_below_threshold(0.8)
sm_constrained = from_pandas(df, tabu_parent_nodes=["diagnosis"], w_threshold=0.8)
viz = plot_structure(
    sm_constrained,
    graph_attributes={"scale": "1.5"},
    all_node_attributes=NODE_STYLE.WEAK,
    all_edge_attributes=EDGE_STYLE.WEAK)
Image(viz.draw(format='png'))

#generate the graph using lasso
sm_constrained_lasso = from_pandas_lasso(df, tabu_parent_nodes=["diagnosis"], w_threshold=0.8,beta=0.8)
viz = plot_structure(
    sm_constrained_lasso,
    graph_attributes={"scale": "1.5"},
    all_node_attributes=NODE_STYLE.WEAK,
    all_edge_attributes=EDGE_STYLE.WEAK)
Image(viz.draw(format='png'))

#similarity between a graph plotted without lasso regularization and one plotted with lasso regularization
def jaccard_similarity(g, h):
    i = set(g).intersection(h)
    return round(len(i) / (len(g) + len(h) - len(i)),3)

jaccard_similarity(sm_constrained.edges(), sm_constrained_lasso.edges())

#Split the data row wise and test the model as we increase the data
df_1 = df.iloc[:100,:]
df_2 = df.iloc[:300,:]
df_3 = df.iloc[:,:]

sm_constrained_lasso_df_1 = from_pandas_lasso(df_1, tabu_parent_nodes=["diagnosis"], w_threshold=0.8,beta=0.8)
viz = plot_structure(
    sm_constrained_lasso_df_1,
    graph_attributes={"scale": "1.5"},
    all_node_attributes=NODE_STYLE.WEAK,
    all_edge_attributes=EDGE_STYLE.WEAK)
Image(viz.draw(format='png'))

sm_constrained_lasso_df_2 = from_pandas_lasso(df_2, tabu_parent_nodes=["diagnosis"], w_threshold=0.8,beta=0.8)
viz = plot_structure(
    sm_constrained_lasso_df_2,
    graph_attributes={"scale": "1.5"},
    all_node_attributes=NODE_STYLE.WEAK,
    all_edge_attributes=EDGE_STYLE.WEAK)
Image(viz.draw(format='png'))

# similarity between df_1 and df_2
jaccard_similarity(sm_constrained_lasso_df_1.edges(), sm_constrained_lasso_df_2.edges())

sm_constrained_lasso_df_3 = from_pandas_lasso(df_3, tabu_parent_nodes=["diagnosis"], w_threshold=0.8,beta=0.8)
viz = plot_structure(
    sm_constrained_lasso_df_3,
    graph_attributes={"scale": "1.5"},
    all_node_attributes=NODE_STYLE.WEAK,
    all_edge_attributes=EDGE_STYLE.WEAK)
Image(viz.draw(format='png'))

# similarity between df_2 and df_3
jaccard_similarity(sm_constrained_lasso_df_2.edges(), sm_constrained_lasso_df_3.edges())

#add the following relations to the graph 
sm_constrained_lasso.add_edge("concave points_mean", "diagnosis")
sm_constrained_lasso.add_edge("concave points_worst", "diagnosis")
sm_constrained_lasso.add_edge("concavity_mean", "diagnosis")
sm_constrained_lasso.add_edge("area_worst", "diagnosis")
sm_constrained_lasso.add_edge("area_mean", "diagnosis")
sm_constrained_lasso.add_edge("concavity_worst", "diagnosis")
sm_constrained_lasso.add_edge("perimeter_worst", "diagnosis")

#plot the graph
viz = plot_structure(
    sm_constrained_lasso,
    graph_attributes={"scale": "2.0"},
    all_node_attributes=NODE_STYLE.WEAK,
    all_edge_attributes=EDGE_STYLE.WEAK)
Image(viz.draw(format='png'))

from causalnex.network import BayesianNetwork

bn = BayesianNetwork(sm)

discretised_data = df.copy()

data_vals = {col: df[col].unique() for col in df.columns}

diagnosis_map = {v:'benign' if v == [str(0)]
                 else 'malignant' for v in data_vals['diagnosis']}
discretised_data["diagnosis"] = discretised_data["diagnosis"].map(diagnosis_map)
discretised_data.tail()

for i in list(discretised_data.columns[1:]):
  map = {v: 'small' if v <= (discretised_data[str(i)].max()-discretised_data[str(i)].min())/2
         else 'large' for v in data_vals[str(i)]}
  discretised_data[str(i)] = discretised_data[str(i)].map(map)

discretised_data.tail()

from causalnex.network import BayesianNetwork
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,precision_score, recall_score, f1_score

bn = BayesianNetwork(sm_constrained_lasso)

train, test = train_test_split(discretised_data, train_size=0.8, test_size=0.2, random_state=7)
bn = bn.fit_node_states(discretised_data)
bn = bn.fit_cpds(train, method="BayesianEstimator", bayes_prior="K2")
pred = bn.predict(test, 'diagnosis')
true = np.where(test['diagnosis'] == 'malignant', 1, 0)
pred = np.where(pred == 'malignant', 1, 0)


print('Recall: {:.2f}'.format(recall_score(y_true=true, y_pred=pred)))
print('F1: {:.2f} '.format(f1_score(y_true=true, y_pred=pred)))
print('Accuracy: {:.2f} '.format(accuracy_score(y_true=true, y_pred=pred)))
print('Precision: {:.2f} '.format(precision_score(y_true=true, y_pred=pred)))

"""From the metrics, the model is probably overfitting but due to limited time.I will stop here."""
