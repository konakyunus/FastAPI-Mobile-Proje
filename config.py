from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


#DATABASE_URL = 'postgresql://postgres:%402013Drk.@test.parantezcrm.com:5432/parantez_dev'
DATABASE_URL = 'postgresql://postgres:postgres@localhost:5432/Deneme'


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush = False, bind=engine)
Base = declarative_base()

#def get_db():
    #db=SessionLocal()
    #try:
     #yield db
    #except:
     #db.close()

