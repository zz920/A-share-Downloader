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
                obj.metadata.create_all(self._connection)

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
                model.metadata.create_all(self._connection)

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


