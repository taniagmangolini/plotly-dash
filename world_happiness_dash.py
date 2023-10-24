from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

app = Dash()

# https://www.kaggle.com/datasets/unsdsn/world-happiness
happiness_df = pd.read_csv('happiness.csv')

line_figure = px.line(happiness_df[happiness_df['Country or region'] == 'Spain'],
                      x='Year',
                      y='Score',
                      title='Happiness Score in the Spain')

radio_metrics_options = dcc.RadioItems(
    id='radio-metrics-options',
    options={
        'Score': 'Happiness Score',
        'GDP per capita': 'GDP Per Capita'
    },
    value='Score'
)

# checklist example
# dcc.Checklist(options=happiness_df['Country or region'].unique(),
#               value=['Spain']),

app.layout = html.Div([
    html.H1('World Happiness Dashboard', style={'textAlign': 'center', 'color': 'blue'}),
    html.P([
        'This dashboard shows the happiness score.',
        html.Br(),
        html.A('World happiness report datasource',
        href='http://https://worldhappiness.report',
        target='_blank')
    ]),
    dcc.Dropdown(id='country-dropdown', options=happiness_df['Country or region'].unique(),
                 value='Spain'),
    html.Br(),
    radio_metrics_options,
    dcc.Graph(id='line-chart', figure=line_figure),
    html.Div(id='average')
])


@app.callback(
    Output(component_id='line-chart', component_property='figure'),
    Output(component_id='average', component_property='children'),
    Input(component_id='country-dropdown', component_property='value'),
    Input(radio_metrics_options, component_property='value')
)
def update_line_chart(selected_country, metric_option):
    filtered_happiness_df = happiness_df[happiness_df['Country or region'] == selected_country]
    average_output = f'The average {metric_option} for this country is {filtered_happiness_df[metric_option].mean()}'
    line_chart_output =  px.line(filtered_happiness_df,
                                 x='Year',
                                 y=metric_option,
                                 title=f'{metric_option} in {selected_country}')
    return line_chart_output, average_output


if __name__ == '__main__':
    app.run_server(debug=True)
