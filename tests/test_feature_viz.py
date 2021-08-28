import unittest
import sys
import pandas as pd

sys.path.append('../scripts')

df = pd.read_csv("../data/mean_features.csv")
df.drop('Unnamed: 0',axis=1,inplace=True)

from feature_viz import VisualizeFeature

class TestFileHandler(unittest.TestCase):
    
    def test_hist_plot(self):
        viz = VisualizeFeature()

        test_list = ['radius_mean','texture_mean','perimeter_mean','area_mean','smoothness_mean','compactness_mean','concavity_mean',
                     'concave points_mean','symmetry_mean']
        NoneType = type(None)
        actual = viz.histplot(df,test_list)
        self.assertTrue(isinstance(actual,NoneType))
        

        
if __name__ == '__main__':
  unittest.main()


