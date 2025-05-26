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

MIT License

Copyright (c) 2025 Juan Manuel Pinto

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
