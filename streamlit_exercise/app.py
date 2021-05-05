import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

st.write('Streamlit Gapminder Exercise')


# read files 
df_life = pd.read_csv('data/life_expectancy_years.csv')
df_gni = pd.read_csv('data/ny_gnp_pcap_pp_cd.csv')
df_population = pd.read_csv('data/population_total.csv')

# replace nan values with backward and forward filling 

df_population = df_population.ffill(axis=1)
df_life = df_life.bfill(axis=1)
df_life = df_life.ffill(axis=1)
df_gni = df_gni.bfill(axis=1)
df_gni = df_gni.ffill(axis=1)

# transpose dataframes
df_life = df_life.melt(id_vars=["country"], 
        var_name="year", 
        value_name="lifeExp")

df_gni = df_gni.melt(id_vars=["country"], 
        var_name="year", 
        value_name="GNIperCapita")

df_population = df_population.melt(id_vars=["country"], 
        var_name="year", 
        value_name="population")

# merge dataframes 
df_2 = df_life.merge(df_gni)
df_all = df_2.merge(df_population)

# visualization 

country = st.multiselect('Select one or more countries', np.unique(df_all.country)) # multiselect widget for country
year = st.slider('Select a year', min_value = int(np.unique(df_all.year).min()), max_value = int(np.unique(df_all.year).max())) # slider for year 

data = df_all[df_all.year == str(year)]
data = data[data['country'].isin(country)]

min_gni = np.log(df_all.GNIperCapita.min())
max_lifeexp = df_all.lifeExp.max()
min_lifeexp = df_all.lifeExp.min()

fig = plt.figure()
ax = sns.scatterplot(data=data, x="GNIperCapita", y="lifeExp", size="population", hue = "country", legend=False)
ax.set_xscale('log')
ax.set(xlim=(min_gni, 10**5))
ax.set(ylim=(min_lifeexp-5, max_lifeexp+5))
ax.set_xticks([10**1, 10**2, 10**3, 10**4, 10**5])
ax.set_ylabel('Life Expactancy')
ax.set_xlabel('GNI per Capita')
st.pyplot(fig)

