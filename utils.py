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
    
    df['Daily New Cases'] = df['confirmed'].diff().abs()
    df['Daily New Cases'][0] = df['Daily New Cases'][1]
    
    df['Daily New Recovered'] = df['recovered'].diff().abs(); 
    df['Daily New Recovered'][0] = df['Daily New Recovered'][1]
    return df

def plt_cases2(df, location):
    """
    plot 2 graphs for selected location
    1 - Daily New Cases
    2 - Active Cases
    """
    x, y_nc, y_ac = df[location].index, df[location]['Daily New Cases'], df[location]['Active Cases']

    fig, ax = plt.subplots(2, 1, figsize=(15,8), constrained_layout=True)
    fig.suptitle(location, fontsize=30)

    ax[0].bar(x, y_nc)
    ax[0].set_title(f'Daily New Cases    /updated {df[location].index[-1].strftime("%d-%b-%Y")}/')
    ax[0].set_ylabel(f'Daily New Cases')

    ax[1].plot(x, y_ac, marker='.')
    ax[1].set_title(f'Active Cases')
    ax[1].set_xlabel('Date')
    ax[1].set_ylabel(f'Active Cases')
    
def plt_cases3(df, location):
    """
    plot 3 graphs for selected location
    1 - Daily New Cases
    2 - Active Cases
    3 - Daily New Recovered
    """

    x, y_nc, y_ac, y_nr = (df[location].index, df[location]['Daily New Cases'], df[location]['Active Cases'],
                           df[location]['Daily New Recovered'])

    fig, ax = plt.subplots(3, 1, figsize=(15,12), constrained_layout=True)
    fig.suptitle(location, fontsize=30)

    ax[0].bar(x, y_nc)
    ax[0].set_title(f'Daily New Cases    /updated {df[location].index[-1].strftime("%d-%b-%Y")}/')
    ax[0].set_ylabel(f'Daily New Cases')

    ax[1].plot(x, y_ac, marker='.')
    ax[1].set_title(f'Active Cases')
    ax[1].set_xlabel('Date')
    ax[1].set_ylabel(f'Active Cases')
    
    ax[2].plot(x, y_nc, marker='.',label='Новые случаи заболевших за день')
    ax[2].plot(x, y_nr, marker='.',label='Новые случаи выздоровивших за день')
    ax[2].set_title(f'(New Cases)vs(New Recovered)')
    ax[2].set_xlabel('Date')
    ax[2].set_ylabel(f'Daily Cases')
    ax[2].legend()

# TODO refactor plot_locations with decorator
def plot_locations2(df, locations):
    for loc in locations:
        plt_cases2(df, loc)
        
def plot_locations3(df, locations):
    for loc in locations:
        plt_cases3(df, loc)


api = CovId19Data(force=False)
# DataFrame with cases for all available countries
df = {}
selected_columns = ['confirmed', 'recovered', 'deaths', 'Active Cases', 'Daily New Cases', 'Daily New Recovered']
for loc in api.show_available_countries():
    df[loc] = get_df(loc)
    df[loc] = add_cases(df[loc]) # calculate 'New cases' and 'Active cases' and add to the DataFrame
    if 'world' in df:
        df['world'] += df[loc][selected_columns]
    else:
        df['world'] = df[loc][selected_columns]
