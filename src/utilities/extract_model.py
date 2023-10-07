# extraction_model.py
from src.models import db, Extractions


class ExtractionModel:
    @staticmethod
    def update_extraction(id, params):
        extraction = db.session.query(Extractions).get(id)
        for key, value in params.items():
            setattr(extraction, key, value)
        db.session.commit()
