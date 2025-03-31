from pathlib import Path

from mssdk_airflow_pipeline.adapters.rml_mapper import RMLMapperABC
from mssdk_airflow_pipeline.services.notice_transformation import transform_notice


def test_notice_transformation_run_with_success(example_notice_str: str,
                                                example_mapping_package_path: Path,
                                                example_rdf_str: str,
                                                rml_mapper: RMLMapperABC) -> None:
    rdf_result: str = transform_notice(notice_str=example_notice_str,
                                  mp_archive_path=example_mapping_package_path,
                                  rml_mapper=rml_mapper)

    assert rdf_result
    assert rdf_result == example_rdf_str