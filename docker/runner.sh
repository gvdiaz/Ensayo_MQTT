#!/usr/bin/bash 

# Objetivo: Correr script runner para ejecutar scripts de python en contenedor.
# Primer versión para ejecutar scripts en contenedor

# Configuración de script
# set -x

# Carpetas necesarias en proyecto
PATH_REPO="$(cd ../ & cd ../ & pwd)"
PATH_SCRIPTS="${PATH_REPO}/Scripts"
PATH_ENV="$(pwd)/proposal/meteo_mqtt_bridge/"

# bash en imagen snappy_9_gvd
sudo docker run -it --rm --name mqtt_test \
    --env-file "${PATH_ENV}/.env" \
    -v $PATH_SCRIPTS:/src/Scripts \
    python_gvd \
    "bash"
    # -p 8888:8888 \
    # bash
    # "jupyter" "notebook" "--allow-root"
    #'jupyter notebook'
# echo $0 $1 $2