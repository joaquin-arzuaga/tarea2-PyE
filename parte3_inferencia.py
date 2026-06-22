"""
Tarea 2 - Probabilidad y Estadistica Aplicada
Parte 3: Inferencia (y Ej 7 de la Parte 2)

Ej 7 (P2): dispersion Gente vs GastoTotal + Pearson
Ej 1 (P3): IC 95% de la media de los gastos
Ej 2 (P3): test de una media, GastoAlojamiento < 350
Ej 3 (P3): GastoAlimentacion vs GastoCompras (apareado + Welch)
Ej 4 (P3): Chi-cuadrado Estadia vs Lugar Salida
Ej 5 (P3): regresion GastoTotal ~ Gente
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

ARCHIVO_MUESTRA = "muestra_2000.csv"
ALFA = 0.05

AZUL = "#1f4e79"
NARANJA = "#c55a11"

# las 9 columnas de gasto. ojo: transporte local viene mal escrito en el
# dataset (GatoTransporteLocal, sin la s), lo dejo igual asi matchea
VARIABLES_GASTO = [
    "GastoTotal", "GastoAlojamiento", "GastoAlimentacion",
    "GastoTransporteInternac", "GatoTransporteLocal", "GastoCultural",
    "GastoTours", "GastoCompras", "GastoResto",
]


def ej7_dispersion(df, archivo):
    """Ej 7 P2: scatter Gente vs GastoTotal y correlacion de Pearson."""
    x, y = df["Gente"], df["GastoTotal"]
    r, p = stats.pearsonr(x, y)

    print("\n--- Ej 7 (P2): dispersion Gente vs GastoTotal ---")
    print(f"Pearson r = {r:.4f}   r2 = {r**2:.4f}   p = {p:.4g}")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(x, y, color=AZUL, alpha=0.35, s=30)
    ax.set_title("Dispersion Gente vs Gasto Total (n=2000)", fontweight="bold")
    ax.set_xlabel("Gente")
    ax.set_ylabel("Gasto total (USD)")
    ax.set_xticks(range(1, 11))
    ax.text(0.97, 0.95, f"r = {r:.4f}\nr2 = {r**2:.4f}",
            transform=ax.transAxes, ha="right", va="top",
            bbox=dict(boxstyle="round", facecolor="white", edgecolor=AZUL))
    ax.grid(linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(archivo, dpi=160)
    plt.close()
    return r


def ej1_intervalos(df):
    """Ej 1: IC 95% para la media de cada gasto (t de Student, n-1 gl)."""
    n = len(df)
    t_crit = stats.t.ppf(1 - ALFA / 2, n - 1)

    print("\n--- Ej 1: IC 95% de la media ---")
    print(f"n = {n}   t_crit(0.975, {n-1}) = {t_crit:.4f}")

    filas = []
    for var in VARIABLES_GASTO:
        x = df[var]
        media = x.mean()
        s = x.std(ddof=1)          # desviacion muestral (n-1)
        ee = s / np.sqrt(n)        # error estandar
        margen = t_crit * ee
        filas.append([var, round(media, 2), round(s, 2), round(ee, 2),
                      round(media - margen, 2), round(media + margen, 2)])

    tabla = pd.DataFrame(filas, columns=["Variable", "Media", "s", "EE",
                                         "IC_inf", "IC_sup"])
    print(tabla.to_string(index=False))
    return tabla


def ej2_alojamiento(df):
    """Ej 2: test de una media, H0 mu>=350 vs H1 mu<350 (cola izq)."""
    mu0 = 350
    x = df["GastoAlojamiento"]
    t, p2 = stats.ttest_1samp(x, mu0)
    # scipy da p a dos colas, paso a una cola (izquierda)
    p = p2 / 2 if t < 0 else 1 - p2 / 2

    print("\n--- Ej 2: GastoAlojamiento < 350 ---")
    print(f"H0: mu >= {mu0}   H1: mu < {mu0}")
    print(f"media = {x.mean():.2f}   t = {t:.2f}   p = {p:.4f}")
    print("=> se rechaza H0" if p < ALFA else "=> no se rechaza H0")


def ej3_medias(df):
    """Ej 3: alimentacion vs compras. Principal: apareado. Control: Welch."""
    alim, comp = df["GastoAlimentacion"], df["GastoCompras"]

    print("\n--- Ej 3: GastoAlimentacion vs GastoCompras ---")
    print(f"media alim = {alim.mean():.2f}   media compras = {comp.mean():.2f}")

    # como son del mismo viaje van apareados, H0 mu_D<=0 vs H1 mu_D>0
    t, p2 = stats.ttest_rel(alim, comp)
    p = p2 / 2 if t > 0 else 1 - p2 / 2
    print(f"apareado: t = {t:.2f}   p = {p:.4f}")

    # Welch como chequeo extra (independientes, var distintas)
    tw, pw2 = stats.ttest_ind(alim, comp, equal_var=False)
    pw = pw2 / 2 if tw > 0 else 1 - pw2 / 2
    print(f"Welch:    t = {tw:.2f}   p = {pw:.4f}")
    print("=> se rechaza H0" if p < ALFA else "=> no se rechaza H0")


def ej4_chi2(df):
    """Ej 4: Chi-cuadrado de independencia Estadia vs Lugar Salida."""
    # agrupo la estadia en clases
    bins = [-0.1, 2, 5, 10, np.inf]
    labels = ["0-2", "3-5", "6-10", "11+"]
    estadia = pd.cut(df["Estadia"], bins=bins, labels=labels)

    # lugares con menos de 50 casos van a "Otros" (regla de Cochran)
    lugar = df["Lugar Salida"].copy()
    vc = lugar.value_counts()
    lugar = lugar.where(~lugar.isin(vc[vc < 50].index), "Otros")

    tabla = pd.crosstab(estadia, lugar)
    chi2, p, gl, esp = stats.chi2_contingency(tabla)

    print("\n--- Ej 4: Chi2 Estadia vs Lugar Salida ---")
    print(tabla.to_string())
    print(f"chi2 = {chi2:.2f}   gl = {gl}   p = {p:.4g}   "
          f"esperada min = {esp.min():.2f}")
    print("=> se rechaza H0 (hay dependencia)" if p < ALFA
          else "=> no se rechaza H0")


def ej5_regresion(df, archivo):
    """Ej 5: regresion lineal GastoTotal ~ Gente."""
    x, y = df["Gente"], df["GastoTotal"]
    reg = stats.linregress(x, y)
    b1, b0, r2 = reg.slope, reg.intercept, reg.rvalue ** 2

    print("\n--- Ej 5: regresion GastoTotal ~ Gente ---")
    print(f"GastoTotal = {b0:.2f} + {b1:.2f} * Gente")
    print(f"R2 = {r2:.4f}")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(x, y, color=AZUL, alpha=0.35, s=30, label="Observaciones")
    xr = np.array([x.min(), x.max()])
    ax.plot(xr, b0 + b1 * xr, color=NARANJA, linewidth=2.5,
            label=f"y = {b0:.2f} + {b1:.2f}x  (R2 = {r2:.4f})")
    ax.set_title("Regresion Gasto Total ~ Gente (n=2000)", fontweight="bold")
    ax.set_xlabel("Gente")
    ax.set_ylabel("Gasto total (USD)")
    ax.set_xticks(range(1, 11))
    ax.legend(loc="upper left")
    ax.grid(linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(archivo, dpi=160)
    plt.close()


if __name__ == "__main__":
    df = pd.read_csv(ARCHIVO_MUESTRA, encoding="utf-8")
    print(f"Muestra: {len(df)} filas, {len(df.columns)} columnas")

    ej7_dispersion(df, "gente_gasto_dispersion.png")
    ej1_intervalos(df)
    ej2_alojamiento(df)
    ej3_medias(df)
    ej4_chi2(df)
    ej5_regresion(df, "gente_gasto_regresion.png")

    print("\nListo.")
