from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


class Connection:
    def __init__(self, user, pwd, host, db):
        self.user = user
        self.pwd = pwd
        self.db = db
        self.host = host

        self.connection_string = \
            'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.\
                format(user=self.user, pw=self.pwd, url=self.host, db=self.db)

        self.engine = create_engine(self.connection_string, echo=False)

    def session(self) -> Session:

        session = sessionmaker(bind=self.engine)

        return session()
