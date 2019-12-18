#Import Flask, dependencies, sessions, basics like from titanic example

import numpy as numpy
import os

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify

#Setup database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Reflect database into new model
Base = automap_base()
base.prepare(engine, relfect=True)

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
        f"/api/v1.0/<start>` and `/api/v1.0/<start>/<end><br>"
    )

@app.route("/api/v1.0/precipitation")
#Communication session with database, Query Measurement database for date and prcp data.
session = Session(engine)
prcp_results = session.query(Mesurement.date, Measurement.prcp).all()

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


if __name__ == '__main__':
    app.run(debug=True)