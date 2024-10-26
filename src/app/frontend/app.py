import folium
import geopandas as gpd
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
from folium import plugins
from shapely import wkb
from geoalchemy2.functions import ST_GeomFromText
# from geoalchemy2.elements import

from taxi_db.model import Location, Trip
from taxi_db.utils.session import TaxiSession

session = TaxiSession().session

st.set_page_config(page_title="NYC Taxi", layout="wide")


@st.cache_data
def get_locations_df() -> pd.DataFrame:
    return pd.read_sql(session.query(Location).statement, con=session.get_bind())


locations_df = get_locations_df()
locations_df[Location.geom.name] = locations_df[Location.geom.name].apply(lambda geom: wkb.loads(bytes(geom.data)))
bzMap = locations_df.groupby(Location.borough.name)[Location.zone.name].apply(lambda x: x.tolist()).to_dict()
gdf = gpd.GeoDataFrame(locations_df, geometry=Location.geom.name)

borough = st.sidebar.selectbox('Borough', bzMap.keys())
zone = st.sidebar.selectbox('Zone', bzMap[borough])

displayed_map = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
plugins.Fullscreen(position="topleft", force_separate_button=True).add_to(displayed_map)

plugins.Draw(
    draw_options={
        "polyline": {
            "shapeOptions": {
                "color": "#ff0000",
                "weight": 5,
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
    gdf.geom.to_json(),
    name="Location",
    style_function=lambda x: {
        "fillColor": "blue",
        "color": "black",
        "weight": 2,
        "fillOpacity": 0.5,
    },
).add_to(displayed_map)

output = st_folium(displayed_map, use_container_width=True, returned_objects=["all_drawings"])

if st.sidebar.button("Add trip to database"):
    if drawings := output.get("all_drawings"):
        for idx, drawing in enumerate(drawings):
            linestring_wkt = f"LINESTRING({', '.join([f'{latitude} {longitude}' for latitude, longitude in drawing["geometry"]["coordinates"]])})"
            geom = ST_GeomFromText(linestring_wkt, 4326)
            trip = Trip(
                tpep_pickup_datetime="2024-10-26 12:31:11",
                tpep_dropoff_datetime="2024-10-26 12:31:11",
                passenger_count=2,
                pu_location_id=1,
                do_location_id=1,
                geom=geom,
            )
            session.add(trip)
            session.commit()

