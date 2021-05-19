"""
    Author: Tejas Dadhaniya
    Created on: 15th MAY 2021
    Project: Create dashboard using plotly and dash.

"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import numpy as np

app = dash.Dash(__name__)

dff = pd.read_csv('SampleSuperstore.csv')

# String manipulation.
# Update columns name so that we can easily access.
dff.columns = dff.columns.str.replace(' ', '_')
dff.columns = dff.columns.str.replace('-', '_')
dff.columns = dff.columns.str.lower()

# US state abbreviation.
# This abbreviation used later when we plot choropleth.
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands': 'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}
dff['state_abbrev'] = [us_state_abbrev[state] for state in dff.state]

colours = {
    'heading': '#0000FF',
    'plot_bgcolor': '#A9A9A9',
    'paper_bgcolor': '#000000',
    'fontcolor': "#FFFFFF",
    'backgroundColor': "#000000",
    'odd': '#80808080',
    'even': '#80808080'
}

app.layout = html.Div(
    children=[
        html.H1('Dashboard',
                style={"textAlign": 'center',
                       'padding': '10px',
                       'color': colours['fontcolor'],
                       'backgroundColor': colours['backgroundColor']}),

        html.Div(
            children=[
                dcc.Dropdown(id='dropdown_state',
                             options=[{'label': state, 'value': state} for state in
                                      dff.state.unique()],
                             multi=False,
                             value='California',
                             placeholder='Select state',
                             style={'width': '85%', 'margin': '15px 1px 10px 30px'}),

                dcc.Dropdown(id='dropdown_city',
                             options=[],
                             multi=False,
                             value='Los Angeles',
                             placeholder='Select city',
                             style={'width': '85%', 'margin': '15px 1px 10px 0px'})
            ],
            style=dict(display='flex', backgroundColor=colours['backgroundColor'])),
        html.Br(),

        html.Div(
            children=[dcc.RadioItems(id='radio_',
                                     options=[
                                         {'label': 'Sales', 'value': 'sales'},
                                         {'label': 'Profit', 'value': 'profit'}],
                                     value='sales')],
            style=dict(color=colours['fontcolor'],
                       backgroundColor=colours['backgroundColor'],
                       margin='15px 1px 10px 60px', fontSize='20px'
                       )),
        html.Br(),

        html.Div(
            children=[
                html.Div(children=[html.H3(children=['Total Sales'], style={'color': '#F0FFF0'}),
                                   html.H1(id='total_sales', children=[], style={'color': 'orange'}),
                                   html.H4(id='state_name1', children=[], style={'color': '#F0FFF0'})],
                         style={'backgroundColor': colours['odd'],
                                'border': '1px solid #80808080',
                                'border-radius': '3px',
                                'opacity': '0.6',
                                'box-shadow': '5px 5px 5px  #80808080'
                                }),
                html.Div(children=[html.H3('Total Profit', style={'color': '#F0FFF0'}),
                                   html.H1(id='total_profit', children=[], style={'color': 'orange'}),
                                   html.H4(id='state_name2', children=[], style={'color': '#F0FFF0'})],
                         style={'backgroundColor': colours['odd'],
                                'border': '1px solid #80808080',
                                'border-radius': '3px',
                                'opacity': '0.6',
                                'box-shadow': '5px 5px 5px  #80808080'
                                }),
                html.Div(children=[html.H3('Top Selling Product', style={'color': '#F0FFF0'}),
                                   html.H1(id='top_selling_amt', children=[], style={'color': 'orange'}),
                                   html.H4(id='top_selling_name', children=[], style={'color': '#F0FFF0'})],
                         style={'backgroundColor': colours['even'],
                                'border': '1px solid #80808080',
                                'border-radius': '3px',
                                'opacity': '0.6',
                                'box-shadow': '5px 5px 5px  #80808080'
                                }),
                html.Div(children=[html.H3('Product With High Profit', style={'color': '#F0FFF0'}),
                                   html.H1(id='high_profit_amt', children=[], style={'color': 'orange'}),
                                   html.H4(id='high_profit_name', children=[], style={'color': '#F0FFF0'})],
                         style={'backgroundColor': colours['even'],
                                'border': '1px solid #80808080',
                                'border-radius': '3px',
                                'opacity': '0.6',
                                'box-shadow': '5px 5px 5px  #80808080'
                                }),
            ],
            style={"textAlign": 'center',
                   'display': 'grid',
                   'grid-template-columns': 'repeat(4, 1fr)',
                   'grid-gap': '2em',
                   'margin': '15px 1px 10px 60px',
                   'width': '90%'}
        ),

        html.Div(
            children=[
                html.Div(children=[dcc.Graph(id='stack', figure={})],
                         style={'width': '45%'}),
                html.Div(children=[dcc.Graph(id='region_pie', figure={})],
                         style={'width': '25%'}),
                html.Div(children=[dcc.Graph(id='pie', figure={})],
                         style={'width': '25%'})],
            style={'display': 'flex'}),

        html.Div(
            children=[
                html.Div(id='chorpleth_id',
                         children=[dcc.Graph(id='chorpleth', figure={})],
                         style={'width': '50%'}),

                html.Div(children=[html.Div(dcc.Dropdown(id='dropdown_product',
                                                         options=[
                                                             {'label': state, 'value': state} for
                                                             state in dff.sub_category.unique()],
                                                         multi=False,
                                                         value='Bookcases',
                                                         placeholder='Select product'),
                                            style={'width': '20%', 'margin': '1px 1px 10px 60px'}),
                                   html.Div(dcc.Graph(id='top_city', figure={}), style={'width': '85%'})
                                   ],
                         style={'display': 'grid',
                                'grid-template-columns': 'repeat(1, 1fr)',
                                'grid-template-raws': 'repeat(1, 1fr)',
                                'width': '50%'}
                         )
            ], style={'display': 'flex', 'backgroundColor': colours['paper_bgcolor']}),

        html.Div(
            children=[dcc.RadioItems(id='state_or_city',
                                     options=[
                                         {'label': 'State', 'value': 'state'},
                                         {'label': 'City', 'value': 'city'}],
                                     value='state')],
            style=dict(color=colours['fontcolor'],
                       backgroundColor=colours['backgroundColor'],
                       margin='15px 1px 10px 60px', fontSize='20px'
                       )),
        html.Div(
            children=[
                html.Div(id='bar1',
                         children=[dcc.Graph(id='state_top', figure={})],
                         style={'width': '25%'}),
                html.Br(),
                html.Div(id='bar2',
                         children=[dcc.Graph(id='state_bottom', figure={})],
                         style={'width': '25%'}),
                html.Br(),
                html.Div(id='bar3',
                         children=[dcc.Graph(id='product_analysis', figure={})], style={'width': '45%'}),
                html.Br(),
            ], style=dict(display='flex'))
    ], style={'backgroundColor': colours['backgroundColor']})


@app.callback([Output(component_id='chorpleth', component_property='figure'),
               Output(component_id='state_top', component_property='figure'),
               Output(component_id='state_bottom', component_property='figure'),
               Output(component_id='product_analysis', component_property='figure')],
              [Input(component_id='radio_', component_property='value'),
               Input(component_id='state_or_city', component_property='value')])
def update_graph(option_, city_or_state):
    df = dff.copy()
    state_abr_sales = pd.DataFrame(df.groupby(['state_abbrev'])['sales', 'profit'].sum())
    choropleth = px.choropleth(state_abr_sales,
                               locations=state_abr_sales.index,
                               locationmode='USA-states',
                               color_continuous_scale="Bluyl",
                               color=option_,
                               scope="usa",
                               title=option_
                               )
    choropleth.update_layout(plot_bgcolor=colours['plot_bgcolor'], paper_bgcolor=colours['paper_bgcolor'],
                             font={'color': colours['fontcolor']})

    state_sales = pd.DataFrame(df.groupby(city_or_state)[option_].sum())
    state_top = state_sales.sort_values(ascending=True, by=option_).tail(10)
    state_bottom = state_sales.sort_values(ascending=False, by=option_).tail(10)
    bar1 = px.bar(data_frame=state_top, x=state_top.index, y=option_,
                  title='{} with most {}'.format(city_or_state, option_))
    bar1.update_layout(xaxis_tickangle=-45, plot_bgcolor=colours['plot_bgcolor'],
                       paper_bgcolor=colours['paper_bgcolor'], font={'color': colours['fontcolor']})
    bar2 = px.bar(data_frame=state_bottom, x=state_bottom.index, y=option_,
                  title='{} with least {}'.format(city_or_state, option_))
    bar2.update_layout(xaxis_tickangle=-45, plot_bgcolor=colours['plot_bgcolor'],
                       paper_bgcolor=colours['paper_bgcolor'], font={'color': colours['fontcolor']})

    product_ = pd.DataFrame(df.groupby('sub_category')[option_].sum()).sort_values(ascending=False, by=option_)
    bar3 = px.bar(data_frame=product_, x=product_.index, y=option_, title='Product vs {}'.format(option_))
    bar3.update_layout(xaxis_tickangle=-45, plot_bgcolor=colours['plot_bgcolor'],
                       paper_bgcolor=colours['paper_bgcolor'], font={'color': colours['fontcolor']})
    return choropleth, bar1, bar2, bar3


@app.callback(Output(component_id='dropdown_city', component_property='options'),
              [Input(component_id='dropdown_state', component_property='value')])
def dropdown_update(val_):
    df = dff.copy()
    cities = df.loc[df['state'] == val_].city.unique()
    list_ = [{'label': city, 'value': city} for city in cities]
    return list_


@app.callback(Output(component_id='stack', component_property='figure'),
              [Input(component_id='dropdown_city', component_property='value')])
def graph_from_dropdown(city_):
    df = dff.copy()
    df1 = df.loc[df['city'] == city_]
    df1 = pd.DataFrame(df1.groupby('sub_category')['sales', 'profit'].sum()).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df1['profit'],
        x=df1['sub_category'],
        name='profit',
    ))
    fig.add_trace(go.Bar(
        y=df1['sales'],
        x=df1['sub_category'],
        name='sales',
    ))
    fig.update_layout(barmode='group', xaxis_tickangle=-45, plot_bgcolor=colours['plot_bgcolor'],
                      paper_bgcolor=colours['paper_bgcolor'], font={'color': colours['fontcolor']})
    return fig


@app.callback([Output(component_id='region_pie', component_property='figure'),
               Output(component_id='pie', component_property='figure')],
              [Input(component_id='dropdown_city', component_property='value'),
               Input(component_id='radio_', component_property='value')])
def graph_from_city_dropdown(city_, radio_item_):
    df = dff.copy()
    df = df.loc[df['city'] == city_]
    df1 = pd.DataFrame(df.groupby('sub_category')['sales', 'profit'].sum()).reset_index()
    fig = px.pie(df1, names=df1.sub_category, values=radio_item_, title='Category')
    fig.update_layout(plot_bgcolor=colours['plot_bgcolor'], paper_bgcolor=colours['paper_bgcolor'],
                      font={'color': colours['fontcolor']})
    pie = px.pie(df, names=df.segment, title='Customer segment')
    pie.update_layout(plot_bgcolor=colours['plot_bgcolor'], paper_bgcolor=colours['paper_bgcolor'],
                      font={'color': colours['fontcolor']})
    return fig, pie


@app.callback(Output(component_id='top_city', component_property='figure'),
              [Input(component_id='dropdown_product', component_property='value'),
               Input(component_id='radio_', component_property='value')])
def graph_from_product_dropdown(product_, radio_item_):
    df = dff.copy()
    df1 = df.loc[df['sub_category'] == product_]
    product_df = pd.DataFrame(df1.groupby('city')['sales', 'profit'].sum()).sort_values(by=radio_item_,
                                                                                        ascending=False).head(10)
    product_bar = px.bar(data_frame=product_df, x=product_df.index, y=radio_item_)
    product_bar.update_layout(xaxis_tickangle=-45, plot_bgcolor=colours['plot_bgcolor'],
                              paper_bgcolor=colours['paper_bgcolor'], font={'color': colours['fontcolor']})
    return product_bar


@app.callback([Output(component_id='total_sales', component_property='children'),
               Output(component_id='state_name1', component_property='children'),
               Output(component_id='total_profit', component_property='children'),
               Output(component_id='state_name2', component_property='children'),
               Output(component_id='top_selling_amt', component_property='children'),
               Output(component_id='top_selling_name', component_property='children'),
               Output(component_id='high_profit_amt', component_property='children'),
               Output(component_id='high_profit_name', component_property='children'), ],
              Input(component_id='dropdown_state', component_property='value'))
def blocks(state_):
    df = dff.copy()
    df1 = df.loc[df['state'] == state_]
    total_sales = '$ ' + str(np.round(df1.sales.sum(), 2))
    total_profit = '$ ' + str(np.round(df1.profit.sum(), 2))
    top_sales = pd.DataFrame(df1.groupby('sub_category')['sales', 'profit'].sum()).sort_values(ascending=False,
                                                                                               by='sales').head(1)
    top_profit = pd.DataFrame(df1.groupby('sub_category')['sales', 'profit'].sum()).sort_values(ascending=False,
                                                                                                by='profit').head(1)
    top_sales_item = top_sales.index.values[0]
    top_sales_item_amt = '$ ' + str(np.round(top_sales.sales.values[0], 2))
    top_profit_item = top_profit.index.values[0]
    top_profit_item_amt = '$ ' + str(np.round(top_profit.profit.values[0], 2))
    return total_sales, state_, total_profit, state_, top_sales_item_amt, top_sales_item, top_profit_item_amt, top_profit_item


if __name__ == "__main__":
    app.run_server(port=5000, debug=True)
