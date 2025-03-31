from pathlib import Path

import pytest

from mssdk_airflow_pipeline import RML_MAPPER_PATH
from mssdk_airflow_pipeline.adapters.rml_mapper import RMLMapperABC, RMLMapper
from tests import TEST_DATA_EXAMPLE_NOTICES_373731_2024_XML_PATH, \
    TEST_DATA_EXAMPLE_MAPPING_PACKAGE_EFORMS_29_V1_8_ZIP_PATH, TEST_DATA_EXAMPLE_RDF_373731_2024_XML_PATH


@pytest.fixture
def example_notice_str() -> str:
    return TEST_DATA_EXAMPLE_NOTICES_373731_2024_XML_PATH.read_text()


@pytest.fixture
def example_mapping_package_path() -> Path:
    return TEST_DATA_EXAMPLE_MAPPING_PACKAGE_EFORMS_29_V1_8_ZIP_PATH

@pytest.fixture
def example_rdf_str() -> str:
    return TEST_DATA_EXAMPLE_RDF_373731_2024_XML_PATH.read_text()

@pytest.fixture
def rml_mapper() -> RMLMapperABC:
    return RMLMapper(rml_mapper_path=RML_MAPPER_PATH)