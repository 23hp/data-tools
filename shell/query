#!/bin/bash

# import var project & dataset
source $(dirname "$0")/set_config

table=$1

set -xe

bq query --nouse_legacy_sql "SELECT * FROM ${project}.${dataset}.${table} LIMIT 1"
