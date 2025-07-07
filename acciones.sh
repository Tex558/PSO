#!/bin/bash

accion=$1
archivo=$2
param3=$3
backup_dir="./backups"
repo_dir=".mini-git"
log_file="$repo_dir/log/log.txt"
hashes_file="$repo_dir/hashes/hashes.txt"

if [ "$accion" != "init" ] && [ ! -d "$repo_dir" ]; then
    echo "ERROR: Repositorio no inicializado. Ejecute 'init' primero." >&2
    exit 1
fi

case "$accion" in
    init)
        mkdir -p $repo_dir/{versions,log,hashes,branches}
        touch "$log_file" "$hashes_file"
        echo "Repositorio inicializado"
        ;;
    save_version)
        if [ -z "$archivo" ] || [ -z "$param3" ]; then
            echo "ERROR: Faltan parámetros. Uso: save_version <archivo> <nombre_version>" >&2
            exit 1
        fi
        
        if [ ! -f "$archivo" ]; then
            echo "ERROR: El archivo $archivo no existe" >&2
            exit 1
        fi
        
        cp "$archivo" "$repo_dir/versions/$param3"
        
        timestamp=$(date +"%Y-%m-%d %H:%M:%S")
        hash_value=$(sha256sum "$archivo" | awk '{print $1}')
        echo "$timestamp|save_version|$param3|$hash_value" >> "$log_file"
        echo "$param3 $hash_value" >> "$hashes_file"
        
        echo "Versión guardada: $param3"
        ;;
    compare)
        if [ -z "$archivo" ] || [ -z "$param3" ]; then
            echo "ERROR: Faltan parámetros. Uso: compare <archivo_actual> <archivo_version>" >&2
            exit 1
        fi
        
        if [ ! -f "$param3" ]; then
            echo "ERROR: La versión $param3 no existe" >&2
            exit 1
        fi
        
        diff --color -u "$param3" "$archivo"
        ;;
    history)
        if [ ! -f "$log_file" ]; then
            echo "No hay historial disponible"
            exit 0
        fi
        column -t -s "|" "$log_file"
        ;;
    md5sum)
        if [ -z "$archivo" ]; then
            echo "ERROR: Debe especificar un archivo" >&2
            exit 1
        fi
        if [ ! -f "$archivo" ]; then
            echo "ERROR: El archivo $archivo no existe" >&2
            exit 1
        fi
        md5sum "$archivo"
        ;;
    sha256sum)
        if [ -z "$archivo" ]; then
            echo "ERROR: Debe especificar un archivo" >&2
            exit 1
        fi
        if [ ! -f "$archivo" ]; then
            echo "ERROR: El archivo $archivo no existe" >&2
            exit 1
        fi
        sha256sum "$archivo"
        ;;
    cat)
        if [ -z "$archivo" ]; then
            echo "ERROR: Debe especificar un archivo" >&2
            exit 1
        fi
        if [ ! -f "$archivo" ]; then
            echo "ERROR: El archivo $archivo no existe" >&2
            exit 1
        fi
        cat "$archivo"
        ;;
    echo)
        if [ -z "$archivo" ] || [ -z "$param3" ]; then
            echo "ERROR: Uso: echo <archivo> <texto>" >&2
            exit 1
        fi
        texto_limpio=$(echo "$param3" | sed -e 's/^"//' -e 's/"$//')
        echo "$texto_limpio" >> "$archivo"
        echo "Texto añadido a $archivo"
        ;;
    create_branch)
        if [ -z "$archivo" ] || [ -z "$param3" ]; then
            echo "ERROR: Uso: create_branch <archivo> <nombre_rama>" >&2
            exit 1
        fi
        
        if [ ! -f "$archivo" ]; then
            echo "ERROR: El archivo $archivo no existe" >&2
            exit 1
        fi
        
        cp "$archivo" "$repo_dir/branches/$param3"
        echo "$(date +"%Y-%m-%d %H:%M:%S")|create_branch|$param3" >> "$log_file"
        echo "Rama creada: $param3"
        ;;
    merge_branch)
        if [ -z "$archivo" ] || [ -z "$param3" ]; then
            echo "ERROR: Uso: merge_branch <archivo_destino> <nombre_rama>" >&2
            exit 1
        fi
        
        if [ ! -f "$repo_dir/branches/$param3" ]; then
            echo "ERROR: La rama $param3 no existe" >&2
            exit 1
        fi
        
        cp "$repo_dir/branches/$param3" "$archivo"
        echo "$(date +"%Y-%m-%d %H:%M:%S")|merge_branch|$param3" >> "$log_file"
        echo "Rama fusionada: $param3 → $(basename "$archivo")"
        ;;
    compress_versions)
        tar -czf "$repo_dir/versions.tar.gz" "$repo_dir/versions"/*
        echo "Versiones comprimidas en versions.tar.gz"
        ;;
    export_csv)
        if [ ! -f "$log_file" ]; then
            echo "No hay historial para exportar"
            exit 0
        fi
        awk -F "|" '{print $1","$2","$3","$4}' "$log_file" > historial.csv
        echo "Historial exportado a historial.csv"
        ;;
    backup_local)
        fecha=$(date +%Y%m%d%H%M%S)
        mkdir -p "$backup_dir"
        tar -czf "$backup_dir/mini-git_backup_$fecha.tar.gz" "$repo_dir"
        echo "Backup local creado: $backup_dir/mini-git_backup_$fecha.tar.gz"
        ;;
    backup_cloud)
        if ! command -v rclone &> /dev/null; then
            echo "ERROR: rclone no está instalado" >&2
            exit 1
        fi
        fecha=$(date +%Y%m%d%H%M%S)
        rclone copy "$repo_dir" "google_drive:/mini-git_backups/backup_$fecha" --progress
        echo "Backup en Google Drive creado: backup_$fecha"
        ;;
    *)
        echo "ERROR: Acción no reconocida: $accion" >&2
        echo "Acciones disponibles: init, save_version, compare, history, md5sum, sha256sum, cat, echo, create_branch, merge_branch, compress_versions, export_csv, backup_local, backup_cloud" >&2
        exit 1
        ;;
esac