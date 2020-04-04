import pandas as pd
from covid.api import CovId19Data
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.dates as dates

api = CovId19Data(force=False)

def get_df(country):
    rez = api.get_history_by_country(country)
    data = rez[list(rez.keys())[0]]
    country_label = data['label']
    df = pd.DataFrame(data['history']).T
    df.index=pd.to_datetime(df.index)
    return df

def add_cases(df):
    df['Active cases'] = df['confirmed'] - df['recovered'] - df['deaths']
    df['New cases'] = df['confirmed'].diff(); df['New cases'][0] = df['New cases'][1]
    return df

def plot_cases(cases):
    for label, df in cases.items():
        df['Active cases'].plot(figsize=(15,8), label=country, legend=True)

def plt_cases(df, location):
    x, y_nc, y_ac = df[location].index, df[location]['New cases'], df[location]['Active cases']

    fig, ax = plt.subplots(2, 1, figsize=(15,8), constrained_layout=True)
    fig.suptitle(location, fontsize=30)

    ax[0].bar(x, y_nc)
    ax[0].set_title(f'New cases [{location}]')
    ax[0].set_ylabel(f'Active cases [{location}]')

    ax[1].plot(x, y_ac, marker='.')
    ax[1].set_title(f'Active cases [{location}]')
    ax[1].set_xlabel('Date')
    ax[1].set_ylabel(f'Active cases [{location}]')


# def plt_cases(df, location):
#     fig, ax = plt.subplots(2, 1, figsize=(15,9), constrained_layout=True)
#
#     df[location]['New cases'].plot.bar(subplots=True, ax=ax[0])
#     ax[0].set_title(f'New cases [{location}]')
#
#     df[location]['Active cases'].plot(subplots=True, ax=ax[1])
#     ax[1].set_title(f'Active cases [{location}]')
#
#     plt.show()
