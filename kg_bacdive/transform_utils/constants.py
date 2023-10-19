"""Constants for transform_utilities."""
from pathlib import Path

BACDIVE_DIR = Path(__file__).parent / "bacdive"
BACDIVE_TMP_DIR = BACDIVE_DIR / "tmp"
BACDIVE_YAML_DIR = BACDIVE_TMP_DIR / "yaml"
MEDIADIVE_DIR = Path(__file__).parent / "mediadive"
MEDIADIVE_TMP_DIR = MEDIADIVE_DIR / "tmp"
MEDIADIVE_MEDIUM_YAML_DIR = MEDIADIVE_TMP_DIR / "medium_yaml"
MEDIADIVE_RECIPE_YAML_DIR = MEDIADIVE_TMP_DIR / "recipe_yaml"


# KEYS FOR JSON FILE
GENERAL = "General"
BACDIVE_ID = "BacDive-ID"
KEYWORDS = "keywords"
GENERAL_DESCRIPTION = "description"
NCBITAXON_ID = "NCBI tax id"
MATCHING_LEVEL = "Matching level"
SPECIES = "species"
STRAIN = "strain"
DOI = "doi"
DSM_NUMBER = "DSM-Number"

NAME_TAX_CLASSIFICATION = "Name and taxonomic classification"
MORPHOLOGY = "Morphology"

CULTURE_AND_GROWTH_CONDITIONS = "Culture and growth conditions"
CULTURE_MEDIUM = "culture medium"
CULTURE_COMPOSITION = "composition"
CULTURE_GROWTH = "growth"
CULTURE_LINK = "link"
CULTURE_NAME = "name"
CULTURE_TEMP = "culture temp"
CULTURE_TEMP_GROWTH = "growth"
CULTURE_TEMP_TYPE = "type"
CULTURE_TEMP_TEMP = "temperature"
CULTURE_TEMP_RANGE = "range"

PHYS_AND_METABOLISM = "Physiology and metabolism"
ISOLATION_SAMPLING_ENV_INFO = "Isolation, sampling and environmental information"
SAFETY_INFO = "Safety information"
SEQUENCE_INFO = "Sequence information"

DATA_KEY = "data"
SOLUTION_KEY = "solutions"

RECIPE_KEY = "recipe"
COMPOUND_KEY = "compound"
COMPOUND_ID_KEY = "compound_id"
SOLUTION_KEY = "solution"
SOLUTIONS_KEY = "solutions"
SOLUTION_ID_KEY = "solution_id"
INGREDIENT_KEY = "ingredient_key"
INGREDIENT_ID_KEY = "ingredient_id_key"
CHEBI_KEY = "ChEBI"
CAS_RN_KEY = "CAS-RN"
KEGG_KEY = "KEGG-Compound"
PUBCHEM_KEY = "PubChem"

EXTERNAL_LINKS = "External links"
EXTERNAL_LINKS_CULTURE_NUMBER = "culture collection no."
REF = "Reference"
NCBITAXON_PREFIX = "NCBITaxon:"
BACDIVE_PREFIX = "bacdive:"
CHEBI_PREFIX = "CHEBI:"
CAS_RN_PREFIX = "CAS-RN:"
PUBCHEM_PREFIX = "PubChem:"
MEDIADIVE_COMPOUND_PREFIX = "mediadive.ingredient:"
MEDIADIVE_SOLUTION_PREFIX = "mediadive.solution:"

KEGG_PREFIX = "KEGG:"

MEDIADIVE_REST_API_BASE_URL = "https://mediadive.dsmz.de/rest/"
BACDIVE_API_BASE_URL = "https://bacmedia.dsmz.de/"

MEDIUM = "medium/"
COMPOUND = "ingredient/"
SOLUTION = "solution/"

BACDIVE_MEDIUM_DICT = {"dsmz": BACDIVE_API_BASE_URL + MEDIUM}

NCBI_TO_MEDIUM_EDGE = "biolink:occurs_in"
MEDIUM_TO_NCBI_EDGE = "biolink:contains_process"
MEDIUM_TO_INGREDIENT_EDGE = "biolink:has_part"  # Could also be has_constituent/has_participant
NCBI_CATEGORY = "biolink:OrganismTaxon"
MEDIUM_CATEGORY = "biolink:ChemicalEntity"
INGREDIENT_CATEGORY = "biolink:ChemicalEntity"

HAS_PART = "BFO:0000051"
IS_GROWN_IN = "BAO:0002924"

BACDIVE_ID_COLUMN = "bacdive_id"
DSM_NUMBER_COLUMN = "dsm_number"
EXTERNAL_LINKS_CULTURE_NUMBER_COLUMN = "culture_collection_number"
NCBITAXON_ID_COLUMN = "ncbitaxon_id"
NCBITAXON_DESCRIPTION_COLUMN = "ncbitaxon_description"
KEYWORDS_COLUMN = "keywords"
MEDIUM_ID_COLUMN = "medium_id"
MEDIUM_LABEL_COLUMN = "medium_label"
MEDIUM_URL_COLUMN = "medium_url"
MEDIADIVE_URL_COLUMN = "mediadive_medium_url"
INGREDIENTS_COLUMN = "ingredents"


MEDIADIVE_ID_COLUMN = "mediadive_id"
MEDIADIVE_NAME_COLUMN = "name"
MEDIADIVE_COMPLEX_MEDIUM_COLUMN = "complex_medium"
MEDIADIVE_SOURCE_COLUMN = "source"
MEDIADIVE_LINK_COLUMN = "link"
MEDIADIVE_MIN_PH_COLUMN = "min_pH"
MEDIADIVE_MAX_PH_COLUMN = "max_pH"
MEDIADIVE_REF_COLUMN = "reference"
MEDIADIVE_DESC_COLUMN = "description"
