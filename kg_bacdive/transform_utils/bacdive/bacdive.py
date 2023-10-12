"""
Template design.

Example script to transform downloaded data into a graph format that KGX can ingest directly,
in either TSV or JSON format:
https://github.com/NCATS-Tangerine/kgx/blob/master/data-preparation.md

Input: any file in data/raw/ (that was downloaded by placing a URL in incoming.txt/yaml
and running `run.py download`.

Output: transformed data in data/raw/[source name]:

Output these two files:
- nodes.tsv
- edges.tsv
"""
import csv
import json
import os
import re
from pathlib import Path
from typing import Optional, Union

import requests
import yaml

from kg_bacdive.transform_utils.transform import Transform

# from kg_bacdive.utils.robot_utils import convert_to_json, extract_convert_to_json

BACDIVE_DIR = Path(__file__).parent
TMP_DIR = BACDIVE_DIR / "tmp"
YAML_DIR = TMP_DIR / "yaml"
MEDIADIVE_DIR = TMP_DIR / "mediadive"

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

EXTERNAL_LINKS = "External links"
EXTERNAL_LINKS_CULTURE_NUMBER = "culture collection no."
REF = "Reference"
NCBITAXON_PREFIX = "NCBITaxon:"
BACDIVE_PREFIX = "BACDIVE:"

MEDIADIVE_REST_API_BASE_URL = "https://mediadive.dsmz.de/rest/"
BACDIVE_API_BASE_URL = "https://bacmedia.dsmz.de/"

MEDIUM = "medium/"

CURIE_MAP = {"DSMZ": BACDIVE_API_BASE_URL + MEDIUM}
NCBI_TO_MEDIUM_EDGE = "biolink:growsIn-PLACEHOLDER"
MEDIUM_TO_NCBI_EDGE = "biolink:supportsGrowth-PLACEHOLDER"
NCBI_CATEGORY = "biolink:IndividualOrganism"
MEDIUM_CATEGORY = "biolink:Medium-PLACEHOLDER"

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


"""
Key-Values from JSON that need to be extracted:
- For subjects (NCBITaxon:XXXX)
    General:
    BacDive-ID:
    DSM-Number:
    NCBI tax id:
        - Matching level:
        NCBI tax id:
        - Matching level:
        NCBI tax id:
    keywords: (List)

- For predicates:
    - "grows in" (tentative for taxa => media)
    - "supports growth" (tentative for media => taxa)


- For objects (culture medium)
Culture and growth conditions:
    culture medium:
    composition: (Has Name: and Composition:)
    name:


"""


class BacDiveTransform(Transform):

    """Template for how the transform class would be designed."""

    def __init__(self, input_dir: Optional[Path] = None, output_dir: Optional[Path] = None):
        """Instantiate part."""
        source_name = "BacDive"
        super().__init__(source_name, input_dir, output_dir)

    def get_mediadive_yaml(self, url: str):
        """
        Download MetaDive data using a url.

        :param url: Path provided by MetaDive API.
        """
        r = requests.get(url, timeout=10)
        data_yaml = yaml.dump(r.json())
        fn = url.strip(MEDIADIVE_REST_API_BASE_URL + MEDIUM) + ".yaml"
        if not (MEDIADIVE_DIR / fn).is_file():
            with open(str(MEDIADIVE_DIR / fn), "w") as f:
                f.write(data_yaml)

    def run(self, data_file: Union[Optional[Path], Optional[str]] = None):
        """Run the transformation."""
        # replace with downloaded data filename for this source
        input_file = os.path.join(self.input_base_dir, "bacdive_strains.json")  # must exist already
        # mediadive_file = os.path.join(self.input_base_dir, "mediadive.json")

        # # Read MediaDive JSON
        # with open(mediadive_file, "r") as f:
        #     mediadive = json.load(f)

        # mediadive_data:List = mediadive["data"]
        # Read the JSON file into the variable input_json
        with open(input_file, "r") as f:
            input_json = json.load(f)

        COLUMN_NAMES = [
            BACDIVE_ID_COLUMN,
            DSM_NUMBER_COLUMN,
            EXTERNAL_LINKS_CULTURE_NUMBER_COLUMN,
            NCBITAXON_ID_COLUMN,
            NCBITAXON_DESCRIPTION_COLUMN,
            KEYWORDS_COLUMN,
            MEDIUM_ID_COLUMN,
            MEDIUM_LABEL_COLUMN,
            MEDIUM_URL_COLUMN,
            MEDIADIVE_URL_COLUMN,
        ]

        # make directory in data/transformed
        os.makedirs(self.output_dir, exist_ok=True)

        with open(str(TMP_DIR / "bacdive.tsv"), "w") as csvfile, open(
            self.output_node_file, "w"
        ) as node, open(self.output_edge_file, "w") as edge:
            writer = csv.writer(csvfile, delimiter="\t")
            # Write the column names to the output file
            writer.writerow(COLUMN_NAMES)

            node_writer = csv.writer(node, delimiter="\t")
            node_writer.writerow(self.node_header)
            edge_writer = csv.writer(edge, delimiter="\t")
            edge_writer.writerow(self.edge_header)

            for key, value in input_json.items():
                fn: Path = Path(str(YAML_DIR / key) + ".yaml")
                if not fn.is_file():
                    with open(str(fn), "w") as outfile:
                        yaml.dump(value, outfile)

                # self._extract_values(value, template)
                # Get "General" information
                general_info = value.get(GENERAL, {})
                # bacdive_id = general_info.get(BACDIVE_ID) # This is the same as `key`
                dsm_number = general_info.get(DSM_NUMBER)
                external_links = value.get(EXTERNAL_LINKS, {})
                culture_number_from_external_links = None
                if EXTERNAL_LINKS_CULTURE_NUMBER in external_links:
                    culture_number_from_external_links = (
                        external_links[EXTERNAL_LINKS_CULTURE_NUMBER] or ""
                    ).split(",")

                    if dsm_number is None:
                        for item in culture_number_from_external_links:
                            match = re.search(r"DSM (\d+)", item)
                            if match:
                                dsm_number = match.group(1)
                                break

                #  SUBJECT part
                ncbitaxon_id = None
                ncbi_description = None
                if NCBITAXON_ID in general_info:
                    if isinstance(general_info[NCBITAXON_ID], list):
                        ncbi_of_interest = None
                        for ncbi in general_info[NCBITAXON_ID]:
                            if MATCHING_LEVEL in ncbi and (
                                ncbi[MATCHING_LEVEL] == STRAIN or ncbi[MATCHING_LEVEL] == SPECIES
                            ):
                                # If a STRAIN is found, assign it to ncbi_of_interest and break
                                if ncbi[MATCHING_LEVEL] == STRAIN:
                                    ncbi_of_interest = ncbi[NCBITAXON_ID]
                                    break
                                # If a SPECIES is found and no STRAIN has been found yet, assign it to ncbi_of_interest
                                elif ncbi[MATCHING_LEVEL] == SPECIES and ncbi_of_interest is None:
                                    ncbi_of_interest = ncbi[NCBITAXON_ID]
                        if ncbi_of_interest is not None:
                            ncbitaxon_id = NCBITAXON_PREFIX + str(ncbi_of_interest)
                    else:
                        ncbitaxon_id = NCBITAXON_PREFIX + str(
                            general_info[NCBITAXON_ID][NCBITAXON_ID]
                        )
                    ncbi_description = general_info.get(GENERAL_DESCRIPTION, "")

                keywords = str(general_info.get(KEYWORDS, ""))

                # OBJECT PART
                medium_id = None
                medium_label = None
                medium_url = None
                mediadive_url = None
                if CULTURE_AND_GROWTH_CONDITIONS in value and value[CULTURE_AND_GROWTH_CONDITIONS]:
                    if (
                        CULTURE_MEDIUM in value[CULTURE_AND_GROWTH_CONDITIONS]
                        and value[CULTURE_AND_GROWTH_CONDITIONS][CULTURE_MEDIUM]
                    ):
                        if (
                            CULTURE_LINK in value[CULTURE_AND_GROWTH_CONDITIONS][CULTURE_MEDIUM]
                            and value[CULTURE_AND_GROWTH_CONDITIONS][CULTURE_MEDIUM][CULTURE_LINK]
                        ):
                            medium_url = str(
                                value[CULTURE_AND_GROWTH_CONDITIONS][CULTURE_MEDIUM][CULTURE_LINK]
                            )
                            medium_id = next(
                                (
                                    medium_url.replace(val, key + ":")
                                    for key, val in CURIE_MAP.items()
                                    if medium_url.startswith(val)
                                ),
                                None,
                            )
                            medium_label = value[CULTURE_AND_GROWTH_CONDITIONS][CULTURE_MEDIUM][
                                CULTURE_NAME
                            ]

                            mediadive_url = medium_url.replace(
                                BACDIVE_API_BASE_URL, MEDIADIVE_REST_API_BASE_URL
                            )
                            # if mediadive_url and not mediadive_url.endswith(".pdf"):
                            #     self.get_mediadive_yaml(mediadive_url)

                data = [
                    BACDIVE_PREFIX + key,
                    dsm_number,
                    culture_number_from_external_links,
                    ncbitaxon_id,
                    ncbi_description,
                    keywords,
                    medium_id,
                    medium_label,
                    medium_url,
                    mediadive_url,
                ]

                writer.writerow(data)  # writing the data
                if ncbitaxon_id and medium_id:
                    node_writer.writerows(
                        [[ncbitaxon_id, ncbi_description, None], [medium_id, medium_label, None]]
                    )

                    edge_writer.writerow(
                        [
                            ncbitaxon_id,
                            NCBI_TO_MEDIUM_EDGE,
                            medium_id,
                            None,
                            BACDIVE_PREFIX + key,
                        ]
                    )
