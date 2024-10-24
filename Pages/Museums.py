import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px
import pydeck as pdk
import geopandas as gpd
from folium import Choropleth
import streamlit.components.v1 as components

# Page configuration
icon_url = "https://scontent-cdg4-3.xx.fbcdn.net/v/t1.6435-9/66793842_10157482127159712_6929831330100281344_n.png?_nc_cat=110&ccb=1-7&_nc_sid=13d280&_nc_ohc=PIRKy4NkNP0Q7kNvgF2LdY0&_nc_ht=scontent-cdg4-3.xx&_nc_gid=AmrnUg8sACmJSov1touWL0M&oh=00_AYAcYM_82DERZSUl0RLmZXOzyszIMsl6xbhevVnGoRqjyg&oe=6721E476"  # Replace with your icon URL

# Page configuration
st.set_page_config(
    page_title="Museums of France: An Interactive Exploration",
    layout="centered",
    page_icon=icon_url
)
# Main title
st.title("Museums of France: An Interactive Exploration")

path = "musees.csv"

st.write("""
The 'Museums of France' are museums accredited by the State that primarily receive its support, according to the terms of the law of January 4, 2002. The designation 'Museum of France' can be granted to museums owned by the State, another public legal entity, or a non-profit private entity. More than 1,200 museums benefit from the designation 'Museum of France'.
""")

@st.cache_data
def load_data():
    # Load the dataset
    df = pd.read_csv(path, delimiter=';')
    return df

df = load_data()

# Container for the folium map
with st.container():    

    st.title("Interactive Map of Museums in France")
    st.write("This map shows the geographical distribution of museums in France.")

    regions = ["All of France"] + list(df['region_administrative'].unique())

    region = st.selectbox('Select a region', regions)


    if region == "All of France":
        df_filtered = df
    else:
        df_filtered = df[df['region_administrative'] == region].copy()  # Use .copy() to avoid errors

    if region == "All of France":
        center_lat, center_lon = 46.603354, 1.888334  # Central coordinates of France
        zoom = 6
    else:
        center_lat, center_lon = df_filtered['latitude'].mean(), df_filtered['longitude'].mean()
        zoom = 7

    df_filtered["icon_data"] = None
    df_filtered["icon_data"] = df_filtered["icon_data"].apply(lambda x: {
        "url": icon_url,
        "width": 128,
        "height": 128,
        "anchorY": 128
    })

   
    icon_layer = pdk.Layer(
        type="IconLayer",
        data=df_filtered,
        get_icon="icon_data",
        get_position=['longitude', 'latitude'],
        get_size=15,
        pickable=True,
    )

    # Configure the initial view of the map
    view_state = pdk.ViewState(
        latitude=center_lat,
        longitude=center_lon,
    zoom=zoom,
    pitch=40
    )

    # Create the map with the IconLayer
    r = pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        layers=[icon_layer],
        initial_view_state=view_state,
        tooltip={"text": "{nom_officiel_du_musee} ({region_administrative}, {departement})"},
    )

    # Display the map in Streamlit
    st.pydeck_chart(r)



# Container for the histogram
with st.container():

    st.title("Interactive Histogram of Museums by Region")
    st.write("This histogram shows the distribution of museums by region in France.")

    choice = st.radio("Show distribution by:", ('Region', 'Department'))

    # Group museums by region or department
    if choice == 'Region':
        df_count = df.groupby('region_administrative').size().reset_index(name='number_of_museums')
        x_column = 'region_administrative'
        title = 'Distribution of Museums by Region'
    else:
        df_count = df.groupby('departement').size().reset_index(name='number_of_museums')
        x_column = 'departement'
        title = 'Distribution of Museums by Department'

    # Create the interactive histogram with Plotly
    fig = px.bar(
        df_count, 
        x=x_column, 
        y='number_of_museums', 
        title=title,
        labels={x_column: choice, 'number_of_museums': 'Number of Museums'},
        color='number_of_museums',
        color_continuous_scale=['#a9c9bc', '#2e5245'],
        height=500,
        hover_data={x_column: False, 'number_of_museums': True},
        custom_data=[x_column]
    )

    # Customize the tooltips
    fig.update_traces(hovertemplate='<b>%{customdata[0]}</b><br>Number of museums: %{y}<extra></extra>')

    # Modify the layout
    fig.update_layout(plot_bgcolor='white', paper_bgcolor='rgba(0,0,0,0)', title_font=dict(size=20, color='#3c3326'), font=dict(color='#3c3326'))

    # Display the histogram in Streamlit
    st.plotly_chart(fig, use_container_width=True)

# Container for the choropleth map
with st.container():

    st.title("Choropleth Map of Museums by Region")
    st.write("This map shows the density of museums by region in France.")

    df_museum_region = df.groupby('region_administrative').size().reset_index(name='number_of_museums')

    # Load geographical data for the regions with GeoPandas
    geo_region_path = "modified_regions.geojson"
    gdf_regions = gpd.read_file(geo_region_path)

    # Merge museum data with geographical data
    gdf_regions = gdf_regions.merge(df_museum_region, left_on='nom', right_on='region_administrative', how='left')

    # Function to create a choropleth map
    def create_choropleth(geo_data, data_col, key, tooltip_name):
        m = folium.Map(location=[46.603354, 1.888334], zoom_start=6, tiles='CartoDB positron')
        Choropleth(
            geo_data=geo_data.to_json(),
            name='choropleth',
            data=geo_data,
            columns=[key, data_col],
            key_on=f'feature.properties.{key}',
            fill_color='Greens',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name=f'Number of Museums per {tooltip_name}'
        ).add_to(m)

        for _, row in geo_data.iterrows():
            folium.Popup(f"{row[key]}: {int(row[data_col])} museums").add_to(
                folium.GeoJson(row['geometry'])
            )

        return m

    # Create the map by region
    m = create_choropleth(gdf_regions, 'number_of_museums', 'nom', 'region')

    # Display the map in Streamlit
    st_folium(m, width=700, height=600)

# Container for the temporal trend
with st.container():

    st.title("Temporal Trend of the Designation 'Museums of France'")
    st.write("This graph shows the evolution of the number of museums in France according to the date of designation.")

    # Filter rows where the date is available
    df_with_dates = df.dropna(subset=['date_arrete_attribution_appellation'])
    df_with_dates['date_arrete_attribution_appellation'] = pd.to_datetime(df_with_dates['date_arrete_attribution_appellation'], errors='coerce')
    df_with_dates['year_of_designation'] = df_with_dates['date_arrete_attribution_appellation'].dt.year

    df_count_by_year = df_with_dates.groupby('year_of_designation').size().reset_index(name='number_of_museums')

    # Create a line graph
    fig = px.line(
        df_count_by_year, 
        x='year_of_designation', 
        y='number_of_museums', 
        title="Evolution of the Number of Museums in France According to the Date of Designation",
        labels={'year_of_designation': 'Year', 'number_of_museums': 'Number of Museums'},
        height=500,
        color_discrete_sequence=['#a9c9bc']
    )

    # Customize the style of the graph
    fig.update_layout(plot_bgcolor='white', paper_bgcolor='rgba(0,0,0,0)', title_font=dict(size=20, color='#3c3326'), font=dict(color='#3c3326'))

    # Display the graph in Streamlit
    st.plotly_chart(fig, use_container_width=True)

# Container for the analysis of museums in France
with st.container():

    st.title("Analysis of Museums in France")
    st.write("This graph shows the distribution of museums by municipality in the 10 cities with the most museums.")

    # Count the number of museums by municipality and take the top 10
    df_count_municipality = df['commune'].value_counts().reset_index().head(10)
    df_count_municipality.columns = ['Municipality', 'Number of Museums']

    # Create a pie chart
    fig = px.pie(
        df_count_municipality,
        values='Number of Museums',
        names='Municipality',
        title='Top 10 Cities with the Most Museums',
        template='plotly_white',
        color_discrete_sequence=px.colors.sequential.Greens_r
    )

    # Add a subtitle
    fig.update_layout(
        annotations=[dict(text='Distribution of Museums by Municipality', x=0.5, y=0.5, font_size=15, font_color='white', showarrow=False)],
        title_font=dict(color='black')  # Title color of the chart
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig)

# Container for the interactive table
with st.container():
    
    df_tableau = df[['nom_officiel_du_musee', 'departement', 'commune', 'adresse', 'telephone']]

    st.title("Interactive Museum Table by Department and Commune")

    departement = st.selectbox(
        "Select a department",
        options=['All departments'] + sorted(df_tableau['departement'].unique())
    )

    # Check if a department has been selected before proceeding
    if departement != 'All departments':
        # Filter the available communes based on the selected department
        communes = ['All communes'] + sorted(df_tableau[df_tableau['departement'] == departement]['commune'].unique())

        # Dropdown menu to select a commune
        commune = st.selectbox(
            "Select a commune",
            options=communes
        )

        df_filtered_tableau = df_tableau[df_tableau['departement'] == departement]

        if commune != 'All communes':
            df_filtered_tableau = df_filtered_tableau[df_filtered_tableau['commune'] == commune]

        df_filtered_tableau['informations'] = df_filtered_tableau.apply(
            lambda row: f"{row['adresse']}<br>{row['telephone']}" if pd.notna(row['telephone']) else row['adresse'], axis=1
        )

        df_filtered_tableau = df_filtered_tableau.drop(columns=['adresse', 'telephone'])

        # Display the interactive table with detailed information
        st.write(df_filtered_tableau[['nom_officiel_du_musee', 'departement', 'commune', 'informations']].to_html(escape=False, index=False), unsafe_allow_html=True)
    else:
        st.write("Please select a department to view the museums.")


    

st.markdown("""
<style>
            
    .Greens .q0-6{fill:rgb(237,248,233)} 
    .Greens .q1-6{fill:rgb(199,233,192)} 
    .Greens .q2-6{fill:rgb(161,217,155)} 
    .Greens .q3-6{fill:rgb(116,196,118)} 
    .Greens .q4-6{fill:rgb(49,163,84)} 
    .Greens .q5-6{fill:rgb(0,109,44)}

    .stApp {
        padding: 10px;
        border-radius: 10px;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #3c3326;
    }
    .stButton>button{
        background-color: #649B88;
        color: white;
        border-radius: 8px;
        border: none;
    }
    .stDownloadButton > button {
        background-color: #649B88;
        color: white;
        border-radius: 8px;
        border: none;
    }
    .stDownloadButton > button:hover {
        background-color: #83a697;
        color: white;
    }
    .stButton>button:hover {
        background-color: #83a697;
        color: white;
    }

    .st-emotion-cache-6qob1r { /* Sidebar background color */
        background-color: #649B88;
    }
    .st-emotion-cache-1rtdyuf{ /* Sidebar text portfolio color */
        color: white;
    }
    .st-emotion-cache-6tkfeg{
        color: white;
    }

            
    .st-emotion-cache-1f3w014{ /* Sidebar arrow color */
        color: black;
    }
                
    }
    .stExpander p {
        color: black;
    }
    .stExpander:hover p {
        color: #649B88; /* Change the text color of <p> inside expander on hover */
    }
    
    .stExpander:hover summary svg path:nth-of-type(2) {
        fill: #649B88; /* Change the color of the arrow on hover */
    }
    
    .stContainer {
    margin-bottom: 0px !important; /* Réduit l'espace en dessous de chaque conteneur */
    padding-bottom: 0px !important;
    }
            
    iframe {
        height: 600px !important;  /* Limiter la hauteur de l'iframe à 600px */
        max-height: 600px !important;
    }

</style>
""", unsafe_allow_html=True)

components.html("""
    <style>
    /* Custom style for vis.js items */
    .vis-item {
        background-color: #649B88 !important;
        border-color: #ff6666 !important;
        color: #649B88 !important;
    }
    </style>
    """, height=0)
