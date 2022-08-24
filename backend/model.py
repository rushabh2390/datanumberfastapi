from sqlalchemy import Column, DateTime, Integer, String


from .database import Base



class Dates(Base):
    __tablename__ = 'dates'
    id = Column(Integer, primary_key=True, index=True)
    month = Column(Integer)
    day = Column(Integer)
    fact = Column(String)
    day_checked = Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
