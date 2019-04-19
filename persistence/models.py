from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship

from database import Base


class Station(Base):
    __tablename__ = 'stations'
    id5 = Column(String(5), primary_key=True)
    alt = Column(Integer)
    x = Column(Float)
    y = Column(Float)
    name = Column(String(50))  # , unique=True) not sure
    land = Column(String(120))

    def __repr__(self):
        return '<Station %r>' % (self.name)


class Measurement(Base):
    __tablename__ = 'measurements'
    id = Column(Integer, primary_key=True)
    station_id = Column(String, ForeignKey('stations.id5'), nullable=False)
    date = Column(Date, nullable=False)
    station = relationship("Station", backref="stations")
    QN_3 = Column(Float)
    FX = Column(Float)
    FM = Column(Float)
    QN_4 = Column(Float)
    RSK = Column(Float)
    RSKF = Column(Float)
    SDK = Column(Float)
    SHK_TAG = Column(Float)
    NM = Column(Float)
    VPM = Column(Float)
    PM = Column(Float)
    TMK = Column(Float)
    UPM = Column(Float)
    TXK = Column(Float)
    TNK = Column(Float)
    TGK = Column(Float)

    def __repr__(self):
        return '<Measurement %r %r>' % (self.station_id, self.date)
