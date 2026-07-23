
"""
customer_analysis.py
Proyecto completo: SQL + Python + Visualizaciones + Segmentación + Modelo predictivo
"""

import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import os
import re
import warnings
warnings.filterwarnings('ignore')

# =====================================================
# 0. Configuración inicial con rutas dinámicas
# =====================================================
# Obtener la ruta de la carpeta donde está este script
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)  # Cambiar al directorio del script

# Crear carpeta de salida si no existe
os.makedirs('outputs', exist_ok=True)

# Estilos de gráficos
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)

# =====================================================
# 1. Cargar datos desde CSV
# =====================================================
print("Cargando datos desde CSV...")
csv_path = os.path.join(script_dir, 'WA_Fn-UseC_-Marketing-Customer-Value-Analysis.csv')
df = pd.read_csv(csv_path, encoding='utf-8')

# Función para limpiar nombres de columnas: espacios -> _, eliminar caracteres extraños
def clean_column_name(col):
    col = col.strip()
    col = re.sub(r'[^\w\s]', '', col)  # eliminar puntuación
    col = re.sub(r'\s+', '_', col)     # espacios a underscore
    return col.lower()

df.columns = [clean_column_name(col) for col in df.columns]
print(f"Nombres de columnas limpios: {list(df.columns)}")

# Limpieza básica
df['income'] = df['income'].replace(0, np.nan)   # ingresos 0 los tratamos como missing
df['customer_lifetime_value'] = pd.to_numeric(df['customer_lifetime_value'], errors='coerce')
df['total_claim_amount'] = pd.to_numeric(df['total_claim_amount'], errors='coerce')

print(f"Dataset cargado: {df.shape[0]} filas, {df.shape[1]} columnas\n")

# =====================================================
# 2. Cargar datos en SQLite (en memoria)
# =====================================================
print("Conectando a base SQLite en memoria...")
conn = sqlite3.connect(':memory:')
df.to_sql('customer_value', conn, index=False, if_exists='replace')
print("Datos cargados en tabla 'customer_value'\n")

# =====================================================
# 3. Leer y ejecutar consultas desde el archivo .sql
# =====================================================
sql_file = os.path.join(script_dir, 'project_queries.sql')
print(f"Leyendo consultas desde {sql_file}...")
with open(sql_file, 'r', encoding='utf-8') as f:
    sql_script = f.read()

# Separar consultas individuales (por ';' y eliminar vacías)
queries = [q.strip() for q in sql_script.split(';') if q.strip() and not q.strip().upper().startswith('DROP')]

print("Ejecutando consultas y mostrando resultados:\n" + "="*60)
for i, query in enumerate(queries, 1):
    if query.upper().startswith('CREATE'):
        continue
    try:
        result = pd.read_sql_query(query, conn)
        print(f"\n--- Resultado consulta {i} ---")
        print(result.head(10) if len(result) > 10 else result)
        print(f"Filas devueltas: {len(result)}\n")
    except Exception as e:
        print(f"Error en consulta {i}: {e}")

# =====================================================
# 4. Visualizaciones de Análisis Exploratorio (EDA)
# =====================================================
print("\nGenerando visualizaciones EDA...")

# 4.1 Distribución del CLV
plt.figure()
sns.histplot(df['customer_lifetime_value'].dropna(), bins=50, kde=True, color='skyblue')
plt.title('Distribución del Customer Lifetime Value')
plt.xlabel('CLV')
plt.ylabel('Frecuencia')
plt.savefig('outputs/distribucion_clv.png', dpi=150)
plt.close()

# 4.2 CLV por respuesta (boxplot)
plt.figure()
sns.boxplot(x='response', y='customer_lifetime_value', data=df)
plt.title('CLV según respuesta a la oferta')
plt.savefig('outputs/clv_by_response.png')
plt.close()

# 4.3 Relación ingresos vs CLV (con regresión)
plt.figure()
sns.regplot(x='income', y='customer_lifetime_value', data=df.dropna(subset=['income']),
            scatter_kws={'alpha':0.3}, line_kws={'color':'red'})
plt.title('Ingresos vs CLV')
plt.xlabel('Ingreso anual')
plt.ylabel('CLV')
plt.savefig('outputs/income_vs_clv.png')
plt.close()

# 4.4 CLV promedio por estado (top 10)
state_clv = df.groupby('state')['customer_lifetime_value'].mean().sort_values(ascending=False).head(10)
plt.figure()
state_clv.plot(kind='bar', color='teal')
plt.title('Promedio de CLV por Estado (Top 10)')
plt.ylabel('CLV promedio')
plt.xticks(rotation=45)
plt.savefig('outputs/clv_by_state.png')
plt.close()

# 4.5 Matriz de correlación
numeric_cols = ['customer_lifetime_value', 'income', 'monthly_premium_auto',
                'months_since_last_claim', 'months_since_policy_inception',
                'number_of_open_complaints', 'number_of_policies', 'total_claim_amount']
corr = df[numeric_cols].corr()
plt.figure(figsize=(10,8))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Matriz de correlación')
plt.savefig('outputs/correlation_matrix.png')
plt.close()
print("Visualizaciones EDA guardadas en carpeta 'outputs/'\n")

# =====================================================
# 5. Segmentación de clientes (KMeans)
# =====================================================
print("Realizando segmentación con KMeans...")
# Seleccionar features relevantes y eliminar missing
seg_features = ['customer_lifetime_value', 'income', 'monthly_premium_auto',
                'months_since_policy_inception', 'total_claim_amount']
df_seg = df[seg_features].dropna()
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_seg)

# Determinar número óptimo de clusters con método del codo
inertias = []
K_range = range(2, 11)
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)

plt.figure()
plt.plot(K_range, inertias, 'bo-')
plt.xlabel('Número de clusters')
plt.ylabel('Inercia')
plt.title('Método del codo para KMeans')
plt.savefig('outputs/elbow_method.png')
plt.close()

# Elegimos k=4 (según codo)
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df_seg['Segment'] = kmeans.fit_predict(X_scaled)

# Reducción a 2D con PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
plt.figure(figsize=(10,6))
sns.scatterplot(x=X_pca[:,0], y=X_pca[:,1], hue=df_seg['Segment'], palette='Set2', alpha=0.6)
plt.title('Segmentación de clientes (PCA)')
plt.xlabel('Componente principal 1')
plt.ylabel('Componente principal 2')
plt.savefig('outputs/segmentation_pca.png')
plt.close()

# Perfil de segmentos
segment_profile = df_seg.groupby('Segment')[seg_features].mean()
print("Perfil de segmentos (valores medios):")
print(segment_profile.round(2))
print("\nSegmentación guardada.\n")

# =====================================================
# 6. Modelo predictivo: Response (Yes/No)
# =====================================================
print("Entrenando modelo para predecir Response...")
# Preparar datos
df_model = df.copy()
df_model['response_binary'] = (df_model['response'] == 'Yes').astype(int)

# Seleccionar columnas para modelo
feature_cols = ['customer_lifetime_value', 'income', 'monthly_premium_auto',
                'months_since_last_claim', 'months_since_policy_inception',
                'number_of_open_complaints', 'number_of_policies', 'total_claim_amount',
                'coverage', 'education', 'employmentstatus', 'gender', 'marital_status',
                'policy_type', 'sales_channel', 'vehicle_size']

# Limpiar missing
df_clean = df_model[feature_cols + ['response_binary']].copy()
df_clean['income'] = df_clean['income'].replace(0, np.nan)
df_clean = df_clean.dropna()

# Codificar categóricas
categorical_cols = ['coverage', 'education', 'employmentstatus', 'gender', 'marital_status',
                    'policy_type', 'sales_channel', 'vehicle_size']
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df_clean[col] = le.fit_transform(df_clean[col].astype(str))
    label_encoders[col] = le

X = df_clean.drop('response_binary', axis=1)
y = df_clean['response_binary']

# Escalar numéricas
scaler2 = StandardScaler()
numeric_cols2 = ['customer_lifetime_value', 'income', 'monthly_premium_auto',
                 'months_since_last_claim', 'months_since_policy_inception',
                 'number_of_open_complaints', 'number_of_policies', 'total_claim_amount']
X[numeric_cols2] = scaler2.fit_transform(X[numeric_cols2])

# División train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Entrenar Random Forest
rf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
rf.fit(X_train, y_train)

# Predicciones
y_pred = rf.predict(X_test)
y_proba = rf.predict_proba(X_test)[:,1]

# Métricas
print("\n=== Reporte de clasificación ===")
print(classification_report(y_test, y_pred))
print(f"AUC-ROC: {roc_auc_score(y_test, y_proba):.3f}")

# Matriz de confusión
cm = confusion_matrix(y_test, y_pred)
plt.figure()
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['No', 'Yes'], yticklabels=['No', 'Yes'])
plt.title('Matriz de confusión - Predicción de Response')
plt.xlabel('Predicho')
plt.ylabel('Real')
plt.savefig('outputs/confusion_matrix_response.png')
plt.close()

# Importancia de variables
importances = rf.feature_importances_
indices = np.argsort(importances)[::-1]
plt.figure(figsize=(10,6))
plt.title('Importancia de variables en Random Forest')
plt.barh(range(X.shape[1]), importances[indices][::-1], align='center')
plt.yticks(range(X.shape[1]), X.columns[indices][::-1])
plt.xlabel('Importancia')
plt.tight_layout()
plt.savefig('outputs/feature_importance.png')
plt.close()

print("Modelo entrenado. Gráficos de evaluación guardados en 'outputs/'.")
print("\n" + "="*60)
print("PROYECTO COMPLETADO CON ÉXITO.")
print("Revisa la carpeta 'outputs/' para todas las visualizaciones.")
print("="*60)

# Cerrar conexión SQLite
conn.close()