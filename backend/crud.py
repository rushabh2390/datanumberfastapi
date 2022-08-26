from sqlalchemy.orm import Session

import models, schemas


def fetch_all_dates(db: Session, user_id: int):
    return db.query(models.Dates).all()


# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()


# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()


def create_dates(db: Session, dates_data: schemas.DatesResponse):

    db_dates = models.Dates(month=dates_data.month,
                            day=dates_data.day, fact=dates_data.fact)
    db.add(db_dates)
    db.commit()
    db.refresh(db_dates)
    return db_dates


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
