import sqlite3
import logging

import table
import car_table
import car_photo_table

logger = logging.getLogger()

stream_handler = logging.StreamHandler()
formatter = logging.Formatter(
    'line_num: %(lineno)s > %(message)s'
)

stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

def main():
    with sqlite3.connect("test.sqlite3") as conn:
        table.Table.conn = conn

        logger.info("started work")

        cr_table = car_table.CarTable()
        crp_table = car_photo_table.CarPhotoTable()

        daewoo = car_table.Car(1, "Daewoo", "Lanos")
        mercs = car_table.Car(2, "Mercedes", "S")
        skoda = car_table.Car(3, "Skoda", "Ocravia")

        crp_table.create(daewoo)
        crp_table.create(merc)
        crp_table.create(skoda)

if __name__ == "__main__":
    main()