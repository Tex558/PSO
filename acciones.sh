#!/bin/bash

accion=$1

case "$accion" in
    diff)
        diff archivo1.txt archivo2.txt
        ;;
    cp)
        cp archivo1.txt copia_archivo1.txt
        ;;
    mv)
        mv copia_archivo1.txt movido_archivo1.txt
        ;;
    md5sum)
        md5sum archivo1.txt
        ;;
    sha256sum)
        sha256sum archivo1.txt
        ;;
    date)
        date
        ;;
    cat)
        cat archivo1.txt
        ;;
    echo)
        echo "Texto de ejemplo" >> archivo1.txt
        echo "Texto agregado a archivo1.txt"
        ;;
    *)
        echo "Acción no reconocida: $accion"
        ;;
esac
    