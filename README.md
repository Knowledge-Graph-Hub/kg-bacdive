# kg-bacdive

Knowledge graph construction for BacDive data

# Setup
 - Create a vrtual environment of your choice.
 - Install poetry using `pip install poetry`
 - `poetry install`
 - `git clone https://github.com/Knowledge-Graph-Hub/kg-bacdive.git`
 - `cd kg-bacdive`
 - Download the [BacDive JSON resource](https://drive.google.com/file/d/1dOquB0M6H5Vxu6cBPa4kJ7F9v44medoV/view?usp=share_link) and place it in the `data/raw`[data/raw/] folder named `bacdive_strains.json`
   - TODO: make `kghub-downloader` GDrive compatible.

## Download resources needed
 - `kg download` : This will download the resources needed for this project.

## Transform
 - `kg transform`: This transforms the resources into knowledge graphs.


# Acknowledgements

This [cookiecutter](https://cookiecutter.readthedocs.io/en/stable/README.html) project was developed from the [kg-cookiecutter](https://github.com/Knowledge-Graph-Hub/kg-cookiecutter) template and will be kept up-to-date using [cruft](https://cruft.github.io/cruft/).