#!/bin/bash

# import var project & dataset
source $(dirname "$0")/set_config

table=$1

set -xe

bq query -n 999 --nouse_legacy_sql \
  "SELECT column_name,data_type,is_nullable  \
    FROM ${project}.${dataset}.INFORMATION_SCHEMA.COLUMNS  \
    WHERE table_name='${table}'  \
    ORDER BY column_name"

