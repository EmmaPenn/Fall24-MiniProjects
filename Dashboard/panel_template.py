import panel as pn
import sankey as sk
import plotly.express as pl
from ADIAPI import INDICATORS
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
'''

Author: John Rachlin 
Modified By: Emma Penn

Description: A File To generate a dashboard for the Data Anxiety and Depression Indicators CSV File From the Center 
For Disease Control (CDC)
Documentation Links:


GEOPANDAS: 
https://geopandas.org/en/stable/gallery/choro_legends.html
https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.plot.html
https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoSeries.scale.html
https://geopandas.org/en/stable/docs/user_guide/geometric_manipulations.html#examples-of-geometric-manipulations
https://geopandas.org/en/stable/docs/user_guide/mapping.html
https://geopandas.org/en/stable/docs/user_guide/interactive_mapping.html 


PANEL HOLOVIZ: 
https://panel.holoviz.org/reference/panes/Str.html
https://panel.holoviz.org/reference/widgets/MultiChoice.html 
https://panel.holoviz.org/reference/widgets/Checkbox.html
https://panel.holoviz.org/reference/templates/FastListTemplate.html
https://panel.holoviz.org/reference/panes/Plotly.html
https://panel.holoviz.org/reference/widgets/IntSlider.html
https://panel.holoviz.org/reference/layouts/Tabs.html#tabs-location
https://panel.holoviz.org/reference/layouts/Column.html
https://panel.holoviz.org/reference/panes/Matplotlib.html#using-pandas-plot
https://panel.holoviz.org/reference/widgets/TextInput.html 



PLOTLY: 
https://plotly.com/python/line-charts/
https://plotly.com/python/sankey-diagram/
'''

# Loads javascript dependencies and configures Panel (required)
pn.extension()

# Declare the api

api = INDICATORS()
api.load_data("Indicators.csv")
api.load_geodata("States/tl_2024_us_state.shp")



# WIDGET DECLARATIONS

# Search Widgets

subgroup = pn.widgets.MultiChoice(name = "Subgroup", options = api.get_unique("Subgroup"),
                                  value = ["18 - 29 years"])

disorder = pn.widgets.Select(name = "Disorder", options = api.get_unique("Indicator"))

weeks = pn.widgets.Select(name = "Weeks", options = api.get_unique("Time Period"))


# plotting Widgets
width = pn.widgets.IntSlider(name= "Line Width", start = 1, end = 10, step = 1, value = 1)

thickness = pn.widgets.IntSlider(name = "Thickness", start = 0, end = 50, step = 5, value = 5)

title = pn.widgets.TextInput(name = "Title", placeholder = "Default Title")



# CALLBACK FUNCTIONS
def sankey_widget(subgroup, disorder, cols, thickness, width, title):
    '''
    Callback function that takes in 2 strings, a list of columns, and 2 number of width and height.
     Makes a sankey with the subgroup and disorder widget by filtering for those values within
    the columns input, uses the height and width from the input to modify the saneky, returns a sankey figure
    '''
    groups = [disorder, subgroup]
    network = api.get_local_network(groups, cols)
    network = api.group_df(network, cols, "Value")
    fig = sk.make_sankey(network, cols, vals = "Value", thickness = thickness, title = title, line_width = width)
    fig.show()
    return fig

def line_plot_tab(subgroup, disorder, weeks, cols, title):
    '''
    Takes in 3 strings for the subgroup, disorder, and weeks were the subgroup and weeks are lists.
    Makes a lineplot with the y value being the value for the percentage of the group with the disorder and the x-axis
    being the time period/weeks. Returns the Lineplot
    '''
    weeks = list(range(1, weeks+1))
    groups = [disorder, subgroup, weeks]
    network = api.get_local_network(groups, cols)
    lineplot = pl.line(network, x = "Time Period", y = "Value", color = "Subgroup", markers = True,
                       title = title)

    lineplot.show()


    return lineplot

def geo_plot(disorder, cols):
    '''
    Creates a Map with each of the states' colors referring  to the percentage of people with the disorder in the state,
    gets the disorder value from the widget and cols is the columns in which to filter for the disorder value. Uses
    the now filtered dataframe to generate the map.

    Code adapted from Code example in Documentation in Panel Holozviz, Using Pandas .plot(), code can be found here:
    https://panel.holoviz.org/reference/panes/Matplotlib.html#using-pandas-plot

    Code Adapted from code from Professor Laney Strange titled Geopandas w/election Data, March 19, 2023,
    Code can be Found Here:
    https://course.ccs.neu.edu/ds2500/schedule.html

    '''

    groups = [disorder]
    network = api.get_local_network(groups, cols)
    network = api.group_df(network, ["State"], "Value")
    network = api.merge_dfs(network, "State", "NAME")

    fig, ax = plt.subplots(1, 1, figsize = (15,15))
    legend = make_axes_locatable(ax)
    cax = legend.append_axes('right', size = "1%", pad = 0.1)
    ax = api.generate_plot(network, geo_col = "geometry", color_col = "Value", ax = ax, cax = cax, scale_y = 1, scale_x =6)

    geo_pane = pn.pane.Matplotlib(fig, tight = True)


    return geo_pane




# CALLBACK BINDINGS (Connecting widgets to callback functions)
show_sankey = pn.bind(sankey_widget, subgroup, disorder, cols = ["Indicator", "Subgroup"], width= width,
                      thickness = thickness, title = title)

plotting = pn.bind(geo_plot, disorder, cols = ["Indicator"])

make_lineplot = pn.bind(line_plot_tab, subgroup, disorder, weeks, cols  = ["Indicator", "Subgroup", "Time Period"],
                        title = title)








# DASHBOARD WIDGET CONTAINERS ("CARDS")

card_width = 320

# making the search card
search_card = pn.Card(
    pn.Column(
        subgroup,
        disorder,
        weeks
    ),
    title="Search", width=card_width, collapsed=False
)

# making the plot card
plot_card = pn.Card(
    pn.Column(
        width,
        thickness,
        title,
    ),

    title="Plot", width=card_width, collapsed=True
)


# LAYOUT

layout = pn.template.FastListTemplate(
    title="Anxiety and Depressive Disorders in the US",
    sidebar=[
        search_card,
        plot_card,
    ],
    theme_toggle = False,
    main=[
        pn.Tabs(
            ("Sankey",show_sankey),  # Replace None with callback binding
            ("Line plot", make_lineplot),
            ("Map", plotting),# Replace None with callback binding
            active=0  # Which tab is active by default?
        ),


    ],
    header_background='#a93226'

).servable()

layout.show()
