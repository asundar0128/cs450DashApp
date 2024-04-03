import pandas as pd
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

modifiedStylesheetValue= [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh',
        'crossorigin': 'anonymous'
    }
]

csvFileCovidDataset = pd.read_csv('diseaseOutbreakData.csv')
indianStatesFocus=pd.read_csv('uniqueDataCity.csv')

entireValue=indianStatesFocus.shape[0]
hiddenValue=indianStatesFocus['current_status'].value_counts()

detectedStateValue=indianStatesFocus['detected_state'].value_counts().reset_index()


endValue=csvFileCovidDataset.groupby('Country/Region')['Deaths'].max().sort_values(ascending=False).reset_index().head(22)


countryOptions=[
    {'label':'All','value':'All'},
    {'label':'China','value':'China'},
    {'label':'Iran','value':'Iran'},
    {'label':'US','value':'US'},
    {'label':'United Kingdom','value':'United Kingdom'},
    {'label':'Italy','value':'Italy'},
    {'label':'India','value':'India'}
]

covidCountryInfo=[
    {'label':'All','value':'All'},
    {'label':'Recovered	','value':'Recovered'},
    {'label':'Hospitalized','value':'Hospitalized'},
    {'label':'Deceased','value':'Deceased'}

]
indianStatesValue=[
    {'label':'All','value':'All'},
    {'label':'Maharashtra','value':'Maharashtra'},
    {'label':'Delhi','value':'Delhi'},
    {'label':'Kerala','value':'Kerala'},
    {'label':'Telangana','value':'Telangana'},
    {'label': 'West Bengal	', 'value': 'West Bengal'},
    {'label': 'Rajasthan', 'value': 'Rajasthan'},
    {'label': 'Tamil Nadu', 'value': 'Tamil Nadu'},
    {'label': 'Uttar Pradesh', 'value': 'Uttar Pradesh'}
]





app = dash.Dash(__name__, external_stylesheets=modifiedStylesheetValue)

app.layout=html.Div([
    html.Div([
        html.H1("Covid-19 Outbreak Findings",style={'margin-top':'10px'}),
        html.P("Covid-19 India Findings",style={'text-align':'left','margin-top':'-25px'})
    ],className='jumbotron'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3(entireValue),
                            html.H6("Cumulative Test Cases Across India")
                        ],className='card-body')
                    ],className='card',style={'background-color':'blue','margin-top':'0.2rem'})
                ],className='col-md-12'),
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3(hiddenValue[0]),
                            html.H6("Validated Instances of Covid-19")
                        ],className='card-body')
                    ],className='card',style={'background-color':'green','margin-top':'0.2rem'})
                ],className='col-md-12'),
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3(hiddenValue[1]),
                            html.H6("Recuperated Instances of Covid-19")
                        ],className='card-body')
                    ],className='card',style={'background-color':'red','margin-top':'0.2rem'})
                ],className='col-md-12'),
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3(hiddenValue[2]),
                            html.H6("Deaths Throughout India Due to Covid-19 Pandemic")
                        ],className='card-body')
                    ],className='card',style={'background-color':' yellow','margin-top':'0.2rem'})
                ],className='col-md-12'),
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3(hiddenValue[3]),
                            html.H6("Number of People Who Moved Due to Covid-19 Pandemic")
                        ],className='card-body')
                    ],className='card',style={'background-color':'orange','margin-top':'0.2rem'})
                ],className='col-md-12')
            ],className='row')
        ],className='col-md-2'),
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            dcc.Graph(id='scatter-plot',
                                        figure={'data':[go.Bar(x=endValue['Country/Region'],y=endValue['Deaths'])],
                                        'layout':go.Layout(title='Number of Death according to Country',xaxis={'title':'Country/Region'},yaxis={'title':'Number of Deaths'},paper_bgcolor='rgba(0,0,0,1)',plot_bgcolor='rgba(0,0,0,1)')})

                        ],className='card-body')
                    ],className='card')
                ],className='col-md-6'),
                html.Div([
                    html.Div([
                        html.Div([
                            dcc.Dropdown(id='pie', options=indianStatesValue, value='All'),
                            dcc.Graph(id='pie1')
                        ],className='card-body')
                    ],className='card')
                ],className='col-md-6'),
                html.Div([
                    html.Div([
                        html.Div([
                            dcc.Graph(id='d_state',
                                      figure={'data':[go.Bar(x=detectedStateValue['index'],y=detectedStateValue['detected_state'])],
                                              'layout':go.Layout(title='No. of  case in Different state',xaxis={'title':'State'},yaxis={'title':'Number of patients'})})
                        ],className='card-body')
                    ],className='card')
                ],className='col-md-6 mt-3'),
                html.Div([
                    html.Div([
                        html.Div([
                            dcc.Dropdown(id='piker',options=countryOptions,value='All'),
                            dcc.Graph(id='line')
                        ],className='card-body')
                    ],className='card')
                ],className='col-md-6 mt-3')

            ],className='row')
        ],className='col-md-10')
    ],className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                        dcc.Dropdown(id='pik',options=covidCountryInfo,value='All'),
                        dcc.Graph(id='line2')
                ],className='card-body')
            ],className='card')
        ],className='col-md-12 mt-3')
    ],className='row'),
    html.Div([],className='row')
],className='container-fluid')




@app.callback(Output('line','figure'), [Input('piker','value')])
def update_graph(type):
    if type=='All':
        hiddenValue = csvFileCovidDataset.groupby('Date')['Deaths'].max().sort_values(ascending=True).reset_index()
        return {'data':[go.Line(x=hiddenValue['Date'],y=hiddenValue['Deaths'])],
                'layout':go.Layout(title='Number of Deaths Per Day',xaxis={'title':'Dates'},yaxis={'title':'Number of Deaths'},paper_bgcolor='rgba(0,0,0,1)',plot_bgcolor='rgba(0,0,0,1)')}
    else:
        hiddenValue = csvFileCovidDataset[csvFileCovidDataset['Country/Region'] == type]
        hiddenValues = hiddenValue.groupby('Date')['Deaths'].max().sort_values(ascending=True).reset_index()
        return {'data': [go.Line(x=hiddenValues['Date'], y=hiddenValues['Deaths'])],
                'layout': go.Layout(title='Number of Deaths Per Day',xaxis={'title':'Dates'},yaxis={'title':'Number of Deaths'},paper_bgcolor='rgba(0,0,0,1)',plot_bgcolor='rgba(0,0,0,1)')}


@app.callback(Output('line2','figure'), [Input('pik','value')])
def update_graph(secondInput):
    if secondInput=='All':
        hiddenValues=indianStatesFocus['detected_state'].value_counts().reset_index()
        return {'data':[go.Line(x=hiddenValues['index'],y=hiddenValues['detected_state'])],
                'layout':go.Layout(title='Number of Patients',xaxis={'title':'Number of Patients'},yaxis={'title':'states'})}
    else:
        indicatorCovid = indianStatesFocus[indianStatesFocus['current_status'] == secondInput]
        hiddenValueIterator = indicatorCovid['detected_state'].value_counts().reset_index()
        return {'data': [go.Line(x=hiddenValueIterator['index'], y=hiddenValueIterator['detected_state'])],
                'layout': go.Layout(title='Number of Patients',xaxis={'title':'Number of patients'},yaxis={'title':'States'})}


@app.callback(Output('pie1','figure'), [Input('pie','value')])
def update_graph(type2):
    if type2=='All':
        predeterminedHiddenValue = indianStatesFocus['current_status'].value_counts().reset_index()
        firstValueIndex = predeterminedHiddenValue['current_status'][0]
        secondValueIndex = predeterminedHiddenValue['current_status'][1]
        thirdValueIndex = predeterminedHiddenValue['current_status'][2]

        covidCategoriesNames = ['Hospitalized', 'Recovered', 'Deceased']
        valueIndices = [firstValueIndex, secondValueIndex, thirdValueIndex]
        generatedDrawing=go.Figure(data=[go.Pie(labels=covidCategoriesNames, values=valueIndices)])
        return generatedDrawing
    else:
        hiddenValue = indianStatesFocus[indianStatesFocus['detected_state'] == type2]
        predeterminedHiddenValue = hiddenValue['current_status'].value_counts().reset_index()
        firstValueIndex = predeterminedHiddenValue['current_status'][0]
        secondValueIndex = predeterminedHiddenValue['current_status'][1]
        thirdValueIndex = predeterminedHiddenValue['current_status'][2]
        valueIndices = [firstValueIndex, secondValueIndex, thirdValueIndex]
        covidCategoriesNames = ['Hospitalized', 'Recovered', 'Deceased']
        generatedDrawing= go.Figure(data=[go.Pie(labels=covidCategoriesNames, values=valueIndices)])
        return generatedDrawing

if __name__ == '__main__':
    app.run_server(debug=True)
