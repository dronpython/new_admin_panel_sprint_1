from time import sleep
from datetime import datetime


from etl.connectors.db_connector import DB
from etl.misc.state import JsonFileStorage, State
from etl.creeds import Settings
from etl.misc.funcs import prepare_data
from etl.connectors.elk_connector import es
from etl.logging_ import logger


def update_data(table, last_update_date, size):
    logger.info(f"Trying to update {table} data")
    data = db.load_all_data(table, last_update_date, size)
    for rows in data:
        logger.info(f"Load {len(rows)} rows")
        data_prepared = prepare_data(rows)
        es.bulk(data_prepared)
    logger.info(f"{table} updated")


while True:
    storage = JsonFileStorage("storage.json")
    state = State(storage)
    current_state = state.get_state("state")
    if current_state is None:
        logger.info("current_state is None. Set to 1970-01-01")
        current_state = "1970-01-01"

    db = DB(Settings().dict()["dsl"])
    logger.info("=======Begin ETL process=======")
    target = state.get_state("target")
    if target is None or target == "film_work":
        update_data("fw", current_state, 100)
        state.set_state("target", "person")

    target = state.get_state("target")
    if target == "person":
        update_data("p", current_state, 100)
        state.set_state("target", "genre")

    target = state.get_state("target")
    if target == "genre":
        update_data("g", current_state, 100)
        state.set_state("target", "film_work")
    logger.info(f"Update finished. Set state to {str(datetime.now())} and sleep 60 sec")

    # Обновляем state только в случае, если дошли до конца и все процессы выполнены
    state.set_state("state", str(datetime.now()))
    logger.info("=========End process=========")
    sleep(60)
