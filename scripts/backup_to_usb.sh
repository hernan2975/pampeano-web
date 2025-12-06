#!/bin/bash
# Script para respaldo automático a USB (Linux/Raspberry Pi)
# Ejecutar al insertar USB con etiqueta "PAMPEANO_BACKUP"

USB_LABEL="PAMPEANO_BACKUP"
MOUNT_POINT="/media/pampeano"
BACKUP_DIR="$MOUNT_POINT/pampeano_backup_$(date +%Y%m%d_%H%M%S)"

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Verificar requisitos
if ! command -v jq &> /dev/null; then
    log "❌ jq no encontrado. Instale con: sudo apt install jq"
    exit 1
fi

# Verificar si hay USB con la etiqueta correcta
USB_DEVICE=$(lsblk -f 2>/dev/null | grep "$USB_LABEL" | head -1 | awk '{print "/dev/" $1}')

if [ -z "$USB_DEVICE" ]; then
    log "❌ No se encontró USB con etiqueta '$USB_LABEL'"
    log "💡 Cree un USB con esta etiqueta usando: sudo e2label /dev/sdX $USB_LABEL"
    exit 1
fi

log "✅ USB detectado: $USB_DEVICE"

# Montar USB
sudo mkdir -p "$MOUNT_POINT"
if ! sudo mount "$USB_DEVICE" "$MOUNT_POINT" 2>/dev/null; then
    log "❌ Error al montar USB"
    exit 1
fi

# Verificar espacio libre (>100 MB)
FREE_SPACE=$(df "$MOUNT_POINT" | tail -1 | awk '{print $4}')
if [ "$FREE_SPACE" -lt 102400 ]; then
    log "❌ Espacio insuficiente en USB (< 100 MB libres)"
    sudo umount "$MOUNT_POINT" 2>/dev/null
    exit 1
fi

log "✅ USB montado en $MOUNT_POINT"

# Crear carpeta de respaldo
mkdir -p "$BACKUP_DIR"

# Respaldo de base de datos
if [ -f "backend/data/pampeano.db" ]; then
    # Modo SQLite
    cp "backend/data/pampeano.db" "$BACKUP_DIR/"
    log "✅ Respaldo: pampeano.db (SQLite)"
elif [ -n "$MONGODB_URL" ] || [ -f "/etc/mongod.conf" ]; then
    # Modo MongoDB: usar mongodump si está disponible
    if command -v mongodump &> /dev/null; then
        mongodump --uri="${MONGODB_URL:-mongodb://localhost:27017/pampeano}" --out="$BACKUP_DIR/mongodb_dump" --quiet
        log "✅ Respaldo: MongoDB dump"
    else
        log "⚠️  mongodump no encontrado. Instale con: sudo apt install mongodb-database-tools"
        # Respaldo mínimo: exportar como JSON
        if command -v mongoexport &> /dev/null; then
            mkdir -p "$BACKUP_DIR/json_export"
            for collection in organizaciones proyectos participantes; do
                mongoexport --uri="${MONGODB_URL:-mongodb://localhost:27017/pampeano}" \
                    --collection="$collection" --out="$BACKUP_DIR/json_export/$collection.json" --quiet
            done
            log "✅ Respaldo: JSON export"
        fi
    fi
else
    log "⚠️  No se encontró base de datos para respaldar"
fi

# Respaldo de configuración
if [ -f ".env" ]; then
    cp ".env" "$BACKUP_DIR/pampeano_config.env"
    # Eliminar credenciales sensibles del backup
    if command -v sed &> /dev/null; then
        sed -i 's/MONGODB_URL=.*/MONGODB_URL=**REDACTADO**/' "$BACKUP_DIR/pampeano_config.env"
        sed -i 's/SECRET_KEY=.*/SECRET_KEY=**REDACTADO**/' "$BACKUP_DIR/pampeano_config.env"
    fi
    log "✅ Respaldo: configuración (credenciales redactadas)"
fi

# Respaldo de logs (últimas 24h)
if [ -d "logs" ]; then
    find logs -type f -mtime -1 -exec cp {} "$BACKUP_DIR/" 2>/dev/null \;
    log "✅ Respaldo: logs recientes"
fi

# Generar índice de respaldo
cat > "$BACKUP_DIR/indice.txt" <<EOF
Respaldo automático - Pampeano Web
Fecha: $(date)
Sistema: $(uname -n)
Versión: 1.0.0

Contenido:
$(ls -lh "$BACKUP_DIR" | grep -v "indice.txt" | awk '{print "- " $9 " (" $5 ")"}')

Instrucciones de restauración:
1. Copie los archivos a la instalación de Pampeano Web
2. Para SQLite: reemplace backend/data/pampeano.db
3. Para MongoDB: use mongorestore --dir="$BACKUP_DIR/mongodb_dump"
EOF

log "✅ Respaldo completado en $BACKUP_DIR"

# Desmontar
sudo umount "$MOUNT_POINT" 2>/dev/null
log "💾 USB desmontado. Puede retirarlo."

# Notificación visual (para Raspberry Pi con pantalla)
if command -v zenity &> /dev/null; then
    zenity --info --text="✅ Respaldo completado.\nPuede retirar el USB." \
           --title="Pampeano Web" --width=300 --timeout=10 2>/dev/null &
elif command -v notify-send &> /dev/null; then
    notify-send "Pampeano Web" "✅ Respaldo completado. Puede retirar el USB." -t 5000
fi

exit 0
