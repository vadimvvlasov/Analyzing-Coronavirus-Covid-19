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
    fig, ax = plt.subplots(2, 1, figsize=(15,9), constrained_layout=True)
    df[location]['Active cases'].plot(subplots=True, ax=ax[0])
    ax[0].set_title(f'Active cases [{location}]')

    df[location]['New cases'].plot.bar(subplots=True, ax=ax[1])
    ax[1].set_title(f'New cases [{location}]')

    plt.show()
