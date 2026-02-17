import os
import requests
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Cerebro de Maya - Capa 1")

# --- CONFIGURACIÓN DE SEGURIDAD (CORS) ---
# Esto permite que tu HTML (puerto 8080) se comunique con este Python (puerto 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CONFIGURACIÓN DE HEYGEN ---
# Pega aquí la llave que acabas de generar en tu cuenta nueva
HEYGEN_API_KEY = "sk_V2_hgu_khwPexdXoX7_0SSDU341LWx6PCUnmIJBl0YhF5OAsSHi" 

@app.get("/test")
async def test():
    """Ruta de prueba para verificar que el servidor está vivo"""
    return {
        "status": "online",
        "message": "Capa 1 funcionando. El puerto 8000 está abierto."
    }

@app.get("/get-token")
async def get_token():
    """Obtiene el token de acceso para el Avatar de HeyGen"""
    print("\n[DEBUG] Solicitando nuevo token a HeyGen...")
    
    url = "https://api.heygen.com/v1/streaming.create_token"
    headers = {
        "x-api-key": HEYGEN_API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers)
        
        # Si HeyGen responde algo distinto a 200, mostramos el error exacto
        if response.status_code != 200:
            print(f"[ERROR] HeyGen respondió: {response.status_code} - {response.text}")
            raise HTTPException(
                status_code=response.status_code, 
                detail=f"Error de HeyGen: {response.text}"
            )

        data = response.json()
        token = data.get("data", {}).get("token")
        
        if not token:
            print("[ERROR] La respuesta de HeyGen no contiene un token.")
            raise HTTPException(status_code=500, detail="Token no encontrado en la respuesta")

        print(f"[SUCCESS] Token obtenido correctamente: {token[:15]}...")
        return {"token": token}

    except requests.exceptions.RequestException as e:
        print(f"[CRÍTICO] Fallo de conexión con HeyGen: {str(e)}")
        raise HTTPException(status_code=500, detail="Error de red al conectar con HeyGen")

if __name__ == "__main__":
    print("--- INICIANDO BACKEND (CAPA 1) ---")
    # Aseguramos que corra en el puerto 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)
