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
<<<<<<< HEAD
    df['Daily New Cases'] = df['confirmed'].diff(); df['Daily New Cases'][0] = df['Daily New Cases'][1]
=======

    df['Daily New Cases'] = df['confirmed'].diff()#.abs()
    df['Daily New Cases'][0] = df['Daily New Cases'][1]

    df['Daily New Recovered'] = df['recovered'].diff()#.abs();
    df['Daily New Recovered'][0] = df['Daily New Recovered'][1]
>>>>>>> b03a6bd... ddded last commit
    return df

def plt_cases2(df, location):
    """
    plot 2 graphs for selected location
    1 - Daily New Cases vs Daily New Recovered
    2 - Active Cases
    """
    x, y_nc, y_ac, y_nr = (df[location].index, df[location]['Daily New Cases'], df[location]['Active Cases'],
                           df[location]['Daily New Recovered'])

    fig, ax = plt.subplots(2, 1, figsize=(15,12), constrained_layout=True)
    fig.suptitle(location, fontsize=30)

    ax[0].bar(x, y_nc, label='Daily New Cases     / Новые случаи заболевших за день')
    ax[0].plot(x, y_nr, color='k', marker='.',label='Daily New Recovered / Новые случаи выздоровивших за день')
    ax[0].set_title(f'Daily New Cases    /updated {df[location].index[-1].strftime("%d-%b-%Y")}/')
    ax[0].set_ylabel(f'Daily Cases')
    ax[0].legend()

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

    ax[2].plot(x, y_nc, marker='.',label='Daily New Cases     / Новые случаи заболевших за день')
    ax[2].plot(x, y_nr, marker='.',label='Daily New Recovered / Новые случаи выздоровивших за день')
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

def detect_peak(df, lang='ru'):
    """
    returns:
    global_peak_detection - True if peak passed, otherwise Folse
    countries_peak_detection - DataFrame(countries, peak_condition=True if peak passed)
    """
    world_peak_detection =  False
    countries_peak_detection = []
    for loc, dataframe in df.items():
        peak_cond = dataframe['Daily New Recovered'][-1] > dataframe['Daily New Cases'][-1]
        if loc == 'world':
            world_peak_detection = peak_cond
            continue
        countries_peak_detection.append([loc, peak_cond,  dataframe['confirmed'][-1]])
    df_cpd = pd.DataFrame(countries_peak_detection)
    if lang == 'ru':
        print_peak_condition(world_peak_detection, df_cpd)
    else:
        print_peak_condition_en(world_peak_detection, df_cpd)
    return world_peak_detection, df_cpd

def print_peak_condition(world_peak_detection, df_cpd):
    threshold = 1000
    df_cpd_thresh = df_cpd[df_cpd[2]>threshold]
    g_temp = '1. Глобальный пик заражения COVID-19'
    if world_peak_detection:
        print(g_temp + ' уже ПРОЙДЕН\n')
    else:
        print(g_temp + ' еще НЕ ПРОЙДЕН\n')

    print(f'2. Пик заражения пройден в {df_cpd_thresh[df_cpd_thresh[1]==1].count()[0]}/{df_cpd_thresh.count()[0]}={df_cpd_thresh[df_cpd_thresh[1]==1].count()[0]/df_cpd_thresh.count()[0]:.1%} стран.\n')
    print(f'3. Список стран c "Total Cases">{threshold}, где пик заражения пройден:\n')
    print('|'.join(df_cpd[(df_cpd[2]>threshold) & (df_cpd[1]==1)][0]))

def print_peak_condition_en(world_peak_detection, df_cpd):
    threshold = 1000
    df_cpd_thresh = df_cpd[df_cpd[2]>threshold]
    g_temp = '1. The global peak of COVID-19 infection is '
    if world_peak_detection:
        print(g_temp + ' already PASSED\n')
    else:
        print(g_temp + ' NOT PASSED yet\n')

    print(f'2. Infection peak passed in {df_cpd_thresh[df_cpd_thresh[1]==1].count()[0]}/{df_cpd_thresh.count()[0]}={df_cpd_thresh[df_cpd_thresh[1]==1].count()[0]/df_cpd_thresh.count()[0]:.1%} countries.\n')
    print(f'3. List of countries with "Total Cases">{threshold}, where infection peak has been passed:\n')
    print('|'.join(df_cpd[(df_cpd[2]>threshold) & (df_cpd[1]==1)][0]))


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
