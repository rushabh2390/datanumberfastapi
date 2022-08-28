from distutils.log import error
from sqlalchemy.orm import Session, joinedload
import services
import models
import schemas
from sqlalchemy.orm import load_only
from sqlalchemy import desc
import logging
logging.basicConfig(level=logging.DEBUG)


async def delete_or_update_months(db: Session, month_id):
    """delete day_checked and upon 0 day_checker delete month

    Args:
        db (Session): database instance
        month_id (_type_): id from months table
    """
    month_record = db.query(models.Months).filter(
        models.Months.id == month_id).first()
    if month_record:
        logging.debug("data found:", month_record)
        count = int(month_record.day_checked) - 1
        if count == 0:
            db.delete(month_record)
            db.commit()
        else:
            setattr(month_record, "day_checked", count)
            db.add(month_record)
            db.commit()
            db.refresh(month_record)
        return month_record
    logging.debug("No data found have month", month_id)
    return


async def create_or_update_months(db: Session, month: int):
    """create or increment day_checked for month

    Args:
        db (Session): database instance
    """
    month_record = db.query(models.Months).filter(
        models.Months.month == month).first()

    if month_record:
        logging.debug("data found:", month_record)
        count = int(month_record.day_checked) + 1
        setattr(month_record, "day_checked", count)
        db.add(month_record)
        db.commit()
        db.refresh(month_record)
    else:
        logging.debug("no month found adding month", month)
        month_record = models.Months(month=month, day_checked=1)
        db.add(month_record)
        db.commit()
        db.refresh(month_record)

    return month_record


async def fetch_all_dates(db: Session):
    """fetach all dates records from dates qlong with their month record.

    Args:
        db (Session): database instance

    Returns:
        _type_: return all date data along with their months
    """
    dates = db.query(models.Dates).options(
        (joinedload(models.Dates.month).load_only("month")), load_only("id", "day", "fact")).all()
    logging.debug("no of dates record found:", len(dates))
    return dates


async def create_dates(db: Session, dates_data: schemas.DatesIn):
    """create dates record  as well create month record(if not exists)

    Args:
        db (Session): database instance
        dates_record (schemas.DatesIn): date input in DatesIn schema

    Returns:
        _type_: return DatesResponse schema or error
    """
    description, error = await services.get_fact_from_number_Api_by_Month_n_date(month=dates_data.month, day=dates_data.day)
    if description:
        logging.debug("add month and dates records for", dates_data)
        month_record = await create_or_update_months(db, dates_data.month)
        dates_record = models.Dates(month_id=month_record.id,
                                    day=dates_data.day, fact=description)
        db.add(dates_record)
        db.commit()
        db.refresh(dates_record)
        dates_record_response = schemas.DatesResponse(
            day=dates_data.day, month=dates_data.month, fact=description)
        return dates_record_response, None
    if error:
        logging.error("Got error from calling service", error)
        return error


async def get_popular(db: Session):
    """return month records order by day_checked in descending order.

    Args:
        db (Session): database instance

    Returns:
        _type_: return month records
    """
    months = db.query(models.Months).order_by(
        desc(models.Months.day_checked)).all()
    logging.debug("no. of months record found", len(months))
    return months


async def delete_dates(db: Session, id: int):
    """delete the date record  as well update month records

    Args:
        db (Session): database instance

    Returns:
        _type_: Return deleted date record
    """
    logging.debug("delete dates records have id ", id)
    dates_record = db.query(models.Dates).filter(models.Dates.id == id).first()
    if dates_record:
        month_record = await delete_or_update_months(
            db, dates_record.month_id)
        db.delete(dates_record)
        db.commit()

    return dates_record
