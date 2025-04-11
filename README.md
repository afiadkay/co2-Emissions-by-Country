<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/3/38/CO2_emissions_world_map.png" width="500" alt="CO₂ Emissions Dashboard">
</p>

<h1 align="center">🌍 Global CO₂ Emissions Dashboard</h1>

<p align="center">
  Visualize and analyze global carbon dioxide emissions by country and source (2000–2021).
</p>

<p align="center">
  <a href="https://your-username.streamlit.app" target="_blank">
    🚀 View Live App
  </a>
</p>

---

## 📊 About the Project

This interactive dashboard lets you explore global CO₂ emissions using data from [Our World in Data](https://github.com/owid/co2-data). It includes:

- 🌐 An interactive world map of CO₂ emissions by country
- 📈 Country-specific CO₂ trends over time
- 📊 Stacked bar charts showing top 5 emitters by source
- 🔍 Filters by year and country

Built with:
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [GeoPandas](https://geopandas.org/)
- [Plotly](https://plotly.com/)
- [Bokeh](https://docs.bokeh.org/)

---

## 🚀 Run Locally

```bash
git clone https://github.com/your-username/co2-dashboard.git
cd co2-dashboard
pip install -r requirements.txt
streamlit run co2_dashboard.py
```

---

## 🌐 Deploy to Streamlit Cloud

1. Push your project to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Click **"New app"**, connect your repo
4. Choose `co2_dashboard.py` as the main file
5. Done!

---

## 🔗 Custom Domain Setup (Optional)

To use your own domain (e.g., `co2.yourdomain.com`):

1. Go to [Streamlit Cloud](https://streamlit.io/cloud)
2. Open your app → ⚙️ → **Settings**
3. Click **"Edit domain"** → Choose "Use a custom domain"
4. Add your custom domain (e.g., `co2.yoursite.com`)
5. Update your DNS records:
    - Type: `CNAME`
    - Name: `co2`
    - Value: `streamlit-app.streamlit.app.`
6. Save changes, wait for propagation

Full details: [Streamlit Custom Domains](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/connect-custom-domain)

---

## 📜 License

MIT License — use it, improve it, share it ✨

---

## 🙌 Credits

- Data: [Our World in Data - CO₂ Dataset](https://github.com/owid/co2-data)
- Map: [Natural Earth GeoJSON](https://github.com/johan/world.geo.json)