# Scrapping Resultados Elecciones Ecuador 2025

Este proyecto contiene scripts en Python para extraer (scrapear) los resultados de las elecciones presidenciales de Ecuador 2025, tanto para la primera como para la segunda vuelta, a nivel de parroquia.

## Estructura

- `Scrapping primera vuelta ecuador.py`: Script para scrapear los resultados de la **primera vuelta**.
- `Scrapping Segunda vuelta ecuador.py`: Script para scrapear los resultados de la **segunda vuelta**.

## Requisitos

- Python 3.7+
- Google Chrome instalado
- Paquetes Python:
  - selenium
  - webdriver-manager

Puedes instalar los requisitos ejecutando:

```sh
pip install selenium webdriver-manager
```

## Uso

1. **Configura la ruta de salida del CSV** en cada script si es necesario.
2. Ejecuta el script correspondiente desde la terminal:

   Primera vuelta:
   ```sh
   python "Scrapping primera vuelta ecuador.py"
   ```

   Segunda vuelta:
   ```sh
   python "Scrapping Segunda vuelta ecuador.py"
   ```

3. El script abrirá una ventana de Chrome, navegará por las provincias, cantones y parroquias, y guardará los resultados en un archivo CSV.

### Notas

- Si el script se interrumpe, puede reanudarse automáticamente desde el último registro guardado en el CSV.
- Puedes activar el modo "headless" (sin ventana) descomentando la línea correspondiente en el código.

## Salida

Los resultados se guardan en archivos CSV con las siguientes columnas:

- Provincia
- Cantón
- id_canton
- Parroquia
- id_parroquia
- Tipo
- Listas y Siglas
- Candidatos
- Votos
- %votos
- Indicador
- Valor

## Licencia

Uso personal y académico. No oficial.
