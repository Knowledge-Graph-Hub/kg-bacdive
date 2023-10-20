from oaklib import get_adapter
from oaklib.implementations import LLMImplementation
from oaklib.datamodels.text_annotator import TextAnnotationConfiguration

import pandas as pd

# object_id='CHEBI:15377', object_label='water', object_categories=['chemical'], subject_label='H20'

def annotate(df:pd.DataFrame, prefix:str):

    ontology = prefix.strip(":")
    oi = get_adapter(f"llm:sqlite:obo:{ontology}")
    configuration = TextAnnotationConfiguration(include_aliases=True)
    annotated_dict = {}
    for row in df.iterrows():
        for ann in oi.annotate_text(row[1].iloc[1], configuration):
            ann_attributes = {k: v for k, v in ann.__dict__.items() if v is not None}
            annotated_dict[row[1].iloc[0]] = ann_attributes
            import pdb; pdb.set_trace()