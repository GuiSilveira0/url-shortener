from sqlalchemy import create_engine
from infrastructure.config import get_environment_variable
from sqlalchemy.orm import sessionmaker


env = get_environment_variable()

class MySqlConnectionHandler:
    def __init__(self) -> None:
        self.__engine = self.__create_database_engine()

    def __create_database_engine(self):
        engine = create_engine(env.DATABASE_URL)
        return engine
    
    def get_engine(self):
        return self.__engine
    
    def __enter__(self):
        session_maker = sessionmaker(bind=self.__engine)
        self.session = session_maker
        return self
    
    def __exit__(self):
        self.session.close()