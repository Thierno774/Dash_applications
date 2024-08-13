from dash import Dash, html, dcc, callback
from dash.dependencies import Input, Output
import plotly.graph_objs as go 
import pandas as pd 
from dash import dash_table as dt 
import plotly.express  as px 
import dash_daq as daq
import dash_auth

## Initialize value 

USERNAME_PASSWORD_PAIRS = [["Thierno", "test123"], ["paul", "test2"]]

sales = pd.read_csv("train.csv")
# Transform time series
sales['Order Date'] = pd.to_datetime(sales["Order Date"], format = "%d/%m/%Y")
sales["Year"] = sales["Order Date"].dt.year
sales['Month'] = sales["Order Date"].dt.month_name()

unique_segment = sales["Segment"].unique()
print(unique_segment)
unique_region = sales["Region"].unique()
print(unique_region)
year_values = sales["Year"].unique()
year_values = list(map(int, year_values))

year_values = sorted(year_values)

print(year_values)
app = Dash(__name__, meta_tags=[{"name" : "viewport", "content": "with=device-width"}])

## Dash authentication
auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)


year_slider =dcc.Slider(id = "select_year",
                        included = False,
                        updatemode="drag",
                        tooltip= {"always_visible": True},
                        min = 2015,
                        max = 2018, 
                        step = 1, 
                        value = 2016, 
                        marks = {str(year): str(year) for year in year_values}, 
                        className = "dcc_compon")


radios_subcategory = dcc.RadioItems(id = "subcategory", 
                                    labelStyle = {"display": "inline-block"},
                                                  value = "Corporate", 
                                                  options = [{"label": i, "value": i} for i in  unique_segment], 
                                                  style = {"text-align": "center", "color": "#3B16C4"}, className= "dcc_compon")

radios_subcategory1 = dcc.RadioItems(id = "radio_item1", 
                                     labelStyle = {"display": "inline-block"}, 
                                     value = "Region", 
                                     options = [{"label" : "Sub-Category", "value": "Sub-Category"},
                                                {"label": "Region", "value": "Region"}],
                                     style = {"text-align": "center", "color": "#3B16C4"}, className = "dcc_compon")


radio_state_city = dcc.RadioItems(id = "radio_state_city",
                                  labelStyle = {"display": "inline-block"}, 
                                  value = "State", 
                                  options = [{"label": "State", "value": "State"}, 
                                              {"label": "City", "value": "City"}],
                                  style = {"text-align": "center", "color": "#3B16C4"}, className = "dcc_compon")

def create_barplot_subCategory(year= 2016, segment = "Constumer", radio_items = "Region"): 
    # Filter data 
    sales1 = sales.groupby(['Year', 'Segment', 'Sub-Category'])['Sales'].sum().reset_index()
    sales2 = sales1[(sales1['Year'] == year) & 
                    (sales1['Segment'] == segment)].sort_values(by = ['Sales'], 
                                ascending = False).nlargest(5, columns = ['Sales'])
    
    ## G
    fig = go.Figure()

    fig.add_trace(go.Bar(x=sales2['Sales'],
                         y=sales2['Sub-Category'],
                         text = sales2["Sales"], 
                         texttemplate= "$" + '%{text:.2s}', 
                         textposition = "auto", 
                         orientation = "h",
                         marker = dict(color = "#19AAE1"), 
                         hoverinfo = "text", 
                         hovertext = "<b> Year</br>: " + sales2["Year"].astype(str) + "<br>"+ 
                                     "<b>Segment</b>: " + sales2["Segment"].astype(str) + "<br>"+ 
                                     "<b>Sub-Category</b>: " + sales2["Sub-Category"].astype(str) + "<br>"+
                                     "<b>Sales</b>: $" + [f"{x:,.2f}" for x in sales2["Sales"]] + "<br>"))
    
    fig.update_layout( plot_bgcolor  = "#BBF0E8 ", 
                      paper_bgcolor = "#BBF0E8 ", 
                     title = {
                         "text" : "Sales by sub-Category in year", 
                         "y" : 0.99, 
                         "x": 0.5, 
                         "xanchor" :"center",
                         "yanchor": "top"}, 
                     titlefont = {
                                "color": "#3B16C4", 
                                "size":12}, 
                     xaxis = dict(title="<br></b>", 
                                  color = "orange", 
                                  showline = True, 
                                  showgrid = True, 
                                  showticklabels = True, 
                                  linecolor = "orange"), 
                     yaxis = dict(title = "<b></b>", 
                                  autorange = "reversed", 
                                  color = "orange", 
                                  showline = False, 
                                  showgrid = False, 
                                  showticklabels = True, 
                                  linecolor = "orange",
                                  linewidth =1, 
                                  ticks = "outside", 
                                  tickfont = dict(
                                                family = "Arial",
                                                size = 12, 
                                                color = "orange")),
                     
                     legend = {
                                "orientation": "h",
                                "bgcolor": "#BBF0E8 ",
                                "x" : 0.5, 
                                "y": 1.25, 
                                "xanchor": "center", 
                                "yanchor": "top"}, 
                     font = dict(
                                family = "sans-serif",
                                size = 15, 
                                color = "#3B16C4"
                     )
                     
                     )

    return fig
# Create barplot with region 
def create_barplot_region(selected_year= 2016, segment = "Constumer", radio_items = "Region"): 
    # Filter data
    sales1 = sales.groupby(["Year", "Segment", "Region"])["Sales"].sum().reset_index()
    sales2 = sales1[(sales1['Year'] == selected_year) & (sales1["Segment"] == segment)].sort_values(by = ['Sales'], 
                                ascending = False).nlargest(5, columns = ['Sales'])
    
    fig = go.Figure()
    
    fig.add_trace (go.Bar( x= sales2["Sales"], 
                          y = sales2['Region'], 
                          text = sales2["Sales"], 
                          texttemplate= "$" +"%{text:.2s}", 
                          textposition= "auto", 
                          orientation = "h", 
                          marker = dict(color = "#19AAE1"), 
                          hoverinfo = "text", 
                          
                          hovertext = "<b> Year</b>:" + sales2["Year"].astype(str)+ "<br>"+
                                        '<b>Segment</b>: ' + sales2['Segment'].astype(str) + '<br>' +
                                        '<b>Sub-Category</b>: ' + sales2['Region'].astype(str) + '<br>' +
                                        '<b>Sales</b>: $' + [f'{x:,.2f}' for x in sales2['Sales']] + '<br>'
                                ))
    
    fig.update_layout(plot_bgcolor = "#BBF0E8 ", 
                      paper_bgcolor = "#BBF0E8 ", 
                      title = {
                         "text" : "Sales by Region in year" + " "+ str(selected_year), 
                         "y" : 0.99, 
                         "x": 0.5, 
                         "xanchor" :"center",
                         "yanchor": "top"},
                      titlefont = {
                          "color": "#3B16C4", 
                          "size":12
                      }, 
                      hovermode = "closest", 
                      margin = dict(t = 40, r= 0), 
                      
                      xaxis = dict(title = "<b></b>", 
                                   color = "orange", 
                                   showline = True, 
                                   showgrid = True, 
                                   showticklabels = True, 
                                   linecolor = "orange", 
                                   linewidth = 1,
                                   ticks = "outside", 
                                   tickfont = dict(
                                       family = "Arial", 
                                       size = 12, 
                                       color = "orange")),
                      yaxis = dict(title = "<b></b>", 
                                   autorange = "reversed", 
                                   color = "orange", 
                                   showline = False,
                                   showgrid = False, 
                                   showticklabels = True, 
                                   linecolor = "orange", 
                                   linewidth =1, 
                                   tickfont = dict(
                                                family = "Helvetica", 
                                                size = 12, 
                                                color = "orange")
                    
                    
                                    
                                )
                      
                      
                      
                      
                      
                      )

    return fig

# Create  function  for to plot the plot
def create_donut_chart(selected_year = 2016, selected_category = "Constumer"): 
    sales1 = sales.groupby(["Year", "Segment", "Category"])["Sales"].sum().reset_index()
    
    furniture_sales = sales1[(sales1["Year"] == selected_year) & 
                              (sales1["Segment"] == selected_category)  &
                              (sales1["Category"] == "Furniture")]["Sales"].sum()
    
    technology_sales = sales1[(sales1["Year"] == selected_year) &
                              (sales1["Segment"] == selected_category) &
                              (sales1["Category"] == "Technology")]["Sales"].sum()
    
    office_sales = sales1[(sales1["Year"] == selected_year) &
                          (sales1["Segment"] == selected_category) &
                              (sales1["Category"] == "Office Supplies")]["Sales"].sum()
    
    # Define labels and values for the pie chart
    labels = ["Furniture", "Office Supplies", "Technologies"]
    values = [furniture_sales, office_sales,office_sales, technology_sales]
    colors = ['#30C9C7', '#7A45D1', 'orange']
    
    # Figure instance 
    fig = go.Figure()
    
    # Add trace to the figure
    fig.add_trace(go.Pie( labels = labels,
                         values = values, 
                         marker = dict(colors = colors), 
                         hoverinfo = "label+value+percent", 
                         textinfo = "label+value", 
                         textfont = dict(size = 13), 
                         texttemplate = "%{label} <br>$%{value:.2f}", 
                         textposition = "auto", 
                         hole = 0.7, 
                         rotation = 160,
                         insidetextorientation = "radial"))
    
    fig.update_layout(plot_bgcolor = '#BBF0E8 ',
                paper_bgcolor = '#BBF0E8 ',
                hovermode = 'x',
                title = {
                    'text': 'Sales by Category in Year' + ' ' + str((selected_year)),

                    'y': 0.93,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                titlefont = {
                    'color': '#3B16C4',
                    'size': 15},
                legend = {
                    'orientation': 'h',
                    'bgcolor': '#BBF0E8 ',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.15},

                font = dict(
                    family = "sans-serif",
                    size = 12,
                    color = '#3B16C4')
            )
    return fig

# Create a baplot for region 
   

def create_barplot_state(selected_year= 2016, selected_segment = "Constumer", radio_items = "State"): 
    # Filter data 
    sales1 = sales.groupby(["Year", "Segment", "State"])["Sales"].sum().reset_index()
    sales1 = sales1[(sales1["Year"] == selected_year) &
                    (sales1["Segment"]== selected_segment)].sort_values(by = ["Sales"], ascending = False).nlargest(10, columns = ['Sales'])
    
    fig = go.Figure() 
    
    fig.add_trace (go.Bar(x = sales1["Sales"], 
                            y = sales1['State'], 
                            text = sales1["Sales"], 
                            texttemplate = "$" + "%{text:.2s}", 
                            textposition = "auto", 
                            orientation = "h", 
                            marker = dict(color = "#19AAE1"), 
                            hoverinfo = "text", 
                            hovertext = 
                                "<b>Year</b>:" + sales1["Year"].astype(str)+ "<br>"+
                                '<b>Segment</b>:'+ sales1['Segment'].astype(str) + '<br>' +
                                '<b>State</b>:'+ sales1['State'].astype(str) + '<br>' +
                                '<b>Sales</b>: $' + [f'{x:,.2f}' for x in sales1['Sales']] + '<br>'
                            
                            

    ))
    fig.update_layout(plot_bgcolor = "#BBF0E8 ", 
                      paper_bgcolor = "#BBF0E8 ",
                      title = {
                          "text": "Sales by State in Year "+ " " + str(selected_year), 
                          "y": 0.99, 
                          "x": 0.5, 
                          "xanchor": "center", 
                          "yanchor": "top"},
                      titlefont = {
                            "color": "#3B16C4",
                            "size": 12},
                      hovermode = "closest", 
                      margin = dict(l = 130, t = 40, r = 0), 
                      xaxis = dict(title = "<b></b>", 
                                   color = "orange", 
                                   showline = True, 
                                   showgrid = True, 
                                   showticklabels = True, 
                                   linecolor = "orange", 
                                   linewidth = 1, 
                                   ticks = "outside",
                                   tickfont = dict(
                                                family = "Arial", 
                                                size = 12, 
                                                color = "orange")
                                   ), 
                      yaxis = dict(title = "<b></b>", 
                                   autorange = "reversed", 
                                   showline = False,
                                   showgrid = False,
                                   showticklabels = True, 
                                   linecolor = "orange", 
                                   linewidth =1, 
                                   ticks = "outside", 
                                   tickfont = dict(
                                                family = "Arial", 
                                                size = 12, 
                                                color = "orange")
                                   ), 
                      
                      legend = {
                            "orientation": "h",
                            "bgcolor": "#F2F2F2", 
                            "x": 0.5, 
                            "y": 1.25, 
                            "xanchor": "center", 
                            "yanchor": "top"}
                      
                      )
    
    return fig
    

def create_barplot_city(selected_year= 2016, selected_segment = "Constumer", radio_items = "State"):
    # Filter data 
    sales1 = sales.groupby(["Year", "Segment", "City"])['Sales'].sum().reset_index()
    sales1 = sales1[(sales1["Year"] == selected_year) & (sales1["Segment"] == selected_segment)].sort_values(by = ["Sales"], ascending = False).nlargest(10, columns = ['Sales'])
    
    # Create a Bar plot instance
    fig = go.Figure()
    ## Add the figure 
    fig.add_trace(go.Bar(x = sales1["Sales"], 
                         y = sales1["City"], 
                         text = sales1["Sales"], 
                         texttemplate= "$"+ "%{text:.2s}", 
                         textposition = "auto", 
                         orientation = "h", 
                         marker = dict(color = "#19AAE1"), 
                         hoverinfo = "text", 
                         hovertext =
                         "<b>Year</b>:" + sales1["Year"].astype(str) + "<br>" +
                         "<b>Segment</b>: " + sales1["Segment"].astype(str) + "<br>" +
                         "<b>City</b>: " + sales1["City"].astype(str) + "<br>" +
                         "<b>Sales</b>: $" + [f'{x:,.2f}' for x in sales1["Sales"]] + "<br>"
                         
                         
                         
                         
                         
                         ))
    fig.update_layout(plot_bgcolor = "#BBF0E8 ", 
                      paper_bgcolor = "#BBF0E8 ",
                      title = {
                            "text": "Sales by city " + " " + str(selected_year), 
                            "y": 0.99, 
                            "x": 0.5, 
                            "xanchor": "center", 
                            "yanchor": "top"},
                      titlefont = {
                            "color": "#3B16C4", 
                            "size":12
                      }, 
                      hovermode = "closest", 
                      margin = dict(l = 130, t = 40, r = 0), 
                      xaxis = dict(title = "<b></b>", 
                                   color = "orange", 
                                   showline = True, 
                                   showgrid = True, 
                                   showticklabels = True,
                                   linecolor = "orange", 
                                   linewidth = 1, 
                                   ticks = "outside", 
                                   tickfont = dict(
                                                family = "Arial",
                                                size = 12, 
                                                color = "orange")),
                      
                      yaxis = dict(title = "<b></b>",
                                   autorange = "reversed", 
                                   showline = False, 
                                   showgrid = False, 
                                   showticklabels = True, 
                                   linecolor = "orange", 
                                   linewidth = 1, 
                                   ticks = "outside", 
                                   tickfont = dict(
                                        family = "Arial", 
                                                size = 12, 
                                                color = "orange")
                                   ), 
                      
                      legend = {
                                "orientation": "h",
                                "bgcolor": "#F2F2F2", 
                                "x": 0.5, 
                                "y": 1.25, 
                                "xanchor": "center", 
                                "yanchor": "top"},
                      
                      font = dict(
                                    family = "sans-serif",
                                    size = 12, 
                                    color = "#3B16C4"
                      )
                      
                                   
                            
                      
                            
                      )
    return fig


## Create a function for to plot scatter 

def create_scatter_plot(selected_year, selected_segment): 
    
    ## Filter data 
    sales1 = sales.groupby(["Year", "Segment", "Month"])["Sales"].sum().reset_index()
    sales1 = sales1[(sales1["Year"] == selected_year) & (sales1["Segment"] == selected_segment)]
    
    # create a figure instance
    fig = go.Figure() 
    fig.add_trace(go.Scatter( x = sales1["Month"],
                             y = sales1["Sales"],
                             name = "Sales", 
                             text = sales1["Sales"],
                             texttemplate = "%{text:.2s}", 
                             #mode = "markers+line+text", 
                            textposition = 'bottom left',
                            mode = 'markers+lines+text',

                             line = dict(width = 3, color = "orange"), 
                             marker = dict(size = 10, symbol = "circle", color = "#19AAE1", 
                                          line = dict(color = "#19AAE1", width = 2)),
                            hoverinfo = "text", 
                            hovertext = 
                                    "<b>Year</b>: "+ sales1["Year"].astype(str) + "<br>" + 
                                    "<b>Month</b>: "+ sales1["Month"].astype(str) + "<br>" + 
                                    "<b>Segment</b>: "+ sales1["Segment"].astype(str) + "<br>" + 
                                    "<b>Sales</b>: "+ [f"{x:.2f}" for x in sales1["Sales"]] + "<br>" 

                                    
    ))
    
    fig.update_layout(plot_bgcolor = "#BBF0E8 ", 
                      paper_bgcolor = "#BBF0E8 ", 
                      title = {
                          "text": "Sales Trend in year" + " " + str(selected_year), 
                          "y": 0.99, 
                          "x": 0.5, 
                          "xanchor": "center", 
                          "yanchor": "top"},
                      
                      titlefont= {
                                    "color": "#3B16C4", 
                                    "size": 15}, 
                      
                      hovermode = "closest",
                      margin = dict(t = 5, l =0, r = 0), 
                      xaxis = dict(title = "<b></b>", 
                                   visible = True, 
                                   color = "orange", 
                                   showline = True, 
                                   showgrid = False, 
                                   showticklabels = True,
                                   linecolor = "orange", 
                                   linewidth = 1, 
                                   ticks = "outside", 
                                   tickfont = dict(
                                            family = "Arial", 
                                            size = 12, 
                                            color = "orange")
                      ), 
                    legend = { "orientation": "h", 
                              "bgcolor": "#BBF0E8 ", 
                              "x": 0.5, 
                              "y": 1.25, 
                              "xanchor": "center", 
                              "yanchor": "top"}, 
                    
                    font = dict(
                                family = "sans-serif", 
                                size = 12, 
                                color = "#3B16C4"
                    )

                           
                                   
                      
                      )
    return fig


## create a bulbble chart
def create_bulbe_chart(selected_year, selected_segment):
    # Filter data 
    sales1 = sales.groupby(["Year", "Segment", "State", "City", "Month"])["Sales"].sum().reset_index()
    sales1 = sales[(sales["Year"] == selected_year) &(sales1["Segment"] == selected_segment)]
    # figure instance 
    fig = go.Figure() 
    fig.add_trace(go.Scatter(x = sales1["Month"], 
                             y = sales1["Sales"], 
                             text = sales1["City"], 
                             mode = "markers", 
                             marker = dict(size = sales1["Sales"] /200,
                                           color = sales1["Sales"], 
                                           colorscale = "HSV", 
                                           showscale = False, 
                                           line = dict(
                                                        color = "MediumPurple", 
                                                        width = 2
                                           )), 
                             hoverinfo= "text", 
                             hovertext = 
                             "<b>Year</b>: "+ sales1["Year"].astype(str) + "<br>" + 
                             "<b>Month</b>: "+ sales1["Month"].astype(str) + "<br>" + 
                             "<b>Segment</b>: "+ sales1["Segment"].astype(str) + "<br>" + 
                             "<b>State</b>: "+ sales1["State"].astype(str) + "<br>" + 
                             "<b>City </br>:" + sales1["City"].astype(str) + "<br>" + 
                             "<b>Sales</b>:" + [f"{x:,.0f}" for x in sales1["Sales"]] + "<br>" 
                             
    ))
    
    fig.update_layout(plot_bgcolor = "#BBF0E8 ", 
                      paper_bgcolor = "#BBF0E8 ", 
                      title = {
                          "text": "Sales Trend in year" + " " + str(selected_year),
                          "y": 0.99,
                          "x": 0.5, 
                          "xanchor": "center", 
                          "yanchor": "top"},
                      titlefont = {
                                "color": "#3B16C4", 
                                "size": 15},
                      margin = dict(t = 40, r = 0, l = 0), 
                      hovermode = "closest", 
                      xaxis = dict(title = "<b> </b>", 
                                   color = "orange", 
                                   showline = False, 
                                   showgrid = False, 
                                   showticklabels = True, 
                                   linecolor = "orange", 
                                   linewidth = 1, 
                                   ticks = "",
                                   tickfont = dict(
                                                family = "Arial", 
                                                size = 12, 
                                                color = "orange"
                                   )), 
                      yaxis = dict(title = "<b></b>", 
                                   color = "orange", 
                                   visible = True, 
                                   showline = False, 
                                   showgrid = True, 
                                   showticklabels = False, 
                                   linecolor = "orange", 
                                   linewidth = 1, 
                                   ticks = '', 
                                   tickfont = dict(
                                            family = "Arial",
                                            size = 12, 
                                            color = "orange"
                                   )), 
                      legend = {
                                "orientation": "h",
                                "bgcolor":"#F2F2F2", 
                                "x": 0.5, 
                                "y": 1.25, 
                                "xanchor": "center", 
                                "yanchor": "top"},
                      font = dict(
                             family = "sans-serif",
                             size = 12, 
                             color = "#3B16C4"
                      )
    )
                      
    
    return fig 






## run the application
app.layout =html.Div([
                html.Div([
                        html.Div([
                            html.Div([
                                html.H4("Sales Scorecard", style = {"margin-bottom": "0px", "color": "#3B16C4"})

                                
                            ])
                        ], className = "one third column", id = "title1"), 
                        html.Div([
                            html.P("Year", className = "fix_label", style = {"color": "#3B16C4"}), 
                            year_slider,
                        ], className = "one-half column", id = "title2"), 
                        html.Div([
                                html.P("Segment", className = "fix_label", style = {"color": "#3B16C4"}), 
                                radios_subcategory
                        ], className = "one-third column", id = "title3")
                ], id = "header", className = "row flex-display", style = {"margin-bottom": "25px"}),
                
                html.Div([
                        radios_subcategory1, 
                        dcc.Graph(id = "barplot_subcategory", 
                                  config = {"displayModeBar" : "hover"}, style = {"height": "350px"}),

                ], className = "create_container2 three columns", style = {"height": "400px"}), 
                
                html.Div([
                        dcc.Graph(id ="donut_chart", 
                                  config = {"displayModeBar" : "hover"}, style = {"height": "350px"}),
                ], className =  "create_container2 three columns", style = {"style": "400px"}), 
                html.Div([
                     
               html.Div([
                        radio_state_city, 
                        dcc.Graph(id = "barplot_state_city", 
                                  config = {"displayModeBar" : "hover"}, style = {"height": "350px"}),

                ], className = "create_container2 four columns", style = {"height": "400px"}), 
               
               html.Div([ 
                         "Cette partie est à completer"]), 
               
                ],className = "row flex-display"), 
            
            html.Div([
                html.Div([
                        dcc.Graph(id = "scatter_plot", 
                                  config = {"displayModeBar": "hover"}, style = {"height": "350px"})
                ], className =  "create_container2 three columns", style = {"style": "400px"}), 
                
                html.Div([
                    dcc.Graph(id = "bulbe_chart", 
                              config = {"displayModeBar": "hover"} , style = {"style": "350px"})
                ], className = "create_container2 three columns", style = {"style" : "350px"}), 
                html.Div([
                    dt.DataTable( id = "datatable", 
                                 columns = [{'name': i, 'id': i} for i in
                                    sales.loc[:, ['Order Date', 'Customer ID', 'Customer Name',
                                                  'Segment', 'City', 'State', 'Region',
                                                  'Category', 'Sub-Category', 'Product Name',
                                                  'Sales', 'Year', 'Month']]],
                                 sort_action = "native", 
                                 sort_mode = "multi", 
                                 virtualization= True, 
                                 style_cell = {"textAlign": "left", 
                                               "min_width" : "100px", 
                                                "backgroundColor": "#BBF0E8 " , 
                                                "color": "#FEFEFE", 
                                                "border-bottom" : "0.01rem solid #19AAE1"
                                     
                                 }, 
                                 style_as_list_view=True, 
                                 style_header = {
                                      "backgroundColor": "#BBF0E8 ", 
                                      "color": "#FEFEFE", 
                                      "fontWeight": "bold", 
                                      "font": "Lato, sans-serif", 
                                      "color": "orange", 
                                      "border": "#BBF0E8 ",
                                 }, 
                                 style_data = {"textOverflow" : "hidden", "color": "#3B16C4"}, 
                                 fixed_rows = {"headers": True}, 
                                 )
                ], className = "create_container2 three columns")
            ])
                
])        








@callback(Output("barplot_subcategory", "figure"), 
          [Input("select_year", "value"), 
           Input("subcategory", "value"), 
           Input("radio_item1", "value")])
def update_graph(selected_year, selected_segment, radio_items): 
    if radio_items == "Sub-Category":
        return create_barplot_subCategory(selected_year, selected_segment)
    elif radio_items == "Region": 
        return create_barplot_region(selected_year, selected_segment, radio_items)
    

@callback(Output("donut_chart", "figure"), 
          [Input("select_year", "value"), 
           Input("subcategory", "value")])
def update_donut_chart (selected_year, selected_segment): 
    return create_donut_chart(selected_year, selected_segment)


@callback(Output("barplot_state_city", "figure"), 
          [Input("select_year", "value"), 
           Input("subcategory", "value"), 
           Input("radio_state_city", "value")])
def update_barplot_state_city(selected_year, selected_segment, radio_items):
    if radio_items == "State": 
        return create_barplot_state(selected_year, selected_segment, radio_items)
    elif radio_items == "City":
        return create_barplot_city(selected_year, selected_segment, radio_items)
        

@callback(Output("scatter_plot", "figure"), 
          [Input("select_year", "value"), 
           Input("subcategory", "value")])
def update_scatter_plot(selected_year, selected_segment): 
    return create_scatter_plot(selected_year, selected_segment)

@callback(Output("bulbe_chart", "figure"), 
          [Input("select_year", "value"), 
           Input("subcategory", "value")])

def update_bulbe_chart(selected_year, selected_segment):
    return create_bulbe_chart(selected_year, selected_segment)


@callback(
    Output("datatable", "data"), 
   [Input("select_year", "value"), 
    Input("subcategory", "value")]
   )
def display_table(selected_year, selected_segment):
    data_table = sales[(sales['Year'] == selected_year) & (sales['Segment'] == selected_segment)]
    return data_table.to_dict('records')

if __name__ == "__main__":
    app.run_server(debug=True, port = 5000)

