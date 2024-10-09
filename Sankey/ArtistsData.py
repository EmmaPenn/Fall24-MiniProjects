import plotly.graph_objects as go
import pandas as pd
from sankey import make_sankey
'''
Emma Penn
Professor John Rachlin 
September 25, 2024

Description: Python File For Generating Visualizations for Artists in the Museum of Contemporary Art In Chicago
'''


def clean_bio(df, variable, num, new_name):
    '''
    Takes in the dataframe, the column name to clean, a number, and the new name to store the variable.
    Will take in as many digits as specified by the num parameter and store it in a new column using the new_name.
    Returns a new dataframe with the cleaned, new column.

    '''

    df[variable] = df[variable].str.split("")
    dateser = []
    for i in df[variable]:
        date = []
        for character in i:
            if character.isdigit():
                date.append(character)
        if len(date)>=(num-1):
            date[num-1] = str(0)
            date = pd.Series(date[:num])
            date = date.str.cat(sep = "")
        else:
            date = 0
        dateser.append(date)
    df[new_name] = dateser

    return df

def group_df(df, group_names, counts_name, threshold):
    '''
    Takes in a dataframe, a list of group_names, a counts name, and a threshold number.
    Will group the data based von the group names list and will give the number of each unique name in the counts_name
    column based on the groups from the groupby function and store in a new dataframe. Filters out all the counts_name
    which is below the specified threshold nubmer
    '''
    new_group = df.groupby(group_names, as_index = False)[counts_name].nunique()
    new_group  = new_group[new_group[counts_name] > threshold]

    return new_group




def main():
    # read in data
    data = pd.read_json('artists.json')

    # drop columns with no artist bio
    data_selected = data[data["ArtistBio"].isna() == False]

    # clean the artist bio column to only have the decade of artist's birth, stores the cleaned values in a new
    # column called Decade
    data_decade = clean_bio(data_selected, "ArtistBio", 4, "Decade")


    # filter out all the rows which does not have an artist birth decade
    data_decade = data_decade[data_decade["Decade"] != 0]




    '''
    MAKING SANKEYS SPACE 
    '''

    # filter out columns where there is no Nationality or Gender listed in their row
    data_decade = data_decade[data_decade["Nationality"].isna() ==False]
    data_decade = data_decade[data_decade["Gender"].isna() ==False]


    # Sankey Plot with Nationality on the left, Decade on the right, and links values being the Artist Name
    decades_sankeydf = group_df(data_decade, ["Nationality", "Decade"],"DisplayName", 25)

    make_sankey(decades_sankeydf, ["Nationality", "Decade"], "DisplayName")



    # Sankey Plot with Nationality on the Left, Gender on the right, and links values being the Artist Name
    gender_sankeydf = group_df(data_decade, ["Nationality", "Gender"],"DisplayName", 25)

    make_sankey(gender_sankeydf, ["Nationality", "Gender"], "DisplayName")



    # Sankey PLoy with Gender on the left, Decade on the right, and the links values being the Artist Name

    gender_decade_sankeydf = group_df(data_decade, ["Gender", "Decade"], "DisplayName",
                                          25)

    make_sankey(gender_decade_sankeydf, ["Gender", "Decade"], "DisplayName")


    make_sankey(data_decade, ["Nationality", "Gender", "Decade"], "DisplayName")


if __name__ == '__main__':
    main()
