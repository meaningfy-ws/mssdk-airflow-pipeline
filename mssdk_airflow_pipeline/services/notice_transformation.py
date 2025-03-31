import shutil
import tempfile
from pathlib import Path
from typing import Optional, NoReturn

from mssdk_airflow_pipeline import RML_MAPPER_PATH
from mssdk_airflow_pipeline.adapters.rml_mapper import RMLMapperABC, RMLMapper

DATA_SOURCE_PACKAGE = "data"


def transform_notice(notice_str: str,
                     mp_archive_path: Path,
                     rml_mapper: RMLMapperABC) -> str:
    with tempfile.TemporaryDirectory() as temp_dir:
        package_path = Path(temp_dir)
        shutil.unpack_archive(filename=mp_archive_path,
                              extract_dir=package_path)
        package_path = package_path / mp_archive_path.stem

        data_source_path = package_path / DATA_SOURCE_PACKAGE
        data_source_path.mkdir(parents=True, exist_ok=True)
        notice_path = data_source_path / "source.xml"
        notice_path.write_text(notice_str)

        rdf_result = rml_mapper.execute(package_path=package_path)
        return rdf_result


def batch_transform_and_save_notices(notices_folder_path: Path,
                                     mp_archive_path: Path,
                                     result_rdf_folder_path: Path,
                                     rml_mapper: Optional[RMLMapperABC] = None) -> None | NoReturn:
    if not rml_mapper:
        rml_mapper = RMLMapper(rml_mapper_path=RML_MAPPER_PATH)

    with tempfile.TemporaryDirectory() as temp_dir:
        package_path = Path(temp_dir)
        shutil.unpack_archive(filename=mp_archive_path,
                              extract_dir=package_path)
        package_path = package_path / mp_archive_path.stem
        data_source_path = package_path / DATA_SOURCE_PACKAGE
        data_source_path.mkdir(parents=True, exist_ok=True)
        notice_archive_path = data_source_path / "source.xml"
        for notice_path in notices_folder_path.iterdir():
            notice_path: Path
            if notice_path.is_file():
                notice_archive_path.write_text(notice_path.read_text())
                rdf_result = rml_mapper.execute(package_path=package_path)
                result_rdf_path = result_rdf_folder_path / f"{notice_path.stem}.rml.ttl"  # TODO: Somehow to get this info from rml mapper adapter
                result_rdf_path.parent.mkdir(parents=True, exist_ok=True)
                result_rdf_path.write_text(rdf_result)
