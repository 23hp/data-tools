# Easy Data
Quick tools save your daily data analysis workload, making life easier.

Support BigQuery in GCP now.

# Features
- List and search tables in specific dataset
- Query records and schema quickly
- Print command for further modification

# Quickstart

    git clone --depth 1 -b main git@github.com:23hp/easy-data.git
    cd easy-data
    # make script executable
    chmod +x shell/*
    export PATH=$PATH:$(dirname "$0")/shell/

# Usage

## List Tables

    list_tables

## Table Searching

    # list_tables [keywords] 
    # e.g. list table names contains 'country'
    list_tables country

## Table Query

    # query [table_name]
    # e.g. show a records from table 'country_series_definitions'
    query country_series_definitions

## Records count

    # count [table_name]
    # e.g. show records count of table 'country_series_definitions'
    count country_series_definitions

## Show table schema

    # schema [table_name]
    # e.g. show schema of table 'country_series_definitions'
    schema country_series_definitions

## Table Analysis
TODO

    # analysis [table_name]
    # e.g. get statistics of columns in table 'country_series_definitions'
    analysis country_series_definitions

# Installation
TODO