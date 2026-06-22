# Tarea 2 – Probabilidad y Estadística aplicada

Este repositorio contiene los scripts de Python utilizados para resolver la Tarea 2,
junto con la muestra de datos analizada. El objetivo de este documento es explicar de
forma clara cómo ejecutar el código y qué resultados produce, sin requerir conocimientos
previos de programación.

## Datos del trabajo

**Curso:** Probabilidad y Estadística aplicada
**Facultad:** Ingeniería y Tecnologías – Universidad Católica del Uruguay
**Docentes:** Sebastián DeCuadro y María Gómez

**Equipo 3:**
- Joaquín Arzuaga
- Diego Renaldín
- Sebastián Martony
- [completar: nombre del cuarto integrante]

## Contenido de la carpeta

- `muestra_2000.csv` – muestra de 2000 registros seleccionados al azar del archivo
  original de turismo emisivo (generada en la Parte 1).
- `parte2_descriptiva.py` – tabla de frecuencias y gráficos correspondientes a la Parte 2.
- `parte3_inferencia.py` – intervalos de confianza, tests de hipótesis y regresión lineal
  correspondientes a la Parte 3.
- Las tablas e imágenes generadas por los scripts se guardan en esta misma carpeta.

## Requisitos previos

Es necesario contar con Python (versión 3.10 o superior) y cuatro librerías. En caso de
no tenerlas instaladas, pueden agregarse abriendo la terminal del sistema y ejecutando el
siguiente comando una única vez:

```
pip install pandas numpy scipy matplotlib
```

## Ejecución

Una vez instaladas las librerías, debe ubicarse la terminal en la carpeta que contiene los
archivos y ejecutar el script deseado.

Para la Parte 2:

```
python parte2_descriptiva.py
```

Para la Parte 3:

```
python parte3_inferencia.py
```

Ambos scripts leen automáticamente el archivo `muestra_2000.csv` ubicado en la misma
carpeta, por lo que no es necesario realizar ninguna configuración adicional.

## Resultados esperados

Al ejecutarse, cada script muestra en pantalla las tablas y los valores numéricos
obtenidos (frecuencias, estadísticos, p-valores, intervalos de confianza, etc.) y guarda
los gráficos como archivos de imagen `.png` en la carpeta. Esas imágenes son las mismas
que se presentan en el informe.

## Observación sobre la muestra

Los scripts están preparados para trabajar sobre la muestra incluida en este repositorio.
Dado que las 2000 filas fueron seleccionadas de manera aleatoria, ejecutar el análisis
sobre una muestra distinta produciría resultados diferentes. Por ese motivo se incluye el
archivo `muestra_2000.csv` exacto utilizado, de modo que los resultados coincidan con los
del informe.

## Resolución de problemas frecuentes

- Si aparece un mensaje indicando que no se encuentra el archivo, verificar que la terminal
  esté ubicada en la carpeta que contiene tanto el `.csv` como los scripts `.py`.
- Si aparece un mensaje del tipo *"No module named..."*, volver a ejecutar el comando de
  instalación indicado en la sección de requisitos previos.