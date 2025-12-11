# 🐳 Guía de Despliegue: Backend Ufox (FastAPI + MySQL)

Este documento detalla la arquitectura, la configuración de los contenedores y los comandos necesarios para levantar el entorno de desarrollo local.

---

## 1. Arquitectura del Sistema

Estamos utilizando **Docker Compose** para orquestar dos servicios independientes que se comunican dentro de una red virtual privada creada por Docker.

### **Contenedor 1: `db` (MySQL 8.0)**  
- **Persistencia:** Usa un volumen `db_data` para conservar los datos.  
- **Puerto:** Expone **3306** para inspección desde tu PC.  
- **Configuración:** Usa las variables definidas en `.env`.

### **Contenedor 2: `api` (FastAPI)**  
- **Entorno:** Python 3.11 (Slim).  
- **Dependencias:** Gestionadas vía `requirements.txt`.  
- **Conexión:** Se conecta al host interno `db`.  
- **Puerto:** Expone **8000** para acceder a la API.

---

## 2. Explicación de la Configuración

### 🧱 A. Dockerfile (Receta de la API)

- Imagen base: `python:3.11-slim`  
- Instala dependencias desde `requirements.txt`  
- Usa `uvicorn` con `--reload` para hot-reload en desarrollo

---

### 🐙 B. Docker Compose (`docker-compose.yml`)

- `env_file: .env`: carga credenciales y configuración  
- `depends_on: - db`: asegura inicio de MySQL antes de la API  
- `volumes`: sincroniza tu carpeta local con la carpeta del contenedor  

---

### 🔐 C. Variables de Entorno (.env)

- `DB_HOST=db` *(clave para que FastAPI encuentre MySQL)*  
- `DB_USER`, `DB_PASS`, `DB_NAME`: definidos en tu `.env`

---

## 3. Comandos de Ejecución

### 🚀 Iniciar el Proyecto (primera vez o cambios en librerías)
```bash
docker-compose up --build
```

### ▶️ Uso Diario
```bash
docker-compose up
```
> Agrega `-d` para ejecutarlo en segundo plano.

### 🛑 Detener el Proyecto
```bash
CTRL + C
docker-compose down
```

### 🧹 Limpieza Total (borrar base de datos)
```bash
docker-compose down -v
```

---

## 4. Verificación y Acceso

### 📘 Documentación Automática (Swagger UI)
http://localhost:8000/docs

### 🗄 Base de Datos (Acceso Externo)
- **Host:** localhost  
- **Port:** 3306  
- **User:** root (o el de `.env`)  
- **Pass:** root (o el de `.env`)  
- **Database:** iot_db  

---

## 5. Solución de Problemas Comunes

### ❌ Connection refused (MySQL)
MySQL puede tardar en arrancar. Espera unos segundos o reinicia el contenedor.

### ❌ Port already in use
Revisa que no tengas **XAMPP**, **MySQL local** o servicios similares ejecutándose.

---
