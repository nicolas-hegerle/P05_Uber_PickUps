import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime

st.set_page_config(layout="wide")

# prepare the sidebar options
daysofweek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
hours = [i for i in range(0, 24)]

date_select = st.sidebar.date_input(
    label = 'Select the date:',
    value = datetime.date(2014, 4, 1),
    min_value = datetime.date(2014, 4, 1),
    max_value = datetime.date(2014, 9, 30)
)

# transform the datetime.date object to retrieve dayofweek, month and dayofmonth
dayofweek = date_select.strftime("%A")
month = date_select.strftime("%B")
dayofmonth = date_select.strftime("%-d")

# create a slider to select the hour of the day we want to visualize
hour_select = st.sidebar.select_slider(
    label = 'Select the hour of the day:',
    options = hours
)

# create a checkbox to choose whether or not to display the DBSCAN outliers on the scattermapbox
show_outliers = st.sidebar.checkbox(
    label = 'Show outliers',
    value = False
)

# load the data based on the inputs
dir = f"datas/DBSCAN_month_day_hour/{month}/{dayofweek}.csv"
data = pd.read_csv(dir, index_col=0, parse_dates=[1])
data.rename(columns = {col:col.lower() for col in data.columns}, inplace = True)

# create the masks from the selected features
hour_mask = data['hour'] == hour_select
day_mask = data['dayofweek'] == dayofweek
month_mask = data['month'] == month
outlier_mask = data['db_clusters'] != -1


# build the plots to be displayed

# plot the clustered data with or without the outliers
if show_outliers:
    mask = hour_mask & day_mask & month_mask
    plot = px.scatter_mapbox(
        data.loc[mask], \
        lat = "lat", \
        lon = "lon", \
        color = 'db_clusters', \
        mapbox_style='carto-positron', \
        center = {'lat' : data['lat'].median(), 'lon' : data['lon'].median()}, \
        zoom = 9 \
        )
else:
    mask = hour_mask & day_mask & month_mask & outlier_mask
    plot = px.scatter_mapbox(
    data.loc[mask], \
    lat = "lat", \
    lon = "lon", \
    color = 'db_clusters', \
    mapbox_style='carto-positron', \
    center = {'lat' : data['lat'].median(), 'lon' : data['lon'].median()}, \
    zoom =9 \
    )

plot.update_layout(showlegend = True, \
                width = 700, \
                height = 400, \
                margin={'l':15, 'r':10, 'b':10, 't':40}
                )


# plot the unclustered data with transparancy
mask = hour_mask & day_mask & month_mask
plot_all = px.scatter_mapbox(data.loc[mask], lat = 'lat', lon = 'lon', \
                        mapbox_style='carto-positron', \
                        opacity = 0.3, color_discrete_sequence=['#16537E'], \
                        center = {'lat' : data['lat'].median(), 'lon' : data['lon'].median()}
                       )

plot_all.update_layout(showlegend = True, \
                width = 500, \
                height = 400, \
                margin={'l':15, 'r':10, 'b':10, 't':40})


# plot the histogram of uber pickups for the selected date
hour_counts = data.groupby(by = 'hour', as_index=False)['hour'].count()
colors = ['#16537E'] * hour_counts.shape[0]
colors[hour_select] = '#0991F0'
x = hour_counts.index
y = hour_counts['hour']

barchart = go.Figure(
    data = [
        go.Bar(
            x = x,
            y = y,
            marker_color = colors,
            text = y,
            textposition = 'auto',
        )
    ]
)

barchart.update_layout(
    height = 500,
    xaxis = dict(
        title = 'Hour of the day',
        titlefont_size = 16,
        tickfont_size = 16,
        type = 'category'
    ),
    yaxis = dict(
        title='Number of pick-ups',
        titlefont_size = 16,
        tickfont_size = 16
    )
)

# build the webpage

header = st.container()
description = st.expander(label = 'Description of the page', expanded = False)
clustering = st.container()
bars = st.container()

with header:
    st.title("Uber pick-ups DBSCAN clustering")
    st.text(f"Selected date and time: {dayofweek}, {dayofmonth} {month} between {hour_select}:00h and {hour_select + 1}:00h ")
    #st.text

with description:
        st.markdown("This project aimed at clustering Uber pick-ups in New-York city.<br> \
                    Available data are pick-ups per **day** and **time** from **May** through **September** of **2014**.<br> \
                    **DBSCAN** clustering with an <ins>epsilon = 0.2, min_sample = 10 and the manhattan metric</ins> was performed on latitude and longitude data for each hour of each day.<br> \
                    In the **sidebar** select the desired date and time you want to display. <br> \
                    You can choose to show DBSCAN outliers by ticking the ```show outliers``` box.", unsafe_allow_html=True)
                    

with clustering:
    all_data, clustered_data = st.columns(2)

    all_data.header("Scatter mapbox of all data")
    all_data.text("Plot of all the pick-ups for the selected date and time.")
    all_data.plotly_chart(plot_all, use_container_width=True)

    clustered_data.header("Scatter mapbox of clustered data")
    if show_outliers:
        clustered_data.text("Plot of the data colored by cluster with the outliers.")
    else:
        clustered_data.text("Plot of the data colored by cluster without the outliers.")
    clustered_data.plotly_chart(plot, use_container_width=True)


with bars:
    st.header("Barchart of Uber pickups")
    st.text("Number of pickups per hour for the selected date")
    st.plotly_chart(barchart, use_container_width=True)

