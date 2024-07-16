import table
import dataclasses

@dataclasses.dataclass
class Car:
    id: int
    brand: str
    model: str


class CarTable(table.Table):
    def __init__(self):
        super().__init__("cars", 
            {
                "id": "integer PRIMARY KEY NOT NULL",
                "brand": "varchar(255) NOT NULL",
                "model": "varchar(255) NOT NULL",
            },
            []
        )
