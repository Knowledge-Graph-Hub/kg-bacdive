"""NLP utilities."""
import csv
from pathlib import Path
import time
from typing import List

import pandas as pd
from oaklib import get_adapter
from oaklib.datamodels.text_annotator import TextAnnotationConfiguration

from kg_bacdive.transform_utils.constants import (
    END_COLUMN,
    OBJECT_ALIASES_COLUMN,
    OBJECT_CATEGORIES_COLUMN,
    OBJECT_ID_COLUMN,
    OBJECT_LABEL_COLUMN,
    START_COLUMN,
    SUBJECT_LABEL_COLUMN,
    TAX_ID_COLUMN,
)

# LLM_MODEL = "gpt-4"


def annotate(df: pd.DataFrame, prefix: str, exclusion_list: List, outfile: Path, llm: bool = False):
    """
    Anotate dataframe column text using oaklib + llm.

    :param df: Input DataFrame
    :param prefix: Ontology to be used.
    :param exclusion_list: Tokens that can be ignored.
    """
    ontology = prefix.strip(":")
    if llm:
        oi = get_adapter(f"llm:sqlite:obo:{ontology}")
        matches_whole_text = False
    else:
        oi = get_adapter(f"sqlite:obo:{ontology}")
        matches_whole_text = True
    configuration = TextAnnotationConfiguration(
        include_aliases=True,
        token_exclusion_list=exclusion_list,
        # model=LLM_MODEL,
        matches_whole_text=matches_whole_text
    )

    annotated_columns = [
        TAX_ID_COLUMN,
        OBJECT_ID_COLUMN,
        OBJECT_LABEL_COLUMN,
        OBJECT_CATEGORIES_COLUMN,
        OBJECT_ALIASES_COLUMN,
        SUBJECT_LABEL_COLUMN,
        START_COLUMN,
        END_COLUMN,
    ]

    start_time = time.time()
    
    with open(str(outfile), "w", newline='') as file:
        writer = csv.writer(file, delimiter='\t', quoting=csv.QUOTE_NONE)
        writer.writerow(annotated_columns)

        for row in df.iterrows():
            for ann in oi.annotate_text(row[1].iloc[1], configuration):
                
                ann_attributes = {k: v for k, v in ann.__dict__.items() if v is not None}
                ann_attributes[TAX_ID_COLUMN] = row[1].iloc[0]

                # Ensure the order of columns matches the header
                row_to_write = [ann_attributes.get(col) for col in annotated_columns]
                writer.writerow(row_to_write)
            
            # Check if 60 minutes have passed
            if (time.time() - start_time) >= 3600:
                print("Pausing for 5 seconds..")
                time.sleep(5)  # Pause for 5 seconds
                start_time = time.time()  # Reset the start time

