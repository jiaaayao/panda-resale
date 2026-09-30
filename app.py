import streamlit as st
import numpy as np
import pandas as pd
from clean import cleaned
from analysis import group_by_flat_type, group_by_town, group_by_year

town_name = st.sidebar.selectbox(
    label="Towns",
    options=cleaned.town.cat.categories.values,
    index=None,
    key="town_select",
)

flat_type = st.sidebar.selectbox(
    label="Flat Type",
    options=cleaned.flat_type.cat.categories.values,
    index=None,
    key="flat_type_select",
)

cleaned = group_by_town(group_by_flat_type(cleaned, flat_type), town_name)

st.title('Panda Resale - A look at HDB resale data from 2012 to today')
st.scatter_chart(
    data=cleaned,
    x="month",
    y="resale_price",
    x_label="Date",
    y_label="Resale Price",
    color="#ff6666",
)

add_slider = st.sidebar.slider(
    "Select a range of values",
    0.0, 100.0, (25.0, 75.0)
)
left_col, right_col = st.columns(2)
left_col.button("Press me!")

with right_col:
    chosen = st.radio(
        "Sorting hat",
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin")
    )
    st.write(f"You are in {chosen} house")
