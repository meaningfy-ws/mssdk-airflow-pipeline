from typing import Optional, Union, Dict, List

from airflow.models import BaseOperator


class MongoDBOperator(BaseOperator):
    ui_color = "#ffcc00"  # Yellow
    ui_fgcolor = "#000000"  # Black text

    def __init__(
            self,
            mongo_conn_id: str,
            database: str,
            collection: str,
            operation: str,  # insert_one, find, update_one, delete_one
            data: Optional[Union[Dict, List[Dict]]] = None,
            query: Optional[Dict] = None,
            update: Optional[Dict] = None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.mongo_conn_id = mongo_conn_id
        self.database = database
        self.collection = collection
        self.operation = operation
        self.data = data
        self.query = query
        self.update = update

    def execute(self, context):
        pass
