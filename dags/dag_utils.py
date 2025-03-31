from airflow.models import BaseOperator
from airflow.providers.common.compat.openlineage.facet import Dataset
from airflow.providers.http.operators.http import HttpOperator
from airflow.providers.openlineage.extractors import OperatorLineage
from airflow.utils.context import Context
from openlineage.client.generated.documentation_dataset import DocumentationDatasetFacet
from openlineage.client.generated.schema_dataset import SchemaDatasetFacet, SchemaDatasetFacetFields

MONGO_DB_DATASET = Dataset(namespace=f"default", name="my_mongo_db",
                           facets={
                               "schema": SchemaDatasetFacet(
                                   fields=[
                                       SchemaDatasetFacetFields(name="_id", type="ObjectId",
                                                                description="MongoDB document ID")

                                   ]
                               ),
                               "documentation": DocumentationDatasetFacet(
                                   description=f"MongoDB collection"
                               )
                           })

setattr(HttpOperator, 'get_openlineage_facets_on_complete', lambda task_instance: OperatorLineage(
    inputs=[
        MONGO_DB_DATASET
    ],
))


class SelectMongoDBOperator(BaseOperator):
    ui_color = "#6874E8"
    ui_fgcolor = "#000000"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self, context: Context):
        pass

    def get_openlineage_facets_on_complete(self, task_instance):
        """
        Implement _on_complete because execute method does preprocessing on internals.

        This means we won't have to normalize self.source_object and self.source_objects,
        destination bucket and so on.
        """

        return OperatorLineage(
            inputs=[
                MONGO_DB_DATASET
            ],
        )


class InsertMongoDBOperator(BaseOperator):
    ui_color = "#E8F0FF"
    ui_fgcolor = "#000000"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self, context: Context):
        pass

    def get_openlineage_facets_on_complete(self, task_instance):
        """
        Implement _on_complete because execute method does preprocessing on internals.

        This means we won't have to normalize self.source_object and self.source_objects,
        destination bucket and so on.
        """

        return OperatorLineage(
            outputs=[
                MONGO_DB_DATASET
            ],
        )
