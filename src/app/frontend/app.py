import pandas as pd
import streamlit as st

from taxi_db.model import Location
from taxi_db.utils.session import TaxiSession

session = TaxiSession().session

df = pd.read_sql(session.query(Location).statement, con=session.get_bind())
d = df.groupby(Location.borough.name)[Location.zone.name].apply(lambda x: x.tolist()).to_dict()

st.title('NYC Taxi Trip Predictor')
borough = st.selectbox('Borough', d.keys())
if borough:
    zone = st.selectbox('Zone', d[borough])
