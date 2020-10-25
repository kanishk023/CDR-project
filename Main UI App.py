import pandas as pd 
import numpy as np
import webbrowser
import dash
import dash_html_components as html
from dash.dependencies import Input,Output
import dash_core_components as dcc
import re

import plotly.graph_objects as go
import plotly.express as px

import dash_bootstrap_components as dbc
import dash_table as dt 


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])







# FUNCTIONS
 
def load_data():
    call_dataset_name = 'Call_data.csv'
    service_dataset_name = 'Service_data.csv'
    device_dataset_name = 'Device_data.csv'
    
    
    
    global call_data
    call_data = pd.read_csv(call_dataset_name)
    
    global service_data
    service_data = pd.read_csv(service_dataset_name)
    
    global device_data
    device_data = pd.read_csv(device_dataset_name)
  

    
    
    temp_list = sorted(call_data['date'].dropna().unique().tolist())

    global start_date_list
    start_date_list =[ { "label": str(i), "value" :str(i) }   for i in temp_list ]

    global end_date_list
    end_date_list =[ { "label": str(i), "value" :str(i) }   for i in temp_list ]
    
    
    
    temp_list1 = ['Hourly', 'Daywise', 'Weekly']
    
    global report_type
    report_type = [ { "label": str(i), "value" :str(i) }   for i in temp_list1 ]
    
       
def open_browser():
    webbrowser.open_new('http://127.0.0.1:8050/')
    
# 'borderBottom': '1px solid #d6d6d6', 'padding': '6px','fontSize':'25px'
def create_app_ui():
    main_layout = html.Div(
    [
    html.H1(children='CDR Analysis with Insights', id='Main_title', style={'text-align': 'center'}),
    html.Br(),
    dcc.Tabs(id="Tabs", value="tab-1", children =
             
    [
    dcc.Tab(label="Call Analytics tool" ,id="Call Analytics tool",value="tab-1",style = {'height': '60px'}, children = 
            
    [
    html.Br(),
    dcc.Dropdown(id='dropdown1',options=start_date_list, placeholder='Select Starting Date', value = "2019-06-20", style={'background':'rgb(225, 225, 225)'}),
    html.Br(),
    dcc.Dropdown(id='dropdown2',options=end_date_list, placeholder='Select Ending Date', value = "2019-06-25", style={'background':'rgb(225, 225, 225)'}),
    html.Br(),
    dcc.Dropdown(id='dropdown3', multi=True, placeholder='Select Group', style={'background':'rgb(225, 225, 225)'}),
    html.Br(),
    dcc.Dropdown(id='dropdown4',options=report_type, placeholder='Select Report Type', value = "Hourly", style={'background':'rgb(225, 225, 225)'})
    ]
    
    ),
    
    dcc.Tab(label = "Device Analytics tool", id="Device Analytics tool", value="tab-2", style = {'height': '60px'}, children = 
    
    [
      html.Br(),
      dcc.Dropdown(
      id='device-date-dropdown', 
      options=start_date_list,
      placeholder = "Select Date here",
      style={'background':'rgb(225, 225, 225)'},
      multi = True),
      html.Br()
    ]),
    
    dcc.Tab(label = "Service Analytics tool", id="Service Analytics tool", value="tab-3", style = {'height': '60px'}, children = 
    [
      html.Br(),
      dcc.Dropdown(
      id='service-date-dropdown', 
      options=start_date_list,
      placeholder = "Select Date here",
      style={'background':'rgb(225, 225, 225)'},
      multi = True), 
      html.Br()
    ])
    
    ]
    
    ),

    html.Br(),
    dcc.Loading(html.Div(id = 'visualization', children = 'Graph, Card, Table')),
    
    html.Br()
    ]                
    )
    
    return main_layout




def create_card(title, body, color):
    card = dbc.Card(dbc.CardBody(
        [
        html.H4(title, className = 'card-title'),
        html.Br(),
        html.H2(body, className = 'card-subtitle'),
        html.Br(),
        ]
        ),
        color = color, inverse = True
        )
    return (card)


def count_devices(data):
    
    # Various devices used for VoIP calls
    device_dict = {"Polycom" :0, "Windows" : 0, "iphone" : 0, "Android" : 0,
                   "Mac" : 0, "Yealink" : 0, "Aastra" : 0, "Others" : 0}
    
    
    
    reformed_data = data["UserDeviceType"].dropna().reset_index()
    for var in reformed_data["UserDeviceType"]:
        if re.search("Polycom", var) :
            device_dict["Polycom"]+=1
        elif re.search("Yealink", var):
            device_dict["Yealink"]+=1
        elif re.search("Aastra", var):
            device_dict["Aastra"]+=1
        
        elif re.search("Windows", var):
            device_dict["Windows"]+=1
        elif re.search("iPhone|iOS", var):
            device_dict["iphone"]+=1
        elif re.search("Mac", var):
            device_dict["Mac"]+=1
        elif re.search("Android", var):
            device_dict["Android"]+=1
            
        else:
            device_dict["Others"]+=1
    final_data = pd.DataFrame()
    final_data["Device"] = device_dict.keys()
    final_data["Count"] = device_dict.values()
    return final_data


@app.callback(
    Output('visualization','children'),
    
    [Input('Tabs', 'value'),
    Input('dropdown1','value'),
    Input('dropdown2','value'),
    Input('dropdown3','value'),
    Input('dropdown4','value'),
    Input('device-date-dropdown', 'value'),
    Input('service-date-dropdown', 'value')]
    )
def update_app_ui(Tabs, start_date, end_date, group, report_type,device_date,service_date):
    
    if Tabs == "tab-1":    
        call_analytics_data = call_data[ (call_data['date']>=start_date) & (call_data['date']<=end_date) ]
    
        if (group is None):
            pass
        else:
            call_analytics_data = call_analytics_data[call_analytics_data['Group'].isin(group)]
        
        
        graph_data = call_analytics_data
        # Group the data based on the drop down
        if report_type == 'Hourly':
            graph_data = graph_data.groupby('hourly_range')['Call_Direction'].value_counts().reset_index(name = "count")
            x = 'hourly_range'
            
            body = call_analytics_data['hourly_range'].value_counts().idxmax()
            title =  'Busiest Hour'
            
        
                
        elif report_type == 'Daywise':
            graph_data = graph_data.groupby('date')['Call_Direction'].value_counts().reset_index(name = "count")
            x = 'date'
            
            body = call_analytics_data['date'].value_counts().idxmax()
            title =  'Busiest Day'
            
        
                
        else:
            graph_data = graph_data.groupby('weekly_range')['Call_Direction'].value_counts().reset_index(name = "count")
            x = 'weekly_range'
            
            body = call_analytics_data['weekly_range'].value_counts().idxmax()
            title =  'Busiest WeekDay'
            
        # PLOTTING GRAPH 
        figure = px.area(graph_data, x = x, y = "count", color = "Call_Direction",
                         hover_data=[ "Call_Direction", "count"], 
                         template = "plotly_dark")
        figure.update_traces(mode = "lines+markers")
    
    
    
    
        # CREATING CARDS
        total_calls = call_analytics_data["Call_Direction"].count()
        card1 = create_card("Total Calls",total_calls,color =  'primary')
        
        incoming_calls = call_analytics_data["Call_Direction"][call_analytics_data["Call_Direction"]=="Incoming"].count()
        card2 = create_card("Incoming Calls", incoming_calls,color =  'success')
        
        outgoing_calls = call_analytics_data["Call_Direction"][call_analytics_data["Call_Direction"]=="Outgoing"].count()
        card3 = create_card("Outgoing Calls", outgoing_calls,color =  'warning')
        
        missed_calls = call_analytics_data["Missed Calls"][call_analytics_data["Missed Calls"] == 19].count()
        card4 = create_card("Missed Calls", missed_calls,color =  'danger')
        
        max_duration = call_analytics_data["duration"].max()
        card5 = create_card("Max Duration", f'{max_duration} min',color =  'dark')
        
        card6 = create_card(title, body,color = "info")
             
        
        
        row1 = dbc.Row([dbc.Col(id='card1', children=[card1], md=3), dbc.Col(id='card2', children=[card2], md=3),
                        dbc.Col(id='card3', children=[card3], md=3)])
        row2 = dbc.Row([dbc.Col(id='card4', children=[card4], md=3), dbc.Col(id='card5', children=[card5], md=3),
                        dbc.Col(id='card6', children=[card6], md=3)])
        
        cardDiv = html.Div([row1, html.Br(), row2, html.Br()])
    
    
    
    
    
        datatable_data = call_analytics_data.groupby(["Group", "UserID", "UserDeviceType"])["Call_Direction"].value_counts().unstack(fill_value = 0).reset_index()
        if call_analytics_data["Missed Calls"][call_analytics_data["Missed Calls"]==19].count()!=0:
            datatable_data["Missed Calls"] = call_analytics_data.groupby(["Group", "UserID", "UserDeviceType"])["Missed Calls"].value_counts().unstack()[19]
        else:
            datatable_data["Missed Calls"] = 0
                
        datatable_data["Total_call_duration"] = call_analytics_data.groupby(["Group", "UserID", "UserDeviceType"])["duration"].sum().tolist()
                
  
    
        # CREATING DATA TABLE 
        datatable = dt.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in datatable_data.columns],
            data=datatable_data.to_dict('records'),
            page_current=0,
            page_size=15,
            page_action='native',
            style_header={'backgroundColor': 'rgb(30, 30, 30)'},
            style_cell={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white'
                }
            )
        
        return [dcc.Graph(figure = figure), html.Br(), cardDiv, html.Br(), datatable, html.Br(), html.Div(html.H6(children = 'Showing 15 records of total records.', id = 'data_shown', style={'color': '#404241', 'text-align': 'right'})),]
    
    
    
    elif Tabs == "tab-2":
        if device_date is None or device_date == []: 
            device_analytics_data = count_devices(device_data)
        else:
            device_analytics_data = count_devices(device_data[device_data["DeviceEventDate"].isin(device_date)])
          
        fig = px.pie(device_analytics_data, names = "Device", values = "Count",color = "Device", hole = .3)
        fig.update_layout(autosize=True,
                          margin=dict(l=0, r=0, t=25, b=20),
                          paper_bgcolor='black',
                          plot_bgcolor='black'
                          )
        return dcc.Graph(figure = fig)
    
    
    
    elif Tabs == "tab-3":
        if service_date is None or service_date == []:
            service_analytics_data = service_data["FeatureName"].value_counts().reset_index(name = "Count")
        else:
            service_analytics_data = service_data["FeatureName"][service_data["FeatureEventDate"].isin(service_date)].value_counts().reset_index(name = "Count")
        fig = px.pie(service_analytics_data, names = "index", values = "Count",color = "index")
        
        fig.update_layout(#autosize=True,
                          margin=dict(l=0, r=0, t=0, b=0),
                          paper_bgcolor='black',
                          plot_bgcolor='black'
                          )
        return dcc.Graph(figure = fig)
    
    
    
    else:
        return None





@app.callback(Output('dropdown3', 'options'),[Input('dropdown1','value'),Input('dropdown2','value')])
def update_group( start_date, end_date ):

    reformed_data = call_data[ (call_data['date']>=start_date ) & (call_data['date']<=end_date)]
    
    group_list = reformed_data['Group'].unique().tolist()
    
    group_list = [ {"label" : i, "value": i }    for i in group_list]

    return group_list


    
# CALL ALL THE FUNCTIONS IN MAIN
def main():
    print('Start of the main function ')
    
    load_data()
    open_browser()
    
    
    global project_name
    project_name = 'CDR Analysis With Insights'
    
    global app
    app.layout = create_app_ui()
    app.title = project_name
    app.run_server()
    
    
    print('End of the main function ')  
    app = None
    global call_data,service_data,device_data, start_date_list,end_date_list,report_type
    call_data = None
    service_data = None
    device_data = None
    start_date_list = None
    end_date_list = None
    report_type= None
    
    
# MAIN CODE WHICH IS EXECUTED
if (__name__ == '__main__'):
    main()
    
    
    