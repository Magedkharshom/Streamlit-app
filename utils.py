import pandas as pd
import geopandas as gpd

data = pd.read_csv(r"D:/study/softlab/Stramlit/ready.csv")
data["Year"] = pd.to_datetime(data["Year"])
data["Year"] = data["Year"].dt.year
data23 = data[data["Year"] == 2023]


class mydata:

    data_life = data[["Year", "Continent", "Country Name", "Life expectancy at birth, total (years)"]]
    data_unemp = data[["Year", "Continent", "Country Name", "Unemployment, total (% of total labor force) (modeled ILO estimate)"]]
    data_elec = data[["Year", "Continent", "Country Name", "Access to electricity (% of population)"]]
    data_mort = data[["Year", "Continent", "Country Name", "Mortality rate, under-5 (per 1,000 live births)"]]

    data_ita_life = data_life[data_life['Country Name'] == 'Italy']
    data_deu_life = data_life[data_life['Country Name'] == 'Germany']
    data_fra_life = data_life[data_life['Country Name'] == 'France']
    data_esp_life = data_life[data_life['Country Name'] == 'Spain']
    combined_data_life = pd.concat([data_ita_life, data_deu_life, data_fra_life, data_esp_life])

    data_ita_unemp = data_unemp[data_unemp['Country Name'] == 'Italy']
    data_deu_umemp = data_unemp[data_unemp['Country Name'] == 'Germany']
    data_fra_umemp = data_unemp[data_unemp['Country Name'] == 'France']
    data_esp_unemp = data_unemp[data_unemp['Country Name'] == 'Spain']
    combined_data_unemp = pd.concat([data_ita_unemp, data_deu_umemp, data_fra_umemp, data_esp_unemp])

    data_ita_mort = data_mort[data_mort['Country Name'] == 'Italy']
    data_deu_mort = data_mort[data_mort['Country Name'] == 'Germany']
    data_fra_mort = data_mort[data_mort['Country Name'] == 'France']
    data_esp_mort = data_mort[data_mort['Country Name'] == 'Spain']
    combined_data_mort = pd.concat([data_ita_mort, data_deu_mort, data_fra_mort, data_esp_mort])

    indicators = ['Life expectancy at birth, total (years)', 'Unemployment, total (% of total labor force) (modeled '
                                                             'ILO estimate)', 'Access to electricity (% of '
                                                                              'population)', 'Mortality rate, '
                                                                                             'under-5 (per 1,'
                                                                                             '000 live births)']

    shapefile_path = "D:/study/softlab/Stramlit/ne_50m_admin_0_countries/ne_50m_admin_0_countries.shp"
    world = gpd.read_file(shapefile_path)

    latest_year = data['Year'].max()
    latest_data = data[data['Year'] == latest_year]
    continent_groups = data.groupby('Continent')
