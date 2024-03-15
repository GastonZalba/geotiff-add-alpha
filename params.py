input_folder = './in'
extensions = ['.tif', '.tiff']

# use None to use the nodata value stored in the source
nodata_src = 255

# use None to mantain same as src
no_data_target = 0

# False to add the transparency as an alpha band
as_internal_mask = True

image_options = [
    'COMPRESS=JPEG',
    'TILED=YES',
    'PHOTOMETRIC=YCBCR',
    'JPEG_QUALITY=80'
]

# use None to export the file next to the original
output_folder = './out'

skip_existing = True