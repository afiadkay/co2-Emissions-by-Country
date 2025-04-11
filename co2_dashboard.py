
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import geopandas as gpd
from bokeh.models import LinearColorMapper, ColorBar, HoverTool
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource
from bokeh.palettes import Viridis256
import json

st.set_page_config(
    page_title="🌍 Global CO₂ Emissions Dashboard",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Global CO₂ Emissions Dashboard")
st.markdown("Track and visualize global CO₂ emissions by country and source from 2000 to 2021.")

@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv'
    df = pd.read_csv(url)
    exclude_regions = [
        'World', 'Asia', 'Africa', 'Europe','Europe (GCP)', 'European Union', 'European Union (28)',
        'European Union (27)','European Union (15)','European Union (20)','European Union (26)',
        'Africa (GCP)','North America (GCP)', 'Asia (GCP)','North America (excl. USA)','South America',
        'North America','South America (GCP)', 'International transport', 'Middle East (GCP)', 'Middle East',
        'Oceania (GCP)','Europe (excl. EU-27)', 'Europe (excl. EU-15)','Europe (excl. EU-20)','Europe (excl. EU-26)',
        'Europe (excl. EU-28)','Africa (excl. EU-15)','Africa (excl. EU-20)','Africa (excl. EU-26)',
        'Oceania', 'Non-OECD (GCP)', 'Asia (excl. China and India)','Upper-middle-income countries',
        'Lower-middle-income countries', 'High-income countries', 'OECD (GCP)'
    ]
    df = df[(df['year'] >= 2000) & (df['year'] <= 2021)]
    df = df[~df['country'].isin(exclude_regions)]
    cols_to_fill = ['cement_co2', 'coal_co2', 'oil_co2', 'gas_co2', 'other_industry_co2']
    df[cols_to_fill] = df[cols_to_fill].fillna(0)
    df = df.dropna(subset=['co2'])
    return df

df = load_data()

st.sidebar.header("Options")
year = st.sidebar.slider("Select Year", 2000, 2021, 2021)
country = st.sidebar.selectbox("Select a Country", sorted(df['country'].unique()), index=0)

st.subheader("Top 5 CO₂ Emitting Countries by Source")
top_emitters = df[df['year'] == year].sort_values(by='co2', ascending=False).head(5)
sources = ['coal_co2', 'oil_co2', 'gas_co2', 'cement_co2', 'other_industry_co2']

fig, ax = plt.subplots(figsize=(10, 6))
top_emitters.set_index('country')[sources].T.plot(kind='bar', stacked=True, ax=ax)
ax.set_title(f'Top 5 CO₂ Emitting Countries by Source ({year})')
ax.set_ylabel('CO₂ Emissions (Mt)')
ax.set_xlabel('Emission Source')
plt.tight_layout()
st.pyplot(fig)

@st.cache_data
def load_geojson():
    world_url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    return gpd.read_file(world_url)

world = load_geojson()

df['country'] = df['country'].replace({'United States': 'United States of America'})
co2_map_df = df[df['year'] == year][['country', 'co2']].rename(columns={'country': 'name'})
geo_df = world.merge(co2_map_df, on='name', how='left')
geo_df['co2'] = geo_df['co2'].fillna(0)

st.subheader("Global CO₂ Emissions Map")

geojson_data = GeoJSONDataSource(geojson=geo_df.to_json())
color_mapper = LinearColorMapper(palette=Viridis256, low=0, high=geo_df['co2'].max())

p = figure(title=f"CO₂ Emissions by Country ({year})", height=500, width=900, toolbar_location='below')
p.patches('xs', 'ys', source=geojson_data,
          fill_color={'field': 'co2', 'transform': color_mapper},
          line_color='black', line_width=0.25)
p.add_tools(HoverTool(tooltips=[("Country", "@name"), ("CO₂ Emissions", "@co2{0.0}")]))
p.add_layout(ColorBar(color_mapper=color_mapper, label_standoff=12), 'right')
st.bokeh_chart(p)

st.subheader(f"CO₂ Emissions Trend: {country}")

country_df = df[df['country'] == country]
fig_line = px.line(
    country_df, x='year', y='co2',
    title=f"CO₂ Emissions Over Time for {country}",
    labels={'co2': 'CO₂ Emissions (Mt)', 'year': 'Year'}
)
st.plotly_chart(fig_line, use_container_width=True)

with st.expander("🔍 Show Raw Data"):
    st.dataframe(country_df)
