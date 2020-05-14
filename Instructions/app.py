import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=True)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate App API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation(): 


    """Return JSON precipitation data"""
    #Retrieve last date from data
    lastDate = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    lastDate = lastDate[0]

    #Find date 1 year prior to last date
    #Retrieve precip. data and create dictionary to return as JSON dict
    date = dt.datetime(2016, 8, 23)
    oneYearAgo = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= date).all()
    prcp_dict = dict(oneYearAgo)

    #Return JSON data
    return jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def stations():


    """Return list of stations"""
    #Retrieve station data from engine
    station_results = session.query(Measurement.station).group_by(Measurement.station).all()


    #Convert data into list
    stationList = list(np.ravel(station_results))

    #Return JSON data
    return jsonify(stationList)


@app.route("/api/v1.0/tobs")
def tobs():

    #Retrieve list of TOBS for the last yeea, convert to dict 
    date = dt.datetime(2016, 8, 23)
    tobsResult = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= date).all()
    tobsDict = dict(tobsResult)

    #Return JSONified data 
    return jsonify(tobsDict)




@app.route("/api/v1.0/start")
def start():


    """Return a JSON dict for the min, max, or average temperature for a specified start date."""
    
    #Pull data from engine for dates after start date specified
    startData = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
    
    #Convert data list into dict
    startDict=dict(startData)
    
    #Return JSONified data 
    return jsonify(startDict)





@app.route("/api/v1.0/start/end")
def start_end():


    """Return a JSON list for the min, max, or average temperature for a specified date range."""
    
    #Pull data for dates range specified
    rangeData = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()
    
    #Convert data list into dict
    rangeDict=list(rangeData)
    
    #Return JSONified data
    return jsonify(rangeDict)


if __name__ == "__main__":
    app.run(debug=True)