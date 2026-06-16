"""
Tarea 2 - Probabilidad y Estadística Aplicada
Parte 1: Acceso, descarga y muestreo del dataset de Turismo Emisivo

Fuente: https://catalogodatos.gub.uy/dataset/ministerio-de-turismo-turismo-emisivo
"""

import pandas as pd
import requests
import urllib3
import io
import os

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

# URL directa del CSV en el catálogo de datos abiertos del gobierno uruguayo
# Si la URL cambia, verificar en: https://catalogodatos.gub.uy/dataset/ministerio-de-turismo-turismo-emisivo
URL_DATASET = "https://catalogodatos.gub.uy/dataset/1c1d75d0-b3c9-4ea4-a519-8c6b1468e589/resource/922f23e1-296c-490a-a3df-61e03e122d17/download/emisivo.csv"

# NOTA: catalogodatos.gub.uy usa un certificado SSL autofirmado.
# Se deshabilita la verificación SSL solo para este sitio del gobierno uruguayo.
# Esto es seguro en este contexto ya que es una fuente de datos pública y conocida.

ARCHIVO_MUESTRA = "muestra_2000.csv"
TAMANIO_MUESTRA = 2000
SEMILLA_ALEATORIA = 42  # Fijamos semilla para reproducibilidad


# =============================================================================
# PASO 1: DESCARGA DEL DATASET COMPLETO
# =============================================================================

def descargar_dataset(url: str) -> pd.DataFrame:
    """
    Descarga el dataset de turismo emisivo desde la URL indicada.
    Retorna un DataFrame con todos los datos.
    """
    print("Descargando dataset desde el catálogo de datos abiertos...")
    print(f"  URL: {url}")

    # catalogodatos.gub.uy usa certificado SSL autofirmado; suprimimos el warning esperado
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    try:
        respuesta = requests.get(url, timeout=60, verify=False)
        respuesta.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(
            f"No se pudo descargar el archivo. Verificar la URL o la conexión.\nError: {e}"
        )

    # Intentar diferentes encodings comunes en datasets uruguayos
    for encoding in ["utf-8", "latin-1", "iso-8859-1"]:
        try:
            df = pd.read_csv(
                io.StringIO(respuesta.content.decode(encoding)),
                sep=",",
                low_memory=False
            )
            break
        except (UnicodeDecodeError, pd.errors.ParserError):
            continue
    else:
        raise ValueError("No se pudo decodificar el archivo con los encodings probados.")

    print(f"  Dataset completo: {len(df):,} filas, {len(df.columns)} columnas")
    return df


# =============================================================================
# PASO 2: MUESTREO ALEATORIO EQUIPROBABLE DE 2000 FILAS
# =============================================================================

def tomar_muestra(df: pd.DataFrame, n: int, semilla: int) -> pd.DataFrame:
    """
    Selecciona n filas al azar de forma equiprobable (sin reposición).
    Fija la semilla para reproducibilidad.
    """
    if len(df) < n:
        raise ValueError(
            f"El dataset tiene {len(df)} filas, se necesitan al menos {n}."
        )

    muestra = df.sample(n=n, replace=False, random_state=semilla)
    muestra = muestra.reset_index(drop=True)

    print(f"\nMuestra aleatoria generada:")
    print(f"  - Tamaño : {len(muestra):,} filas")
    print(f"  - Semilla: {semilla} (para reproducibilidad)")
    return muestra


# =============================================================================
# PASO 3: EXPORTAR MUESTRA A CSV
# =============================================================================

def exportar_csv(df: pd.DataFrame, nombre_archivo: str) -> None:
    """
    Guarda el DataFrame en un archivo CSV con encoding UTF-8.
    """
    df.to_csv(nombre_archivo, index=False, encoding="utf-8")
    ruta_absoluta = os.path.abspath(nombre_archivo)
    print(f"\nArchivo exportado:")
    print(f"  - Nombre : {nombre_archivo}")
    print(f"  - Ruta   : {ruta_absoluta}")
    print(f"  - Filas  : {len(df):,} registros + 1 fila de encabezado")


# =============================================================================
# EJECUCIÓN PRINCIPAL
# =============================================================================

if __name__ == "__main__":

    # 1. Descargar dataset completo
    df_completo = descargar_dataset(URL_DATASET)

    # 2. Tomar muestra aleatoria equiprobable de 2000 filas
    df_muestra = tomar_muestra(df_completo, n=TAMANIO_MUESTRA, semilla=SEMILLA_ALEATORIA)

    # 3. Exportar muestra a CSV (archivo entregable)
    exportar_csv(df_muestra, ARCHIVO_MUESTRA)

    print("\nParte 1 completada. Continuar con parte2.py usando muestra_2000.csv")
