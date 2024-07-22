import table
import dataclasses

@dataclasses.dataclass
class CarPhoto:
    id: int
    url: str
    car_id_fn: int

    
class CarPhotoTable(table.Table):
    def __init__(self):
        super().__init__("cars_photos",
            {
                "id": "integer PRIMARY KEY NOT NULL",
                "url": "varchar(255) NOT NULL",
                "car_id_fn": "integer"
            },
            [
                "FOREIGN KEY(car_id_fn) REFERENCES cars(id)"
            ]
        )

    def create(self, car_photo: CarPhoto) -> None:
        super().create(car_photo.__dict__)

    def get_all(self) -> list[CarPhoto]:
        result = []
        rows = super().get_all()

        for i in rows:
            result.append(CarPhoto(*i))

        return result