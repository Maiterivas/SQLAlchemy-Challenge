import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Creating engine for existing database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table station and classes
Stations = Base.classes.station
Measurements = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#Change and define start and end dates for queries
start_date = '2016-08-23'
end_date = '2017-08-24'
#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to Maite Rivas's Hawaii SQLAlchemy Challenge! This page will offer some analysis on Hawaii weather to help plan a great vacation.<br/>"
        f"<br/>"
        f"Please see the web directory below for help navigating the page:<br/>"
        f"- Precipitation Data (inches) and Dates: "
        f"/api/v1.0/precipitation <br/>"
        f"- Stations and Location Names: "
        f"/api/v1.0/stations<br/>"
        f"- Temperature Observations (Most Active Station: USC00519281, 12 months of most recent data): "
        f"/api/v1.0/tobs<br/>"
        f"- Minimum, Average, and Maximum Temperatures for Inputted Start Date('YYYY-MM-DD'): "
        f"/api/v1.0/{start_date}<br/>"
        f"- Minimum, Average, and Maximum Temperatures for Inputted Start and End Date('YYYY-MM-DD'/'YYYY-MM-DD'): "
        f"/api/v1.0/{start_date}/{end_date}<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return precipitation the data in a dictionary"""
    # Query all precipitation data 
    sel = [Measurements.date, Measurements.prcp]
    results = session.query(*sel).all()
    
    session.close()

    # (not needed) Convert list of tuples into normal list ex: all_names = list(np.ravel(results))
    precipitation = []

    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
    
        precipitation.append(precipitation_dict)

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of Hawaii stations"""
    # Query all Hawaii stations
    sel = [Stations.station, Stations.name]
    results = session.query(*sel).all()

    session.close()

    # Create a dictionary from data and append to a list
    stations_list = []
    for station, name in results:
        stations_dict = {}
        stations_dict["station"] = station
        stations_dict["name"] = name
        
        stations_list.append(stations_dict)
    
    return jsonify(stations_list)
        
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature observations from most active station during 1 year"""
    # Query temperature observations
    sel = [Measurements.date, Measurements.tobs]
    results = session.query(*sel).\
        filter(Measurements.station == 'USC00519281').\
        filter(Measurements.date >= start_date).\
        group_by(Measurements.date).all()

    session.close()
    
    #Create a dictionary from the data and append to a list
    tobs_list = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs

        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

@app.route(f"/api/v1.0/{start_date}")
def startdate():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of MIN, MAX, AVG for temps during given start date"""
    # Query all min, max, and average temps for given start date
    sel = [Measurements.station, func.min(Measurements.tobs), func.max(Measurements.tobs), func.avg(Measurements.tobs)]
    results = session.query(*sel).\
        filter(Measurements.date >= start_date).\
        group_by(Measurements.station).all()

    session.close()
    
    #Initialize list and append to dictionary with elements
    start_list = []
    start_dict = {}
    for station, min, max, avg in results:
        start_dict["station"] = station
        start_dict["min"] = min
        start_dict["max"] = max
        start_dict["avg"] = avg

        start_list.append(start_dict)

    return jsonify(start_list)


@app.route(f"/api/v1.0/{start_date}/{end_date}")
def startenddate():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of MIN, MAX, AVG for temps during given start and end date"""
    # Query all max, min, avg temps for a given start and end date
    sel = [Measurements.station, func.min(Measurements.tobs), func.max(Measurements.tobs), func.avg(Measurements.tobs)]
    results = session.query(*sel).\
        filter(Measurements.date >= start_date).\
        filter(Measurements.date <= end_date).\
        group_by(Measurements.station).all()

    session.close()
    
    #Initialize list and append to dictionary with elements
    start_end_list = []
    start_end_dict = {}
    for station, min, max, avg in results:
        start_end_dict["station"] = station
        start_end_dict["min"] = min
        start_end_dict["max"] = max
        start_end_dict["avg"] = avg

        start_end_list.append(start_end_dict)

    return jsonify(start_end_list)

if __name__ == '__main__':
    app.run(debug=True)
