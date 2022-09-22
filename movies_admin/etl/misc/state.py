import abc
import json
import os
import logging
from typing import Any, Optional

logger = logging.getLogger("elk")


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""
        pass


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: Optional[str] = "storage.json"):
        self.file_path = os.path.abspath(file_path)

    def save_state(self, state):
        logger.info(f"saving state {str(state)}")
        with open(self.file_path, 'w') as file:
            file.write(json.dumps(state))

    def retrieve_state(self):
        try:
            with open(self.file_path, 'r') as file:
                state = json.loads(file.read())
        except FileNotFoundError:
            state = {}
        return state


class State:

    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа"""
        logger.info(f"Set state {key}={value}")
        state = self.storage.retrieve_state()
        state[key] = value
        self.storage.save_state(state)

    def get_state(self, key: str = None) -> Any:
        """Получить состояние по определённому ключу"""
        state = self.storage.retrieve_state().get(key)
        logger.info(f"Getting state by key {key}. Result: {str(state)}")
        return state
