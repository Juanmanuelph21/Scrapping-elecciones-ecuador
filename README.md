# Análisis de las Elecciones Presidenciales Ecuador 2025

Este repositorio contiene el código y los datos utilizados para el análisis de las elecciones presidenciales de Ecuador en 2025, con énfasis en el fenómeno de polarización política. El análisis completo fue publicado en [Razón Pública](https://razonpublica.com/ecuador-pais-partido-dos-noboa-gonzalez-dilema-indigena/).

## 📁 Estructura del Repositorio

```
ecuador-elecciones/
├── Datos/                       # Datos crudos y procesados (CSV)
├── Indicadores de polarización/ # Notebooks con análisis y visualización
├── Web Scrapping/              # Scripts de scraping primera y segunda vuelta
└── LICENSE
```

## 🧩 Componentes

### 1. Web Scraping

Scripts en Python que extraen los resultados oficiales de las elecciones desde los dashboards del CNE para:

- **Primera vuelta:** https://resultados2025.cne.gob.ec/
- **Segunda vuelta:** https://resultados2025-2v.cne.gob.ec/

Los datos de elecciones anteriores (como 2023) disponibles en [bases de datos del CNE](https://www.cne.gob.ec/estadisticas/bases-de-datos/)

#### Archivos:

- `Scrapping primera vuelta ecuador.py`
- `Scrapping segunda vuelta ecuador.py`

#### Requisitos:

- Python 3.7+
- Google Chrome
- Paquetes:
  ```sh
  pip install selenium webdriver-manager
  ```

#### Instrucciones:

```bash
python "Scrapping primera vuelta ecuador.py"
python "Scrapping segunda vuelta ecuador.py"
```

Los resultados se guardan en archivos `.csv` con columnas como: Provincia, Cantón, Parroquia, Candidato, Votos, %votos, etc.

### 2. Análisis de Polarización

En la carpeta **Indicadores de polarización/** se encuentran notebooks en Jupyter que procesan los datos y calculan los siguientes indicadores clave:

#### 📊 Indicadores utilizados

- **Número Efectivo de Candidatos (NEC):** estima cuántos candidatos fueron realmente competitivos.
- **Polarización L1 (vs. ideal 50/50):** mide la cercanía del resultado a una competencia perfectamente polarizada entre dos candidatos.
- **Balanza de Polarización (L1):** compara si los resultados se asemejan más a una distribución 50/50 entre dos líderes o a una fragmentación total.
- **Balanza de Polarización (Euclidiana):** misma lógica anterior, pero usando distancia euclidiana.

## 📌 Resultado del Análisis

Puedes leer el artículo completo con los resultados y visualizaciones en:

👉 [Ecuador: ¿un país partido en dos? Noboa, González y el dilema indígena (Razón Pública)](https://razonpublica.com/ecuador-pais-partido-dos-noboa-gonzalez-dilema-indigena/)

## 📄 Licencia

MIT License  
(c) 2025 Juan Manuel Pinto
