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
import json
import os
from pathlib import Path
from typing import Optional, Union

import yaml

from kg_bacdive.transform_utils.transform import Transform

# from kg_bacdive.utils.robot_utils import convert_to_json, extract_convert_to_json

BACDIVE_DIR = Path(__file__).parent
TMP_DIR = BACDIVE_DIR / "tmp"
BACDIVE_CLASSES = BACDIVE_DIR / "bacdive-classes.yaml"


class BacDiveTransform(Transform):

    """Template for how the transform class would be designed."""

    def __init__(self, input_dir: Optional[Path] = None, output_dir: Optional[Path] = None):
        """Instantiate part."""
        source_name = "some_unique_name"
        super().__init__(source_name, input_dir, output_dir)

    # TODO: Function to extract values based on template
    def _extract_values(self, data, template):
        if isinstance(template, dict):
            return [self._extract_values(data.get(key), value) for key, value in template.items()]
        elif isinstance(template, list):
            return [self._extract_values(data[i], template[0]) for i in range(len(data))]
        else:
            return data

    def run(self, data_file: Union[Optional[Path], Optional[str]] = None):
        """Run the transformation."""
        # replace with downloaded data filename for this source
        input_file = os.path.join(self.input_base_dir, "bacdive_strains.json")  # must exist already
        # Read the JSON file into the variable input_json
        with open(input_file, "r") as f:
            input_json = json.load(f)

            # # Load the template YAML file
            # with open(str(BACDIVE_CLASSES), "r") as template_file:
            #     template = yaml.safe_load(template_file)

        for key, value in input_json.items():
            fn: Path = Path(str(TMP_DIR / key) + ".yaml")
            if not fn.is_file():
                with open(str(fn), "w") as outfile:
                    yaml.dump(value, outfile)

            # self._extract_values(value, template)
            # import pdb

            # pdb.set_trace()

        # # make directory in data/transformed
        # os.makedirs(self.output_dir, exist_ok=True)

        # # transform data, something like:
        # with open(input_file, "r") as f, open(self.output_node_file, "w") as node, open(
        #     self.output_edge_file, "w"
        # ) as edge:
        #     # write headers (change default node/edge headers if necessary
        #     node.write("\t".join(self.node_header) + "\n")
        #     edge.write("\t".join(self.edge_header) + "\n")

        #     # transform data, something like:
        #     for line in f:
        #         # transform line into nodes and edges
        #         # node.write(this_node1)
        #         # node.write(this_node2)
        #         # edge.write(this_edge)
        #         print(line)

        # #####################################################
        # #  If ROBOT needs to be implemented on an ontology.
        # #####################################################
        # # Convert OWL to JSON
        # convert_to_json(self.input_base_dir, "NAME_OF_ONTOLOGY")

        # # Get subset of ontology and save as JSON file.
        # # "subset_terms_file" could be either a CURIE
        # # or a txt file of CURIEs list
        # # ROBOT Method options:
        # #   - STAR
        # #   - TOP
        # #   - BOT
        # #   - MIREOT
        # extract_convert_to_json(
        #     self.input_base_dir, "NAME_OF_ONTOLOGY", self.subset_terms_file, "ROBOT_METHOD"
        # )
