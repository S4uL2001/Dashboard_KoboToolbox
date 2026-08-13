from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/webhook-kobo")
async def recibir_kobo(request: Request):
    datos = await request.json()
    print("¡DATOS RECIBIDOS DESDE KOBO!")
    print(datos)
    return {"status": "success"}