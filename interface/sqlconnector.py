import logging
import sqlalchemy as sql


class SqlConnector():

    def __init__(self, URL=None):

        """
        # SqlConnector provide an interface of user database
        #
        # Parameter:
        #   URL : string | sql URL
        """
        self._connection = sql.create_engine(URL)
        self._DBsession = sql.orm.sessionmaker(bind=self._connection)

    def push_object(self, obj=None):

        """
        # push single sqlalchemy object to db
        #
        # Parameter:
        #   obj : sqlalchemy mapped class | data
        #
        # return:
        #   operation success status : boolean
        """

        if obj is not None:
            try:
                session = self._DBsession()
                session.add(obj)
                session.commit()
                session.close()

            except Exception as e:
                logging.error("SQLError: %s" % e)
            else:
                return True

        return False

    def push_frame(self, model=None, obj=None):

        """
        # push amount of sqlalchemy objects to db
        #
        # Parameter:
        #   model : sqlalchemy mapped class | insert data as model
        #   obj : list of dict | data
        #
        # return:
        #   operation success status : boolean
        """

        if obj is not None:
            if model is None or not isinstance(obj, list):
                logging.error("ValueError: model class or obj invalid.")
                return False
            try:
                session = self._DBsession()
                session.execute(
                    model.__table__.insert(),
                    obj
                )
                session.commit()
                session.close()
            except Exception as e:
                logging.error("SQLError: %s" % e)
            else:
                return True
        return False

    def copy_csvfile(self, table, filepath):

        """
        # To increase the speed, use copy method to insert a cvs file into the
        # table. 5M trade recoders take about 40s.
        #
        # Parameter:
        #   table : string | data table name
        #   filepath : string | csv file path
        #
        # return:
        #   operation success status : boolean
        """

        try:
            session = self._DBsession()
            _query = "COPY {} (time, price, volume, amount, type, date) FROM '{}' with csv header".format(
                table, filepath)
            session.execute(_query)
            session.commit()
            session.close()
        except Exception as e:
            logging.error("SQLError: %s" % e)
        else:
            return True
        return False

    def create_table(self, model):

        try:
            model.metadata.create_all(self._connection)
        except Exception as e:
            logging.error("SQLError: %s" % e)

