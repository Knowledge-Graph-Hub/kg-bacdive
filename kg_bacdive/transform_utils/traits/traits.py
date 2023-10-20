"""Transform the traits data from NCBI and GTDB."""

from typing import Optional, Union
from kg_bacdive.transform_utils.constants import CHEBI_PREFIX, GO_PREFIX
from kg_bacdive.transform_utils.transform import Transform
from pathlib import Path
import pandas as pd

from kg_bacdive.utils.nlp_utils import annotate

TAX_ID_COLUMN = "tax_id"
CARBON_SUBSTRATES_COLUMN = "carbon_substrates"
PATHWAYS_COLUMN = "pathways"

class TraitsTransform(Transform):

    """
    Ingest traits dataset (NCBI/GTDB).

    Essentially just ingests and transforms this file:
    https://github.com/bacteria-archaea-traits/bacteria-archaea-traits/blob/master/output/condensed_traits_NCBI.csv
    And extracts the following columns:
        - tax_id
        - org_name
        - metabolism
        - pathways
        - shape
        - carbon_substrates
        - cell_shape
        - isolation_source
    Also implements:
        -   OGER to run NLP via the 'nlp_utils' module and
        -   ROBOT using 'robot_utils' module.
    """

    def __init__(self, input_dir: str, output_dir: str, nlp=True) -> None:
        """
        Initialize TraitsTransform Class.

        :param input_dir: Input file path (str)
        :param output_dir: Output file path (str)
        """
        source_name = "traits"
        super().__init__(source_name, input_dir, output_dir, nlp)  # set some variables
        self.nlp = nlp
    def run(self, data_file: Union[Optional[Path], Optional[str]] = None):
        """
        Call method and perform needed transformations for trait data (NCBI/GTDB).

        :param data_file: Input file name.
        """
        if data_file is None:
            data_file = self.source_name + ".csv"
        input_file = self.input_base_dir / data_file
        cols_for_nlp = [TAX_ID_COLUMN, PATHWAYS_COLUMN, CARBON_SUBSTRATES_COLUMN]
        nlp_df = pd.read_csv(input_file, usecols=cols_for_nlp, low_memory=False)
        go_nlp_df = nlp_df[[TAX_ID_COLUMN, PATHWAYS_COLUMN]].dropna()
        chebi_nlp_df = nlp_df[[TAX_ID_COLUMN, CARBON_SUBSTRATES_COLUMN]].dropna()
        # go_result = annotate(go_nlp_df, GO_PREFIX)
        chebi_result = annotate(chebi_nlp_df, CHEBI_PREFIX)
        import pdb; pdb.set_trace()