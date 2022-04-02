# Copyright 2022 Marin Pejcin


from core.database.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
