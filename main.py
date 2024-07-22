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

        cr_table.create(daewoo)
        cr_table.create(mercs)
        cr_table.create(skoda)

        my_car_photo = car_photo_table.CarPhoto(1, "https://cdn2.riastatic.com/photosnew/auto/photo/daewoo_lanos__542790792s.jpg", 1)

        crp_table.create(my_car_photo)

        logger.debug(cr_table.get_all())
        logger.debug(crp_table.get_all())


if __name__ == "__main__":
    main()