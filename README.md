# UBER Pickups 

**<font size = 4>Visit the app at https://share.streamlit.io/nicolas-hegerle/p05_uber_pickups/main</font>**

## Company's Description 📇

<a href="http://uber.com/" target="_blank">Uber</a> is one of the most famous startup in the world. It started as a ride-sharing application for people who couldn't afford a taxi. Now, Uber expanded its activities to Food Delivery with <a href="https://www.ubereats.com/fr-en" target="_blank">Uber Eats</a>, package delivery, freight transportation and even urban transportation with <a href="https://www.uber.com/fr/en/ride/uber-bike/" target="_blank"> Jump Bike</a> and <a href="https://www.li.me/" target="_blank"> Lime </a> that the company funded. 


The company's goal is to revolutionize transportation accross the globe. It operates now on about 70 countries and 900 cities and generates over $14 billion revenue! 😮

## Project 🚧

One of the main pain point that Uber's team found is that sometimes drivers are not around when users need them. For example, a user might be in San Francisco's Financial District whereas Uber drivers are looking for customers in Castro.  

(If you are not familiar with the bay area, check out <a href="https://www.google.com/maps/place/San+Francisco,+CA,+USA/@37.7515389,-122.4567213,13.43z/data=!4m5!3m4!1s0x80859a6d00690021:0x4a501367f076adff!8m2!3d37.7749295!4d-122.4194155" target="_blank">Google Maps</a>)

Eventhough both neighborhood are not that far away, users would still have to wait 10 to 15 minutes before being picked-up, which is too long. Uber's research shows that users accept to wait 5-7 minutes, otherwise they would cancel their ride. 

Therefore, Uber's data team would like to work on a project where **their app would recommend hot-zones in major cities to be in at any given time of day.**  

## Goals 🎯

Uber already has data about pickups in major cities. Your objective is to create algorithms that will determine where are the hot-zones that drivers should be in. Therefore you will:

* Create an algorithm to find hot zones 
* Visualize results on a nice dashboard 

## Scope of this project 🖼️

To start off, Uber wants to try this feature in New York city. Therefore you will only focus on this city. Data can be found here: 

👉👉<a href="https://full-stack-bigdata-datasets.s3.eu-west-3.amazonaws.com/Machine+Learning+non+Supervis%C3%A9/Projects/uber-trip-data.zip" target="_blank"> Uber Trip Data</a> 👈👈

**You only need to focus on New York City for this project**

## Results and available files

### <ins>Notebooks</ins>
* ```P05_Uber_PickUps.ipynb``` contains EDA as well as clustering with K-Means clustering and DBSCAN
* DBSCAN clustering allows insightfull clustering of Uber PickUps in NYC by showing hot-spots of pickups per hour and day

### <ins>Python script</ins>
* ```graph_func.py``` a script to plot satter mapboxes to display cluster on maps
    * ```map_clusters``` generates an interactive scatter mapbox with dropdown menus allowing to plot results of multiple clustering and switch between each clustering results
    * ```subplot_cluster``` generates a subplot where the results of each clustering are displayed on individual subplots. Results of such plotting are available in ```cluster_maps```.

### <ins>streamlit_app.py</ins>
* script to build a webapp to visualize Uber PickUp clustering.  
Visit the app: https://share.streamlit.io/nicolas-hegerle/p05_uber_pickups/main 