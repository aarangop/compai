from __future__ import annotations

from pydantic import BaseModel
from tinydb import Query, TinyDB
from tinydb.table import Table

from compaipair.utils import get_db


class CompletionTemplate(BaseModel):
    name: str
    priming: str = None
    decorator: str = None
    _db: TinyDB
    _table: Table

    def __init__(self, **data):
        super().__init__(**data)
        self._db = get_db()
        self._table = self._db.table("templates")

    @staticmethod
    def find_template(name: str) -> CompletionTemplate | None:
        db = get_db()
        condition = Query().name == name
        templates_table = db.table("templates")
        result = templates_table.get(condition)
        if isinstance(result, list):
            result = result[0]
        return CompletionTemplate.model_validate(result)

    @staticmethod
    def find_templates(name: str | None) -> list[CompletionTemplate]:
        db = get_db()
        templates_table = db.table("templates")
        if name is not None:
            condition = Query().name == name
            results = templates_table.search(condition)
        else:
            results = templates_table.all()

        return [CompletionTemplate.model_validate(template) for template in results]

    def save(self) -> list[int]:
        """
        Persists the model object to the database. If the model object does not
        yet have an id, one is assigned before persisting.

        Returns:
            int: the id of the persisted object
        """
        query = Query()
        return self._table.upsert(
            self.model_dump(exclude_none=True), query.name == self.name
        )

    def update_template(self, **kwargs) -> list[int]:
        update_obj = {}

        for key, val in kwargs.items():
            if key in self.__dict__.keys() and val is not None:
                update_obj[key] = val

        self.__dict__.update(update_obj)
        return self.save()

    def prompt(self, question: str):
        return f"{self.priming}\n{question}\n{self.decorator}"
