import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# 💫 Page settings
st.set_page_config(
    page_title="Global CO₂ Emissions Dashboard",
    page_icon="📊",
    layout="wide"
)

# 🌍 Main app title
st.title("🌍 Global CO₂ Emissions Dashboard")
st.markdown("Track and visualize global carbon dioxide emissions by country and source from 2000 to 2021.")

# 🎛️ Sidebar controls
st.sidebar.header("🎛️ Dashboard Controls")
st.sidebar.markdown("---")
st.sidebar.subheader("🔗 Share this app")

app_url = "https://afiadkay.streamlit.app"  
st.sidebar.code(app_url, language='text')


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

# --- Dark Mode Toggle ---
theme = st.sidebar.radio("Theme", options=["🌞 Light", "🌙 Dark"])
plotly_theme = "plotly_dark" if theme == "🌙 Dark" else "plotly"

# --- Top Emitters Chart ---
st.subheader("Top 5 CO₂ Emitting Countries by Source")
top_emitters = df[df['year'] == year].sort_values(by='co2', ascending=False).head(5)
sources = ['coal_co2', 'oil_co2', 'gas_co2', 'cement_co2', 'other_industry_co2']
stacked_totals = top_emitters[sources].sum(axis=1)
max_y = stacked_totals.max()

fig, ax = plt.subplots(figsize=(10, 6))
top_emitters.set_index('country')[sources].T.plot(kind='bar', stacked=True, ax=ax)
ax.set_ylim(0, max_y * 1.15)
ax.set_title(f'Top 5 CO₂ Emitting Countries by Source ({year})')
ax.set_ylabel('CO₂ Emissions (Mt)')
ax.set_xlabel('Emission Source')
plt.tight_layout()
st.pyplot(fig)

# --- Plotly Choropleth Map ---
st.subheader("Global CO₂ Emissions Map")
map_df = df[df['year'] == year][['country', 'co2']].rename(columns={'country': 'location', 'co2': 'CO₂ Emissions'})

fig_map = px.choropleth(
    map_df,
    locations='location',
    locationmode='country names',
    color='CO₂ Emissions',
    color_continuous_scale='Viridis',
    template=plotly_theme,
    title=f'CO₂ Emissions by Country ({year})',
    labels={'CO₂ Emissions': 'Mt CO₂'}
)
st.plotly_chart(fig_map, use_container_width=True)

# --- Country Line Chart ---
st.subheader(f"CO₂ Emissions Trend: {country}")
country_df = df[df['country'] == country]
max_line_y = country_df['co2'].max()

fig_line = px.line(
    country_df, x='year', y='co2',
    title=f"CO₂ Emissions Over Time for {country}",
    labels={'co2': 'CO₂ Emissions (Mt)', 'year': 'Year'},
    template=plotly_theme,
    range_y=[0, max_line_y * 1.1]
)
st.plotly_chart(fig_line, use_container_width=True)

with st.expander("🔍 Show Raw Data"):
    st.dataframe(country_df)
