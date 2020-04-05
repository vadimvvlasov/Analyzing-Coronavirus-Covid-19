import pandas as pd
from covid.api import CovId19Data
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.dates as dates
from matplotlib import style
style.use('seaborn-poster')

def get_df(country):
    rez = api.get_history_by_country(country)
    data = rez[list(rez.keys())[0]]
    country_label = data['label']
    df = pd.DataFrame(data['history']).T
    df.index=pd.to_datetime(df.index)
    return df

def add_cases(df):
    df['Active Cases'] = df['confirmed'] - df['recovered'] - df['deaths']
    df['Daily New Cases'] = df['confirmed'].diff(); df['Daily New Cases'][0] = df['Daily New Cases'][1]
    return df

def plot_cases(cases):
    for label, df in cases.items():
        df['Active Cases'].plot(figsize=(15,8), label=country, legend=True)

def plt_cases(df, location):
    x, y_nc, y_ac = df[location].index, df[location]['Daily New Cases'], df[location]['Active Cases']

    fig, ax = plt.subplots(2, 1, figsize=(15,8), constrained_layout=True)
    fig.suptitle(location, fontsize=30)

    ax[0].bar(x, y_nc)
    ax[0].set_title(f'Daily New Cases [{location}], last update {df[location].index[-1]}')
    ax[0].set_ylabel(f'Daily New Cases')

    ax[1].plot(x, y_ac, marker='.')
    ax[1].set_title(f'Active Cases [{location}]')
    ax[1].set_xlabel('Date')
    ax[1].set_ylabel(f'Active Cases')

def plot_locations(df, locations):
    for loc in locations:
        plt_cases(df, loc)

api = CovId19Data(force=False)
# DataFrame with cases for all available countries
df = {}
selected_columns = ['confirmed', 'recovered', 'deaths', 'Active Cases', 'Daily New Cases']
for loc in api.show_available_countries():
    df[loc] = get_df(loc)
    df[loc] = add_cases(df[loc]) # calculate 'New cases' and 'Active cases' and add to the DataFrame
    if 'world' in df:
        df['world'] += df[loc][selected_columns]
    else:
        df['world'] = df[loc][selected_columns]
