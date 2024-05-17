import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import seaborn as sns
from utils import data, mydata
from matplotlib.ticker import MaxNLocator
import matplotlib as mpl


with st.sidebar:
    selected = option_menu("Main Menu", ["Time-series", "Best and worst continents", "Scatter plot", "Maps"],
                           icons=["graph-up", "arrow-down-up", "yin-yang", "umbrella"], menu_icon="cast",
                           default_index=0)


@st.cache_data
def timeseries():
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.title("TIME - SERIES")

    st.divider()
    st.subheader("Life expectancy at birth, total (years)\n")
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=mydata.combined_data_life, x='Year', y='Life expectancy at birth, total (years)',
                 hue='Country Name')
    plt.xlabel('\nYear')
    plt.ylabel('Life expectancy at birth, total (years)\n')
    plt.legend(title='Country')
    plt.grid(True)
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()
    st.pyplot()

    st.divider()
    st.subheader("Unemployment, total (% of total labor force) (modeled ILO estimate)\n")
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=mydata.combined_data_unemp, x='Year',
                 y='Unemployment, total (% of total labor force) (modeled ILO estimate)',
                 hue='Country Name')
    plt.xlabel('\nYear')
    plt.ylabel('Unemployment, total (% of total labor force) (modeled ILO estimate)\n')
    plt.legend(title='Country')
    plt.grid(True)
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()
    st.pyplot()

    st.divider()
    st.subheader("Mortality rate, under-5 (per 1,000 live births)\n")
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=mydata.combined_data_mort, x='Year', y='Mortality rate, under-5 (per 1,000 live births)',
                 hue='Country Name')
    plt.xlabel('\nYear')
    plt.ylabel('Mortality rate, under-5 (per 1,000 live births)\n')
    plt.legend(title='Country')
    plt.grid(True)
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()
    st.pyplot()

   

def scatter():
    st.title("SCATTER PLOT")
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        my_year = st.select_slider(label ="", options = data["Year"].unique())
    with col2:
        x_axis = st.radio(label="X-axis", options=data.columns[4:])
    with col3:
        y_axis = st.radio(label = "Y-axis", options =data.columns[4:])
    st.divider()
    plt.figure(figsize=(10, 6))
    filtered_data = data[data["Year"] == my_year]
    for name, group in filtered_data.groupby("Continent"):
        plt.scatter(x=group[x_axis], y=group[y_axis], s=100, alpha=0.7, label=name)

    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.title("Relationhip between " + str(x_axis) + " and " + str(y_axis) + " in " + str(my_year) + ":\n")
    plt.legend(title='Continent')
    plt.grid(True)
    st.pyplot()


def bestworst():

    st.title("BEST AND WORST CONTINENTS")

    st.divider()
    st.write("Choose a year and a metric")
    col1, col2 = st.columns(2)
    with col1:
        selected_year = st.select_slider(label ="", options = data["Year"].unique())
    with col2:
        chosen = st.selectbox(label = "", options = ["Life expectancy at birth", "Unemployment", "Access to electricity", "Mortality rate"], index = None, placeholder="Choose the metric")
    st.divider()
    data_selected_year = data[data['Year'] == selected_year]
    continent_means_selected_year = data_selected_year.groupby('Continent')[mydata.indicators].mean()

    if chosen == "Life expectancy at birth":
        st.subheader("Life expectancy at birth, total (years)")
        plt.figure(figsize=(7, 5))
        continent_means_selected_year['Life expectancy at birth, total (years)'].plot(kind='bar', color='skyblue')
        plt.ylabel('Years\n')
        plt.xlabel("")
        plt.tight_layout()
        st.pyplot()

    if chosen == "Unemployment":
        st.subheader("Unemployment, total (% of total labor force) (modeled ILO estimate)")
        plt.figure(figsize=(7, 5))
        continent_means_selected_year['Unemployment, total (% of total labor force) (modeled ILO estimate)'].plot(kind='bar',
                                                                                                           color='lightgreen')
        plt.ylabel('Percentage\n')
        plt.xlabel("")
        plt.tight_layout()
        st.pyplot()

    if chosen == "Access to electricity":
        st.subheader("Access to electricity (% of population)")
        plt.figure(figsize=(7, 5))
        continent_means_selected_year['Access to electricity (% of population)'].plot(kind='bar', color='salmon')
        plt.ylabel('Percentage\n')
        plt.xlabel("")
        plt.tight_layout()
        st.pyplot()

    if chosen == "Mortality rate":
        st.subheader("Mortality rate, under-5 (per 1,000 live births)")
        plt.figure(figsize=(7, 5))
        continent_means_selected_year['Mortality rate, under-5 (per 1,000 live births)'].plot(kind='bar', color='orchid')
        plt.ylabel('Per 1,000 live births\n')
        plt.xlabel("")
        plt.tight_layout()
        st.pyplot()

def plot_continent_data(continent, mydata, indicators, latest_year):
    continent_limits = {
        'Africa': (-30, 60, -35, 40),
        'Asia': (30, 150, -15, 55),
        'Europe': (-20, 60, 30, 70),
        'North America': (-170, -50, 0, 80),
        'South America': (-90, -30, -60, 20),
        'Oceania': (90, 180, -55, 0)
    }

    continent_data = mydata.world[mydata.world['CONTINENT'] == continent]
    continent_codes = continent_data['ADM0_A3'].unique()
    continent_df = mydata.latest_data[mydata.latest_data['Country Code'].isin(continent_codes)]
    continent_data = continent_data.merge(continent_df, left_on='ADM0_A3', right_on='Country Code')

    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(20, 15))
    for i, ax in enumerate(axes.flat):
        col = indicators[i]
        norm = mpl.colors.Normalize(vmin=continent_data[col].min(), vmax=continent_data[col].max())
        continent_data.boundary.plot(ax=ax)
        plot = continent_data.plot(column=col, ax=ax, legend=False, cmap='coolwarm', norm=norm)
        cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap='coolwarm'), ax=ax, fraction=0.046, pad=0.04)
        cbar.ax.tick_params(labelsize=8)
        ax.set_title(f'{col} ({latest_year})')
        ax.set_xlim(continent_limits[continent][0], continent_limits[continent][1])
        ax.set_ylim(continent_limits[continent][2], continent_limits[continent][3])

    plt.tight_layout()
    st.pyplot(fig)


def maps():
    st.title("MAPS")
    st.divider()
    st.write("Choose a continent to see the maps")
    selcont = st.selectbox(label="", options=(data["Continent"].unique()), index = None, placeholder = "Click here")
    if selcont:
        plot_continent_data(selcont, mydata, mydata.indicators, mydata.latest_year)


if selected == "Time-series":
    timeseries()
if selected == "Scatter plot":
    scatter()
if selected == "Best and worst continents":
    bestworst()
if selected == "Maps":
    maps()
