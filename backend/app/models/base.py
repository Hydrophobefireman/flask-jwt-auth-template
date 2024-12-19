from pydantic import BaseModel


class CustomBase(BaseModel):
    @classmethod
    def from_db(cls, db):
        return cls.model_validate(db.as_json)
