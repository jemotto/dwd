DWD_FTP_SERVER = 'ftp-cdc.dwd.de'
DWD_FTP_DIR = '/pub/CDC/observations_germany/climate/daily/kl/recent/'
DWD_FTP_URL = 'ftp://' + DWD_FTP_SERVER + DWD_FTP_DIR
DWD_STATIONS = 'KL_Tageswerte_Beschreibung_Stationen.txt'


def dwd_station_zipfile(station_id):
    return 'tageswerte_KL_' + station_id + '_akt.zip'


ETL_FILE_TMP_DIR = 'tmp/'


def tmp(filename = ''):
    return ETL_FILE_TMP_DIR + filename
