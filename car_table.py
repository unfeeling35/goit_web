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

    def create(self, car: Car) -> None:
        super().create(car.__dict__)

    def get_all(self) -> list[Car]:
        result = []
        rows = super().get_all()

        for i in rows:
            result.append(Car(*i))

        return result