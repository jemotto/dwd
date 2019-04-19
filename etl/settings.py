DWD_FTP_URL = 'ftp://ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/daily/kl/recent/'
DWD_STATIONS = 'KL_Tageswerte_Beschreibung_Stationen.txt'

def dwd_station_zipfile(station_id):
    return 'tageswerte_KL_' + station_id + '_akt.zip'

ETL_FILE_TMP_DIR = 'tmp/'