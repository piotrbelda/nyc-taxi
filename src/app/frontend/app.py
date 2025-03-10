from typing import List

import folium
import geopandas as gpd
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
from folium import plugins
from shapely import wkb
from geoalchemy2.functions import ST_GeomFromText
from datetime import date, datetime, timedelta
import httpx

from taxi_db.model import Location, Trip
from taxi_db.utils.session import TaxiSession

session = TaxiSession().session

st.set_page_config(page_title="NYC Taxi", page_icon="taxi", layout="wide")


@st.cache_data
def get_locations_df() -> pd.DataFrame:
    locations_data = httpx.get(
        "http://backend.taxi:7000/locations/",
        headers={
            "Content-Type": "application/json",
            "accept": "application/json",
        }
    ).json()
    df = pd.DataFrame(locations_data)
    df[Location.geom.name] = df[Location.geom.name].apply(lambda geom: wkb.loads(bytes.fromhex(geom)))
    return df


locations_df = get_locations_df()
bzMap = locations_df.groupby(Location.borough.name)[Location.zone.name].apply(lambda x: x.tolist()).to_dict()
gdf = gpd.GeoDataFrame(locations_df, geometry=Location.geom.name)

st.sidebar.markdown('<h2 style="text-align: center">Trip parameters</h2>', unsafe_allow_html=True)

borough = st.sidebar.selectbox("Borough", bzMap.keys(), index=None)
zone = st.sidebar.selectbox("Zone", bzMap.get(borough, []), index=None)
if zone:
    x_min, y_min, x_max, y_max = gdf[gdf[Location.zone.name] == zone].bounds.values[0]

passenger_count = st.sidebar.slider("Passengers count", min_value=1, max_value=9, step=1)
pu_date = st.sidebar.date_input("Pickup date", date.today())

if "pu_time" not in st.session_state:
    st.session_state["pu_time"] = datetime.now().time()
pu_time = st.sidebar.time_input("Pickup time", st.session_state["pu_time"], step=timedelta(hours=1))
pu_datetime = datetime.combine(pu_date, pu_time)

do_date = st.sidebar.date_input("Dropoff date", date.today())
if "do_time" not in st.session_state:
    st.session_state["do_time"] = datetime.now().time()
do_time = st.sidebar.time_input("Dropoff time", st.session_state["do_time"], step=timedelta(hours=1))
do_datetime = datetime.combine(do_date, do_time)

fare_amount = st.sidebar.number_input("Fare amount", min_value=0.0, step=0.01)

displayed_map = folium.Map(location=[40.71207833506073, -74.01020032229094], zoom_start=10)
if zone:
    displayed_map.fit_bounds([[y_min, x_min], [y_max, x_max]])
plugins.Fullscreen(position="topleft", force_separate_button=True).add_to(displayed_map)

plugins.Draw(
    draw_options={
        "polyline": {
            "shapeOptions": {
                "color": "#ff0000",
                "weight": 2,
                "opacity": 0.7,
                "dashArray": "10, 5",
            }
        },
        "polygon": False,
        "circle": False,
        "marker": False,
        "circlemarker": False,
        "rectangle": False,
    }
).add_to(displayed_map)

folium.GeoJson(
    gdf[[Location.geom.name, Location.zone.name]].to_json(),
    name="Location",
    style_function=lambda x: {
        "fillColor": "blue",
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.3,
    },
    popup=folium.GeoJsonPopup(fields=[Location.zone.name])
).add_to(displayed_map)

output = st_folium(displayed_map, use_container_width=True, returned_objects=["all_drawings"])

if st.sidebar.button("Save trip", use_container_width=True):
    if drawings := output.get("all_drawings"):
        trips: List[Trip] = []
        for idx, drawing in enumerate(drawings):
            linestring_wkt = f"LINESTRING({', '.join([f'{longitude} {latitude}' for longitude, latitude in drawing["geometry"]["coordinates"]])})"
            geom = ST_GeomFromText(linestring_wkt, 4326)
            trip = Trip(
                tpep_pickup_datetime=pu_datetime,
                tpep_dropoff_datetime=do_datetime,
                passenger_count=passenger_count,
                fare_amount=fare_amount,
                geom=geom,
            )
            session.add(trip)
            session.commit()
            session.refresh(trip)

            trips.append(trip)
        st.session_state["trips"] = trips

trips = st.session_state.get("trips")
if st.sidebar.button("Predict duration", use_container_width=True) and trips:
    response = httpx.post(
        "http://backend.taxi:7000/predict",
        json=[
            {
                Trip.tpep_pickup_datetime.name: str(trip.tpep_pickup_datetime),
                Trip.tpep_dropoff_datetime.name: str(trip.tpep_dropoff_datetime),
                Trip.passenger_count.name: trip.passenger_count,
                Trip.trip_distance.name: float(trip.trip_distance),
                Trip.fare_amount.name: float(trip.fare_amount),
                Trip.pu_location_id.name: trip.pu_location_id,
                Trip.do_location_id.name: trip.do_location_id,
            }
            for trip in trips
        ],
        headers={
            "Content-Type": "application/json",
            "accept": "application/json",
        }
    )
