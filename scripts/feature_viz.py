import pandas as pd

import plotly.express as px
import plotly.io as pio

pio.renderers.default = "svg"

df = pd.read_csv(r"..\data\mean_features.csv")
df.drop('Unnamed: 0',axis=1,inplace=True)


class VisualizeFeature():

    def __init__(self):
        pass

    def histplot(self,df:pd.DataFrame,col_list:list):

        for x in col_list:
            fig = px.histogram(df, x=x, color="diagnosis", marginal="box",hover_data=df.columns)

            fig.show()


    def barplot(self,df:pd.DataFrame,title:str):
        fig = px.bar(df.drop('diagnosis',axis=1).corrwith(df.diagnosis),title = title)

        fig.show()


