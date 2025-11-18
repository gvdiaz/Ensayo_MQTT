#!/usr/bin/bash 

# Objetivo: Correr script runner para ejecutar scripts de python en contenedor.
# Primer versión para ejecutar scripts en contenedor

# Configuración de script
set -x

PATH_REPO="$(cd ../ && cd ../ && pwd)"
PATH_SCRIPTS="${PATH_REPO}/Scripts"
PATH_VECTORES="${PATH_REPO}/Vectores"
PATH_UTILS="${PATH_REPO}/utils"
PATH_TOKEN="${PATH_REPO}/token"
PATH_OUTPUT="${PATH_REPO}/output"

# echo "Entradas a script $0"
# echo $1
# echo $2

# bash en imagen snappy_9_gvd
sudo docker run --rm --name snappy_11_develop \
    -v $PATH_SCRIPTS:/src/Scripts \
    -v $PATH_VECTORES:/src/Vectores \
    -v $PATH_UTILS:/src/utils \
    -v $PATH_TOKEN:/src/token \
    -v $PATH_OUTPUT:/src/Output \
    --workdir /src/Scripts \
    snappy_11_gvd \
    "python3" $1 $2
    # -p 8888:8888 \
    # bash
    # "jupyter" "notebook" "--allow-root"
    #'jupyter notebook'
# echo $0 $1 $2