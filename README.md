# add-alpha

Script en Python para procesar GeoTiffs RGB y agregarles canal alpha a partir de un valor noData en específico. 

## Instalación

- Descargar e instalar [Python](https://www.python.org/downloads/)
- Testear en console `python --version` y `pip --version` para corroborar que esté todo andando.
- Descargar [GDAL](https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal), seleccionando la versión más nueva de GDAL, y la adecuada según la versión de Python instalado y el procesador. Si se está usando Python 3.7, por ejemplo, descargar y luego instalar usando `pip install GDAL-3.3.1-cp37-cp37m-win_amd64.whl` (siempre ajustando según la versión descargada).
- Para poder usar el paquete instalado desde la consola, configurar variables de entorno (poniendo la ruta completa según donde esté instalado el paquete y la versión de python):
  - `GDAL_DATA`: '...\Python\Python37\Lib\site-packages\osgeo\data\gdal'
  - `PROJ_LIB`: '...\Python\Python37\Lib\site-packages\osgeo\data\proj'
  - Agregar a la variable `Path` la ruta '...\Python\Python37\Lib\site-packages\osgeo'
  - Chequear en consola `gdalinfo --version`.
- Instalar la librería Numpy mediante el comando `pip install numpy`.

## Configuración

- Modificar archivo `params.py`.