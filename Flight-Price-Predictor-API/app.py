from flask import Flask,request,jsonify
app = Flask(__name__)
from flask_cors import cross_origin
from flask_cors import CORS

import json
import pickle
import numpy as np
import pandas as pd

app.config['CORS_HEADER'] = 'application/json'
CORS(app,resources={r"/*":{"origins":"*"}})

__data_columns = None
__sources = None
__destinations = None
__airlines = None
__stopages = None
__model = None

def get_sources_val():
    return __sources
    
def get_destinations_val():
    return __destinations

def get_airlines_val():
    return __airlines

def get_stopages_val():
    return __stopages

def get_flight_price_val(departureDate,arrivalDate,source,destination,stopage,airlineName):

    
    date_dep = departureDate
    Journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
    Journey_month = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").month)
    print("Journey Date : ",Journey_day, Journey_month)


    Dep_hour = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").hour)
    Dep_min = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").minute)
    print("Departure : ",Dep_hour, Dep_min)


    date_arr = arrivalDate
    Arrival_hour = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").hour)
    Arrival_min = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").minute)
    print("Arrival : ", Arrival_hour, Arrival_min)


    Duration_hours = abs(Arrival_hour - Dep_hour)
    Duration_mins = abs(Arrival_min - Dep_min)
    print("Duration : ", Duration_hours, Duration_mins)

    Total_Stops = stopage
    print("Total_stops : ",Total_Stops)
    # X = data_train.loc[:, ['Total_Stops', 'Journey_day', 'Journey_month', 'Dep_hour',
    #    'Dep_min', 'Arrival_hour', 'Arrival_min', 'Duration_hours',
    #    'Duration_mins', 'Airline_Air India', 'Airline_GoAir', 'Airline_IndiGo',
    #    'Airline_Multiple carriers',
    #    'Airline_Multiple carriers Premium economy', 'Airline_SpiceJet',
    #    'Airline_Trujet', 'Airline_Vistara', 'Airline_Vistara Premium economy',
    #    'Source_Chennai', 'Source_Delhi', 'Source_Kolkata', 'Source_Mumbai',
    #    'Destination_Cochin', 'Destination_Delhi', 'Destination_Hyderabad',
    #    'Destination_Kolkata', 'Destination_New Delhi']]
    df_data = pd.DataFrame({'Total_Stops':[Total_Stops],'Journey_day':[Journey_day],
    'Journey_month':[Journey_month],'Dep_hour':[Dep_hour],'Dep_min':[Dep_min],
    'Arrival_hour':[Arrival_hour],'Arrival_min':[Arrival_min],'Duration_hours':[Duration_hours],
    'Duration_mins':[Duration_mins] })
    print(' df_data: ', df_data)
    df_one_hot = pd.get_dummies(pd.DataFrame({'Airline':[airlineName],'Source':[source],'Destination':[destination]}))
    print('Before df_one_hot: ', df_one_hot)
    print('Categorical Columns: ',__categorical_columns)
    df_one_hot = df_one_hot.reindex(columns = __categorical_columns,fill_value =0)
    print('After df_one_hot: ', df_one_hot)
    df_result = pd.concat([df_data,df_one_hot], axis=1)
    print('df_result: ',df_result.head())
    prediction = __model.predict(df_result)
    return round(prediction[0],2)


def get_flight_price_all(departureDate,arrivalDate,source,destination,stopage,airlineName):

    
    date_dep = departureDate
    Journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
    Journey_month = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").month)
    print("Journey Date : ",Journey_day, Journey_month)


    Dep_hour = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").hour)
    Dep_min = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").minute)
    print("Departure : ",Dep_hour, Dep_min)


    date_arr = arrivalDate
    Arrival_hour = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").hour)
    Arrival_min = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").minute)
    print("Arrival : ", Arrival_hour, Arrival_min)


    Duration_hours = abs(Arrival_hour - Dep_hour)
    Duration_mins = abs(Arrival_min - Dep_min)
    print("Duration : ", Duration_hours, Duration_mins)

    Total_Stops = stopage
    print("Total_stops : ",Total_Stops)
    # X = data_train.loc[:, ['Total_Stops', 'Journey_day', 'Journey_month', 'Dep_hour',
    #    'Dep_min', 'Arrival_hour', 'Arrival_min', 'Duration_hours',
    #    'Duration_mins', 'Airline_Air India', 'Airline_GoAir', 'Airline_IndiGo',
    #    'Airline_Multiple carriers',
    #    'Airline_Multiple carriers Premium economy', 'Airline_SpiceJet',
    #    'Airline_Trujet', 'Airline_Vistara', 'Airline_Vistara Premium economy',
    #    'Source_Chennai', 'Source_Delhi', 'Source_Kolkata', 'Source_Mumbai',
    #    'Destination_Cochin', 'Destination_Delhi', 'Destination_Hyderabad',
    #    'Destination_Kolkata', 'Destination_New Delhi']]
    df_data = pd.DataFrame({'Total_Stops':[Total_Stops],'Journey_day':[Journey_day],
    'Journey_month':[Journey_month],'Dep_hour':[Dep_hour],'Dep_min':[Dep_min],
    'Arrival_hour':[Arrival_hour],'Arrival_min':[Arrival_min],'Duration_hours':[Duration_hours],
    'Duration_mins':[Duration_mins] })
    print(' df_data: ', df_data)

    price_output_list = []
    for airline in __airlines:
        df_one_hot = pd.get_dummies(pd.DataFrame({'Airline':[airline],'Source':[source],'Destination':[destination]}))
        print('Before df_one_hot: ', df_one_hot)
        print('Categorical Columns: ',__categorical_columns)
        df_one_hot = df_one_hot.reindex(columns = __categorical_columns,fill_value =0)
        print('After df_one_hot: ', df_one_hot)
        df_result = pd.concat([df_data,df_one_hot], axis=1)
        print('df_result: ',df_result.head())
        prediction = __model.predict(df_result)
        prediction = round(prediction[0],2)
        ap = {'airline':airline,'predictedPrice':prediction}
        price_output_list.append(ap)
    print(price_output_list)
    return price_output_list

@app.before_first_request
def load_saved_artifacts():
    print("loading the artifacts...start")
    global __data_columns
    global __sources
    global __destinations
    global __airlines
    global __stopages
    global __categorical_columns
    global __model 

    with open("./artifacts/dropdown_values.json","r") as f:
        __data_columns = json.load(f)['data_columns']
        __destinations = [i.replace('Destination_','') for i in __data_columns  if i.startswith('Destination_')]
        __airlines = [i.replace('Airline_','') for i in __data_columns  if i.startswith('Airline_')]
        __sources = [i.replace('Source_','') for i in __data_columns  if i.startswith('Source_')]
        __stopages = [{'stop':'Non-Stop', 'value':0},
                      {'stop':'1 Stop','value':1},
                      {'stop':'2 Stop','value':2},
                      {'stop':'3 Stop','value':3}]

    with open("./artifacts/flight_rf.pkl",'rb') as f:
        __model = pickle.load(f)
    with open("./artifacts/categorical_columns.json","r") as f:
        __categorical_columns = json.load(f)['data_columns']
    print('loading the artifacts are done.')


@app.route('/hello')
def hello():
    return "Hello from flight prediction app"

@app.route('/getSources')
def get_sources():
    response= jsonify({
        'sources':get_sources_val()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getDestinations')
def get_destinations():
    response= jsonify({
        'destinations':get_destinations_val()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getAirlines')
def get_airlines():
    response= jsonify({
        'airlines':get_airlines_val()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getStopages')
def get_stopages():
    response= jsonify({
        'stopages':get_stopages_val()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/predictPrice', methods = ['POST'])
def get_flight_price():
    print(".............get price.........")
    req = request.get_json()
    print(request.get_json())
    #print(request.form['departureDate'])
    response= jsonify(
      get_flight_price_all(req["departureDate"],req["arrivalDate"],req["source"],req["destination"],req["stopage"],req["airlineName"])
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers['Content-Type'] = "application/json; charset=utf-8"
    response.status_code =200
    return response



if __name__ == "__main__":
    print('Starting Python Flask Server for Flight Price Prediction.....')
    #load_saved_artifacts()
    app.run(debug=True)