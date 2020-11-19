import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt


#################################################
# Database Setup
#################################################
# generate the engine to the correct sqlite file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# # Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)
Base.classes.keys()
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
#Create Session
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################

# Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "Welcome to my 'Home' page!"
@app.route("/about")
def about():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
       
    )   
# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
        # Convert the Query Results to a Dictionary Using `date` as the Key and `prcp` as the Value
        # Calculate the Date 1 Year Ago from the Last Data Point in the Database
        one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
        # Design a Query to Retrieve the Last 12 Months of Precipitation Data Selecting Only the `date` and `prcp` Values
        precipitation = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date >= one_year_ago).\
                order_by(Measurement.date).all()
        # Convert List of Tuples Into a Dictionary
        precipitation_list = dict(precipitation)
        # Return JSON Representation of Dictionary
        return jsonify(precipitation_list)

# Station Route
@app.route("/api/v1.0/stations")
def stations():
        # Return a JSON List of Stations From the Dataset
        stations_all = session.query(Station.station, Station.name).all()
        # Convert List of Tuples Into Normal List
        station_list = list(stations_all)
        # Return JSON List of Stations from the Dataset
        return jsonify(station_list)

# TOBs Route
@app.route("/api/v1.0/tobs")
def tobs():
        # Query for the Dates and Temperature Observations from a Year from the Last Data Point
        one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
        # Design a Query to Retrieve the Last 12 Months of Precipitation Data Selecting Only the `date` and `prcp` Values
        highest_temp_obs = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= one_year_ago).\
                order_by(Measurement.date).all()
        # Convert List of Tuples Into Normal List
        highest_temp_obs_list = list(highest_temp_obs)
        # Return JSON List of Temperature Observations (tobs) for the Previous Year
        return jsonify(highest_temp_obs_list)


# Define Main Behavior
if __name__ == '__main__':
    app.run(debug=True)