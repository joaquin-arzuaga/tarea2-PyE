"""
Tarea 2 - Probabilidad y Estadística Aplicada
Parte 2: Análisis descriptivo de la muestra

Acá resolvemos los ejercicios 2 y 3 de la Parte 2:
  - Ejercicio 2: tabla de frecuencias para la variable 'Destino'.
  - Ejercicio 3: gráfico de barras y gráfico circular para 'Destino'.

Se trabaja sobre la muestra de 2000 viajes generada en parte1.py.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Nombre del archivo de la muestra generada en la Parte 1
ARCHIVO_MUESTRA = "muestra_2000.csv"

# Umbral para agrupar categorías chicas en la torta. Las categorías con
# menos del 2% quedan agrupadas en 'Otros' para que el gráfico se entienda
# (si no, los sectores chicos se solapan y no se lee nada).
UMBRAL_OTROS = 2.0

# Paleta de colores elegida a propósito sobria (azules + naranjas + verde
# + grises) pensando en que el informe puede ir impreso en blanco y negro.
PALETA = ["#1f4e79", "#2e75b6", "#c55a11", "#ed7d31",
          "#548235", "#a5a5a5", "#7f6000", "#525252"]



# EJERCICIO 2 - TABLA DE FRECUENCIAS PARA 'Destino'


def tabla_frecuencias_destino(df: pd.DataFrame) -> pd.DataFrame:
    """
    Arma la tabla de frecuencias para la variable 'Destino'.

    'Destino' es una variable cualitativa nominal (Argentina, Brasil,
    Europa, etc.), así que no tiene sentido calcular frecuencias
    acumuladas porque no hay un orden natural entre las categorías.
    Solo incluimos:
      - n_i: frecuencia absoluta (cuántas veces aparece cada categoría)
      - f_i: frecuencia relativa (n_i / n)
      - Porcentaje (%): la f_i expresada en %
    """
    n = len(df)

    # value_counts nos da los conteos por categoría ya ordenados de
    # mayor a menor, que es como se muestra la tabla.
    abs_freq = df["Destino"].value_counts(dropna=False)
    rel_freq = abs_freq / n

    tabla = pd.DataFrame({
        "Destino": abs_freq.index,
        "n_i": abs_freq.values,
        "f_i": rel_freq.values.round(4),
        "Porcentaje (%)": (rel_freq.values * 100).round(2),
    })

    # Agregamos una fila de TOTAL como control: la suma de n_i tiene
    # que dar 2000 y la de f_i tiene que dar 1. Si no da, algo está mal.
    total = pd.DataFrame({
        "Destino": ["TOTAL"],
        "n_i": [tabla["n_i"].sum()],
        "f_i": [round(tabla["f_i"].sum(), 4)],
        "Porcentaje (%)": [round(tabla["Porcentaje (%)"].sum(), 2)],
    })
    return pd.concat([tabla, total], ignore_index=True)



# EJERCICIO 3 - GRAFICOS PARA 'Destino'


def grafico_barras(tabla: pd.DataFrame, archivo: str) -> None:
    """
    Gráfico de barras de frecuencias absolutas por destino.
    Para una variable cualitativa el gráfico de barras es el que más
    se usa porque permite comparar fácilmente la magnitud entre
    categorías.
    """
    # Sacamos la fila TOTAL: en el gráfico no la queremos como una barra más
    datos = tabla[tabla["Destino"] != "TOTAL"]
    x = list(datos["Destino"])
    y = list(datos["n_i"])
    colores = [PALETA[i % len(PALETA)] for i in range(len(x))]

    fig, ax = plt.subplots(figsize=(11, 6))
    barras = ax.bar(x, y, color=colores, edgecolor="black", linewidth=0.6)

    # Le ponemos arriba de cada barra el valor exacto para que se pueda
    # leer sin tener que estimar contra el eje Y.
    for b, v in zip(barras, y):
        ax.text(b.get_x() + b.get_width() / 2,
                b.get_height() + max(y) * 0.012,
                f"{int(v)}", ha="center", va="bottom",
                fontsize=9, fontweight="bold")

    ax.set_title("Gráfico de barras — Destino del turismo emisivo (n = 2000)",
                 fontsize=13, fontweight="bold", pad=14)
    ax.set_xlabel("Destino")
    ax.set_ylabel("Frecuencia absoluta (viajes)")

    # Los nombres de los destinos son largos, así que los rotamos para
    # que no se solapen.
    ax.tick_params(axis="x", rotation=30)
    plt.setp(ax.get_xticklabels(), ha="right")

    # Grilla solo en el eje Y, en gris suave, para ayudar a leer alturas
    # sin recargar el gráfico.
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)

    # Quitamos los bordes superior y derecho del recuadro (queda más limpio).
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)

    plt.tight_layout()
    plt.savefig(archivo, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def grafico_circular(tabla: pd.DataFrame, archivo: str,
                     umbral_pct: float = UMBRAL_OTROS) -> None:
    """
    Gráfico circular con leader lines (palitos que salen de cada sector
    hasta una etiqueta exterior).

    Las categorías con porcentaje menor a umbral_pct se agrupan en
    'Otros (<2%)'. Esto es necesario porque la muestra tiene 12
    categorías y muchas son muy chicas: si las dejamos sueltas, los
    sectores se ven como líneas finas pegadas y las etiquetas se
    superponen.
    """
    # Separamos en categorías "grandes" (las que van solas) y "chicas"
    # (las que vamos a fusionar en 'Otros').
    datos = tabla[tabla["Destino"] != "TOTAL"].copy()
    mask = datos["Porcentaje (%)"] >= umbral_pct
    grandes = datos[mask]
    chicas = datos[~mask]

    if len(chicas) > 0:
        # Armamos la categoría 'Otros' sumando las frecuencias chicas
        otros = pd.DataFrame({
            "Destino": [f"Otros (<{int(umbral_pct)}%)"],
            "n_i": [chicas["n_i"].sum()],
            "Porcentaje (%)": [round(chicas["Porcentaje (%)"].sum(), 2)],
        })
        datos_pie = pd.concat(
            [grandes[["Destino", "n_i", "Porcentaje (%)"]], otros],
            ignore_index=True
        )
    else:
        datos_pie = grandes[["Destino", "n_i", "Porcentaje (%)"]]

    etiquetas = list(datos_pie["Destino"])
    valores = list(datos_pie["Porcentaje (%)"])
    colores = [PALETA[i % len(PALETA)] for i in range(len(etiquetas))]

    fig, ax = plt.subplots(figsize=(11, 7.5))

    # Dibujamos la torta empezando arriba (startangle=90) y avanzando
    # en sentido horario, que es la convención más natural para leer.
    wedges, _ = ax.pie(
        valores, labels=None, startangle=90, counterclock=False,
        colors=colores,
        wedgeprops={"edgecolor": "white", "linewidth": 1.2},
    )

    # Si el sector es grande (>= 8%) le ponemos el % adentro en blanco;
    # si es chico no, porque no entra el texto y queda apretado.
    for w, v in zip(wedges, valores):
        if v >= 8:
            ang = (w.theta2 + w.theta1) / 2.0
            x = 0.62 * np.cos(np.deg2rad(ang))
            y = 0.62 * np.sin(np.deg2rad(ang))
            ax.text(x, y, f"{v:.1f}%", ha="center", va="center",
                    fontsize=13, color="white", fontweight="bold")

    # Leader lines: para cada sector calculamos el ángulo medio, sacamos
    # un palito desde el borde del círculo y le ponemos la etiqueta
    # (destino + %) afuera.
    kw = dict(arrowprops=dict(arrowstyle="-", color="gray", lw=0.9),
              zorder=5, va="center")
    for w, etiqueta, v in zip(wedges, etiquetas, valores):
        ang = (w.theta2 + w.theta1) / 2.0
        x = np.cos(np.deg2rad(ang))
        y = np.sin(np.deg2rad(ang))
        # Si el sector cae a la derecha del círculo, la etiqueta va a
        # la derecha; si cae a la izquierda, a la izquierda.
        ha = "left" if x >= 0 else "right"
        kw["arrowprops"].update(
            {"connectionstyle": f"angle,angleA=0,angleB={ang}"})
        ax.annotate(f"{etiqueta}  {v:.1f}%",
                    xy=(x, y),                         # punta del palito
                    xytext=(1.30 * np.sign(x), 1.15 * y),  # texto afuera
                    horizontalalignment=ha, fontsize=11, **kw)

    ax.set_title("Gráfico circular — Destino del turismo emisivo (n = 2000)",
                 fontsize=13, fontweight="bold", pad=18)
    ax.axis("equal")

    # Estiramos un poco los límites para que las etiquetas exteriores
    # no queden cortadas al guardar la imagen.
    ax.set_xlim(-1.9, 1.9)
    ax.set_ylim(-1.4, 1.4)

    plt.tight_layout()
    plt.savefig(archivo, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()



if __name__ == "__main__":
    # Levantamos la muestra ya generada en la Parte 1. Usamos utf-8
    # porque el CSV trae tildes (Paraguay, Asia del Este y Pacífico, etc.).
    df = pd.read_csv(ARCHIVO_MUESTRA, encoding="utf-8")
    print(f"Muestra cargada: {len(df):,} filas, {len(df.columns)} columnas\n")

    # Ejercicio 2: armamos e imprimimos la tabla de frecuencias.
    tabla = tabla_frecuencias_destino(df)
    print("Tabla de frecuencias - Destino")
    print(tabla.to_string(index=False))

    # Ejercicio 3: generamos los dos gráficos pedidos.
    grafico_barras(tabla, "destino_barras.png")
    grafico_circular(tabla, "destino_torta.png")

    print("\nParte 2 completada.")
