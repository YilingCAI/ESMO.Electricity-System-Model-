# -*- coding: utf-8 -*-
from __future__ import division, absolute_import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm as CM
import seaborn as sb
import plotly.graph_objs as go
sb.set()


def get_year(dt):
    return dt.year


def get_doy(dt):
    return dt.dayofyear


def get_month(dt):
    return dt.month


def get_weekday(dt):
    return dt.weekday_name


def get_hour(dt):
    return dt.hour


def count_rows(rows):
    return len(rows)


def plot_interactive_timeseries(scenario, simulation_series, start_time,
                                end_time, columns, plot_type, add_range_slider,
                                timestep, resample_way, fig_name):

    font_title = {
        'family': 'sans serif',
        'color': 'black',
        'size': 20,
    }

    font_lable = {
        'family': 'sans serif',
        'color': 'black',
        'size': 15,
    }

    scenario = 'Scenario_' + scenario + ' ' + fig_name + ' ' + timestep + '_' + resample_way + ' figure (' + plot_type + ')'

    # Load data
    df = simulation_series[columns]
    df = df.loc[start_time:end_time]

    if resample_way == 'mean':
        if timestep == 'hourly':
            df = df

        if timestep == 'daily':
            df = df.resample('D').mean()

        if timestep == 'weekly':
            df = df.resample('W').mean()

        if timestep == 'monthly':
            df = df.resample('M').mean()

        if timestep == 'yearly':
            df = df.resample('Y').mean()

    elif resample_way == 'min':
        if timestep == 'hourly':
            df = df

        if timestep == 'daily':
            df = df.resample('D').min()

        if timestep == 'weekly':
            df = df.resample('W').min()

        if timestep == 'monthly':
            df = df.resample('M').min()

        if timestep == 'yearly':
            df = df.resample('Y').min()

    elif resample_way == 'sum':
        if timestep == 'hourly':
            df = df

        if timestep == 'daily':
            df = df.resample('D').sum()

        if timestep == 'weekly':
            df = df.resample('W').sum()

        if timestep == 'monthly':
            df = df.resample('M').sum()

        if timestep == 'yearly':
            df = df.resample('Y').sum()

    elif resample_way == 'max':
        if timestep == 'hourly':
            df = df

        if timestep == 'daily':
            df = df.resample('D').max()

        if timestep == 'weekly':
            df = df.resample('W').max()

        if timestep == 'monthly':
            df = df.resample('M').max()

        if timestep == 'yearly':
            df = df.resample('Y').max()

    # crate traces
    traces = {}
    traces1 = {}

    # build figure
    fig = go.Figure()

    # COLOURS = {
    #     0: 'black',
    #     1: 'gold',  # nuclear
    #     2: 'red',  # oil
    #     3: 'navy',  # lignite
    #     4: 'cyan',  # hard_coal
    #     5: 'green',  # gas
    #     6: 'orange',  # chp
    #     7: 'gray',  # biomass
    #     8: 'forestgreen',  # wind_offshore
    #     9: 'limegreen',  # wind_onshore
    #     10: 'orange',  # pv 
    #     11: 'orangered',  # hydro_ror
    #     12: 'red',  # hydro_dam
    #     13: 'indigo',  # battery
    #     14: 'blue',  # phs
    #     15: 'lightsteelblue',  # dsm
    #     16: 'royalblue',  # ptg
    #     17: 'peru',  # import
    #     18: 'indigo',  # load_shedding
    #     19: 'indigo',  
    #     20: 'blue',  
    #     21: 'lightsteelblue', 
    #     22: 'royalblue',  
    #     23: 'peru', 
    #     24: 'silver',
    #     25: 'indigo', 
    #     26: 'blue', 
    #     27: 'lightsteelblue', 
    #     28: 'royalblue'
    # }

    # COLOURS = {
    #     0: 'gray',
    #     1: 'gold',  # nuclear
    #     2: 'red',  # oil
    #     3: 'blue',  # lignite
    #     4: 'cyan',  # hard_coal
    #     5: 'green',  # gas
    #     6: 'orange',  # chp
    #     7: 'forestgreen',  # wind_offshore
    #     8: 'limegreen',  # wind_onshore
    #     9: 'limegreen',  # wind_onshore
    #     10: 'orange',  # pv 
    #     11: 'orangered',  # hydro_ror
    #     12: 'red',  # hydro_dam
    #     13: 'indigo',  # battery
    #     14: 'blue',  # phs
    #     15: 'lightsteelblue',  # dsm
    #     16: 'royalblue',  # ptg
    #     17: 'peru',  # import
    #     18: 'indigo',  # load_shedding
    #     19: 'indigo',  
    #     20: 'blue',  
    #     21: 'lightsteelblue', 
    #     22: 'royalblue',  
    #     23: 'peru', 
    #     24: 'silver',
    #     25: 'indigo', 
    #     26: 'blue', 
    #     27: 'lightsteelblue', 
    #     28: 'royalblue'
    # }

    # COLOURS1 = {
    #     0: 'blue',  # battery
    #     1: 'gray',  # phs
    #     2: 'gray',  # dsm
    #     3: 'royalblue',  # ptg
    #     4: 'peru',  # export
    #     5: 'silver'  # excess
    # }

    COLOURS = {
        0: 'lime',
        1: 'green',  # nuclear
        2: 'navy',  # oil
        3: 'grey',  # lignite
        4: 'magenta',  # hard_coal
        5: 'green',  # gas
        6: 'orange',  # chp
        7: 'forestgreen',  # wind_offshore
        8: 'limegreen',  # wind_onshore
        9: 'limegreen',  # wind_onshore
        10: 'orange',  # pv 
        11: 'orangered',  # hydro_ror
        12: 'red',  # hydro_dam
        13: 'indigo',  # battery
        14: 'blue',  # phs
        15: 'lightsteelblue',  # dsm
        16: 'royalblue',  # ptg
        17: 'peru',  # import
        18: 'indigo',  # load_shedding
        19: 'indigo',  
        20: 'blue',  
        21: 'lightsteelblue', 
        22: 'royalblue',  
        23: 'peru', 
        24: 'silver',
        25: 'indigo', 
        26: 'blue', 
        27: 'lightsteelblue', 
        28: 'royalblue'
    }

    COLOURS1 = {
        0: 'grey',  # battery
        1: 'navy',  # phs
        2: 'magenta',  # dsm
        3: 'royalblue',  # ptg
        4: 'peru',  # export
        5: 'silver'  # excess
    }

    i = 0
    n = 0
    m = 0
    for col in df.columns:

        if plot_type == 'scatter':
            fig.add_trace(
                go.Scatter(x=df.index, y=df[col] / 1000, name=col, mode='lines', marker_color=COLOURS[m]))
            m = m+1
        if plot_type == 'bar':
            fig.add_trace(
                go.Bar(x=df.index, y=df[col] / 1000, name=col))
        if plot_type == 'stacked_area_percentage':  # Stacked Area Chart with Normalized Values
            fig.add_trace(
                go.Scatter(x=df.index,
                           y=df[col] / 1000,
                           name=col,
                           stackgroup='one',
                           groupnorm='percent'))
        if plot_type == 'stacked_area':  # Stacked Area Chart
            if col in [
                    'battery_char', 'phs_char', 'dsm_char', 'ptg_char', 'exp',
                    'excess'
            ]:
                fig.add_trace(
                    go.Scatter(x=df.index,
                               y=df[col] / 1000,
                               name=col,
                               mode='lines',
                               stackgroup='one',
                               line=dict(width=0,color=COLOURS1[n])))

                n = n + 1
            elif col not in ['demand']:
                fig.add_trace(
                    go.Scatter(x=df.index,
                               y=df[col] / 1000,
                               name=col,
                               mode='lines',
                               stackgroup='two',
                               line=dict(width=0,color=COLOURS[i])))

                i = i + 1

        # convert data to form required by plotly
        # data=list(traces.values())

    # Set title
    fig.update_layout(height=700, width=900)
    fig.update_layout(legend_orientation="h")
    # Set axis lable
    fig.update_layout(xaxis=go.layout.XAxis(title=go.layout.xaxis.Title(
        text="",
        font=font_lable,
    ), ),
                      yaxis=go.layout.YAxis(title=go.layout.yaxis.Title(
                          text="Power(GW)",
                          font=font_lable,
                      ), ))

    if plot_type == 'bar':
        fig.update_layout(barmode='stack',
                          xaxis={
                              'categoryorder':
                              'array',
                              'categoryarray': [
                                  'Jan', 'Feb', 'Mars', 'April', 'Mai', 'Juin',
                                  'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
                              ]
                          })

        if timestep == 'monthly':
            fig.layout.xaxis.tickvals = pd.date_range(start_time,
                                                      end_time,
                                                      freq='MS')
            fig.layout.xaxis.tickformat = '%b'

    if plot_type == 'stacked_area':
        fig.add_trace(
            go.Scatter(x=df.index,
                       y=df['demand'] / 1000,
                       name='demand',
                       opacity=1,
                       line=dict(color='black', width=4)))

    if plot_type == 'stacked_area_percentage':
        fig.update_layout(showlegend=True,
                          yaxis=dict(type='linear',
                                     range=[1, 100],
                                     ticksuffix='%'))

    if resample_way == 'sum':
        fig.update_layout(yaxis=go.layout.YAxis(title=go.layout.yaxis.Title(
            text="GWh",
            font=font_lable,
        ), ))

    if add_range_slider == 1:
        fig.layout.update(xaxis=go.layout.XAxis(rangeselector=dict(
            buttons=list([
                dict(count=1, label='1 day', step='day', stepmode='todate'),
                dict(count=7, label='1 week', step='day', stepmode='backward'),
                dict(count=1,
                     label='1 month',
                     step='month',
                     stepmode='backward'),
                dict(count=1, label="1 year", step="year",
                     stepmode="backward"),
                dict(step='all')
            ])),
                                                type="date"))

    fig.show()

    return


def plot_residual_load_curve(scenario, simulation_series, year, fig_name):

    scenario = 'Scenario_' + scenario + ' ' + fig_name
    # Load data
    df = simulation_series
    df['year'] = df.index.map(get_year)
    df = df.loc[df.year == year]
    df['load'] = df['demand']
    df['residual_load'] = df['demand'] - df['wind_onshore'] - df[
        'wind_offshore'] - df['pv_ground']

    by_sorted1 = df.sort_values(by=['load'], ascending=False)
    by_sorted2 = df.sort_values(by=['residual_load'], ascending=False)

    df['hour'] = df.index.map(get_hour) + df.index.map(get_doy) * 24
    x = df['hour']
    y1 = by_sorted1['load'] / 1000
    y2 = by_sorted2['residual_load'] / 1000

    f = plt.figure(figsize=(16, 9))
    plt.subplots_adjust(left=0.125,
                        bottom=0.1,
                        right=0.9,
                        top=0.9,
                        wspace=0.1,
                        hspace=0.3)
    ax1 = f.add_subplot(221)
    ax2 = f.add_subplot(222)
    ax3 = f.add_subplot(223)
    ax4 = f.add_subplot(224)

    ax1.plot(x, df['load'] / 1000, marker='.', linestyle='-', linewidth=0.1)
    ax1.set_title('Load Curve', fontsize=18)
    ax1.set_xlabel('hour', fontsize=15)
    ax1.set_ylabel('(GW)', fontsize=15)

    ax2.plot(x, y1)
    ax2.set_title('Load Duration Curve', fontsize=18)
    ax2.set_xlabel('hour', fontsize=15)
    ax2.set_ylabel('(GW)', fontsize=15)

    ax3.plot(x,
             df['residual_load'] / 1000,
             marker='.',
             linestyle='-',
             linewidth=0.1)
    ax3.set_title('Residual Load Curve', fontsize=18)
    ax3.set_xlabel('hour', fontsize=15)
    ax3.set_ylabel('(GW)', fontsize=15)

    ax4.plot(x, y2)
    ax4.set_title('Residual Load Duration Curve', fontsize=18)
    ax4.set_xlabel('hour', fontsize=15)
    ax4.set_ylabel('(GW)', fontsize=15)

    plt.show()

    return


def plot_heatmap(scenario, simulation_series, column, start_time, end_time,
                 fig_name):
    scenario = 'Scenario_' + scenario + ' ' + fig_name
    df = simulation_series

    df['hour'] = df.index.map(get_hour)
    df['day_of_year'] = df.index.map(get_doy)
    df['weekday'] = df.index.map(get_weekday)
    df['month'] = df.index.map(get_month)
    df['year'] = df.index.map(get_year)

    df[column] = df[column] / 1000
    df = df.pivot("hour", "day_of_year", column)

    ax = sb.heatmap(df, cmap=CM.jet)
    plt.title(scenario, fontsize=20)
    plt.xlabel('day_of_year', fontsize=15)  # x-axis label with fontsize 15
    plt.ylabel('hour', fontsize=15)  # y-axis label with fontsize 15
    figure = plt.gcf()  # get current figure
    plt.show()

    return


def plot_boxplot(scenario, simulation_series, sample_time, start_time,
                 end_time, columns, fig_name):
    scenario = 'Scenario_' + scenario + ' ' + fig_name + ' (' + sample_time + ')'

    # Load data
    df = simulation_series
    df = df.loc[start_time:end_time]
    if sample_time == 'year':
        df[sample_time] = df.index.map(get_year)
    if sample_time == 'month':
        df[sample_time] = df.index.map(get_month)
    if sample_time == 'weekday':
        df[sample_time] = df.index.map(get_weekday)
    if sample_time == 'hour':
        df[sample_time] = df.index.map(get_hour)

    df[columns] = df[columns] / 1000

    ax = sb.boxplot(data=df, x=sample_time, y=columns)
    ax.set_ylabel('GW', fontsize=15)
    ax.set_xlabel(sample_time, fontsize=15)
    ax.set_title(scenario, fontsize=20)
    ax.legend()
    plt.show()
    return


def plot_histogram(scenario, simulation_series, columns, costs_detail_arr,
                   year, fig_name):
    scenario = 'Scenario_' + scenario + ' ' + fig_name
    installed_capacity = costs_detail_arr.loc[
        costs_detail_arr.energy_source == columns, 'installed_power'].iat[0]

    df = simulation_series
    df['year'] = df.index.map(get_year)
    df = df.loc[df.year == year]
    df = df.resample('D', how=mean)

    df['hour'] = (df.index.map(get_hour) + df.index.map(get_doy) * 24) / 8760
    x = df['hour']
    by_sorted = df.sort_values(by=[columns])
    y = by_sorted[columns] / installed_capacity / 1000

    fig, ax = plt.subplots()
    ax.plot(x, y, label=columns)
    ax.grid(b=1)
    ax.set(xlim=[0, 1])
    ax.set(ylim=[0, 0.8])
    ax.set_xlabel('time', fontsize=15)
    ax.set_ylabel('load factor', fontsize=15)
    ax.legend()
    ax.set_title(scenario, fontsize=20)
    plt.show()

    return


def plot_density_histogram(scenario, simulation_series, columns,
                           costs_detail_arr, year, fig_name):
    scenario = 'Scenario_' + scenario + ' ' + fig_name
    installed_capacity = costs_detail_arr.loc[
        costs_detail_arr.energy_source == columns, 'installed_power'].iat[0]

    df = simulation_series
    df['year'] = df.index.map(get_year)
    df = df.loc[df.year == year]
    y = df[columns] / installed_capacity / 1000

    # draw the plot
    fig, ax = plt.subplots()
    weights = np.ones_like(y) / float(len(y))
    ax.hist(y, bins=20, weights=weights, label=columns)

    # plot formatting
    ax.set_ylabel('Density', fontsize=15)
    ax.set_xlabel('Load factor', fontsize=15)
    ax.set_title(scenario, fontsize=20)
    ax.set(xlim=[0, 1])
    new_ticks = np.linspace(0, 1, 11)
    ax.set_xticks(new_ticks)
    ax.legend()
    plt.show()

    return


def plot_elec_mix(scenario, costs_detail_arr, install_list, prod_list,
                  fig_name):

    # Data to plot
    installed_capacity_arr = []
    production_arr = []
    total_installed_capacity = 0
    total_production = 0

    for i in install_list:
        installed_capacity = costs_detail_arr.loc[
            costs_detail_arr.energy_source == i, 'installed_power'].iat[0]
        installed_capacity_arr.append(installed_capacity)
        total_installed_capacity += installed_capacity

    for i in prod_list:
        production = costs_detail_arr.loc[costs_detail_arr.energy_source ==
                                          i, 'production'].iat[0]
        production_arr.append(production)
        total_production += production

    # pie chart lables and sizes
    labels = install_list
    sizes = installed_capacity_arr
    labels_prod = prod_list
    sizes_prod = production_arr

    # Plot
    centre_circle = plt.Circle((0, 0), 0.30, fc='white')
    centre_circle2 = plt.Circle((0, 0), 0.30, fc='white')

    f = plt.figure(figsize=(16, 9))
    plt.subplots_adjust(left=0.125,
                        bottom=0.1,
                        right=0.9,
                        top=0.9,
                        wspace=0.1,
                        hspace=0.3)
    explode1 = (0, 0, 0, 0, 0, 0, 0, 0)
    ax1 = f.add_subplot(121)
    ax1.set_title('Installed capapcity (GW)', fontsize=18)
    ax1.pie(sizes,
            explode=explode1,
            labels=labels,
            startangle=90,
            autopct='%1.1f%%')
    text1 = str(int(total_installed_capacity)) + 'GW'
    ax1.text(0, 0, text1, ha='center', fontsize=18)
    fig1 = plt.gcf()
    fig1.gca().add_artist(centre_circle)

    explode2 = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    ax2 = f.add_subplot(122)
    ax2.set_title('Production (GWh)', fontsize=18)
    ax2.pie(sizes_prod,
            explode=explode2,
            labels=labels_prod,
            startangle=90,
            autopct='%1.1f%%')
    text = str(int(total_production)) + 'GWh'
    ax2.text(0, 0, text, ha='center', fontsize=18)
    fig2 = plt.gcf()
    fig2.gca().add_artist(centre_circle2)

    plt.axis('equal')
    plt.tight_layout()
    plt.show()

    return


def plot_costs_detail(scenario, costs_detail_arr, fig_name):
    scenario = 'Scenario_' + scenario + ' ' + fig_name
    # Build the plot
    ax = costs_detail_arr.pivot("year", "energy_source",
                                "lcoe").plot(kind='bar')
    ax.set_ylabel('€/MWh', fontsize=15)
    ax.set_xlabel('Year', fontsize=15)
    ax.set_title(scenario, fontsize=20)
    ax.legend()
    # Save the figure and show
    plt.tight_layout()
    plt.show()
    return


def plot_costs_avg(costs_total_arr, fig_name):
    scenario = fig_name
    # Build the plot
    ax = costs_total_arr.pivot("year", "scenario",
                               "total_avg_system_cost[€/MWh]").plot(kind='bar')
    ax.set_ylabel('€/MWh', fontsize=15)
    ax.set_xlabel('Year', fontsize=15)
    ax.set_title(scenario, fontsize=20)
    ax.legend()
    # Save the figure and show
    plt.tight_layout()
    plt.show()

    return


def plot_emissions(scenario, emissions_arr, fig_name):
    scenario = 'Scenario_' + scenario + ' ' + fig_name
    # Build the plot

    ax = emissions_arr.pivot("year", "emission_source",
                             "values[MtCO2]").plot(kind='bar')
    ax.set_ylabel('MtCO2', fontsize=15)
    ax.set_xlabel('Year', fontsize=15)
    ax.set_title(scenario, fontsize=20)
    ax.legend()
    # Save the figure and show
    plt.tight_layout()
    plt.show()

    return


if __name__ == '__main__':
    pass