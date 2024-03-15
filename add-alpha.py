import os
import sys
import numpy as np
from pathlib import Path

from osgeo import gdal
from osgeo.gdalconst import GA_ReadOnly

import params as params

def get_extension(filename):
    return os.path.splitext(filename)[1]

def process_file(filepath):

    if (get_extension(filepath) in params.extensions):
        
        if not params.output_folder:
            output_file = os.path.join(os.path.dirname(filepath), f'_processed_{os.path.basename(filepath)}')
        else:
            if not os.path.isdir(params.output_folder):
                sys.exit('ERROR: Output folder doesn\'t exist')
            
            output_file = os.path.join(params.output_folder, f'{os.path.basename(filepath)}')
        
        if (os.path.exists(output_file) and params.skip_existing):
            print(f'Skipping existing file {output_file}')
            return
        
        print(f'Processing file {output_file}')

        dataset = gdal.Open(str(filepath), GA_ReadOnly)    

        red_band = dataset.GetRasterBand(1).ReadAsArray()
        green_band = dataset.GetRasterBand(2).ReadAsArray()
        blue_band = dataset.GetRasterBand(3).ReadAsArray()
        
        if isinstance(params.nodata_src, int):
            nodata = params.nodata_src
        else:
            nodata = red_band.GetNoDataValue()

        alpha_band = np.where(np.logical_and(red_band == nodata, green_band == nodata, blue_band == nodata), 0, 255).astype(np.uint8)
        
        if isinstance(params.no_data_target, int):
            red_band = np.where(alpha_band == 0, params.no_data_target, red_band)
            green_band = np.where(alpha_band == 0, params.no_data_target, green_band)
            blue_band = np.where(alpha_band == 0, params.no_data_target, blue_band)
        
        driver = gdal.GetDriverByName('GTiff')
        masked_dataset = driver.Create(
            output_file,
            dataset.RasterXSize, 
            dataset.RasterYSize, 
            3 if params.as_internal_mask else 4, 
            gdal.GDT_Byte, 
            options=params.image_options
        )
        masked_dataset.SetGeoTransform(dataset.GetGeoTransform())
        masked_dataset.SetProjection(dataset.GetProjection())

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

def process_folder(folder):
    folder_path = Path(folder)
    
    for subdir in folder_path.iterdir():
        if subdir.is_dir():
            process_folder(subdir)
        else:
            process_file(subdir)

def main():
    if params.as_internal_mask:
        gdal.SetConfigOption('GDAL_TIFF_INTERNAL_MASK', 'YES')
    
    process_folder(params.input_folder)

if __name__ == '__main__':
    main()
