import time

from sqlalchemy.exc import OperationalError


def init_db(db, app):
    max_retries = 20
    for iterator in range(max_retries):
        try:
            db.create_all()
            return
        except OperationalError as oe:
            app.logger.info('retrying connection to mysql server for the ' + str(iterator) + " time")
            if 'Can\\\'t connect to MySQL server on ' in oe.message:
                time.sleep(5)
            else:
                raise oe
    raise Exception("Reached " + str(max_retries) + " retries and did not manage to connect to DB:(")
