import io
import logging.config
import os
import re
import urllib
from datetime import datetime
from string import join
from zipfile import ZipFile

# from backend.app.settings import DB_FILE
from encoding import determine_encoding
from settings import *
from backend.app.timelines import db, Station, Measurement

logging.config.fileConfig('backend/etl/logging.conf')
log = logging.getLogger('extract')

# drop database and start over
# os.remove(DB_FILE)

if not os.path.exists(tmp()):
    os.makedirs(tmp())

log.info('downloading main stations file')
filename, headers = urllib.urlretrieve(DWD_FTP_URL + DWD_STATIONS, tmp(DWD_STATIONS))

log.info('determining main stations file encoding')
enc = determine_encoding(tmp(DWD_STATIONS))

published_id5s = set()  # hashset

log.info('listing remote directory')
urllib.urlcleanup()  # https://stackoverflow.com/questions/44733710/downloading-second-file-from-ftp-fails
filename, headers = urllib.urlretrieve(DWD_FTP_URL, tmp('ls'))
with io.open(tmp('ls'), mode='r', encoding=enc) as ls_file:
    line = ls_file.readline()
    while line:
        if line == "":
            continue  # ignore empty lines
        if re.match(r'.*\.zip$', line):
            published_id5s.add(line.split()[-1][14:19])
        line = ls_file.readline()


# takes about 6min
log.info('pulling data per each id5 when file was published')
with io.open(tmp(DWD_STATIONS), mode='r', encoding=enc) as stations_file:
    line = stations_file.readline()  # first line containg table headers
    line = stations_file.readline()  # second line containg dashes
    line = stations_file.readline()
    progress_count = 0
    while line:
        if line == "":
            continue  # ignore empty lines
        spl = line.split()
        if len(spl) > 8:
            spl[6] = join(spl[6:-1])
            spl[7] = spl[-1]
            spl = spl[:8]
        id5, from_date, to_date, alt, y, x, name, land = spl
        station = Station(id5=id5, alt=alt, x=x, y=y, name=name, land=land)
        db.session.add(station)

        if id5 in published_id5s:
            log.debug('loading ' + DWD_FTP_URL + dwd_station_zipfile(id5))
            urllib.urlcleanup()  # https://stackoverflow.com/questions/44733710/downloading-second-file-from-ftp-fails
            filename, headers = urllib.urlretrieve(DWD_FTP_URL + dwd_station_zipfile(id5), tmp(id5 + '.zip'))
            log.debug('loaded ' + DWD_FTP_URL + dwd_station_zipfile(id5))
            with ZipFile(tmp(id5 + '.zip')) as zip:
                for info in zip.infolist():
                    if re.match(r'^produkt_klima_tag_.*\.txt$', info.filename):
                        zip.extract(info, tmp())

                        with io.open(tmp(info.filename), mode='r') as klima_file:
                            kline = klima_file.readline()  # first line containg table headers
                            kline = klima_file.readline()
                            while kline:
                                if kline == "":
                                    continue  # ignore empty lines
                                spl = [el.strip() for el in kline.split(';')]
                                station_id, date, QN_3, FX, FM, QN_4, RSK, RSKF, SDK, SHK_TAG, \
                                NM, VPM, PM, TMK, UPM, TXK, TNK, TGK, eor = spl

                                measurement = Measurement(station_id=id5,
                                                          date=datetime.strptime(date, "%Y%m%d").date(),
                                                          QN_3=QN_3, FX=FX,
                                                          FM=FM, QN_4=QN_4, RSK=RSK, RSKF=RSKF, SDK=SDK,
                                                          SHK_TAG=SHK_TAG, NM=NM, VPM=VPM, PM=PM, TMK=TMK,
                                                          UPM=UPM, TXK=TXK, TNK=TNK, TGK=TGK)
                                db.session.add(measurement)
                                kline = klima_file.readline()
            log.debug('deleting tmp station file of id5:' + id5)
            os.remove(tmp(id5 + '.zip'))
            os.remove(tmp(info.filename))
            log.debug('deleted tmp station file of id5:' + id5)
            progress_count += 1
            if progress_count % 50 == 0:
                log.info(str(progress_count) + ' files extracted')
        else:
            log.debug("ommitting nonpublished id5: " + id5)
        line = stations_file.readline()
db.session.commit()
log.info('deleting main stations file')
