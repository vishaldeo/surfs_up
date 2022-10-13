import datetime as dt
import numpy as np
import pandas as pd
from flask import Flask
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


#################################################
# Database Setup
#################################################


# Save reference to the table
# Passenger = Base.classes.passenger

#
engine = create_engine("sqlite:///hawaii.sqlite")
#
Base = automap_base()
# # reflect the database
Base.prepare(engine, reflect=True)
# #
Measurement = Base.classes.measurement
Station = Base.classes.station

 # create a session link from Python to our database
session = Session(engine)
# results = session.query(Measurement.station).all()
# print(results)

app = Flask(__name__)


@app.route('/')

def welcome():
    return(
    '''
<!DOCTYPE html>
<html>

<body>
    <h1>    Welcome to the Climate Analysis API! </h1>
    <h2>    Available Routes: </h2>
    <h3>        /api/v1.0/precipitation    </h3>
    <h3>        /api/v1.0/stations   </h3>
    <h3>        /api/v1.0/tobs   </h3>
    <h3>        /api/v1.0/temp/start/end    </h3>





</body>

</html>

    ''')


@app.route("/api/v1.0/precipitation")
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)


@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(  stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

if __name__ == "__main__":
    print("example is being run directly.")
else:
    print("example is being imported")
