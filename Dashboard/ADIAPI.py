'''
Filename: ADIAPI.py
Description: defines a class and reads in a dataframe and a shape file and defines methods to modify and return
a modified dataframe.

API for Dashboards

pandas Documentation:
https://pandas.pydata.org/docs/user_guide/groupby.html
https://pandas.pydata.org/docs/reference/api/pandas.merge.html#pandas.merge


Geopandas Documentation:
https://geopandas.org/en/stable/docs/user_guide/io.html
'''


import pandas as pd
import geopandas as gpd
import pyogrio
#import matplotlib.pyplot as plt

class INDICATORS:
    df = None
    geoframe = None
    grouped_df = None

    def load_data(self, filename):
        '''
        Takes in a csv file and reads it in and makes it an attribute to the df object
        '''
        self.df = pd.read_csv(filename)

        return self.df

    def load_geodata(self, filename):
        '''
        Takes in a shape file and reads it in using geopandas and returns the geodataframe as an attribute of the object
        '''
        self.geoframe = gpd.read_file(filename)

        return self.geoframe

    def merge_dfs(self, network, colname_1, colname_2):
        '''
        Takes in a data frame and merges it with a geo dataframe by first creating a same column name, taking in all the variable names
        and making them uppercase for both dataframes and merging on the created shared name column, returns as an attribute
        of the object
        '''
        geoframe = self.geoframe
        network[colname_1] = network[colname_1].str.upper()
        geoframe[colname_1] = geoframe[colname_2].str.upper()
        self.grouped_df = pd.merge(network, geoframe, on = colname_1)
        return self.grouped_df

    def get_unique(self, attr):
        '''
        Takes in an attribute/column for the object's dataframe and returns all the unique observations for that column
        '''
        uniques = list(self.df[attr].unique())
        return uniques

    def group_df(self, df, attrs, countcol):
        '''
        Takes in a dataframe, an attribute/column and which column the mean operation should be performed on.
        Returns the dataframe with the groups and modified columns
        '''
        df = df.groupby(attrs, as_index = False)[countcol].mean()
        return df



    def get_local_network(self, groups, cols):
        '''
        Takes in a list of groups and a list of columns.
        Gets filters out the data based on the specific values in the groups list that are in the columns attributes.
        Returns the modfiied dataframe
        '''
        df = self.df
        for i in range(len(cols)):
            if i == 0:
                df = df[df[cols[0]] == groups[0]]
            else:
                attr = cols[i]
                df = df[df[cols[i]].isin(groups[i])]
        return df

    def generate_plot(self, network, geo_col, color_col, ax, cax, scale_x, scale_y):
        '''
        Takes in a dataframe, a values column for a map with color value, the axes (ax,), and legend axes (cax) and 2
        numbers used to scale the graph.Generate a geopandas plot, scales the geometry column with scale_x and scale_y
        and makes legend, uses the axes and legend axes provided from the parameters. Returns the plot.



         Code adapted from Code example in Documentation in Panel Holozviz, Using Pandas .plot(), code can be found here:
        https://panel.holoviz.org/reference/panes/Matplotlib.html#using-pandas-plot

        Code Adapted from code from Professor Laney Strange titled Geopandas w/election Data, March 19, 2023,
        Code can be Found Here:
        https://course.ccs.neu.edu/ds2500/schedule.html
        '''
        grouped_df = gpd.GeoDataFrame(network)
        grouped_df[geo_col].scale(scale_y, scale_x)


        return grouped_df.plot(column=color_col, ax=ax, cax=cax, legend=True)








