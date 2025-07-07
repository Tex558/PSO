#!/bin/bash

accion=$1
archivo=$2
backup_dir="./backups"
remote_drive="google_drive:/mini-git_backups"

# Verifica si el archivo está vacío
if [ -z "$archivo" ]; then
    echo "ERROR: No se ha especificado un archivo." >&2  # Redirigir error a stderr
    exit 1
fi

case "$accion" in
    init)
        mkdir -p .mini-git/versions
        mkdir -p .mini-git/log
        mkdir -p .mini-git/hashes
        mkdir -p .mini-git/branches
        echo "Repositorio inicializado"
        ;;
    save_version)
        # Guardar versión actual del archivo
        version=$(date +%Y%m%d%H%M%S)
        cp "$archivo" .mini-git/versions/"$archivo"_v$version.txt
        echo "Guardada nueva versión $archivo_v$version.txt" >> .mini-git/log.txt
        sha256sum "$archivo" >> .mini-git/hashes.txt
        ;;
    compare)
        # Comparar el archivo con la versión guardada
        archivo_version=$3
        diff "$archivo" ".mini-git/versions/$archivo_version"
        ;;
    history)
        # Mostrar historial de commits
        cat .mini-git/log.txt
        ;;
    md5sum)
        # Generar MD5
        md5sum "$archivo"
        ;;
    sha256sum)
        # Generar SHA256
        sha256sum "$archivo"
        ;;
    cat)
        # Mostrar contenido de archivo
        cat "$archivo"
        ;;
    echo)
        # Escribir en archivo
        texto=$3
        echo "$texto" >> "$archivo"
        ;;
    create_branch)
        # Crear una rama
        branch_name=$3
        if [ -z "$branch_name" ]; then
            echo "Se requiere el nombre de la rama"
            exit 1
        fi
        cp "$archivo" ".mini-git/branches/$branch_name"
        echo "Rama '$branch_name' creada"
        ;;
    merge_branch)
        # Fusionar una rama
        branch_name=$3
        if [ -z "$branch_name" ]; then
            echo "Se requiere el nombre de la rama"
            exit 1
        fi
        cp ".mini-git/branches/$branch_name" "$archivo"
        echo "Rama '$branch_name' fusionada"
        ;;
    compress_versions)
        # Comprimir versiones viejas
        tar -czf .mini-git/versions.tar.gz .mini-git/versions/*
        echo "Versiones comprimidas en versions.tar.gz"
        ;;
    export_csv)
        # Exportar historial a CSV
        while IFS= read -r line
        do
            fecha=$(echo $line | awk '{print $1}')
            accion=$(echo $line | awk '{print $2}')
            archivo=$(echo $line | awk '{print $3}')
            hash=$(echo $line | awk '{print $4}')
            echo "$fecha,$accion,$archivo,$hash" >> historial.csv
        done < .mini-git/log.txt
        echo "Historial exportado a historial.csv"
        ;;
    backup_local)
        # Crear un backup local de .mini-git
        fecha=$(date +%Y%m%d%H%M%S)
        mkdir -p "$backup_dir"
        cp -r .mini-git "$backup_dir/mini-git_backup_$fecha"
        echo "Backup local realizado con éxito en $backup_dir/mini-git_backup_$fecha"
        ;;
    backup_cloud)
        # Copiar archivos del repositorio a Google Drive usando rclone
        fecha=$(date +%Y%m%d%H%M%S)
        rclone copy .mini-git $remote_drive/mini-git_backup_$fecha --progress
        echo "Backup realizado en Google Drive como mini-git_backup_$fecha"
        ;;
    *)
        echo "ERROR: Acción no reconocida: $accion" >&2  # Redirigir error a stderr
        ;;
esac
