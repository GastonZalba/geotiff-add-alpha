import os
import numpy as np

from osgeo import gdal
from osgeo.gdalconst import GA_ReadOnly

import params as params

def getExtension(filename):
    return os.path.splitext(filename)[1]

def main():
    if params.as_internal_mask:
        gdal.SetConfigOption('GDAL_TIFF_INTERNAL_MASK', 'YES')

    for subdir, dirs, files in os.walk(params.input_folder):
        for file in files:
            filepath = subdir + os.sep + file
            if (getExtension(file) in params.extensions):
                
                output_file = f'{params.output_folder}/{file}'
                
                if (os.path.exists(output_file) and params.skip_existing):
                    continue
                
                dataset = gdal.Open(filepath, GA_ReadOnly)    

                # Leer la banda de datos RGB
                red_band = dataset.GetRasterBand(1).ReadAsArray()
                green_band = dataset.GetRasterBand(2).ReadAsArray()
                blue_band = dataset.GetRasterBand(3).ReadAsArray()
                
                nodata = params.nodata

                # Crear una máscara basada en los valores de nodata
                mask = np.where(np.logical_and(red_band == nodata, green_band == nodata, blue_band == nodata), 0, 255).astype(np.uint8)
                
                alpha_band = np.where(mask == 0, 0, 255).astype(np.uint8)

                # Crear un nuevo archivo GeoTIFF con la máscara
                driver = gdal.GetDriverByName('GTiff')
                masked_dataset = driver.Create(
                    output_file,
                    dataset.RasterXSize, 
                    dataset.RasterYSize, 
                    3 if params.as_internal_mask else 4, 
                    gdal.GDT_Byte, 
                    options=['COMPRESS=DEFLATE']
                )
                masked_dataset.SetGeoTransform(dataset.GetGeoTransform())
                masked_dataset.SetProjection(dataset.GetProjection())

                # Escribir los datos en el nuevo archivo GeoTIFF
                masked_dataset.GetRasterBand(1).WriteArray(red_band)
                masked_dataset.GetRasterBand(2).WriteArray(green_band)
                masked_dataset.GetRasterBand(3).WriteArray(blue_band)

                if params.as_internal_mask:
                    #https://gdal.org/development/rfc/rfc15_nodatabitmask.html#default-createmaskband
                    masked_dataset.CreateMaskBand(gdal.GMF_PER_DATASET)
                    for iBand in range(1, 4):
                        inband = masked_dataset.GetRasterBand(iBand)
                        inband.GetMaskBand().WriteArray(alpha_band)
                else:
                    masked_dataset.GetRasterBand(4).WriteArray(alpha_band)

                dataset = None
                masked_dataset = None


if __name__ == '__main__':
    main()
