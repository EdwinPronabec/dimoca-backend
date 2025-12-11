from fastapi import APIRouter, status, Query
from app.database import get_db_connection
from app.schemas import SigfoxPayload
from typing import List, Optional

router = APIRouter(tags=["IoT Sigfox"])

@router.post("/callback-uplink", status_code=status.HTTP_200_OK)
def receive_sigfox_data(payload: SigfoxPayload):
    print(f"[IOT] Dato recibido - Device: {payload.device}, Temp: {payload.temp}")
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "INSERT INTO mediciones (device_id, temperatura, humedad, bateria) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (payload.device, payload.temp, payload.hum, payload.bat))
        conn.commit()
        conn.close()
        return {"status": "success", "message": "Datos procesados y almacenados"}
    except Exception as e:
        print(f"[ERROR] Fallo al guardar datos IoT: {e}")
        return {"status": "error", "detail": str(e)}

@router.get("/mediciones", status_code=status.HTTP_200_OK)
def get_measurements(
    limit: int = Query(20, ge=1, le=500),
    start_date: Optional[str] = None, # Formato esperado: YYYY-MM-DD
    end_date: Optional[str] = None
):
    conn = get_db_connection()
    results = []
    try:
        with conn.cursor() as cursor:
            # CASO A: FILTRO POR FECHAS (Prioridad Alta)
            if start_date and end_date:
                # Le sumamos horas al final del día para cubrir todo el día 'Hasta'
                # Ejemplo: Si pides hasta el 2025-12-11, buscamos hasta 2025-12-11 23:59:59
                sql = """
                    SELECT * FROM mediciones 
                    WHERE fecha >= %s AND fecha <= CONCAT(%s, ' 23:59:59')
                    ORDER BY fecha DESC
                """
                cursor.execute(sql, (start_date, end_date))
            
            # CASO B: FILTRO POR CANTIDAD (Por defecto)
            else:
                sql = "SELECT * FROM mediciones ORDER BY fecha DESC LIMIT %s"
                cursor.execute(sql, (limit,))
                
            results = cursor.fetchall()
    finally:
        conn.close()
    return results