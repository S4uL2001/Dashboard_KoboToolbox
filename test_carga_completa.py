#!/usr/bin/env python3
"""
Script de prueba para verificar que se carguen todos los registros desde KoboToolbox.
"""

import sys
sys.path.insert(0, '/workspaces/Dashboard_KoboToolbox')

from logica_etl import obtener_todos_registros_kobo, obtener_datos_historicos
import pandas as pd
import os

print("=" * 80)
print("PRUEBA DE CARGA COMPLETA DE REGISTROS DESDE KOBOTOOLBOX")
print("=" * 80)

# Verificar CSV actual
if os.path.exists("datos_historicos.csv"):
    df_actual = obtener_datos_historicos()
    print(f"\n📊 Estado actual del CSV:")
    print(f"   - Registros en CSV: {len(df_actual)}")
    if not df_actual.empty and '_id' in df_actual.columns:
        print(f"   - ID mínimo: {df_actual['_id'].min()}")
        print(f"   - ID máximo: {df_actual['_id'].max()}")
else:
    print("\n📊 El archivo datos_historicos.csv no existe aún")

print("\n🔄 Iniciando carga completa desde KoboToolbox...")
print("   (Sin filtro de ID, obteniendo TODOS los registros disponibles)")

df_kobo = obtener_todos_registros_kobo(max_id=None)

if df_kobo.empty:
    print("\n❌ ERROR: No se obtuvo ningún registro desde KoboToolbox")
else:
    print(f"\n✅ Carga completada exitosamente")
    print(f"   - Registros obtenidos: {len(df_kobo)}")
    print(f"   - ID mínimo: {df_kobo['_id'].min()}")
    print(f"   - ID máximo: {df_kobo['_id'].max()}")
    
    # Detectar duplicados
    duplicados = df_kobo.duplicated(subset=['_id']).sum()
    if duplicados > 0:
        print(f"   - ⚠️  Duplicados detectados: {duplicados}")
        df_kobo_limpio = df_kobo.drop_duplicates(subset=['_id'], keep='first')
        print(f"   - ✅ Después de eliminar duplicados: {len(df_kobo_limpio)}")
    
    # Mostrar información de columnas clave
    print(f"\n📋 Columnas en los datos obtenidos: {len(df_kobo.columns)}")
    
    # Verificar columnas esperadas
    columnas_esperadas = ['_id', 'group_bo0sv10/Facultad', 'group_bo0sv10/_2_2_Carrera']
    for col in columnas_esperadas:
        if col in df_kobo.columns:
            print(f"   ✅ {col} encontrada")
        else:
            print(f"   ❌ {col} NO encontrada")

print("\n" + "=" * 80)
print("FIN DE LA PRUEBA")
print("=" * 80)
