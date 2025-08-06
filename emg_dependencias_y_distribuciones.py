import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm, expon, gumbel_r, rayleigh

# Cargar el dataset
datos = pd.read_csv("datos_emg_columnas2.csv")

# Columnas que vamos a analizar
columnas = ["dedo1", "dedo2", "dedo3", "dedo4", "dedo5", "mano"]

# ================================
# 1. MATRIZ DE COVARIANZA Y CORRELACIÓN
# ================================

print("\n📊 Matriz de Covarianzas:\n")
print(datos[columnas].cov().round(2))

print("\n🔗 Matriz de Correlación:\n")
matriz_corr = datos[columnas].corr()
print(matriz_corr.round(2))

# Graficar la matriz de correlación como un heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(matriz_corr, annot=True, cmap="coolwarm", center=0)
plt.title("🔗 Mapa de Calor: Correlación entre señales EMG")
plt.tight_layout()
plt.show()

# ================================
# 2. GRAFO DE DEPENDENCIAS MÁS SIGNIFICATIVAS
# ================================
import networkx as nx

# Crear grafo con umbral de correlación alta (> 0.7)
G = nx.Graph()
for i in range(len(columnas)):
    for j in range(i + 1, len(columnas)):
        corr = matriz_corr.iloc[i, j]
        if abs(corr) > 0.7:
            G.add_edge(columnas[i], columnas[j], weight=round(corr, 2))

# Dibujar grafo
plt.figure(figsize=(7, 5))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2500, font_size=10, font_weight='bold')
edges = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edges)
plt.title("🔗 Grafo de Dependencias Significativas (> 0.7)")
plt.tight_layout()
plt.show()

# ================================
# 3. DISTRIBUCIONES DE PROBABILIDAD
# ================================
from scipy.stats import probplot

distribuciones = {
    "Normal": norm,
    "Exponencial": expon,
    "Gumbel": gumbel_r,
    "Rayleigh": rayleigh
}

for col in columnas:
    serie = datos[col].dropna()

    plt.figure(figsize=(14, 8))
    for i, (nombre, dist) in enumerate(distribuciones.items()):
        plt.subplot(2, 2, i + 1)
        # Ajustar la distribución
        params = dist.fit(serie)
        x = np.linspace(min(serie), max(serie), 100)
        y = dist.pdf(x, *params)
        # Graficar
        sns.histplot(serie, bins=20, stat="density", color="lightgray", alpha=0.6)
        plt.plot(x, y, label=f"{nombre} ajustada", color="red")
        plt.title(f"{col} - {nombre}")
        plt.legend()

    plt.suptitle(f"Ajuste de Distribuciones para {col}", fontsize=14)
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.show()
