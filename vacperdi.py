# print('Hello')

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objs as go
import plotly.offline as offline
import subprocess as sp
import os

if os.path.exists('owid-covid-data.csv') == True:
    sp.call("rm owid-covid-data.csv",shell=True)

elif os.path.exists('vaccinations.csv') == True:
    sp.call("rm vaccinations.csv",shell=True)

else:
    pass

print('国名を入れてください')
country = input()
country = str(country)

sp.call('wget https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv', shell=True)
sp.call('wget https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv', shell=True)

df_vaccination = pd.read_csv('vaccinations.csv')
df_owid_covid = pd.read_csv('owid-covid-data.csv')

df_country_vac = df_vaccination.query('location == @country')
df_country_vac['people_fully_vaccinated_per_hundred_abs'] = df_country_vac['people_fully_vaccinated_per_hundred'].fillna(method='ffill')
df_country_owid = df_owid_covid.query('location == @country')
df_country_owid['new_cases_abs'] = df_country_owid['new_cases'].abs()

covid_vaccinations = go.Bar(x=df_country_vac['date'], y=df_country_vac['people_fully_vaccinated_per_hundred_abs'], name='ワクチンを２回打った人の割合',  yaxis='y1')
covid_death = go.Scatter(x=df_country_owid['date'], y=df_country_owid['new_deaths'], mode = 'lines', name='1日あたりの死者数', yaxis='y2')
covid_infected = go.Scatter(x=df_country_owid['date'], y=df_country_owid['new_cases_abs'], mode = 'lines', name='新規感染者数', yaxis='y2')

layout = go.Layout(title = 'Covid-19のワクチン接種数と死者数の関係' + '(' + country + ')',
            xaxis = dict(title = '日付'),
            yaxis = dict(title = 'ワクチンを２回打った人の割合', side = 'right', showgrid=False),
            yaxis2 = dict(title = '1日あたりの死者数', side = 'left', overlaying = 'y', showgrid=False))


fig = go.Figure(data = [covid_vaccinations, covid_death, covid_infected], layout = layout)
# fig.update_layout(yaxis2=dict(range=(0, 1000)))
fig.show()

sp.call("rm vaccinations.csv",shell=True)
sp.call("rm owid-covid-data.csv",shell=True)