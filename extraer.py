import cloudscraper
import pandas as pd

TOKEN = "5dd1bac1233a1976ef537ff20088936c523fcd60"
URL = "https://app-dataumsa.sociest.org/api/v2/assets/aMogtYSaa7qJJCoF2Tkf2W/data/?format=json&limit=1500"

headers = {
    "Authorization": f"Token {TOKEN}",
    "Accept": "application/json"  # Le decimos al servidor que NO queremos la página web
}

scraper = cloudscraper.create_scraper()
print("Conectando al servidor y solicitando datos en formato JSON...")

response = scraper.get(URL, headers=headers)
print(f"Código de estado HTTP: {response.status_code}")

try:
    datos = response.json()
    if "results" in datos:
        df = pd.DataFrame(datos["results"])
        print("\n--- Vista previa de los datos ---")
        print(df.head())
        
        # Guardamos en CSV
        df.to_csv('datos_historicos.csv', index=False)
        print(f"\n✅ ¡Éxito! Se han descargado y guardado {len(df)} registros históricos en 'datos_historicos.csv'.")
    else:
        print("\n⚠️ Se recibió un JSON, pero sin la clave 'results':")
        print(datos)
except Exception as e:
    print("\n❌ Error: El servidor no devolvió datos JSON. Esto es lo que respondió el servidor:")
    print(response.text[:1000])