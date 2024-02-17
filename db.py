from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine('sqlite:///db.sqlite3')

Session = sessionmaker(bind=engine)

# 创建所有表
Base.metadata.create_all(engine)