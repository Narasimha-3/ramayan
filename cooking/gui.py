import os

import streamlit as st
from streamlit_navigation_bar import st_navbar

import script as pg
st.set_page_config(layout="wide")


pages = ["QA", "Chunks", "Query Variants", "Verses"]

styles = {
    "nav": {
        "background-color": "rgb(24, 27, 43)",
        # "height" : "10rem"
    },
    "div": {
        "max-width": "69rem",
        "width": "100%",
    },
    "span": {
        "border-radius": "0.5rem",
        "color": "rgb(255, 255, 255)",
        "margin": "0 0.125rem",
        "padding": "0.4375rem 0.625rem",
    },
    "active": {
        "background-color": "rgba(204, 204, 255, 0.9)",
    },    
    "hover": {
        "background-color": "rgba(204, 204, 255, 0.7)",
    },
}


page = st_navbar(
    pages,
    # logo_path= r"D:\toxie\icon.svg",
    styles=styles,
    options=False
)

functions = {
    "QA": pg.lab,
    "Chunks": pg.chunks,
    "Query Variants": pg.query_variants,
    "Verses": pg.verses,
}

go_to = functions.get(page)
if go_to:
    go_to()