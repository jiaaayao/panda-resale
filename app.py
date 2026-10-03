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
st.header(body='A Look at HDB Resale Data from 2012 to 2016', divider="gray")

mychart = st.container()

date_range = st.slider(
    label="Hello",
    min_value=min(cleaned["month"].dt.date),
    max_value=max(cleaned["month"].dt.date),
    value=(dt.date(2012, 1, 1), dt.date(2016, 12, 1)),
    format="YYYY-MM", 
)

with mychart:
    st.plotly_chart(
        figure_or_data=px.scatter(
            #data_frame=filter_by_flat_type(filter_by_towns(cleaned, town_name), flat_type),
            data_frame=filter_by_date(
                filter_by_flat_type(
                    filter_by_towns(cleaned, town_name),
                    flat_type,
                ),
                date_range
            ),
            x="month",
            y="resale_price",
            color="town",
            hover_data=["flat_type", "flat_model"],
            labels={"month": "Month", "resale_price": "Resale Price"},  
        ),
        height="stretch",
        key="chart1",
    )