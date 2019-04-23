import os

from flask import Flask, Response, json
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from init_db import init_db
from settings import DB_STRING

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = DB_STRING
db = SQLAlchemy(app)

CORS(app)


class Station(db.Model):
    __tablename__ = 'stations'
    id5 = db.Column(db.String(5), primary_key=True)
    alt = db.Column(db.Integer)
    x = db.Column(db.Float)
    y = db.Column(db.Float)
    name = db.Column(db.String(50))  # , unique=True) not sure
    land = db.Column(db.String(120))

    def __repr__(self):
        return '<Station %r>' % (self.name)

    @property
    def serialize(self):
        return {'id5': self.id5, 'name': self.name}


class Measurement(db.Model):
    __tablename__ = 'measurements'
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.String(5), db.ForeignKey('stations.id5'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    station = db.relationship("Station", backref="stations")
    QN_3 = db.Column(db.Float)
    FX = db.Column(db.Float)
    FM = db.Column(db.Float)
    QN_4 = db.Column(db.Float)
    RSK = db.Column(db.Float)
    RSKF = db.Column(db.Float)
    SDK = db.Column(db.Float)
    SHK_TAG = db.Column(db.Float)
    NM = db.Column(db.Float)
    VPM = db.Column(db.Float)
    PM = db.Column(db.Float)
    TMK = db.Column(db.Float)
    UPM = db.Column(db.Float)
    TXK = db.Column(db.Float)
    TNK = db.Column(db.Float)
    TGK = db.Column(db.Float)

    def __repr__(self):
        return '<Measurement %r %r>' % (self.station_id, self.date)


init_db(db, app)


@app.route('/api/stations', methods=['GET'])
def fetch_all_stations():
    all_stations = Station.query.all()
    res = [s.serialize for s in all_stations]
    return Response(json.dumps(res), mimetype='application/json')


@app.route('/api/variables', methods=['GET'])
def fetch_all_variables():
    all_variables = Measurement.__table__.c.keys()
    res = [{'variable_name': v} for v in all_variables if v not in ["id", "station_id", "date"]]
    return Response(json.dumps(res), mimetype='application/json')


@app.route('/api/measurements/<path:station_id>/<path:variable_name>', methods=['GET'])
def fetch_measurements(station_id, variable_name):
    measurements = Measurement.query.with_entities(Measurement.date, getattr(Measurement, variable_name)).filter_by(
        station_id=station_id)
    res = [{'date': m.date.strftime('%Y-%m-%d'), 'value': getattr(m, variable_name)} for m in measurements]
    return Response(json.dumps(res), mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=os.environ['PORT'])
