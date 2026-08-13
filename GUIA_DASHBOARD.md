# 📊 Guía del Dashboard UMSA - Tienda Universitaria

## Descripción General

El dashboard es una herramienta interactiva para analizar respuestas de encuestas de demanda de la Tienda Universitaria UMSA. Proporciona análisis por facultad, carrera, tipo de participante y detección de registros duplicados.

---

## 🚀 Cómo Ejecutar

```bash
cd /workspaces/Dashboard_KoboToolbox
streamlit run app.py
```

El dashboard se abrirá automáticamente en tu navegador (normalmente en `http://localhost:8501`).

---

## 📍 Secciones del Dashboard

### 1️⃣ TAB: "Resumen General" 📊

**Descripción:**
Vista general de toda la base de datos con métricas principales y distribuciones globales.

**Métricas Mostradas:**
- 📋 **Total de Respuestas**: Cantidad total de registros válidos
- 🏫 **Facultades**: Número de facultades presentes en los datos
- 🎓 **Carreras**: Número total de carreras/programas únicos
- 👥 **Estudiantes/Egresados**: Desglose por tipo de participante

**Secciones:**
1. **Respuestas por Facultad**
   - Tabla con cantidad de respuestas por facultad
   - Gráfico de barras horizontal ordenado por cantidad

2. **Respuestas por Carrera**
   - Tabla con cantidad de respuestas por carrera (primeras 20)
   - Gráfico de barras horizontal con todas las carreras

3. **Análisis: Estudiantes vs Egresados**
   - Cantidad de estudiantes de pregrado
   - Cantidad de egresados
   - Porcentaje de egresados
   - Gráfico de pastel con distribución

---

### 2️⃣ TAB: "Análisis por Facultad" 🏫

**Descripción:**
Análisis detallado de una facultad específica, incluyendo sus carreras y distribuación de participantes.

**Cómo Usar:**
1. Selecciona una facultad del dropdown en la parte superior
2. El dashboard actualiza automáticamente con la información de esa facultad

**Información Mostrada:**

**A) Métricas de la Facultad:**
- 📋 Total de respuestas en la facultad
- 🎓 Número de carreras
- 👥 Desglose estudiantes/egresados

**B) Carreras de la Facultad:**
- Tabla con todas las carreras y cantidad de respuestas
- Gráfico de barras con distribución de carreras

**C) Distribución por Tipo de Participante:**
- Gráfico de barras mostrando estudiantes vs egresados
- Distribuación específica de la facultad

**D) Datos Detallados:**
- Tabla con registros individuales de la facultad (primeros 20)
- Columnas: Número de Registro, Facultad, Carrera, Tipo de Participante

---

### 3️⃣ TAB: "Duplicados" ⚠️

**Descripción:**
Detección y análisis de registros duplicados en la base de datos.

**Métodos de Detección:**
- Se identifican por **Número de Registro Universitario** (campo clave)
- Un mismo estudiante respondiendo múltiples veces se detecta como duplicado

**Métricas Principales:**
- 📋 **Total de Registros**: Cantidad total de respuestas
- ✅ **Registros Únicos**: Registros sin duplicados
- ⚠️ **Registros Duplicados**: Cantidad de respuestas duplicadas
- 📊 **% Duplicados**: Porcentaje del total

**Análisis Disponibles:**

**A) Duplicados por Facultad:**
- Tabla: Facultad y cantidad de registros duplicados
- Gráfico: Visualización con escala de colores (rojo = más duplicados)

**B) Duplicados por Carrera:**
- Tabla: Carrera y cantidad de registros duplicados
- Gráfico: Visualización ordenada

**C) Tabla Detallada de Duplicados:**
- Información completa de cada registro duplicado
- Columnas: Número de Registro, Facultad, Carrera, Tipo, Timestamp
- Ordenada por Número de Registro para facilitar comparación

---

## 🔄 Botón "Actualizar Datos"

**Ubicación:** Parte superior derecha del dashboard

**Función:**
Sincroniza la base de datos local con los datos más recientes de KoboToolbox.

**Proceso:**
1. Conecta con el servidor de KoboToolbox
2. Obtiene registros nuevos desde la última actualización
3. Incorpora los nuevos registros sin crear duplicados
4. Actualiza automáticamente todas las métricas y gráficos
5. Muestra mensaje de éxito o error

**Mensajes Posibles:**
- ✅ "Se incorporaron X registro(s) nuevo(s)"
- ✅ "Sin registros nuevos"
- ❌ "Error al actualizar: [descripción del error]"

---

## ⏱️ Timestamp de Actualización

Se muestra debajo del botón "Actualizar Datos" con la fecha y hora de la última sincronización.

Ejemplo: `⏱️ Última actualización: 2026-08-13 14:30:45`

---

## 📊 Interpretación de Datos

### Tipos de Participante

Los participantes se clasifican en:

1. **Estudiante de Pregrado**
   - Incluye estudiantes en cualquier año (1-5)
   - Valor en BD: 'anula' o 'semestral'

2. **Egresado**
   - Personas que ya completaron sus estudios
   - Valor en BD: 'egresado'

### Estructura Jerárquica

```
Base de Datos
├── Facultad (13 total)
│   ├── Carrera (58 total)
│   │   ├── Estudiante
│   │   └── Egresado
│   └── Programa (solo algunas facultades)
│       └── Estudiante
└── Registros Duplicados (12 total)
```

---

## 💡 Casos de Uso

### Caso 1: Revisar estado actual de la encuesta
1. Abre el TAB "Resumen General"
2. Observa las métricas principales
3. Revisa las gráficas de distribución

### Caso 2: Analizar una facultad específica
1. Ve al TAB "Análisis por Facultad"
2. Selecciona la facultad deseada
3. Analiza carreras, estudiantes/egresados y datos detallados

### Caso 3: Identificar y resolver duplicados
1. Abre el TAB "Duplicados"
2. Revisa la tabla detallada
3. Identifica qué registros están duplicados
4. Contacta a las personas para validar
5. Marca en la fuente si es necesario resolver

### Caso 4: Actualizar datos desde KoboToolbox
1. Click en el botón "🔄 Actualizar Datos"
2. Espera el mensaje de confirmación
3. El dashboard se recarga automáticamente
4. Verifica que las métricas cambiaron

---

## 🔍 Problemas Comunes y Soluciones

### Problema: El dashboard carga lentamente
**Solución:** 
- Es normal con muchos registros
- La primera carga toma más tiempo
- Después se cachean los datos

### Problema: "Actualizar Datos" muestra error
**Solución:**
- Verifica conexión a internet
- Revisa que el token de KoboToolbox sea válido
- Comprueba que la URL base sea correcta

### Problema: Los gráficos no se ven bien
**Solución:**
- Intenta hacer zoom in/out en el navegador
- Redimensiona la ventana del navegador
- Recarga la página (F5)

### Problema: Falta información de alguna facultad
**Solución:**
- Verifica que hay registros en esa facultad en el TAB "Resumen General"
- Es posible que no haya respuestas de esa facultad aún

---

## 📋 Diccionarios de Traducción

El dashboard automáticamente traduce los valores de KoboToolbox (que vienen en formato "slug") a nombres legibles:

### Ejemplo de Facultades:
- `facultad_de_ciencias_econ_mica` → Facultad de Ciencias Económicas
- `facultad_de_ingenier_a` → Facultad de Ingeniería

### Ejemplo de Carreras:
- `inform_tica` → Informática
- `administraci_n_de_empresas` → Administración de Empresas

---

## ⚙️ Configuración Técnica

### Archivos Principales:
- `app.py` - Interfaz del dashboard (Streamlit)
- `logica_etl.py` - Lógica de actualización de datos
- `datos_historicos.csv` - Base de datos local

### Campos Clave en la BD:
- `group_bo0sv10/Facultad` - Facultad del estudiante
- `group_bo0sv10/_2_2_Carrera*` - Carrera (fragmentada en múltiples columnas)
- `group_bo0sv10/_1_Nro_de_Registro_Universitario` - ID único del estudiante
- `group_bo0sv10/Su_carrera_es_anual_o_semestra` - Tipo de participante
- `_id` - ID único de la respuesta

---

## 📞 Soporte

Si tienes preguntas o encuentras problemas:
1. Revisa esta guía
2. Verifica que los datos se carguen correctamente
3. Intenta actualizar desde KoboToolbox
4. Comprueba la conexión de internet

---

**Última actualización:** 13 de agosto, 2026
**Versión del Dashboard:** 2.0 (Mejorado)
