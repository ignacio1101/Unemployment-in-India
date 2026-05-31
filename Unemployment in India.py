# ==========================================
# 1. IMPORTAR LIBRERÍAS
# ==========================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración estética de los gráficos
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# ==========================================
# 2. CARGAR Y LIMPIAR DATOS
# ==========================================
# NOTA: Asegúrate de descargar el archivo "Unemployment in India.csv" 
# de la plataforma de CodeAlpha y guardarlo en tu escritorio.
ruta_dataset = r'C:\Users\valen\OneDrive\Desktop\Unemployment in India.csv'

# Cargar el dataset eliminando espacios en blanco invisibles en los nombres de columnas
df = pd.read_csv(ruta_dataset)
df.columns = df.columns.str.strip()

print("--- Primeras filas del dataset de Desempleo ---")
print(df.head())

# Formatear la columna de fecha para poder hacer análisis temporal
df['Date'] = df['Date'].str.strip()
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')

# Extraer mes y año para evaluar tendencias estacionales
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month

# Limpieza: Eliminar filas completamente nulas si las hay
df = df.dropna()

print("\n--- Estructura del Dataset Post-Limpieza ---")
print(df.info())

# ==========================================
# 3. VISUALIZACIÓN 1: IMPACTO DEL COVID-19
# ==========================================
# Agrupamos la tasa de desempleo promedio por mes y año para ver la línea de tiempo
tendencia_temporal = df.groupby('Date')['Estimated Unemployment Rate (%)'].mean().reset_index()

plt.figure(figsize=(12, 5))
sns.lineplot(data=tendencia_temporal, x='Date', y='Estimated Unemployment Rate (%)', marker='o', color='crimson', linewidth=2.5)

# Resaltar la zona del confinamiento por Covid-19 (Marzo - Junio 2020 aprox)
plt.axvspan('2020-03-01', '2020-07-01', color='yellow', alpha=0.3, label='Pico de la Pandemia (COVID-19)')

plt.title("Evolución de la Tasa de Desempleo Absoluta e Impacto de la Pandemia", fontsize=14, fontweight='bold')
plt.xlabel("Línea de Tiempo (Meses / Años)", fontsize=12)
plt.ylabel("Tasa de Desempleo Estimada (%)", fontsize=12)
plt.legend()
plt.tight_layout()
plt.show()

# ==========================================
# 4. VISUALIZACIÓN 2: IMPACTO URBANO VS. RURAL
# ==========================================
# Comparar el comportamiento del desempleo según el tipo de área residencial
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x='Area', y='Estimated Unemployment Rate (%)', palette='Set2')
plt.title("Distribución del Desempleo: Áreas Urbanas vs. Rurales", fontsize=14, fontweight='bold')
plt.xlabel("Área de Residencia", fontsize=12)
plt.ylabel("Tasa de Desempleo Estimada (%)", fontsize=12)
plt.tight_layout()
plt.show()

# ==========================================
# 5. VISUALIZACIÓN 3: ANÁLISIS REGIONAL (TOP ESTADOS AFECTADOS)
# ==========================================
# Agrupamos por Estado (Region) para identificar cuáles sufrieron más la crisis
desempleo_regional = df.groupby('Region')['Estimated Unemployment Rate (%)'].mean().reset_index()
desempleo_regional = desempleo_regional.sort_values(by='Estimated Unemployment Rate (%)', ascending=False).head(10)

plt.figure(figsize=(12, 6))
sns.barplot(data=desempleo_regional, x='Estimated Unemployment Rate (%)', y='Region', palette='viridis')
plt.title("Top 10 Regiones con Mayor Tasa Promedio de Desempleo", fontsize=14, fontweight='bold')
plt.xlabel("Tasa de Desempleo Promedio (%)", fontsize=12)
plt.ylabel("Estado / Región", fontsize=12)
plt.tight_layout()
plt.show()

# ==========================================
# 6. ESTADÍSTICAS E INSIGHTS PARA POLÍTICAS PÚBLICAS
# ==========================================
print("\n=== HALLAZGOS CLAVE PARA PROPUESTAS DE POLÍTICAS ECONÓMICAS ===")
promedio_area = df.groupby('Area')['Estimated Unemployment Rate (%)'].mean()
print(f"-> Desempleo Promedio por Área:\n{promedio_area}\n")

max_historico = df.loc[df['Estimated Unemployment Rate (%)'].idxmax()]
print(f"-> El pico máximo registrado fue de {max_historico['Estimated Unemployment Rate (%)']}% en la región de {max_historico['Region']} durante el mes de {max_historico['Date'].strftime('%B %Y')}.")