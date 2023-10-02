# extraction_model.py
from src.models import db, Extractions

class ExtractionModel:
    @staticmethod
    def update_extraction(id, document_name):
        update = {"output_document_name": document_name}
        extraction = db.session.query(Extractions).get(id)
        for key, value in update.items():
            setattr(extraction, key, value)
        db.session.commit()
