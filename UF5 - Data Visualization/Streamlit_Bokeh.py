import pandas as pd

import streamlit as st
from bokeh.plotting import figure

url = "https://raw.githubusercontent.com/tylerjrichards/Streamlit-for-Data-Science/refs/heads/main/trees_app/trees.csv"

st.title('SF Trees')
st.write(
"This app demonstrates plotting Bokeh scatterplot charts embedded in a Streamlit dashboard"
)
st.subheader('Bokeh Chart')
trees_df = pd.read_csv(url)
st.write(trees_df.describe())
scatterplot = figure(title = 'Bokeh Scatterplot')
scatterplot.scatter(trees_df['dbh'], trees_df['site_order'])
st.bokeh_chart(scatterplot)
scatterplot.xaxis.axis_label = "dbh"
