from pathlib import Path

DAGS_PATH = Path(__file__).parent.resolve()


DAGS_SOURCES_PATH = DAGS_PATH / "sources"
DAGS_SOURCES_INPUT_MP_PATH = DAGS_SOURCES_PATH / "input_mp"
DAGS_SOURCES_INPUT_NOTICE_PATH = DAGS_SOURCES_PATH / "input_notice"
DAGS_SOURCES_PUTPUT_RDF_PATH = DAGS_SOURCES_PATH / "output_rdf"

DEFAULT_POC_INTERVAL = 2 # 2 seconds
