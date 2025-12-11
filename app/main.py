import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import get_db_connection

# Importamos los routers (los departamentos)
from app.routers import auth, iot

app = FastAPI(
    title="Ufox IoT Backend",
    description="Backend Modular",
    version="2.0.0"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- STARTUP EVENT (Creación de tablas) ---
@app.on_event("startup")
def startup_db_check():
    max_retries = 10
    for i in range(max_retries):
        try:
            print(f"[INFO] Verificando conexión a BD ({i+1}/{max_retries})...")
            conn = get_db_connection()
            with conn.cursor() as cursor:
                # Tablas (Mismo código de antes)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS mediciones (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        device_id VARCHAR(50),
                        temperatura FLOAT,
                        humedad FLOAT,
                        bateria INT,
                        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        email VARCHAR(100),
                        hashed_password VARCHAR(255) NOT NULL,
                        disabled BOOLEAN DEFAULT FALSE
                    )
                """)
            conn.commit()
            conn.close()
            print("[SUCCESS] DB lista.")
            return
        except Exception as e:
            print(f"[WAIT] Esperando DB... {e}")
            if i < max_retries - 1:
                time.sleep(2)

# --- AQUI UNIMOS TODO ---
app.include_router(auth.router)
app.include_router(iot.router)

@app.get("/")
def home():
    return {"status": "Sistema Modular Online 🚀"}