# DBT Project
This is a dbt project for BigQuery.

## Installation
- Upload your csv file to big query and create a dataset. 
- Upload your big query service account json file to the root of the project.
- make sure all the source file and source dataset in your big query is the same as in this project.

## Usage
- Run the following command to install the required packages:
```
pip install -r requirements.txt
```
- Run the following command to build the dbt project:
```
dbt build
```
- Run the following command to run the dbt project:
```
dbt run
```
- Run the following command to generate the documentation:
```
dbt docs generate && dbt docs serve
```


