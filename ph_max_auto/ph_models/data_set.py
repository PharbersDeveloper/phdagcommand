import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Float


Base = declarative_base()


class DataSet(Base):
    __tablename__ = 'dataSet'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    parent = Column(String, default='{}')
    child = Column(String, default='{}')
    blockDs = Column(String)
    job = Column(String)
    sampleData = Column(String, default='{}')
    name = Column(String)
    schema = Column(String, default='{}')
    source = Column(String)
    storeType = Column(String, default='parquet')
    size = Column(Float)
    created = Column(DateTime, default=datetime.now())
    modified = Column(DateTime, default=datetime.now())
    description = Column(String)
    url = Column(String)
    tabName = Column(String)
    status = Column(String)
    mart = Column(String)
    assetDs = Column(String)
    colNames = Column(String, default='{}')
    length = Column(Float)

    def __repr__(self):
        return str(self.__dict__)


if __name__ == '__main__':
    ds = DataSet(id="id", parent="{}", child="{}", blockDs="blockDs", job="job", sampleData="{}",
                 name="name", schema="{}", source="source", storeType="storeType", size=0,
                 created=datetime.now(), modified=datetime.now(), description="description", url="url",
                 tabName="tabName", status="status", mart="mart", assetDs="assetDs", colNames="{}", length=0)
    print(ds)
