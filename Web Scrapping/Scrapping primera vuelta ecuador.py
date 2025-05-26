import csv
import os # Importar os para verificar existencia y tamaño de archivo
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, TimeoutException

# --- Función para leer el último registro del CSV ---
def obtener_ultimo_registro(path):
    """Lee el CSV y devuelve la última provincia, cantón y parroquia procesados."""
    ultimo_prov, ultimo_cant, ultimo_parr = None, None, None
    try:
        if os.path.exists(path) and os.path.getsize(path) > 0:
            with open(path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader) # Saltar cabecera
                last_row = None
                for row in reader:
                    if row: # Asegurarse de que la fila no esté vacía
                        last_row = row
                
                if last_row:
                    # Asegurarse de que las columnas existan y no estén vacías
                    # Indices basados en la cabecera: ['Provincia'(0), 'Cantón'(1), 'id_canton'(2), 'Parroquia'(3), ...]
                    if len(last_row) > 3:
                        ultimo_prov = last_row[0].strip() if last_row[0] else None
                        ultimo_cant = last_row[1].strip() if last_row[1] else None
                        # La parroquia es crucial para saber dónde continuar
                        ultimo_parr = last_row[3].strip() if last_row[3] else None 
                        print(f"Reanudando desde: Provincia='{ultimo_prov}', Cantón='{ultimo_cant}', Parroquia='{ultimo_parr}'")
                    else:
                        print("Advertencia: La última fila del CSV no tiene suficientes columnas.")
                else:
                    print("CSV existe pero parece vacío después de la cabecera. Empezando desde el principio.")
        else:
            print("Archivo CSV no encontrado o vacío. Empezando desde el principio.")
    except StopIteration:
         print("Archivo CSV solo contiene la cabecera. Empezando desde el principio.")
    except Exception as e:
        print(f"Error al leer el último registro del CSV: {e}. Empezando desde el principio.")
    
    return ultimo_prov, ultimo_cant, ultimo_parr

# Función para hacer clic en "Consultar" con reintentos, esperando a que desaparezca el overlay
def click_consultar(wait, btn_locator, max_retries=5):
    retries = 0
    while retries < max_retries:
        try:
            # Espera a que el overlay (preloader) desaparezca
            wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "preloader-content-accion-Template")))
            btn = wait.until(EC.element_to_be_clickable(btn_locator))
            btn.click()
            return True
        except (ElementClickInterceptedException, TimeoutException):
            print(f"Click interceptado o timeout esperando overlay. Reintento {retries+1}/{max_retries}...")
            time.sleep(3 + retries) # Incrementar espera en cada reintento
            retries += 1
        except Exception as e:
             print(f"Error inesperado al hacer clic en Consultar: {e}. Reintento {retries+1}/{max_retries}...")
             time.sleep(3 + retries)
             retries += 1
             
    print("No se pudo hacer clic en Consultar después de varios intentos.")
    return False

# --- Inicio del Script Principal ---

# Configurar Selenium y abrir la URL
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
# options.add_argument("--headless") # Descomentar para ejecutar sin ventana de navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://resultados2025.cne.gob.ec")
wait = WebDriverWait(driver, 20) # Aumentar el tiempo de espera general

# --- Configuración CSV y Reanudación ---
output_path = r'C:\Users\juanm.PC-JUAN\Documents\Python\Ecuador\resultados_parroquias_primera.csv'
cabecera = ['Provincia', 'Cantón', 'id_canton', 'Parroquia', 'id_parroquia',
            'Tipo', 'Listas y Siglas', 'Candidatos', 'Votos', '%votos', 'Indicador', 'Valor']

# Verificar si el archivo existe y si necesita cabecera
archivo_existe = os.path.exists(output_path)
necesita_cabecera = not archivo_existe or os.path.getsize(output_path) == 0

# Obtener el último registro procesado
ultimo_provincia, ultimo_canton, ultimo_parroquia = obtener_ultimo_registro(output_path)

# Bandera para controlar cuándo empezar a procesar/escribir datos
empezar_procesamiento = (ultimo_provincia is None and ultimo_canton is None and ultimo_parroquia is None)

# Abrir el CSV en modo 'append' (añadir)
csv_file = open(output_path, 'a', newline='', encoding='utf-8')
writer = csv.writer(csv_file)

# Escribir cabecera si es necesario
if necesita_cabecera:
    writer.writerow(cabecera)
    print("Escribiendo cabecera del CSV.")

try:
    # Paso 1: Seleccionar la dignidad (Presidente y Vicepresidente)
    print("Seleccionando dignidad 'Presidente y Vicepresidente'...")
    dignidad_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'myButtonDig') and contains(., 'PRESIDENTE')]")))
    dignidad_btn.click()
    time.sleep(3) # Espera extra para asegurar carga
    print("Dignidad seleccionada.")

    # Paso 2: Obtener y recorrer el dropdown de provincias
    print("Cargando provincias...")
    provincias_dropdown = wait.until(EC.presence_of_element_located((By.ID, "ddlProvincia")))
    select_provincias = Select(provincias_dropdown)
    lista_provincias = select_provincias.options[1:] # Omitir "TODOS"

    for provincia_option in lista_provincias:
        provincia_valor = provincia_option.get_attribute("value")
        provincia_nombre = provincia_option.text.strip()

        # --- Lógica de Reanudación (Provincia) ---
        if not empezar_procesamiento and provincia_nombre < ultimo_provincia:
            print(f"Saltando provincia ya procesada: {provincia_nombre}")
            continue
        elif not empezar_procesamiento and provincia_nombre == ultimo_provincia:
            print(f"Reanudando en provincia: {provincia_nombre}")
            # No activamos empezar_procesamiento aún, lo hará el nivel inferior
            pass # Continuar al siguiente nivel (cantón)
        elif not empezar_procesamiento and provincia_nombre > ultimo_provincia:
             print(f"Comenzando procesamiento normal desde provincia: {provincia_nombre}")
             empezar_procesamiento = True # Empezar a procesar todo desde aquí

        print(f"Seleccionando provincia: {provincia_nombre}")
        try:
            # Volver a encontrar el elemento antes de interactuar, puede volverse 'stale'
            provincias_dropdown_actual = wait.until(EC.presence_of_element_located((By.ID, "ddlProvincia")))
            select_provincias_actual = Select(provincias_dropdown_actual)
            select_provincias_actual.select_by_value(provincia_valor)
            time.sleep(3) # Espera para que carguen cantones/circunscripciones
        except (NoSuchElementException, TimeoutException, Exception) as e:
            print(f"Error al seleccionar provincia {provincia_nombre}: {e}. Saltando provincia.")
            driver.refresh() # Intentar refrescar la página en caso de error grave
            time.sleep(5)
            # Reintentar seleccionar dignidad si es necesario
            try:
                 print("Re-seleccionando dignidad después de refrescar...")
                 dignidad_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'myButtonDig') and contains(., 'PRESIDENTE')]")))
                 dignidad_btn.click()
                 time.sleep(3)
                 print("Dignidad re-seleccionada.")
                 # Volver a obtener el dropdown de provincias
                 provincias_dropdown = wait.until(EC.presence_of_element_located((By.ID, "ddlProvincia")))
                 select_provincias = Select(provincias_dropdown)

            except Exception as refresh_err:
                 print(f"Error crítico al intentar recuperar estado después de refrescar: {refresh_err}. Deteniendo.")
                 break # Salir del bucle de provincias si no se puede recuperar
            continue # Saltar al siguiente ciclo de provincia


        # Paso 3: Procesar cantones o circunscripciones
        try:
            # Esperar a que el dropdown de cantón esté presente y verificar si está habilitado
            cantones_dropdown = wait.until(EC.presence_of_element_located((By.ID, "ddlCanton")))
            
            # Caso 1: Procesar por Circunscripción y luego Cantón
            # (Asumiendo que si el cantón está deshabilitado, existe circunscripción)
            # Puede necesitar ajuste si la lógica es diferente
            # OJO: La lógica original busca 'disabled', pero podría ser que simplemente no tenga opciones > 1
            # if cantones_dropdown.get_attribute("disabled"): # Revisar si 'disabled' es el atributo correcto
            # Una mejor comprobación podría ser ver si hay opciones en circunscripción
            try:
                circunscripciones_dropdown = driver.find_element(By.ID, "ddlCircunscripcion")
                if circunscripciones_dropdown.is_displayed() and circunscripciones_dropdown.is_enabled():
                     select_circunscripciones = Select(circunscripciones_dropdown)
                     if len(select_circunscripciones.options) > 1: # Si hay más que la opción por defecto
                          print(f"Provincia {provincia_nombre} tiene circunscripciones.")
                          lista_circunscripciones = select_circunscripciones.options[1:] # Omitir "TODOS" o similar
                          
                          for circun_option in lista_circunscripciones:
                               circun_valor = circun_option.get_attribute("value")
                               circun_nombre = circun_option.text.strip()
                               if not circun_valor: continue
                               
                               print(f"  Seleccionando circunscripción: {circun_nombre}")
                               select_circunscripciones.select_by_value(circun_valor)
                               time.sleep(3)

                               # Procesar cantones dentro de esta circunscripción
                               cantones_dropdown_circ = wait.until(EC.presence_of_element_located((By.ID, "ddlCanton")))
                               select_cantones_circ = Select(cantones_dropdown_circ)
                               lista_cantones_circ = select_cantones_circ.options[1:] # Omitir "TODOS"

                               for canton_option in lista_cantones_circ:
                                    canton_valor = canton_option.get_attribute("value")
                                    canton_nombre = canton_option.text.strip()
                                    if not canton_valor: continue

                                    # --- Lógica de Reanudación (Cantón en Circunscripción) ---
                                    if not empezar_procesamiento and provincia_nombre == ultimo_provincia and canton_nombre < ultimo_canton:
                                        print(f"    Saltando cantón ya procesado: {canton_nombre}")
                                        continue
                                    elif not empezar_procesamiento and provincia_nombre == ultimo_provincia and canton_nombre == ultimo_canton:
                                         print(f"    Reanudando en cantón: {canton_nombre}")
                                         pass # Continuar al nivel de parroquia
                                    elif not empezar_procesamiento and provincia_nombre == ultimo_provincia and canton_nombre > ultimo_canton:
                                         print(f"    Comenzando procesamiento normal desde cantón: {canton_nombre}")
                                         empezar_procesamiento = True
                                    
                                    print(f"    Seleccionando cantón: {canton_nombre}")
                                    try:
                                        # Re-encontrar elemento
                                        cantones_dropdown_circ_actual = wait.until(EC.presence_of_element_located((By.ID, "ddlCanton")))
                                        select_cantones_circ_actual = Select(cantones_dropdown_circ_actual)
                                        select_cantones_circ_actual.select_by_value(canton_valor)
                                        time.sleep(3) # Esperar carga de parroquias
                                    except Exception as e:
                                         print(f"Error seleccionando cantón {canton_nombre} en circ {circun_nombre}: {e}. Saltando cantón.")
                                         continue # Saltar al siguiente cantón

                                    # Procesar Parroquias dentro de este cantón
                                    try:
                                        parroquias_dropdown = wait.until(EC.presence_of_element_located((By.ID, "ddlParroquia")))
                                        select_parroquias = Select(parroquias_dropdown)
                                        lista_parroquias = select_parroquias.options[1:] # Omitir "TODOS"

                                        for parroquia_option in lista_parroquias:
                                            parroquia_valor = parroquia_option.get_attribute("value")
                                            parroquia_nombre = parroquia_option.text.strip()
                                            if not parroquia_valor: continue

                                            # --- Lógica de Reanudación (Parroquia) ---
                                            if not empezar_procesamiento and provincia_nombre == ultimo_provincia and canton_nombre == ultimo_canton and parroquia_nombre <= ultimo_parroquia:
                                                print(f"      Saltando parroquia ya procesada: {parroquia_nombre}")
                                                continue # Saltar esta parroquia (incluida la última guardada)
                                            
                                            # Si llegamos aquí, debemos procesar
                                            empezar_procesamiento = True 
                                            
                                            print(f"      Procesando parroquia: {parroquia_nombre}")
                                            try:
                                                # Re-encontrar elemento
                                                parroquias_dropdown_actual = wait.until(EC.presence_of_element_located((By.ID, "ddlParroquia")))
                                                select_parroquias_actual = Select(parroquias_dropdown_actual)
                                                select_parroquias_actual.select_by_value(parroquia_valor)
                                                time.sleep(2)
                                            except Exception as e:
                                                print(f"Error seleccionando parroquia {parroquia_nombre}: {e}. Saltando parroquia.")
                                                continue

                                            # --- Click en Consultar y Extracción ---
                                            if click_consultar(wait, (By.ID, "btnConsultar")):
                                                time.sleep(4) # Espera más larga para carga de datos
                                                
                                                # --- Extracción de datos (igual que antes) ---
                                                try:
                                                    filas_candidatos = driver.find_elements(By.XPATH, "//table[@id='tablaCandi']/tbody/tr")
                                                    for fila in filas_candidatos:
                                                        celdas = fila.find_elements(By.TAG_NAME, "td")
                                                        if len(celdas) >= 4:
                                                            lista_siglas = celdas[0].text.strip()
                                                            candidato = celdas[1].text.strip()
                                                            votos = celdas[2].text.strip()
                                                            porcentaje = celdas[3].text.strip()
                                                            # Escribir fila de candidato
                                                            writer.writerow([provincia_nombre, canton_nombre, canton_valor,
                                                                             parroquia_nombre, parroquia_valor, "Candidato",
                                                                             lista_siglas, candidato, votos, porcentaje, "", ""])
                                                    
                                                    filas_indicadores = driver.find_elements(By.XPATH, "//tr[contains(@class, 'tdTablaPro')]")
                                                    for fila in filas_indicadores:
                                                        celdas = fila.find_elements(By.TAG_NAME, "td")
                                                        if len(celdas) == 2:
                                                            label = celdas[0].text.strip()
                                                            valor_indicador = celdas[1].text.strip()
                                                            indicador = ""
                                                            # Mapeo de indicadores (ajustar si es necesario)
                                                            if "Blancos" in label: indicador = "Blancos"
                                                            elif "Nulos" in label: indicador = "Nulos"
                                                            elif "Sufragantes" in label: indicador = "Sufragantes"
                                                            elif "Ausentismo" in label: indicador = "Ausentismo"
                                                            else: continue # Saltar si no es un indicador conocido
                                                            # Escribir fila de indicador
                                                            writer.writerow([provincia_nombre, canton_nombre, canton_valor,
                                                                             parroquia_nombre, parroquia_valor, "Indicador",
                                                                             "", "", "", "", indicador, valor_indicador])
                                                    csv_file.flush() # Forzar escritura al disco periódicamente
                                                except Exception as extr_err:
                                                     print(f"Error extrayendo datos para {provincia_nombre}>{canton_nombre}>{parroquia_nombre}: {extr_err}")

                                            else:
                                                print(f"      Fallo al consultar datos para parroquia: {parroquia_nombre}")
                                                # Considerar si continuar o detenerse aquí
                                            
                                            time.sleep(2) # Pausa antes de la siguiente parroquia

                                    except (NoSuchElementException, TimeoutException):
                                         print(f"    No se encontró el dropdown de parroquias o no cargó para cantón {canton_nombre}. Saltando.")
                                    except Exception as e:
                                         print(f"    Error procesando parroquias en cantón {canton_nombre}: {e}")

                                # Fin del bucle de cantones en circunscripción
                          # Fin del bucle de circunscripciones
                     else:
                          # Si no hay circunscripciones, procesar cantones directamente (copiado abajo)
                          raise ValueError("Se esperaba circunscripción pero no había opciones.") # Forzar ir al bloque 'except' o 'else'
                else:
                     # Si el dropdown de circunscripción no es usable, asumir procesamiento directo por cantón
                     raise ValueError("Dropdown de circunscripción no usable.")

            except (NoSuchElementException, ValueError): # Atrapa la no existencia o el error forzado
                # Caso 2: Procesar directamente por Cantón
                print(f"Provincia {provincia_nombre} no parece tener circunscripciones activas. Procesando por cantón.")
                cantones_dropdown = wait.until(EC.presence_of_element_located((By.ID, "ddlCanton"))) # Re-asegurar elemento
                select_cantones = Select(cantones_dropdown)
                lista_cantones = select_cantones.options[1:] # Omitir "TODOS"

                for canton_option in lista_cantones:
                    canton_valor = canton_option.get_attribute("value")
                    canton_nombre = canton_option.text.strip()
                    if not canton_valor: continue

                    # --- Lógica de Reanudación (Cantón) ---
                    if not empezar_procesamiento and provincia_nombre == ultimo_provincia and canton_nombre < ultimo_canton:
                        print(f"  Saltando cantón ya procesado: {canton_nombre}")
                        continue
                    elif not empezar_procesamiento and provincia_nombre == ultimo_provincia and canton_nombre == ultimo_canton:
                         print(f"  Reanudando en cantón: {canton_nombre}")
                         pass # Continuar al nivel de parroquia
                    elif not empezar_procesamiento and provincia_nombre == ultimo_provincia and canton_nombre > ultimo_canton:
                         print(f"  Comenzando procesamiento normal desde cantón: {canton_nombre}")
                         empezar_procesamiento = True

                    print(f"  Seleccionando cantón: {canton_nombre}")
                    try:
                        # Re-encontrar elemento
                        cantones_dropdown_actual = wait.until(EC.presence_of_element_located((By.ID, "ddlCanton")))
                        select_cantones_actual = Select(cantones_dropdown_actual)
                        select_cantones_actual.select_by_value(canton_valor)
                        time.sleep(3) # Esperar carga de parroquias
                    except Exception as e:
                         print(f"Error seleccionando cantón {canton_nombre}: {e}. Saltando cantón.")
                         continue

                    # Procesar Parroquias dentro de este cantón
                    try:
                        parroquias_dropdown = wait.until(EC.presence_of_element_located((By.ID, "ddlParroquia")))
                        select_parroquias = Select(parroquias_dropdown)
                        lista_parroquias = select_parroquias.options[1:] # Omitir "TODOS"

                        for parroquia_option in lista_parroquias:
                            parroquia_valor = parroquia_option.get_attribute("value")
                            parroquia_nombre = parroquia_option.text.strip()
                            if not parroquia_valor: continue
                            
                            # --- Lógica de Reanudación (Parroquia) ---
                            if not empezar_procesamiento and provincia_nombre == ultimo_provincia and canton_nombre == ultimo_canton and parroquia_nombre <= ultimo_parroquia:
                                print(f"    Saltando parroquia ya procesada: {parroquia_nombre}")
                                continue # Saltar esta parroquia

                            # Si llegamos aquí, debemos procesar
                            empezar_procesamiento = True 

                            print(f"    Procesando parroquia: {parroquia_nombre}")
                            try:
                                # Re-encontrar elemento
                                parroquias_dropdown_actual = wait.until(EC.presence_of_element_located((By.ID, "ddlParroquia")))
                                select_parroquias_actual = Select(parroquias_dropdown_actual)
                                select_parroquias_actual.select_by_value(parroquia_valor)
                                time.sleep(2)
                            except Exception as e:
                                print(f"Error seleccionando parroquia {parroquia_nombre}: {e}. Saltando parroquia.")
                                continue

                            # --- Click en Consultar y Extracción ---
                            if click_consultar(wait, (By.ID, "btnConsultar")):
                                time.sleep(4) # Espera más larga para carga de datos

                                # --- Extracción de datos (igual que antes) ---
                                try:
                                    filas_candidatos = driver.find_elements(By.XPATH, "//table[@id='tablaCandi']/tbody/tr")
                                    for fila in filas_candidatos:
                                        celdas = fila.find_elements(By.TAG_NAME, "td")
                                        if len(celdas) >= 4:
                                            lista_siglas = celdas[0].text.strip(); candidato = celdas[1].text.strip(); votos = celdas[2].text.strip(); porcentaje = celdas[3].text.strip()
                                            writer.writerow([provincia_nombre, canton_nombre, canton_valor, parroquia_nombre, parroquia_valor, "Candidato", lista_siglas, candidato, votos, porcentaje, "", ""])
                                            
                                    filas_indicadores = driver.find_elements(By.XPATH, "//tr[contains(@class, 'tdTablaPro')]")
                                    for fila in filas_indicadores:
                                         celdas = fila.find_elements(By.TAG_NAME, "td")
                                         if len(celdas) == 2:
                                             label = celdas[0].text.strip(); valor_indicador = celdas[1].text.strip(); indicador = ""
                                             if "Blancos" in label: indicador = "Blancos"
                                             elif "Nulos" in label: indicador = "Nulos"
                                             elif "Sufragantes" in label: indicador = "Sufragantes"
                                             elif "Ausentismo" in label: indicador = "Ausentismo"
                                             else: continue
                                             writer.writerow([provincia_nombre, canton_nombre, canton_valor, parroquia_nombre, parroquia_valor, "Indicador", "", "", "", "", indicador, valor_indicador])
                                    csv_file.flush() # Forzar escritura
                                except Exception as extr_err:
                                    print(f"Error extrayendo datos para {provincia_nombre}>{canton_nombre}>{parroquia_nombre}: {extr_err}")

                            else:
                                print(f"    Fallo al consultar datos para parroquia: {parroquia_nombre}")

                            time.sleep(2) # Pausa antes de la siguiente parroquia

                    except (NoSuchElementException, TimeoutException):
                         print(f"  No se encontró el dropdown de parroquias o no cargó para cantón {canton_nombre}. Saltando.")
                    except Exception as e:
                         print(f"  Error procesando parroquias en cantón {canton_nombre}: {e}")

                # Fin del bucle de cantones (sin circunscripción)

        except (NoSuchElementException, TimeoutException) as e:
             print(f"Error al intentar encontrar dropdown de cantón o circunscripción para provincia {provincia_nombre}: {e}")
        except Exception as e:
            print(f"Error general procesando cantones/circunscripciones en provincia {provincia_nombre}: {e}")

    # Fin del bucle de provincias
    print(f"Proceso completo (o reanudado). Resultados guardados/añadidos en '{output_path}'.")

except Exception as main_error:
    print(f"Ocurrió un error inesperado en el script principal: {main_error}")

finally:
    # Asegurarse de cerrar el archivo y el navegador
    if 'csv_file' in locals() and csv_file and not csv_file.closed:
        csv_file.close()
        print("Archivo CSV cerrado.")
    if 'driver' in locals() and driver:
        driver.quit()
        print("Navegador cerrado.")