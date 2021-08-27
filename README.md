# Using Casual Inference

In this project I am going to :

1. Use casual inference using Pearl's framework.
2. Infer the causal graph from observational data and then validate the graph;
3. Merge machine learning with causal inference;


## Table of Content
- [Introduction](#introduction)
- [Data Exploration](#DataExploarion)
- [Feature Importance](#FeatureImportance)

### Introduction
Judea Pearl and his research group have developed in the last decades a solid
theoretical framework to deal with that, but the first steps toward merging it with
mainstream machine learning are just beginning.

### Data Exploration
The features of the dataset were grouped into 3 features.The 'mean features','worst error features' and 'squared error features'.
The correlation of how each variable in the group of features affected the 'diagnosis' was calculated and a bar plot showing feature
correlations were plotted.

The outliers for each variable were identified and removed.

### Feature Importance 
Random Forest Classiffier was used to identify relative importance of the features to the 'diagnosis'. A random forest classfier was 
built and trained on the dataset. The Accuracy score was calculated.It achieved an accuracy score of 95%.This score was good enough 
for our model.'fetaure_imprtances_' was used to get the order of feature importance.

### Causal Model
Causalnex was used to construct the Causal graph.Constructing the causal graph was an itereative process.
