from elasticsearch import Elasticsearch
from etl.creeds import Settings

# ToDo: Как правильно организовать работу с es?
es = Elasticsearch(Settings().dict()["es_server"])
