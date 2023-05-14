import json
import psycopg2
from py2neo import Graph
import glob
import json
from typing import Collection
from difflib import SequenceMatcher
import re



class MySQLPipeline:
    # graph = Graph("bolt://localhost:7687", auth=("neo4j", "123"))
    # graph = Graph("bolt://103.252.1.143:7687", auth=("neo4j", "neo4j"))

    def __init__(self):
        # self.model, self.enc_tag = load_model()
        self.dateLimit = 20  # Number of days to check
        self.tolerables = 0
        self.maxTolerables = 30
        self.last = None


    def process_item(self, item, spider):
        print(spider)


        #
        # text = item["trieu_chung"]
        # text_process = process_data(text)
        # result_dict = predict(text_process, self.model, self.enc_tag)
        # for label in result_dict:
        #     entity = (label)[1]
        #     if entity == "trieu_chung_benh":
        #         entity = "symptom"
        #         conetent_entity = process_data(label[0]).lower()
        #         self.create_entity(entity, conetent_entity)
        #         conetent_entity = process_data(label[0]).lower()
        #
        #         entity_end = {"type": "symptom", "name": conetent_entity}
        #         self.create_rela_entity(entity_start, entity_end, "HAS_SYMPTOM")

        # pass

