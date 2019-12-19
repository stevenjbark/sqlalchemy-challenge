#Import Flask, dependencies, sessions, basics like from titanic example

import numpy as numpy
import os

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#Setup database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Reflect database into new model
Base = automap_base()
Base.prepare(engine, reflect=True)

#Save reference variables to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#Flask
app = Flask(__name__)

#Flask routes
@app.route("/")
def welcome():
#List all routes available
    return(
        f"Available Routes:<br><br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/temp_calculator/START_DATE/END_DATE<br>"
        f"For temp_calculator, enter the following formatting: /api/v1.0/temp_calculator/START_DATE/END_DATE in 'YYY-MM-DD'<br>"
        f"If no END_DATE is specified, the end date is last entry in database: 2017-08-23.<br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    #Communication session with Measurement database, query Measurement database for date and prcp data.
    session = Session(engine)
    prcp_results = session.query(Measurement.date, Measurement.prcp).all()

    #Close session
    session.close()

    #Create dictionary of Measurement.date key and Measurement.prcp value
    precipitation = []
    for p in prcp_results:
        p_dict = {}
        p_dict["date"] = p.date
        p_dict["prcp"] = p.prcp
        precipitation.append(p_dict)

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():

    #Communication session with Stations database, query for stations. 
    session = Session(engine)
    station_results = session.query(Station.station).all()

    #Close session
    session.close()

    #Create unique list for stations in query by set, not using a dictionary which would also work.
    station_list = []
    for l in station_results:
        station_list.append(l)
        final_stations = list(set(station_list))

    return jsonify(final_stations)    

@app.route("/api/v1.0/tobs")
def temperature():

    #Communication session with Measurement database, query for date and tobs after 2016-08-23
    session = Session(engine)
    temp_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>="2016-08-23")

    #Close session
    session.close()

    #Like above, create dictionary of date and observed temperature for past year
    temp_list = []
    for t in temp_results:
        t_dict = {}
        t_dict["date"] = t.date
        t_dict["tobs"] = t.tobs
        temp_list.append(t_dict)

    return jsonify(temp_list)

@app.route("/api/v1.0/temp_calculator/<start_date>/<end_date>")
def ave_temp(start_date,end_date="2017-08-23"):

    #Communication session with Measurement database for temperature data over start and end dates
    session = Session(engine)

    #Query based on start and start/end dates. Uses func capabilities for calculations inside sqlalchemy session.query.
    temp_calcs = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
           filter(Measurement.date >= start_date).filter(Measurement.date <= end_date)

    calc_list = []
    for c in temp_calcs:
        calc_list.append(c)

    #Returns final list for max, min, and average temps, start date.
    return jsonify(calc_list, f"Start Date: {start_date}", f"End Date: {end_date}")

    
if __name__ == '__main__':
    app.run(debug=True)