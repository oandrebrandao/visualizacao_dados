import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from dash_bootstrap_templates import ThemeSwitchAIO

FONT_AWESOME = ["https://use.fontawesome.com/releases/v5.10.2/css/all.css"]

app = dash.Dash(__name__,  external_stylesheets=[FONT_AWESOME, dbc.themes.FLATLY, dbc.themes.DARKLY])

app.scripts.config.serve_locally = True
server = app.server

# ========== Styles ============ #
tab_card = {'height': '100%'}

main_config = {
    "hovermode": "x unified",
    "legend": {"yanchor":"top", 
                "y":0.9, 
                "xanchor":"left",
                "x":0.1,
                "title": {"text": None},
                "font" :{"color":"white"},
                "bgcolor": "rgba(0,0,0,0.5)"},
    "margin": {"l":10, "r":10, "t":10, "b":10}
}

config_graph={"displayModeBar": False, "showTips": False}

template_theme1 = "flatly"
template_theme2 = "darkly"
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY


# ===== Reading n cleaning File ====== #
df = pd.read_excel('assets/output.xlsx')
df_copia = df.copy()

# ===== Treating data ===== #
# ===== DF oficial ==== #
df['Data da Compra'] = pd.to_datetime(df['Data da Compra'])
df['Valor Integral'] = df['Valor da Compra']/(1-(df['Desconto (%)']/100))
df['Valor Desconto'] = df['Valor Integral'] - df['Valor da Compra']
df['Mes da Compra']=df['Data da Compra'].dt.month
df['Dia da Compra']=df['Data da Compra'].dt.day
bins = [18, 25, 35, 45, 55, 65, float('inf')]
labels = ['18 a 25 Anos', '26 a 35 Anos', '36 a 45 Anos', '46 a 55 Anos', '56 a 65 Anos', 'Acima de 65 Anos']
df['Faixa Etária'] = pd.cut(df['Idade do Cliente'], bins=bins, labels=labels, right=True)

# ===== DF Secundario ===== #
df_copia['Data da Compra'] = pd.to_datetime(df['Data da Compra'])
df_copia['Mes da Compra']=df_copia['Data da Compra'].dt.month
df_copia['Dia da Compra']=df_copia['Data da Compra'].dt.day
df_copia['Mes da Compra'].replace({ '1':'Jan','2':'Fev','3':'Mar','4':'Abr','5':'Mai','6':'Jun','7':'Jul','8':'Ago','9':'Set','10':'Out','11':'Nov','12':'Dez'}, inplace=True)

##Criando opções pros filtros que virão
options_month = [{'label': 'Ano todo', 'value': 0}]
for i, j in zip(df['Mes da Compra'].unique(), df_copia['Mes da Compra'].unique()):
     options_month.append({'label': i, 'value': j})
options_month = sorted(options_month, key=lambda x: x['value']) 

options_consultant = [{'label': 'Todas Equipes', 'value': 0}]
for i in df['Nome do Vendedor'].unique():
    options_consultant.append({'label': i, 'value': i})
# ========= Função dos Filtros ========= #
def month_filter(month):
    if month == 0:
        mask = df['Mes da Compra'].isin(df['Mes da Compra'].unique())
    else:
        mask = df['Mes da Compra'].isin([month])
    return mask

def consultant_filter(consultant):
    if consultant == 0:
        mask = df['Nome do Vendedor'].isin(df['Nome do Vendedor'].unique())
    else:
        mask = df['Nome do Vendedor'].isin([consultant])
    return mask

def convert_to_text(month):
    match month:
        case 0:
            x = 'Ano Todo'
        case 1:
            x = 'Janeiro'
        case 2:
            x = 'Fevereiro'
        case 3:
            x = 'Março'
        case 4:
            x = 'Abril'
        case 5:
            x = 'Maio'
        case 6:
            x = 'Junho'
        case 7:
            x = 'Julho'
        case 8:
            x = 'Agosto'
        case 9:
            x = 'Setembro'
        case 10:
            x = 'Outubro'
        case 11:
            x = 'Novembro'
        case 12:
            x = 'Dezembro'
    return x


# =========  Layout  =========== #
app.layout = dbc.Container(children=[
    # Armazenamento de dataset
    # dcc.Store(id='dataset', data=df_store),
## Layout
dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([   
                            html.Legend("Analise de Vendas")
                        ], sm=8),
                        dbc.Col([        
                            html.I(className='fa fa-balance-scale', style={'font-size': '300%'})
                        ], sm=4, align="center")
                    ]),
                    dbc.Row([
                        dbc.Col([
                            ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2])
                        ])
                    ], style={'margin-top': '10px'})
                ])
            ], style=tab_card)
        ], sm=12, md=4, lg=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row(
                        dbc.Col(
                            html.Legend('Indicadores Gerais')
                        )
                    ),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='graph1', className='dbc', config=config_graph)
                        ], sm=12, md=6, lg=3),
                        dbc.Col([
                            dcc.Graph(id='graph2', className='dbc', config=config_graph)
                        ], sm=12, md=6, lg=3),
                        dbc.Col([
                            dcc.Graph(id='graph3', className='dbc', config=config_graph)
                        ], sm=12, md=6, lg=3),
                        dbc.Col([
                            dcc.Graph(id='graph4', className='dbc', config=config_graph)
                        ], sm=12, md=6, lg=3)     
                    ])
                ])
            ], style=tab_card)
        ], sm=12, lg=7),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row(
                        dbc.Col([
                            html.H5('Escolha o Mês'),
                            dbc.RadioItems(
                                id="radio-month",
                                options=options_month,
                                value=0,
                                inline=True,
                                labelCheckedClassName="text-success",
                                inputCheckedClassName="border border-success bg-success",
                            ),
                            html.Div(id='month-select', style={'text-align': 'center', 'margin-top': '30px'}, className='dbc')
                        ])
                    )
                ])
            ], style=tab_card)
        ], sm=12, lg=3)
    ], className='g-2 my-auto', style={'margin-top': '7px'}),

    # Row 2
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph5', className='dbc', config=config_graph)
                        ])
                    ], style=tab_card),
                ], sm=12, lg=6),
                dbc.Col([    
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph6', className='dbc', config=config_graph)
                        ])
                    ], style=tab_card)
                ], sm=12, lg=6)
            ], className='g-2 my-auto', style={'margin-top': '7px'})
        ], sm=12, lg=5),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph7', className='dbc', config=config_graph)    
                        ])
                    ], style=tab_card)
                ], sm=12, md=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph8', className='dbc', config=config_graph)    
                        ])
                    ], style=tab_card)
                ], sm=12, md=6)
            ], className='g-2'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dcc.Graph(id='graph9', className='dbc', config=config_graph)
                    ], style=tab_card)
                ], sm=12, md=8),
                dbc.Col([
                    dbc.Card([
                        dcc.Graph(id='graph10', className='dbc', config=config_graph)
                    ], style=tab_card)
                ], sm=12, md=4)
            ], className='g-2 my-auto', style={'margin-top': '7px'})
        ], sm=12, lg=7)
    ], className='g-2 my-auto', style={'margin-top': '7px'}),

    # Row 3
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4('Análise por Faixa Etária'),
                            dcc.Graph(id='graph11', className='dbc', config=config_graph)
                        ])
                    ], style=tab_card)
                ], sm=12, lg=7), 
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph12', className='dbc', config=config_graph)
                        ])
                    ], style=tab_card)
                ], sm=12, lg=5),       
            ]),    
        ], sm=12, lg=5),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='graph13', className='dbc', config=config_graph)
                ])
            ], style=tab_card)
        ], sm=12, lg=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5('Escolha o Vendedor'),
                    dbc.RadioItems(
                        id="radio-consultant",
                        options=options_consultant,
                        value=0,
                        inline=True,
                        labelCheckedClassName="text-warning",
                        inputCheckedClassName="border border-warning bg-warning",
                    ),
                    html.Div(id='team-select', style={'text-align': 'center', 'margin-top': '30px'}, className='dbc')
                ])
            ], style=tab_card)
        ], sm=12, lg=3),
    ], className='g-2 my-auto', style={'margin-top': '7px'})
], fluid=True, style={'height': '100vh'})
# ======== Callbacks ========== #
# Graph 1, 2 , 3 and 4
@app.callback(
    Output('graph1', 'figure'),
    Output('graph2', 'figure'),
    Output('graph3', 'figure'),
    Output('graph4', 'figure'),
    Output('month-select', 'children'),
    Input('radio-month', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph1(month, toggle):
    template = template_theme1 if toggle else template_theme2
    
    mask = month_filter(month)
    df_1 = df.loc[mask]
    
    fig1 = go.Figure()
    fig1.add_trace(go.Indicator(mode='number',
        title = {"text": f"<span style='font-size:150%'>Valor Total</span><br><span style='font-size:70%'>Em Reais</span><br>"},
        value = df['Valor da Compra'].sum(),
        number = {'prefix': "R$"}
    ))
    fig2 = go.Figure()
    fig2.add_trace(go.Indicator(mode='number',
        title = {"text": f"<span style='font-size:150%'>Total de Vendas</span>"},
        value = len(df['Quantidade de Peças'])
    ))
    fig3 = go.Figure()
    fig3.add_trace(go.Indicator(
    mode='number',
    title={"text": "<span style='font-size:150%'>Ticket Médio</span><br><span style='font-size:70%'>Em Reais</span><br>"},
    value=(df['Valor da Compra'].sum()) / len(df['Quantidade de Peças']),
    number={'prefix': "R$"}
    ))
    fig4 = go.Figure()
    fig4.add_trace(go.Indicator(
    mode='number',
    title={"text": "<span style='font-size:150%'>Peças por Venda</span><br><span style='font-size:70%'>Média</span><br>"},
    value=(df_1['Quantidade de Peças'].sum()) / len(df_1['Quantidade de Peças'])
    ))
    fig1.update_layout(main_config, height=200, template=template)
    fig2.update_layout(main_config, height=200, template=template)
    fig3.update_layout(main_config, height=200, template=template)
    fig4.update_layout(main_config, height=200, template=template)
    fig1.update_layout({"margin": {"l":0, "r":0, "t":20, "b":0}})
    fig2.update_layout({"margin": {"l":0, "r":0, "t":20, "b":0}})
    fig3.update_layout({"margin": {"l":0, "r":0, "t":20, "b":0}})
    fig4.update_layout({"margin": {"l":0, "r":0, "t":20, "b":0}})
    
    select = html.H1(convert_to_text(month))
        
    return fig1,fig2,fig3,fig4,select
    
# # Graph 5 and 6 
@app.callback(
    Output('graph5', 'figure'),
    Output('graph6', 'figure'),
    Input('radio-month', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph5(month, toggle):
    template = template_theme1 if toggle else template_theme2
    
    mask = month_filter(month)
    df_2 = df.loc[mask]

    df_2 = df_2.groupby('Nome do Vendedor')['Valor da Compra'].sum().reset_index()

    fig5=go.Figure(go.Bar(
                x=df_2['Valor da Compra'],
                y=df_2['Nome do Vendedor'],
                orientation='h',
                textposition='auto',
                text=df_2['Valor da Compra'],
                insidetextfont=dict(family='Times', size=12)))
    fig6= go.Figure()
    fig6.add_trace(go.Pie(labels=df_2['Nome do Vendedor'], values=df_2['Valor da Compra'],hole=.6))
    fig5.update_layout(main_config, height=600, template=template)
    fig6.update_layout(main_config, height=600, template=template, showlegend=False)
    return fig5,fig6

## Graph 7        
@app.callback(
    Output('graph7', 'figure'),
    Input('radio-consultant', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph7(consultant, toggle):
    template = template_theme1 if toggle else template_theme2
    
    mask = consultant_filter(consultant)
    df_3 = df.loc[mask]

    df_3 = df_3.groupby('Dia da Compra')['Quantidade de Peças'].sum().reset_index()

    fig7= go.Figure(go.Scatter(
        x=df_3['Dia da Compra'],
        y=df_3['Quantidade de Peças'], mode='lines', fill='tonexty'))

    fig7.add_annotation(text='Quantidade de Peças Vendidas',
                    xref= 'paper', yref='paper',
                    font=dict(size=20, color='gray'), align='center',
                    bgcolor='rgba(0,0,0,0.8)',
                    x=0.05, y=0.85, showarrow=False)
    fig7.add_annotation(text=f"Média : {round(df_3['Quantidade de Peças'].mean(), 2)}",
        xref="paper", yref="paper",
        font=dict(
            size=30,
            color='gray'
            ),
        align="center", bgcolor="rgba(0,0,0,0.8)",
        x=0.05, y=0.55, showarrow=False)
    fig7.update_layout(main_config, height=200, template=template)
    return fig7

## Graph8
@app.callback(
    Output('graph8', 'figure'),
    Input('radio-consultant', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph8(consultant, toggle):
    template = template_theme1 if toggle else template_theme2
    
    mask = consultant_filter(consultant)
    df_4 = df.loc[mask]
    
    df_4= df_4.groupby('Mes da Compra')['Quantidade de Peças'].sum().reset_index()
    
    fig8 = go.Figure(go.Scatter(x=df_4['Mes da Compra'], y=df_4['Quantidade de Peças'], mode='lines', fill='tonexty'))

    fig8.add_annotation(text='Média de Peças por Mês',
        xref="paper", yref="paper",
        font=dict(
            size=20,
            color='gray'
            ),
        align="center", bgcolor="rgba(0,0,0,0.8)",
        x=0.05, y=0.85, showarrow=False)
    fig8.add_annotation(text=f"Média : {round(df_4['Quantidade de Peças'].mean(), 2)}",
        xref="paper", yref="paper",
        font=dict(
            size=30,
            color='gray'
            ),
        align="center", bgcolor="rgba(0,0,0,0.8)",
        x=0.05, y=0.55, showarrow=False)
    fig8.update_layout(main_config, height=200, template=template)
    return fig8

# Graph 9 and 10 
@app.callback(
    Output('graph9', 'figure'),
    Output('graph10', 'figure'),
    Input('radio-month', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph9(month, toggle):
    template = template_theme1 if toggle else template_theme2
    
    df_5= df.groupby(['Nome do Vendedor', 'Mes da Compra'])['Valor da Compra'].sum().reset_index()
    df5_group= df_5.groupby('Mes da Compra')['Valor da Compra'].sum().reset_index()

    fig9=px.line(df_5, x='Mes da Compra', y='Valor da Compra', color='Nome do Vendedor')
    fig9.add_trace(go.Scatter(x=df5_group['Mes da Compra'],y=df5_group['Valor da Compra'],mode='lines', fill='tonexty',name='Total de Vendas'))
    
    
    mask=month_filter(month)
    df_6= df.loc[mask]
    
    df_6= df_6.groupby('Nome do Vendedor')['Valor da Compra'].sum()
    df_6.sort_values(ascending=False, inplace=True)
    df_6= df_6.reset_index()
    
    fig10=go.Figure()
    fig10.add_trace(go.Indicator(mode='number+delta',
        title = {"text": f"<span style='font-size:150%'>{df_6['Nome do Vendedor'].iloc[0]} - Top Consultant</span><br><span style='font-size:70%'>Em vendas - em relação a média</span><br>"},
        value = df_6['Valor da Compra'].iloc[0],
        number = {'prefix': "R$"},
        delta = {'relative': True, 'valueformat': '.1%', 'reference': df_6['Valor da Compra'].mean()}
    ))
    fig9.update_layout(main_config, yaxis={'title': None}, xaxis={'title': None}, height=400, template=template)
    fig9.update_layout({"legend": {"yanchor": "top", "y":0.99, "font" : {"color":"white", 'size': 10}}})
    fig10.update_layout(main_config, height=400, template=template)
    fig10.update_layout({"margin": {"l":0, "r":0, "t":20, "b":0}})
    return fig9, fig10

# Graph 11 and 12
@app.callback(
    Output('graph11', 'figure'),
    Output('graph12', 'figure'),
    Input('radio-month', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph11(month, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = month_filter(month)
    df_7 = df_8 = df.loc[mask]

    df_7=df_7.groupby('Faixa Etária')['Valor da Compra'].mean().reset_index()

    fig11=go.Figure(go.Bar(x=df_7['Faixa Etária'],y=df_7['Valor da Compra'],textposition='auto',text=df_7['Valor da Compra'],insidetextfont=dict(family='Times', size=12)))

    df_8=df_8.groupby(['Faixa Etária'])['Quantidade de Peças'].mean().reset_index()

    fig12= go.Figure()
    fig12.add_trace(go.Pie(labels=df_8['Faixa Etária'], values=df_8['Quantidade de Peças'],hole=.6))
    fig11.update_layout(main_config, height=400, template=template)
    fig12.update_layout(main_config, height=400, template=template, showlegend=False)
    return fig11,fig12
# Graph 11

@app.callback(
    Output('graph13', 'figure'),
    Output('consultant-select', 'children'),
    Input('radio-month', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph13(month, consultant, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = month_filter(month)
    df_9 = df.loc[mask]

    df_9= df_9.groupby('Mes da Compra')[['Valor da Compra','Valor Integral']].sum().reset_index()

    fig13 = go.Figure()
    fig13.add_trace(go.Bar(x=df_9['Mes da Compra'], y=df_9['Valor da Compra'], name='Valor da Compra'))
    fig13.add_trace(go.Bar(x=df_9['Mes da Compra'], y=df_9['Valor Integral'], name='Valor Integral'))
    fig13.update_layout(main_config, height=400, template=template)    
    select = html.H1("Todos os Vendedores") if consultant == 0 else html.H1(consultant)
    return fig13, select


# Run server
if __name__ == '__main__':
    app.run_server(debug=False)
    