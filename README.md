# PROGRAMA-DE-AN-LISIS-ENERG-TICO-DE-INFRAESTRUCTURAS
PROYECTO INTEGRADOR: PROGRAMA DE ANÁLISIS ENERGÉTICO DE INFRAESTRUCTURAS- Pablo Colina - Laura Ortiz
# Sistema de Gestión Energética e Infraestructura (Análisis LEED & ANDE)

Este es un programa interactivo desarrollado en Python para el análisis de eficiencia energética y la gestión 
de infraestructuras industriales. El sistema permite evaluar el consumo de energía en kilovatios-hora (kWh) frente a 
metas de certificación **LEED**, identificar anomalías críticas en el Factor de Potencia (riesgo de penalizaciones por la **ANDE**),
 y administrar el inventario de equipos mediante un sistema **CRUD** completo sincronizado con un archivo de datos local (.csv).

---
---
## 🚀 Características Principales

1. **Reporte de Eficiencia y Gráficos LEED (Dinámico):**
   - El usuario puede ingresar de forma manual el límite de consumo ideal para la infraestructura según la auditoría o normativa
    vigente.
   - Calcula de manera precisa el consumo total, la media por equipo y el puntaje LEED acumulado.
   - Genera automáticamente dos gráficos en ventana emergente usando `matplotlib`:
     - **Gráfico de Torta:** Muestra la distribución del consumo porcentual por **Área**, agrupando inteligentemente 
     los datos sin sobrecargar la visualización.
     - **Gráfico de Barras:** Indica el estatus actual de la certificación (Certificado Básico, Plata, Oro o Platino) y
      cuántos puntos faltan para ascender al siguiente nivel.

2. **Reporte de Anomalías (Riesgo ANDE):**
   - Analiza los equipos cuyo Factor de Potencia (FP) sea inferior al límite permitido de **0.90**.
   - Lista de manera clara el ID, nombre y ubicación de los equipos ineficientes que podrían generar sobrecostos o multas.

3. **Gestión Completa de Consumos y Equipos (CRUD):**
   - **Añadir:** Permite ingresar nuevos equipos validados numéricamente para evitar fallos.
   - **Eliminar:** Borra equipos por ID de la memoria y actualiza la base de datos automáticamente.
   - **Editar:** Modifica campos individuales (ID, Nombre, Área, Consumo o FP) seleccionando el equipo deseado.
   - **Persistencia de datos:** Todos los cambios se guardan instantáneamente en el archivo `equipos_industriales.csv`.

4. **Normalización Automática de Datos:**
   - El sistema limpia espacios accidentales y estandariza las mayúsculas/minúsculas de las áreas 
   (ej: `"produccion"`, `"Produccion "` y `"PRODUCCION"` se unifican como `"Produccion"`), garantizando reportes 
   limpios y gráficos legibles.

5. **Robustez y Seguridad (Try-Except):**
   - Protegido contra caídas accidentales. Si el archivo CSV falta o el usuario digita letras en campos numéricos, 
   el programa captura la excepción, informa del error amigablemente y regresa al menú de forma segura.

---

## 📁 Estructura del Proyecto

```
├── proyecto.py                   # Código fuente principal del sistema
├── equipos_industriales.csv  # Base de datos local en formato CSV
└── README.md                 # Documentación del proyecto (este archivo)
