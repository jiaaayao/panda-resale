import streamlit as st
import datetime as dt
import plotly.express as px
from clean import cleaned
from analysis import filter_by_towns, filter_by_flat_type, filter_by_date

town_name = st.sidebar.multiselect(
    label="Towns",
    options=cleaned.town.cat.categories.values,
    select_all=True,
    default=cleaned.town.cat.categories.values,
    key="town_select",
)

flat_type = st.sidebar.multiselect(
    label="Flat Type",
    options=cleaned.flat_type.cat.categories.values,
    select_all=True,
    default=cleaned.flat_type.cat.categories.values,
    key="flat_type_select",
)

st.title('Panda Resale')
st.header(body='A Look at HDB Resale Data from 2012 to 2017', divider="gray")

st.plotly_chart(
    figure_or_data=px.scatter(
        data_frame=filter_by_flat_type(filter_by_towns(cleaned, town_name), flat_type),
        x="month",
        y="resale_price",
        color="town",
        hover_data=["flat_type", "flat_model"]
    ),
    height="stretch",
    key="chart1",
)