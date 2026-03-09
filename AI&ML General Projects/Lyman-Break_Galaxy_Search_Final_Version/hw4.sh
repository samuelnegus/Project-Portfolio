#!/bin/bash

TGZ_FILE="$1"
DIR_NAME=$(basename "$TGZ_FILE" .tgz)

tar -xzf "$TGZ_FILE"

Rscript hw4.R cB58_Lyman_break.fit "$DIR_NAME"

