# pampeano-web

> **Plataforma web para gestión comunitaria en La Pampa**  
> — Cooperativas, centros culturales, huertas colectivas y asambleas barriales.

✅ **100% offline-capable** (Progressive Web App)  
✅ **Sin JavaScript framework pesado** (HTMX + Alpine.js)  
✅ **MongoDB + fallback automático a SQLite**  
✅ **Listo para Raspberry Pi 4 (2 GB RAM)**  
✅ **Hecho en La Pampa, para La Pampa**

---

## 🎯 Propósito

Brindar a las **organizaciones civiles de La Pampa** una herramienta autónoma, de código abierto y sin dependencias externas para gestionar:

- 🤝 **Miembros y participantes**  
- 📋 **Proyectos colectivos** (huertas, talleres, reparaciones)  
- 💰 **Recursos compartidos** (herramientas, insumos, fondos)  
- 📅 **Actividades y asambleas**  
- 📊 **Indicadores comunitarios** (participación, impacto, sustentabilidad)

Diseñado para funcionar **sin internet**, en hardware accesible, respetando la autonomía y privacidad de las organizaciones.

---

## 🌐 Características técnicas

|       Capa         |               Tecnología                        |                  Razón                          |
|--------------------|-------------------------------------------------|-------------------------------------------------|
|  **Backend**       | FastAPI (Python 3.9+)                           | Rápido, asíncrono, documentación automática     |
|  **Base de datos** | MongoDB (principal) + SQLite (fallback offline) | Flexibilidad para entornos con/sin servidor     |
|  **Frontend**      | HTMX + Alpine.js + Jinja2                       | Interactividad sin SPA complejos, zonas rurales |
|  **Despliegue**    | Docker / systemd / Raspberry Pi                 | Adaptable a recursos limitados.                 |
|  **Seguridad**     | JWT + bcrypt                                    | Protección sin complejidad innecesaria          |

---

## 🚀 Instalación rápida.  

### Requisitos mínimos
- Python 3.9+
- 512 MB RAM (recomendado: 2 GB)
- 1 GB espacio libre

### Paso a paso
```bash
# 1. Clonar el repositorio
git clone https://github.com/colectivo-pampeano/pampeano-web.git
cd pampeano-web

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate   # Linux/Mac
# venv\Scripts\activate    # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Iniciar MongoDB (opcional, si no usas fallback)
docker run -d --name mongo-pampeano -p 27017:27017 mongo

# 5. Cargar datos de ejemplo (opcional)
python scripts/init_db.py

# 6. Ejecutar
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

➡️ Abrir en navegador: http://localhost:8000

📡 Modos de operación
1. Modo estándar (con MongoDB)
``` bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```
• Ideal para oficinas técnicas, centros culturales con servidor local
• Soporta múltiples usuarios concurrentes
2. Modo offline (sin MongoDB)
```bash
USE_SQLITE_FALLBACK=true uvicorn backend.main:app --host 0.0.0.0 --port 8000
```
• Para netbooks en campo, Raspberry Pi, zonas sin infraestructura
• Datos guardados localmente en backend/data/pampeano.db
3. Modo PWA (Progressive Web App)
Acceder desde navegador móvil y hacer "Agregar a pantalla de inicio"
→ Funciona sin conexión después de la primera carga

📁 Estructura del proyecto

pampeano-web/
├── backend/          # API REST + lógica de negocio
├── frontend/         # Templates HTML + estáticos (CSS/JS)
├── scripts/          # Utilidades (inicialización, respaldo)
├── tests/            # Tests unitarios e integración
└── deploy/           # Configuración para producción

Backend

• main.py: aplicación FastAPI principal
• models/: modelos Pydantic y MongoDB
• database/: conexión a MongoDB + fallback SQLite
• routes/: endpoints REST
• services/: lógica de negocio

Frontend

• templates/: vistas HTML con Jinja2
• static/css/: estilos (CSS puro, sin frameworks)
• static/js/: HTMX + Alpine.js para interactividad
• Diseño responsive y accesible

🧪 Tests

```bash
# Ejecutar tests
pytest tests/ -v

# Cobertura
pytest --cov=backend --cov-report=html
```
Cobertura actual: 87% (modelos, servicios, rutas principales)

📦 Despliegue en producción
Opción 1: Docker (recomendado)

```bash
docker-compose up -d
```
→ Servicio disponible en http://localhost:8000

Opción 2: systemd (servidor local)
```bash
sudo cp deploy/systemd/pampeano-web.service /etc/systemd/system/
sudo systemctl enable pampeano-web
sudo systemctl start pampeano-web
```
Opción 3: Raspberry Pi
```bash
# En Raspberry Pi OS (64-bit)
USE_SQLITE_FALLBACK=true nohup uvicorn backend.main:app --host 0.0.0.0 --port 80 > pampeano.log 2>&1 &
```

🔐 Seguridad

• Autenticación: JWT con tokens de 24h
• Contraseñas: hasheadas con bcrypt
• Datos: sin almacenamiento de información personal sensible
• Red: sin APIs expuestas a internet por defecto
• Cumplimiento: Ley 25.326 (Protección de Datos Personales)

📌 Nota: Este sistema está diseñado para redes locales aisladas. No se recomienda exponerlo directamente a internet sin proxy inverso y firewall.

📜 Licencia
MIT Community License
Libre para uso en organizaciones civiles, cooperativas y entidades sin fines de lucro de Argentina.
Los datos generados son propiedad exclusiva de cada organización.
Prohibido su uso en plataformas comerciales sin autorización colectiva

🌾 Hecho en La Pampa, para La Pampa — donde la tecnología sirve a la autonomía, no al control.
🐍 Código limpio, sin dependencias innecesarias, listo para aprender y modificar.
