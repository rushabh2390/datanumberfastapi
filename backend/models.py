from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship, deferred


class Months(Base):
    __tablename__ = 'months'

    id = deferred(Column(Integer, primary_key=True, index=True))
    month = Column(Integer)
    day_checked = Column(Integer)
    dates = relationship("Dates",  back_populates="month")


class Dates(Base):
    __tablename__ = 'dates'

    id = Column(Integer, primary_key=True, index=True)
    day = Column(Integer)
    fact = Column(String)
    month_id = Column(Integer, ForeignKey("months.id"))

    month = relationship("Months",  back_populates="dates")
