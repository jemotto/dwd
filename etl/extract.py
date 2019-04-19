import io
import logging.config
import os
import re
import urllib
from string import join
from zipfile import ZipFile

from etl.encoding import determine_encoding
from etl.settings import *

logging.config.fileConfig('etl/logging.conf')
log = logging.getLogger('extract')

if not os.path.exists('tmp'):
    os.makedirs('tmp')

filename, headers = urllib.urlretrieve(DWD_FTP_URL + DWD_STATIONS, ETL_FILE_TMP_DIR + DWD_STATIONS)
log.info('finished downloading stations file')

enc = determine_encoding(ETL_FILE_TMP_DIR + DWD_STATIONS)
log.info('finished determining stations file encoding')

with io.open(ETL_FILE_TMP_DIR + DWD_STATIONS, mode='r', encoding=enc) as stations_file:
    line = stations_file.readline()  # first line containg table headers
    line = stations_file.readline()  # second line containg dashes
    line = stations_file.readline()
    while line:
        if line == "":
            continue  # ignore empty lines
        spl = line.split()
        if len(spl) > 8:
            # print "sdf"
            spl[6] = join(spl[6:-1])
            # print spl
            spl[7] = spl[-1]
            # print spl
            spl = spl[:8]
        id5, from_date, to_date, alt, y, x, name, land = spl
        line = stations_file.readline()

log.info('finished parsing stations file')

log.info('loading ' + DWD_FTP_URL + dwd_station_zipfile(id5))


urllib.urlcleanup() # https://stackoverflow.com/questions/44733710/downloading-second-file-from-ftp-fails
filename, headers = urllib.urlretrieve(DWD_FTP_URL + dwd_station_zipfile(id5), ETL_FILE_TMP_DIR + id5 + '.zip')
with ZipFile(ETL_FILE_TMP_DIR + id5 + '.zip') as zip:
    for info in zip.infolist():
        if re.match(r'^produkt_klima_tag_.*\.txt$', info.filename):
            zip.extract(info, ETL_FILE_TMP_DIR)

            with io.open(ETL_FILE_TMP_DIR + info.filename, mode='r') as klima_file:
                line = klima_file.readline()  # first line containg table headers
                line = klima_file.readline()
                while line:
                    if line == "":
                        continue  # ignore empty lines
                    spl = [el.strip() for el in line.split(';')]
                    id, date, QN_3, FX, FM, QN_4, RSK, RSKF, SDK, SHK_TAG, NM, VPM, PM, TMK, UPM, TXK, TNK, TGK, eor = spl
                    line = klima_file.readline()
print SDK

os.remove(ETL_FILE_TMP_DIR + id5 + '.zip')
os.remove(ETL_FILE_TMP_DIR + info.filename)
