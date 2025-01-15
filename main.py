import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns


# ----------------------------------------------------------------------------
# 1) Càrrega i filtratge de les dades
# ----------------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv('Money_vs_Happiness_dataset_corrected.csv')
    # Només anys entre 2010 i 2021
    df = df[(df['Year'] >= 2010) & (df['Year'] <= 2021)]
    df['Country'] = df['Country'].astype(str)
    return df


# Carreguem les dades
data_all = load_data()

unique_years = sorted(data_all['Year'].unique())
min_year, max_year = min(unique_years), max(unique_years)

# ----------------------------------------------------------------------------
# 2) Seleccionador d'any
# ----------------------------------------------------------------------------
selected_year = st.sidebar.slider(
    'Selecciona un any:',
    min_value=min_year,
    max_value=max_year,
    step=1
)

# Creació d'un data_year amb l'any seleccionat
data_year = data_all[data_all['Year'] == selected_year]

# ----------------------------------------------------------------------------
# 3) Carrega del mapa mundial
# ----------------------------------------------------------------------------
@st.cache_data
def load_world():
    world = gpd.read_file("mapa/ne_110m_admin_0_countries.shp")
    return world


world = load_world()

# ----------------------------------------------------------------------------
# 4) Funció per unir els datasets (el de dades i el del mapa)
# ----------------------------------------------------------------------------
def merge_data(world, df):
    # En el diccionari de geopandas la columna amb els noms es diu ADMIN
    df_renamed = df.rename(columns={'Country': 'ADMIN'})
    merged = world.merge(df_renamed, on='ADMIN', how='left')
    return merged

world_data = merge_data(world, data_year)

# ----------------------------------------------------------------------------
# 5) Inici de la visualització
# ----------------------------------------------------------------------------
st.title('Diners i somriures')

st.markdown("""
Diuen que els diners no donen la felicitat però hi ajuden. La pregunta és...
  * *en quina mesura ho fan?*,
  * *què dona la felicitat?*

En aquesta visualització intentaré donar resposta a aquestes preguntes perquè, 
al cap i a la fi, qui no vol ser feliç?😃
""")

# ----------------------------------------------------------------------------
# 6) Mapa mundi per a l'any seleccionat
# ----------------------------------------------------------------------------
st.subheader('Comencem per una visió general')
st.markdown("""
La felicitat d'una persona canvia al llarg de la seva vida, però afecta el temps a la felicitat global?  
""")
fig, ax = plt.subplots(1, figsize=(15, 10))

# Primera capa de pintura
base = world_data.plot(ax=ax, color='lightgrey', edgecolor='white')

# Segona capa de pintura, país per país
world_data.dropna(subset=['Life Ladder']).plot(
    ax=base,
    column='Life Ladder',
    cmap='viridis',
    legend=True,
    legend_kwds={
        'label': "Índex de felicitat",
        'orientation': "horizontal"
    }
)

ax.set_title(f"Mapa de l'any ({selected_year})")
ax.set_axis_off()
st.pyplot(fig)

# ----------------------------------------------------------------------------
# 7) Correlacions
# ----------------------------------------------------------------------------
st.subheader("Quins altres factors hem de tindre en compte?")

st.markdown("""
Mirem els més influents, tant a favor de la felicitat com en contra
""")

numeric_cols = data_year.select_dtypes(include=['float64', 'int64']).columns

# Correlació amb "Life Ladder"
if 'Life Ladder' in numeric_cols:
    correlations = data_year[numeric_cols].corr()['Life Ladder'].dropna().sort_values(ascending=False)
    correlations = correlations[correlations.index != 'Life Ladder']

    # Top 5 positives i top 5 negatives
    top_5_positive = correlations.head(5)
    top_5_negative = correlations.tail(5)
    top_correlations = pd.concat([top_5_positive, top_5_negative])

    def assign_colors(values):
        viridis = sns.color_palette("viridis", as_cmap=True)  # Paleta viridis
        colors = []
        for val in values:
            if val > 0:  # Correlacions positives -> colors càlids
                colors.append(viridis(0.7 + 0.3 * val))  # Valors càlids a partir de 0.7
            else:  # Correlacions negatives -> colors freds
                colors.append(viridis(0.3 + 0.3 * val))  # Valors freds fins a 0.3
        return colors


    custom_colors = assign_colors(top_correlations.values)

    # Presentem els resultats
    fig_corr, ax_corr = plt.subplots(figsize=(8, 6))
    sns.barplot(
        x=top_correlations.values,
        y=top_correlations.index,
        hue=top_correlations.index,
        palette=custom_colors,
        legend=False,
        ax=ax_corr
    )
    ax_corr.set_title('Top 5 correlacions positives i negatives')
    ax_corr.set_xlabel('Valor de correlació')
    ax_corr.set_ylabel('Variables')
    fig_corr.tight_layout()

    st.pyplot(fig_corr)

# ----------------------------------------------------------------------------
# 8) Gràfic de dispersió
# ----------------------------------------------------------------------------
# Selector de variables
variable = st.sidebar.selectbox(
    'Selecciona una variable para visualizar',
    [
        'Log GDP per capita',
        'Human Development Index',
        'Perceptions of corruption',
        'Negative affect'
    ]
)

st.subheader(f'Gràfic de dispersió per a la variable {variable}')
st.markdown("""
Mirem aquestes correlacions  amb més detall...
""")

fig2 = px.scatter(
    data_year,
    x=variable,
    y='Life Ladder',
    trendline='ols',
    trendline_color_override='red',
    hover_name='Country'    
)
st.plotly_chart(fig2)

# ----------------------------------------------------------------------------
# 9) Comparativa entre països
# ----------------------------------------------------------------------------
st.subheader("Mirem ara si el que hem après és igual per a tots els països")

all_countries = sorted(data_all['Country'].astype(str).unique())

selected_countries = st.sidebar.multiselect(
    'Tria un país:',
    all_countries,
    default=['Spain', 'United States of America', 'Mexico']
)

# Filtrem els països seleccionats
df_filtered = data_all[data_all['Country'].isin(selected_countries)]

fig_all_years = px.scatter(
    df_filtered,
    x='Log GDP per capita',
    y='Life Ladder',
    color='Country',
    hover_name='Country',
    hover_data=['Year'],    
    title='Relació entre Log GDP per capita i Life Ladder'
)
st.plotly_chart(fig_all_years)

st.subheader("Conclusions")

st.markdown("""
La hipòtesi inicial és que els diners i el desenvolupament econòmic, influeixen
positivament en la felicitat, però no n'expliquen tota la variabilitat.

Hem vist que països amb bons indicadors socioeconòmics no sempre són els més feliços, ja que
factors com el suport social, la percepció de corrupció o les emocions negatives tenen també un paper
determinant. A més, les variacions en la felicitat al llarg del temps són menors que les diferències
regionals, cosa que posa en relleu la importància de l'entorn cultural i social. 
""")
