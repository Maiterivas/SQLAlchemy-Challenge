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
stations = Base.classes.station
measurements = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to my Hawaii SQLAlchemy Challenge! This page will offer some analysis on Hawaii weather to help plan a great vacation.<br/>"
        f"<br/>"
        f"Please see the web directory below for help navigating the page:<br/>"
        f"Precipitation Data with Dates:"
        <a href=\"/api/v1.0/precipitation<a><br/>"
        f"Stations and Names:"
        <a href=\"/api/v1.0/stations<a><br/>"
        f"Temperature Observations (1 yr from the last data point):"
        <a href=\"/api/v1.0/tobs<a><br/>"
        f"Minimum, Average, and Maximum Temperatures for Inputted Start Date('YYYY-MM-DD'):"
        <a href=\"/api/v1.0/<start><a><br/>"
        f"Minimum, Average, and Maximum Temperatures for Inputted Start and End Date('YYYY-MM-DD'/'YYYY-MM-DD'):"
        <a href=\"/api/v1.0/<start>/<end><a>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return precipitation for the last year in the data"""
    # Query all passengers
    results = session.query(Passenger.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of Hawaii stations"""
    # Query all passengers
    results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_passengers = []
    for name, age, sex in results:
        passenger_dict = {}
        passenger_dict["name"] = name
        passenger_dict["age"] = age
        passenger_dict["sex"] = sex
        all_passengers.append(passenger_dict)
        
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature observations"""
    # Query all passengers
    results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

    session.close()
        
    
@app.route("/api/v1.0/<start>")
def starttemps():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

    session.close()

@app.route("/api/v1.0/<start>/<end>")
def startendtemps():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()
    

if __name__ == '__main__':
    app.run(debug=True)
