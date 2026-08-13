import pandas as pd
import cloudscraper
import os
from datetime import datetime
import time

TOKEN = "5dd1bac1233a1976ef537ff20088936c523fcd60"
URL_BASE = "https://app-dataumsa.sociest.org/api/v2/assets/aMogtYSaa7qJJCoF2Tkf2W/data/"
ARCHIVO_DATOS = "datos_historicos.csv"
LIMITE_REGISTROS_API = 30000  # Límite máximo de registros por consulta

def obtener_datos_historicos():
    """Lee los datos del archivo CSV."""
    if os.path.exists(ARCHIVO_DATOS):
        return pd.read_csv(ARCHIVO_DATOS)
    else:
        return pd.DataFrame()

def obtener_todos_registros_kobo(max_id=None):
    """
    Obtiene TODOS los registros desde KoboToolbox con paginación.
    
    Parámetros:
        max_id: Si se proporciona, obtiene solo registros con _id > max_id
    
    Retorna: DataFrame con todos los registros obtenidos
    """
    registros_totales = []
    scraper = cloudscraper.create_scraper()
    headers = {
        "Authorization": f"Token {TOKEN}",
        "Accept": "application/json"
    }
    
    try:
        # Primera consulta: obtener todos los registros o solo los nuevos
        if max_id is not None:
            # Búsqueda incremental: solo registros nuevos
            url_consulta = f'{URL_BASE}?format=json&limit={LIMITE_REGISTROS_API}&query={{"_id":{{"$gt":{max_id}}}}}'
        else:
            # Búsqueda completa: todos los registros (sin filtro)
            url_consulta = f'{URL_BASE}?format=json&limit={LIMITE_REGISTROS_API}'
        
        print(f"[DEBUG] URL consulta: {url_consulta}")
        
        while url_consulta:
            print(f"[DEBUG] Consultando: {url_consulta[:100]}...")
            response = scraper.get(url_consulta, headers=headers, timeout=30)
            
            if response.status_code != 200:
                print(f"[ERROR] Status code: {response.status_code}")
                break
            
            datos = response.json()
            resultados = datos.get("results", [])
            
            if not resultados:
                print(f"[DEBUG] No hay más resultados. Total acumulado: {len(registros_totales)}")
                break
            
            registros_totales.extend(resultados)
            print(f"[DEBUG] Registros obtenidos en esta consulta: {len(resultados)}, Total acumulado: {len(registros_totales)}")
            
            # Verificar si hay más páginas
            url_consulta = datos.get("next")
            if url_consulta:
                time.sleep(0.5)  # Pequeña pausa entre consultas
        
        print(f"[DEBUG] Total de registros obtenidos: {len(registros_totales)}")
        
        if registros_totales:
            return pd.DataFrame(registros_totales)
        else:
            return pd.DataFrame()
    
    except Exception as e:
        print(f"[ERROR] En obtener_todos_registros_kobo: {str(e)}")
        return pd.DataFrame()

def actualizar_base_datos():
    """
    Actualiza la base de datos desde KoboToolbox.
    
    Estrategia:
    1. Si CSV está vacío: Carga TODOS los registros desde cero
    2. Si CSV tiene registros: Carga incremental (solo registros nuevos)
    3. Detecta registros faltantes y los recupera si es necesario
    
    Retorna: dict con status, mensaje, registros_nuevos, timestamp
    """
    resultado = {
        'exito': False,
        'mensaje': '',
        'registros_nuevos': 0,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    try:
        df_actual = obtener_datos_historicos()
        registros_actuales = len(df_actual)
        
        # Estrategia 1: Si no hay datos, hacer carga completa
        if df_actual.empty:
            print("[INFO] CSV vacío. Iniciando carga completa desde KoboToolbox...")
            df_nuevos = obtener_todos_registros_kobo(max_id=None)
            
            if df_nuevos.empty:
                resultado['exito'] = False
                resultado['mensaje'] = "❌ No se pudieron obtener registros desde KoboToolbox"
                return resultado
            
            df_nuevos = df_nuevos.drop_duplicates(subset=['_id'], keep='first')
            df_nuevos.to_csv(ARCHIVO_DATOS, index=False)
            
            resultado['exito'] = True
            resultado['registros_nuevos'] = len(df_nuevos)
            resultado['mensaje'] = f"✅ Carga inicial completada: {len(df_nuevos)} registros cargados"
            return resultado
        
        # Estrategia 2: Si hay datos, intentar carga incremental
        max_id = int(df_actual['_id'].max())
        df_nuevos = obtener_todos_registros_kobo(max_id=max_id)
        
        # Verificar si hay registros nuevos
        if df_nuevos.empty:
            # Si no hay nuevos, intentar carga completa de verificación
            print("[DEBUG] No hay registros con _id > max_id. Verificando integridad...")
            df_verificacion = obtener_todos_registros_kobo(max_id=None)
            
            if df_verificacion.empty:
                resultado['exito'] = True
                resultado['mensaje'] = "Base de datos actualizada. Sin registros nuevos."
                resultado['registros_nuevos'] = 0
                return resultado
            
            total_en_kobo = len(df_verificacion)
            registros_faltantes = total_en_kobo - registros_actuales
            
            if registros_faltantes > 0:
                print(f"[WARNING] Registros faltantes detectados: {registros_faltantes}")
                # Usar la carga completa como fuente de verdad
                df_verificacion = df_verificacion.drop_duplicates(subset=['_id'], keep='first')
                df_verificacion.to_csv(ARCHIVO_DATOS, index=False)
                
                resultado['exito'] = True
                resultado['registros_nuevos'] = registros_faltantes
                resultado['mensaje'] = f"✅ Se recuperaron {registros_faltantes} registro(s) faltante(s). Total: {total_en_kobo}"
                return resultado
            else:
                resultado['exito'] = True
                resultado['mensaje'] = "Base de datos actualizada. Sin registros nuevos."
                resultado['registros_nuevos'] = 0
                return resultado
        
        # Procesar registros nuevos
        df_nuevos = df_nuevos.drop_duplicates(subset=['_id'], keep='first')
        df_final = pd.concat([df_actual, df_nuevos], ignore_index=True)
        df_final = df_final.drop_duplicates(subset=['_id'], keep='first')
        df_final.to_csv(ARCHIVO_DATOS, index=False)
        
        resultado['exito'] = True
        resultado['registros_nuevos'] = len(df_nuevos)
        resultado['mensaje'] = f"✅ Se incorporaron {len(df_nuevos)} registro(s) nuevo(s). Total: {len(df_final)}"
        
        return resultado
        
    except Exception as e:
        print(f"[ERROR] En actualizar_base_datos: {str(e)}")
        resultado['mensaje'] = f"❌ Error al actualizar: {str(e)}"
        return resultado