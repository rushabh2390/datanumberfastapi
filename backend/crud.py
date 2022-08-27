from sqlalchemy.orm import Session, joinedload

import models
import schemas
from sqlalchemy.orm import load_only
from sqlalchemy import desc


def create_or_update_months(db: Session, month: int):
    """_summary_

    Args:
        db (Session): _description_
    """
    month_record = db.query(models.Months).filter(
        models.Months.month == month).first()

    if month_record:
        count = int(month_record.day_checked) + 1
        setattr(month_record, "day_checked", count)
        db.add(month_record)
        db.commit()
        db.refresh(month_record)
    else:
        month_record = models.Months(month=month, day_checked=1)
        db.add(month_record)
        db.commit()
        db.refresh(month_record)
        return month_record

    return month_record


def fetch_all_dates(db: Session):
    """_summary_

    Args:
        db (Session): _description_

    Returns:
        _type_: _description_
    """
    # dates = db.query(models.Dates, models.Months).options(
    #     load_only("id", "month", "day", "fact")).all()
    dates = db.query(models.Dates).options(
        (joinedload(models.Dates.month).load_only("month")), load_only("id", "day", "fact")).all()
    return dates


def create_dates(db: Session, dates_data: schemas.DatesResponse):
    """_summary_

    Args:
        db (Session): _description_
        dates_data (schemas.DatesResponse): _description_

    Returns:
        _type_: _description_
    """
    month_record = create_or_update_months(db, dates_data.month)

    dates_record = models.Dates(month_id=month_record.id,
                                day=dates_data.day, fact=dates_data.fact)
    db.add(dates_record)
    db.commit()
    db.refresh(dates_record)
    return dates_record


def get_popular(db: Session):
    """_summary_

    Args:
        db (Session): _description_

    Returns:
        _type_: _description_
    """
    months = db.query(models.Months).order_by(
        desc(models.Months.day_checked)).all()
    return months
