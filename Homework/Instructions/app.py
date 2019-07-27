import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import numpy as np
import pandas as pd
from flask import Flask, jsonify

###########################################
# Setup Database
###########################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

#Create references to Measurement and Station tables

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

####################################
# Setup Flask app
####################################
app = Flask(__name__)

################################
#Setup Flask Routes
################################

@app.route("/")
def homepage():
    
    return(
       
        f"/api/v1.0/precipitation<br/>"
        f" This route will query the precipitation data for the past year within the data showing date and precipitation. <br/>"

        f"/api/v1.0/stations<br/>"
        f" This route will return all the stations in a JSON format. <br/>"

        f"/api/v1.0/tobs<br/>"
        f" This will return a JSON result of temperature observations for the previous year.<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    precipitation_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").\
        filter(Measurement.date <= "2017-08-23").all()

    precipitation_data_json = [precipitation_data]

    return jsonify(precipitation_data_json)

@app.route("/api/v1.0/stations")
def stations():
    
    stations = session.query(Station.name, Station.station, Station.elevation, Station.latitude, Station.longitude).all()

    station_json = [stations]
    
    return jsonify(station_json)
    

@app.route("/api/v1.0/tobs")
def temp_data():
    
    temp_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= "2016-08-23").\
        filter(Measurement.date <= "2017-08-23").all()

    temp_data_json = [temp_data]

    return jsonify(temp_data_json)


if __name__ == '__main__':
    app.run(debug=True)