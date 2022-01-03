# import the libraries required for the functions
import plotly.graph_objects as go
from math import *
import pandas as pd

# define a function to draw plotly scatter mapboxes from multiple columns holding different cluster classes for each lon:lat couple
def map_clusters(df, lat_col, lon_col, k_cols, access_token, title='Mapbox'):

    '''
    Plots a scatter_mapbox of the latitude and longitude data colored by cluster labels given a dataframe
    and the name of the columns containing the latitude, longitude and cluster labels data.

    Args:
        df: pd.dataframe in which the datas are stored
        lat_col: string, name of the column in which the latitudes are stored
        lon_col: string, name of the column in which the longitudes are stored
        k_cols: list, name of the columns containing the cluster labels
        title: string, title of the figure
        access_token: plotly mapbox access token for plotly's API

    Returns:
    fig: a plotly figure object

    '''


    fig = go.Figure() #instatiate the figure object
    buttons = [] #initialize the list that will contain the button objects

    for i, k in enumerate(k_cols): #loop over indexes and items in k_cols to generate traces and buttons

        mask = df.loc[ : , k] != -1 #generate mask in case clusters belong to outliers with dbscan. No effect in case of k-means clustering

        #Add the traces to the figure object
        fig.add_trace(
            go.Scattermapbox(
                lat = df.loc[mask][lat_col],
                lon = df.loc[mask][lon_col],
                mode = 'markers',
                text = df.loc[mask][k],
                marker=go.scattermapbox.Marker(
                    color = df.loc[mask][k],
                    colorscale="Viridis"),
                visible = (True if i == 0 else False) #display the trace for the first cluster
                            )
                    )

        #Generate the buttons for the update menu
        vis = [False] + [False] * (len(k_cols))
        vis[i] = True
        args = [{'visible' : vis}]
        buttons.append(go.layout.updatemenu.Button(label = k_cols[i], method = "update", args = args))

    fig.update_layout(
        title = {'text': title, 'y':0.97, 'x':0.23, 'xanchor': 'left', 'yanchor': 'top'},
        showlegend = False,
        hovermode='closest',
        mapbox=dict(
            accesstoken=access_token,
            center=dict(
                lat=df[lat_col].median(),
                lon=df[lon_col].median()
                        ),
            pitch=0,
            zoom=9
                    ),
        updatemenus = [go.layout.Updatemenu(active = 0, buttons = buttons)], \
                    autosize = False, \
                    width = 900, \
                    height = 600, \
                    margin={'l':15, 'r':10, 'b':10, 't':40}
                    )


    return fig


# creates a scatter mapbox subplot of the desired dataframe colums

def subplot_clusters(df, lat_col, lon_col, k_cols, access_token, title='Mapbox graph', frac = 0.5, zoom = 8, nb_cols = 1, width = 900, height = 900):

    '''
    Plots scatter_mapbox subplots of the latitude and longitude data colored by cluster labels given a dataframe,
    the name of the columns containing the latitude, longitude and cluster labels data and the nb of wanted columns
    in the subplot

    Args:
        df: pd.dataframe in which the datas are stored
        lat_col: string, name of the column in which the latitudes are stored
        lon_col: string, name of the column in which the longitudes are stored
        k_cols: list, name of the columns containing the cluster labels
        access_token: plotly mapbox access token for plotly's API
        title: string, title of the figure
        frac: float, fraction of data to plot to avoid crashing in case too many plots. Frac = 1 plots all the data
        zoom: int, zomm level on the mapbox
        nb_cols: int, the number of columns desired for the subplots
        width: int, the width of the figure object
        height: int, the height of the figure object

    Returns:
    fig: a plotly figure object

    '''

    fig = go.Figure() # instantiate the figure object


    counter = 0 # initialize a counter used for plotting
    # k_cols.reverse() #reverse colum items to plot in the right order

    # dividing the layout window into the desired number of subplots

    nb_plots = len(k_cols) # count the total number of plots
    nb_cols = nb_cols # the number of columns specified as an argument. Default is 1
    nb_rows = ceil(nb_plots / nb_cols) # calculate the number of rows required to fit all the plots

    # divide the plotting space to fit all the plots
    x_frontiers = [i/nb_cols for i in range(nb_cols + 1)]
    y_frontiers = [i/nb_rows for i in range(nb_rows + 1)]

    # calculate each subplot's x and y coordinates
    x_coor = [[x_frontiers[i],x_frontiers[i+1]] for i in range(len(x_frontiers)-1)]
    y_coor = [[y_frontiers[i],y_frontiers[i+1]] for i in range(len(y_frontiers)-1)]
    y_coor.reverse()

    for row in y_coor:
        for col in x_coor:

            try: # in case there are empty subplots

                # prepare the data for plotting by masking DBSCAN outliers => -1
                df_col = k_cols[counter] # retrieve the column name of index 'counter'
                mask = df[df_col] != -1 # boolean where -1 returns False to hide outliers from the graph is DBSCAN was used
                df_plot = df.loc[mask].sample(frac = frac) # sample the dataframe in case to many points for plotly. Default = 0.5 <=> 50%

                # add the traces to the figure object
                fig.add_trace(go.Scattermapbox(
                                    lat = df_plot[lat_col],
                                    lon = df_plot[lon_col],
                                    mode = 'markers',
                                    marker = go.scattermapbox.Marker(
                                                        color = df_plot[df_col],
                                                        colorscale="Viridis"),
                                    text = str(df_col),
                                    subplot = 'mapbox{}'.format(counter+1)
                                            ))

                fig.update_layout({
                    'mapbox{}'.format(counter+1):{
                        'accesstoken':access_token,\
                        'bearing':0, 'pitch':0,'zoom':zoom, \
                        'domain':{'x': col, 'y': row}, \
                        'center':{'lat':df[lat_col].median(),'lon':df[lon_col].median()}
                            }
                                })




            except IndexError:
                break

            counter += 1

    fig.update_layout(showlegend = False, \
                    title = {'text': title, 'y':0.97, 'x':0.23, 'xanchor': 'left', 'yanchor': 'top'}, \
                    width = width, \
                    height = height, \
                    margin={'l':15, 'r':10, 'b':10, 't':40})

    return fig
