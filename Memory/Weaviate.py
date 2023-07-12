import json
import time
import weaviate
from colorama import Fore, Style
from Config import Config

config = Config()

class Weaviate:
    def __init__(self):
        self.client = weaviate.Client(
            url="http://localhost:8080",  # Replace with your endpoint
            additional_headers={
                "X-OpenAI-Api-Key": config["OPENAI_API_KEY"],
            },
        )
        self.vec_num = 0
        self.class_obj = {
            "class": "Personality",
            # description of the class
            "description": "A peice of information about ballbert's personality",
            "properties": [
                {
                    "dataType": ["text"],
                    "description": "A fact about ballbert's personality",
                    "name": "fact",
                },
            ],
            "vectorizer": "text2vec-openai",
        }

        if not self.client.schema.contains(self.class_obj):
            self.client.schema.create_class(self.class_obj)

    def add_list(self, data: list):
        with self.client.batch(
            batch_size=100, weaviate_error_retries=weaviate.WeaviateErrorRetryConf()
        ) as batch:
            for fact in data:
                properties = {
                    "fact": fact,
                }

                self.client.batch.add_data_object(properties, "Personality")

                time.sleep(0.1)

    def get(self, data):
        return self.get_relevant(data, 1)

    def clear(self):
        self.client.schema.delete_class(
            "Personality"
        )  # deletes all classes along with the whole data
        self.client.schema.create_class(self.class_obj)
        return "Obliviated"

    def get_relevant(self, data, num_relevant=5):
        """
        Returns all the data in the memory that is relevant to the given data.
        :param data: The data to compare to.
        :param num_relevant: The number of relevant data to return. Defaults to 5
        """
        result = (
            self.client.query.get("Personality", ["fact"])
            .with_near_text({"concepts": [str(data)]})
            .with_limit(num_relevant)
            .do()
        )

        return [item["fact"] for item in result["data"]["Get"]["Personality"]]

    def get_stats(self):
        return self.client.schema()

    def delete(self, where={}):
        # default QUORUM
        self.client.batch.consistency_level = (
            weaviate.data.replication.ConsistencyLevel.ALL
        )

        result = self.client.batch.delete_objects(
            class_name="Personality",
            # same where operator as in the GraphQL API
            where=where,
            output="verbose",
            dry_run=False,
        )
        return result
