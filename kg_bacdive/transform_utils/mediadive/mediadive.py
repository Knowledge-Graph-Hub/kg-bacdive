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
from pathlib import Path
from urllib.parse import urlparse
from typing import Dict, Optional, Union

import requests
import requests_cache
import yaml
from oaklib import get_adapter
from tqdm import tqdm

from kg_bacdive.transform_utils.constants import (
    CAS_RN_KEY,
    CAS_RN_PREFIX,
    CHEBI_KEY,
    CHEBI_PREFIX,
    COMPOUND,
    COMPOUND_ID_KEY,
    COMPOUND_KEY,
    DATA_KEY,
    INGREDIENTS_COLUMN,
    IS_INGREDIENT_EDGE,
    KEGG_KEY,
    KEGG_PREFIX,
    MEDIADIVE_COMPLEX_MEDIUM_COLUMN,
    MEDIADIVE_COMPOUND_PREFIX,
    MEDIADIVE_DESC_COLUMN,
    MEDIADIVE_ID_COLUMN,
    MEDIADIVE_LINK_COLUMN,
    MEDIADIVE_MAX_PH_COLUMN,
    MEDIADIVE_MIN_PH_COLUMN,
    MEDIADIVE_NAME_COLUMN,
    MEDIADIVE_REF_COLUMN,
    MEDIADIVE_REST_API_BASE_URL,
    MEDIADIVE_SOLUTION_PREFIX,
    MEDIADIVE_SOURCE_COLUMN,
    MEDIADIVE_TMP_DIR,
    MEDIADIVE_MEDIUM_YAML_DIR,
    MEDIUM,
    PUBCHEM_KEY,
    PUBCHEM_PREFIX,
    RECIPE_KEY,
    SOLUTION,
    SOLUTION_ID_KEY,
    SOLUTION_KEY,
    SOLUTIONS_KEY,
)
from kg_bacdive.transform_utils.transform import Transform


class MediaDiveDiveTransform(Transform):

    """Template for how the transform class would be designed."""

    def __init__(self, input_dir: Optional[Path] = None, output_dir: Optional[Path] = None):
        """Instantiate part."""
        source_name = "MediaDive"
        super().__init__(source_name, input_dir, output_dir)
        requests_cache.install_cache('mediadive_cache')
        self.chebi_impl = get_adapter("sqlite:obo:chebi")

    def _get_mediadive_json(self, url: str) -> Dict[str, str]:
        """
        Use the API url to get a dict of information.

        :param url: Path provided by MetaDive API.
        :return: JSON response as a Dict.
        """
        r = requests.get(url, timeout=30)
        data_json = r.json()
        return data_json[DATA_KEY]

    def _get_label_via_oak(self, curie: str):
        prefix = curie.split(":")[0]
        if prefix.startswith(CHEBI_KEY):
            (_, label) = list(self.chebi_impl.labels([curie]))[0]
        return label

    def get_compounds_of_solution(self, id: str):
        """
        Get ingredients of solutions via the MediaDive API>.

        :param id: ID of solution
        :return: Dictionary of {compound_name: compound_id}
        """
        url = MEDIADIVE_REST_API_BASE_URL + SOLUTION + id
        data = self._get_mediadive_json(url)
        ingredients_dict = {}
        for item in data[RECIPE_KEY]:
            if COMPOUND_ID_KEY in item and item[COMPOUND_ID_KEY] is not None:
                ingredients_dict[item[COMPOUND_KEY]] = self.standardize_compound_id(
                    str(item[COMPOUND_ID_KEY])
                )
            elif SOLUTION_ID_KEY in item and item[SOLUTION_ID_KEY] is not None:
                ingredients_dict[item[SOLUTION_KEY]] = MEDIADIVE_SOLUTION_PREFIX + str(
                    item[SOLUTION_ID_KEY]
                )
            else:
                continue
        return ingredients_dict

    def standardize_compound_id(self, id: str):
        """
        Get IDs via Metadive API.

        :param id: Metadive compound ID
        :return: Standardized ID
        """
        url = MEDIADIVE_REST_API_BASE_URL + COMPOUND + id
        data = self._get_mediadive_json(url)
        if data[CHEBI_KEY] is not None:
            return CHEBI_PREFIX + str(data[CHEBI_KEY])
        elif data[KEGG_KEY] is not None:
            return KEGG_PREFIX + str(data[KEGG_KEY])
        elif data[PUBCHEM_KEY] is not None:
            return PUBCHEM_PREFIX + str(data[PUBCHEM_KEY])
        elif data[CAS_RN_KEY] is not None:
            return CAS_RN_PREFIX + str(data[CAS_RN_KEY])
        else:
            return MEDIADIVE_COMPOUND_PREFIX + id

    def download_yaml_and_get_json(self, url: str, target_dir: Path, ) -> Dict[str, str]:
        """
        Download MetaDive data using a url.

        :param url: Path provided by MetaDive API.
        """
        data_json = self._get_mediadive_json(url)
        parsed_url = urlparse(url)
        fn = parsed_url.path.split('/')[-1]+".yaml"
        if not (target_dir / fn).is_file():
            with open(str(target_dir / fn), "w") as f:
                f.write(yaml.dump(data_json))
        return data_json

    def run(self, data_file: Union[Optional[Path], Optional[str]] = None):
        """Run the transformation."""
        # replace with downloaded data filename for this source
        input_file = os.path.join(self.input_base_dir, "mediadive.json")  # must exist already

        # mediadive_data:List = mediadive["data"]
        # Read the JSON file into the variable input_json
        with open(input_file, "r") as f:
            input_json = json.load(f)

        COLUMN_NAMES = [
            MEDIADIVE_ID_COLUMN,
            MEDIADIVE_NAME_COLUMN,
            MEDIADIVE_COMPLEX_MEDIUM_COLUMN,
            MEDIADIVE_SOURCE_COLUMN,
            MEDIADIVE_LINK_COLUMN,
            MEDIADIVE_MIN_PH_COLUMN,
            MEDIADIVE_MAX_PH_COLUMN,
            MEDIADIVE_REF_COLUMN,
            MEDIADIVE_DESC_COLUMN,
            INGREDIENTS_COLUMN,
        ]

        # make directory in data/transformed
        os.makedirs(self.output_dir, exist_ok=True)

        with open(str(MEDIADIVE_TMP_DIR / "mediadive.tsv"), "w") as csvfile, open(
            self.output_node_file, "w"
        ) as node, open(self.output_edge_file, "w") as edge:
            writer = csv.writer(csvfile, delimiter="\t")
            # Write the column names to the output file
            writer.writerow(COLUMN_NAMES)

            node_writer = csv.writer(node, delimiter="\t")
            node_writer.writerow(self.node_header)
            edge_writer = csv.writer(edge, delimiter="\t")
            edge_writer.writerow(self.edge_header)

            with tqdm(total=len(input_json[DATA_KEY]) + 1, desc="Processing files") as progress:
                for dictionary in input_json[DATA_KEY]:
                    id = str(dictionary["id"])
                    fn: Path = Path(str(MEDIADIVE_MEDIUM_YAML_DIR / id) + ".yaml")
                    if not fn.is_file():
                        url = MEDIADIVE_REST_API_BASE_URL+MEDIUM+id
                        json_obj = self.download_yaml_and_get_json(url, MEDIADIVE_MEDIUM_YAML_DIR)
                    else:
                        # Import YAML file fn as a dict
                        with open(fn, 'r') as f:
                            try:
                                json_obj = yaml.safe_load(f)
                            except yaml.YAMLError as exc:
                                print(exc)
                    if SOLUTIONS_KEY not in json_obj:
                        continue
                    solution_id_list = [solution['id'] for solution in json_obj[SOLUTIONS_KEY]]
                    ingredients_dict = {}
                    medium_ingredient_edges = []
                    medium_id = MEDIADIVE_COMPOUND_PREFIX+str(id)  # SUBJECT

                    for solution_id in solution_id_list:
                        ingredients_dict.update(self.get_compounds_of_solution(str(solution_id)))
                        medium_ingredient_edges.extend([
                            [medium_id, IS_INGREDIENT_EDGE, v, MEDIADIVE_REST_API_BASE_URL+SOLUTION+str(solution_id)] for _,v in ingredients_dict.items()
                        ])

                    ingredient_nodes = [
                        [v, k, None] for k, v in ingredients_dict.items()
                    ]

                    data = [
                        medium_id,
                        dictionary[MEDIADIVE_NAME_COLUMN],
                        dictionary[MEDIADIVE_COMPLEX_MEDIUM_COLUMN],
                        dictionary[MEDIADIVE_SOURCE_COLUMN],
                        dictionary[MEDIADIVE_LINK_COLUMN],
                        dictionary[MEDIADIVE_MIN_PH_COLUMN],
                        dictionary[MEDIADIVE_MAX_PH_COLUMN],
                        dictionary[MEDIADIVE_REF_COLUMN],
                        dictionary[MEDIADIVE_DESC_COLUMN],
                        str(ingredients_dict)
                    ]

                    writer.writerow(data)  # writing the data

                    # Combine list creation and extension
                    nodes_data_to_write = [
                        [medium_id, dictionary[MEDIADIVE_NAME_COLUMN], None],
                        *ingredient_nodes,
                    ]
                    node_writer.writerows(nodes_data_to_write)

                    edge_writer.writerows(medium_ingredient_edges)

                    progress.set_description(f"Processing ingredient: {medium_id}")
                    # After each iteration, call the update method to advance the progress bar.
                    progress.update()
