import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
from folium import plugins

from taxi_db.model import Location
from taxi_db.utils.session import TaxiSession

session = TaxiSession().session

locations_df = pd.read_sql(session.query(Location).statement, con=session.get_bind())
bzMap = locations_df.groupby(Location.borough.name)[Location.zone.name].apply(lambda x: x.tolist()).to_dict()

st.set_page_config(page_title="NYC Taxi", layout="wide")

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

output = st_folium(displayed_map, use_container_width=True, returned_objects=["all_drawings"])

if output and "all_drawings" in output:
    if drawings := output["all_drawings"]:
        for idx, drawing in enumerate(drawings):
            st.sidebar.write(f"LineString {idx+1}")
