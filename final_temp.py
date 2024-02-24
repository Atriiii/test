import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
# app.title = "Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
# List of years 
year_list = [i for i in range(1980, 2024, 1)]
#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    # TASK 2.1 Add title to the dashboard
    html.H1("Automobile Sales Statistics Dashboard",
           style={'textAlign': 'left', 'color': '#503D36',
                                'font-size': 24}),
    html.Div([
        # TASK 2.2: Add two dropdown menus
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            placeholder='Select a report type.',
            style={'width': '50%'}
        ),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': str(i), 'value': i} for i in year_list],
            value='2020',
            placeholder='Select Year',
            style={'width': '50%'}
        ),
    ]),
    html.Div([# TASK 2.3: Add a division for output display
        html.Div(id='output-container', className='chart-grid', style={'flex': '1'}),
    ])
])

# TASK 2.4: Creating Callbacks
# Callback for updating input container visibility
@app.callback(
    Output('output-container', 'children'),
    Input('dropdown-statistics', 'value')
)
def update_input_container(value):
    if value == 'Yearly Statistics':
        return False
    else:
        return True

# Callback for updating output container based on selected statistics
@app.callback(
    Output('output-container', 'children'),
    [Input('select-year', 'value'), Input('dropdown-statistics', 'value')]
)
def update_output_container(input_year, selected_statistics):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]

        # Plot 1: Automobile sales fluctuate over the Recession Period (year-wise)
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales fluctuation over Recession Period"
            )
        )

        # Plot 2: Calculate the average number of vehicles sold by vehicle type
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title="Average Number of Vehicles Sold by Vehicle Type"
            )
        )

        # Plot 3: Pie chart for total expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Total_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                names='Vehicle_Type',
                values='Total_Expenditure',
                title="Total Expenditure Share by Vehicle Type during Recessions"
            )
        )

        # Plot 4: Bar chart for the effect of unemployment rate on vehicle type and sales
        avg_sales_unemp = recession_data.groupby(['Vehicle_Type', 'Unemployment_Rate'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(
                avg_sales_unemp,
                x='Unemployment_Rate',
                y='Automobile_Sales',
                color='Vehicle_Type',
                title="Effect of Unemployment Rate on Vehicle Type and Sales"
            )
        )

        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1), html.Div(children=...)]), #style={...}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart2), html.Div(children=...)]),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3), html.Div(children=...)]),
            html.Div(className='chart-item', children=[html.Div(children=R_chart4), html.Div(children=...)])
        ]

    elif input_year and selected_statistics == 'Yearly Statistics':
        yearly_data = data[data['Year'] == int(input_year)]

        # Plot 1: Yearly Automobile sales using a line chart for the whole period.
        yas = yearly_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(
            yas,
            x='Year',
            y='Automobile_Sales',
            title='Yearly Automobile Sales'
        ))

        # Plot 2: Total Monthly Automobile sales using a line chart.
        Y_chart2 = dcc.Graph(figure=px.line(
            # Replace with the relevant data and parameters
        ))

        # Plot 3: Bar chart for the average number of vehicles sold during the given year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(
            avr_vdata,
            x='Vehicle_Type',
            y='Automobile_Sales',
            title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)
        ))

        # Plot 4: Total Advertisement Expenditure for each vehicle using a pie chart
        exp_data = yearly_data.groupby('Vehicle_Type')['Total_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(
            exp_data,
            names='Vehicle_Type',
            values='Total_Expenditure',
            title='Total Advertisement Expenditure by Vehicle Type'
        ))

        return [
            html.Div(className='chart-item', children=[html.Div(children=Y_chart1)]),
            html.Div(className='chart-item', children=[html.Div(children=Y_chart2)]),
            html.Div(className='chart-item', children=[html.Div(children=Y_chart3)]),
            html.Div(className='chart-item', children=[html.Div(children=Y_chart4)])
        ]

    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
