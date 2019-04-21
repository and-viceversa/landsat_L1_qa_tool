
import os
import argparse
import sys
from osgeo import gdal
from osgeo import gdalconst


class QualityBandConverter:

    def __init__(self, args):
        self.args = args
        self.bqa_dict = {}
        self.nodatavalue = gdal.GDT_UInt16

        if self.args.cirrus:
            self.cirrus_dict = {}

        if self.args.clear_terrain:
            self.clear_terrain_dict = {}

        if self.args.cloud_confidence:
            self.cloud_conf_dict = {}

        if self.args.cloud_shadow:
            self.cloud_shadow_dict = {}

        if self.args.clouds:
            self.clouds_dict = {}

        if self.args.radiometric_saturation:
            self.rad_sat_dict = {}

        if self.args.snow_ice:
            self.snow_ice_dict = {}

        if self.args.terrain_occlusion:
            self.terrain_occlusion_dict = {}

        if self.args.fill:
            self.fill_dict = {}

    def find_bqa_files(self):
        print('Searching for Landsat-8 BQA files...')
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file[-8:] == '_BQA.TIF':
                    self.bqa_dict[root] = file
                    print(' Found ', os.path.join(root, file))

    def split_qa_bands(self):

        print('Writing individual QA files...')

        for key in self.bqa_dict:
            root = key
            file_name = self.bqa_dict[key]
            val_set = set()
            print(' Reading', file_name)

            # Get input file
            driver = gdal.GetDriverByName('GTiff')  # open GeoTIFF driver
            driver.Register()                       # register driver

            # Open the BQA file as a GDAL DataSet
            input_bqa_dataset = gdal.Open(os.path.join(root, file_name), gdalconst.GA_ReadOnly)

            cols = input_bqa_dataset.RasterXSize                            # get required attributes
            rows = input_bqa_dataset.RasterYSize
            projection = input_bqa_dataset.GetProjection()
            metadata = input_bqa_dataset.GetMetadata()
            geo_transform = input_bqa_dataset.GetGeoTransform()

            input_bqa_band = input_bqa_dataset.GetRasterBand(1)             # get the BQA band
            input_bqa_data = input_bqa_band.ReadAsArray(0, 0, cols, rows)   # read band into an Array

            # Initialize appropriate band files from command line arguments.
            if self.args.fill:
                fill_suffix = '/' + file_name[0:-4] + '_fill_data.tif'
                self.fill_dict[root] = fill_suffix
                fill_dataset = driver.Create(root + fill_suffix, cols, rows, 1, gdal.GDT_UInt16)
                fill_band = fill_dataset.GetRasterBand(1)
                fill_values = fill_band.ReadAsArray(0, 0, cols, rows)
                val_set.add(1)

            if self.args.terrain_occlusion:
                terrain_occlusion_suffix = '/' + file_name[0:-4] + '_terrain_occlusion.tif'
                self.terrain_occlusion_dict[root] = terrain_occlusion_suffix
                terrain_occlusion_dataset = driver.Create(root + terrain_occlusion_suffix, cols, rows, 1,
                                                          gdal.GDT_UInt16)
                terrain_occlusion_band = terrain_occlusion_dataset.GetRasterBand(1)
                terrain_occlusion_values = terrain_occlusion_band.ReadAsArray(0, 0, cols, rows)
                val_set.add(2)

            if self.args.radiometric_saturation:
                rad_sat_suffix = '/' + file_name[0:-4] + '_radiometric_saturation.tif'
                self.rad_sat_dict[root] = rad_sat_suffix
                rad_sat_dataset = driver.Create(root + rad_sat_suffix, cols, rows, 1, gdal.GDT_UInt16)
                rad_sat_band = rad_sat_dataset.GetRasterBand(1)
                rad_sat_values = rad_sat_band.ReadAsArray(0, 0, cols, rows)
                val_set.add(2724), val_set.add(2728), val_set.add(2732), val_set.add(2804), \
                    val_set.add(2808), val_set.add(2812), val_set.add(3748), val_set.add(3752), \
                    val_set.add(3756), val_set.add(6820), val_set.add(6824), val_set.add(6828)

            if self.args.clouds:
                clouds_suffix = '/' + file_name[0:-4] + '_clouds.tif'
                self.clouds_dict[root] = clouds_suffix
                clouds_dataset = driver.Create(root + clouds_suffix, cols, rows, 1, gdal.GDT_UInt16)
                clouds_band = clouds_dataset.GetRasterBand(1)
                clouds_values = clouds_band.ReadAsArray(0, 0, cols, rows)
                val_set.add(2800), val_set.add(2804), val_set.add(2808), val_set.add(2812), val_set.add(6896)

            if self.args.cloud_confidence:
                cloud_conf_suffix = '/' + file_name[0:-4] + '_cloud_confidence.tif'
                self.cloud_conf_dict[root] = cloud_conf_suffix
                cloud_conf_dataset = driver.Create(root + cloud_conf_suffix, cols, rows, 1, gdal.GDT_UInt16)
                cloud_conf_band = cloud_conf_dataset.GetRasterBand(1)
                cloud_conf_values = cloud_conf_band.ReadAsArray(0, 0, cols, rows)
                val_set.add(2752), val_set.add(2800), val_set.add(2804), val_set.add(2808), val_set.add(2812), \
                    val_set.add(6896)

            if self.args.cloud_shadow:
                cloud_shadow_suffix = '/' + file_name[0:-4] + '_cloud_shadow.tif'
                self.cloud_shadow_dict[root] = cloud_shadow_suffix
                cloud_shadow_dataset = driver.Create(root + cloud_shadow_suffix, cols, rows, 1, gdal.GDT_UInt16)
                cloud_shadow_band = cloud_shadow_dataset.GetRasterBand(1)
                cloud_shadow_values = cloud_shadow_band.ReadAsArray(0, 0, cols, rows)
                val_set.add(2976), val_set.add(7072)

            if self.args.snow_ice:
                snow_ice_suffix = '/' + file_name[0:-4] + '_snow_ice.tif'
                self.snow_ice_dict[root] = snow_ice_suffix
                snow_ice_dataset = driver.Create(root + snow_ice_suffix, cols, rows, 1, gdal.GDT_UInt16)
                snow_ice_band = snow_ice_dataset.GetRasterBand(1)
                snow_ice_values = snow_ice_band.ReadAsArray(0, 0, cols, rows)
                val_set.add(3756), val_set.add(3752), val_set.add(3748), val_set.add(3744)

            if self.args.cirrus:
                cirrus_suffix = '/' + file_name[0:-4] + '_cirrus.tif'
                self.cirrus_dict[root] = cirrus_suffix
                cirrus_dataset = driver.Create(root + cirrus_suffix, cols, rows, 1, gdal.GDT_UInt16)
                cirrus_band = cirrus_dataset.GetRasterBand(1)
                cirrus_values = cirrus_band.ReadAsArray(0, 0, cols, rows)
                val_set.add(6816), val_set.add(6820), val_set.add(6824), val_set.add(6828), val_set.add(6896), \
                    val_set.add(7072)

            if self.args.clear_terrain:
                clear_terrain_suffix = '/' + file_name[0:-4] + '_clear_terrain.tif'
                self.clear_terrain_dict[root] = clear_terrain_suffix
                clear_terrain_dataset = driver.Create(root + clear_terrain_suffix, cols, rows, 1, gdal.GDT_UInt16)
                clear_terrain_band = clear_terrain_dataset.GetRasterBand(1)
                clear_terrain_values = clear_terrain_band.ReadAsArray(0, 0, cols, rows)
                val_set.add(2720), val_set.add(2724), val_set.add(2728), val_set.add(2732)

            # Traverse entire input BQA image, assign values in the new QA bands.
            for y in range(0, rows):
                for x in range(0, cols):
                    val = int(input_bqa_data[y][x])

                    if val in val_set:

                        if self.args.fill:
                            if val == 1:
                                fill_values[y][x] = 1
                                continue

                        if self.args.terrain_occlusion:
                            if val == 2:
                                terrain_occlusion_values[y][x] = 2
                                continue

                        if self.args.cloud_shadow:
                            if val in (2976, 7072):
                                cloud_shadow_values[y][x] = val

                        if self.args.clear_terrain:
                            if val in (2720, 2724, 2728, 2732):
                                clear_terrain_values[y][x] = val

                        if self.args.radiometric_saturation:
                            if val in (2724, 2728, 2732, 2804, 2808, 2812, 3748, 3752, 3756, 6820, 6824, 6828):
                                rad_sat_values[y][x] = val

                        if self.args.clouds:
                            if val in (2800, 2804, 2808, 2812, 6896):
                                clouds_values[y][x] = val

                        if self.args.cloud_confidence:
                            if val in (2752, 2800, 2804, 2808, 2812, 6896):
                                cloud_conf_values[y][x] = val

                        if self.args.cirrus:
                            if val in (6816, 6820, 6824, 6828, 6896, 7072):
                                cirrus_values[y][x] = val

                        if self.args.snow_ice:
                            if val in (3756, 3752, 3748, 3744):
                                snow_ice_values[y][x] = val

            # Write value Arrays and other attributes.
            if self.args.fill:
                print('     Writing', file_name, 'fill file.')
                fill_band.WriteArray(fill_values, 0, 0)
                fill_band.SetNoDataValue(self.nodatavalue)
                fill_dataset.SetProjection(projection)
                fill_dataset.SetGeoTransform(geo_transform)
                fill_dataset.SetMetadata(metadata)

            if self.args.terrain_occlusion:
                print('     Writing', file_name, 'terrain_occlusion file.')
                terrain_occlusion_band.WriteArray(terrain_occlusion_values, 0, 0)
                terrain_occlusion_band.SetNoDataValue(self.nodatavalue)
                terrain_occlusion_dataset.SetProjection(projection)
                terrain_occlusion_dataset.SetGeoTransform(geo_transform)
                terrain_occlusion_dataset.SetMetadata(metadata)

            if self.args.radiometric_saturation:
                print('     Writing', file_name, 'radiometric_saturation file.')
                rad_sat_band.WriteArray(rad_sat_values, 0, 0)
                rad_sat_band.SetNoDataValue(self.nodatavalue)
                rad_sat_dataset.SetProjection(projection)
                rad_sat_dataset.SetGeoTransform(geo_transform)
                rad_sat_dataset.SetMetadata(metadata)

            if self.args.clouds:
                print('     Writing', file_name, 'clouds file.')
                clouds_band.WriteArray(clouds_values, 0, 0)
                clouds_band.SetNoDataValue(self.nodatavalue)
                clouds_dataset.SetProjection(projection)
                clouds_dataset.SetGeoTransform(geo_transform)
                clouds_dataset.SetMetadata(metadata)

            if self.args.cloud_confidence:
                print('     Writing', file_name, 'cloud_confidence file.')
                cloud_conf_band.WriteArray(cloud_conf_values, 0, 0)
                cloud_conf_band.SetNoDataValue(self.nodatavalue)
                cloud_conf_dataset.SetProjection(projection)
                cloud_conf_dataset.SetGeoTransform(geo_transform)
                cloud_conf_dataset.SetMetadata(metadata)

            if self.args.cloud_shadow:
                print('     Writing', file_name, 'cloud_shadow file.')
                cloud_shadow_band.WriteArray(cloud_shadow_values, 0, 0)
                cloud_shadow_band.SetNoDataValue(self.nodatavalue)
                cloud_shadow_dataset.SetProjection(projection)
                cloud_shadow_dataset.SetGeoTransform(geo_transform)
                cloud_shadow_dataset.SetMetadata(metadata)

            if self.args.snow_ice:
                print('     Writing', file_name, 'snow and ice file.')
                snow_ice_band.WriteArray(snow_ice_values, 0, 0)
                snow_ice_band.SetNoDataValue(self.nodatavalue)
                snow_ice_dataset.SetProjection(projection)
                snow_ice_dataset.SetGeoTransform(geo_transform)
                snow_ice_dataset.SetMetadata(metadata)

            if self.args.cirrus:
                print('     Writing', file_name, 'cirrus file.')
                cirrus_band.WriteArray(cirrus_values, 0, 0)
                cirrus_band.SetNoDataValue(self.nodatavalue)
                cirrus_dataset.SetProjection(projection)
                cirrus_dataset.SetGeoTransform(geo_transform)
                cirrus_dataset.SetMetadata(metadata)

            if self.args.clear_terrain:
                print('     Writing', file_name, 'clear_terrain file.')
                clear_terrain_band.WriteArray(clear_terrain_values, 0, 0)
                clear_terrain_band.SetNoDataValue(self.nodatavalue)
                clear_terrain_dataset.SetProjection(projection)
                clear_terrain_dataset.SetGeoTransform(geo_transform)
                clear_terrain_dataset.SetMetadata(metadata)

    def build_composites(self):

        print('Building composites...')

        image_list = []

        if self.args.fill:
            print('Building fill composite...')
            for key in self.fill_dict:
                image_list.append(key + self.fill_dict[key])

            out_vrt = './outvrt.vrt'
            out_image = './fill_composite.tif'
            out_ds = gdal.BuildVRT(out_vrt, image_list, separate=True)
            out_ds = gdal.Translate(out_image, out_ds)
            image_list.clear()
            os.system('rm ./outvrt.vrt')

        if self.args.terrain_occlusion:
            print('Building terrain_occlusion composite...')
            for key in self.terrain_occlusion_dict:
                image_list.append(key + self.terrain_occlusion_dict[key])

            out_vrt = './outvrt.vrt'
            out_image = './terrain_occlusion_composite.tif'
            out_ds = gdal.BuildVRT(out_vrt, image_list, separate=True)
            out_ds = gdal.Translate(out_image, out_ds)
            image_list.clear()
            os.system('rm ./outvrt.vrt')

        if self.args.clear_terrain:
            print('Building clear_terrain composite...')
            for key in self.clear_terrain_dict:
                image_list.append(key + self.clear_terrain_dict[key])

            out_vrt = './outvrt.vrt'
            out_image = './clear_terrain_composite.tif'
            out_ds = gdal.BuildVRT(out_vrt, image_list, separate=True)
            out_ds = gdal.Translate(out_image, out_ds)
            image_list.clear()
            os.system('rm outvrt.vrt')

        if self.args.radiometric_saturation:
            print('Building radiometric_saturation composite...')
            for key in self.rad_sat_dict:
                image_list.append(key + self.rad_sat_dict[key])

            out_vrt = './outvrt.vrt'
            out_image = './radiometric_saturation_composite.tif'
            out_ds = gdal.BuildVRT(out_vrt, image_list, separate=True)
            out_ds = gdal.Translate(out_image, out_ds)
            image_list.clear()
            os.system('rm ./outvrt.vrt')

        if self.args.clouds:
            print('Building clouds composite...')
            for key in self.clouds_dict:
                image_list.append(key + self.clouds_dict[key])

            out_vrt = './outvrt.vrt'
            out_image = './clouds_composite.tif'
            out_ds = gdal.BuildVRT(out_vrt, image_list, separate=True)
            out_ds = gdal.Translate(out_image, out_ds)
            image_list.clear()
            os.system('rm ./outvrt.vrt')

        if self.args.cloud_confidence:
            print('Building cloud_confidence composite...')
            for key in self.cloud_conf_dict:
                image_list.append(key + self.cloud_conf_dict[key])

            out_vrt = './outvrt.vrt'
            out_image = './cloud_confidence_composite.tif'
            out_ds = gdal.BuildVRT(out_vrt, image_list, separate=True)
            out_ds = gdal.Translate(out_image, out_ds)
            image_list.clear()
            os.system('rm ./outvrt.vrt')

        if self.args.cloud_shadow:
            print('Building cloud_shadow composite...')
            for key in self.cloud_shadow_dict:
                image_list.append(key + self.cloud_shadow_dict[key])

            out_vrt = './outvrt.vrt'
            out_image = './cloud_shadow_composite.tif'
            out_ds = gdal.BuildVRT(out_vrt, image_list, separate=True)
            out_ds = gdal.Translate(out_image, out_ds)
            image_list.clear()
            os.system('rm ./outvrt.vrt')

        if self.args.cirrus:
            print('Building cirrus composite...')
            for key in self.cirrus_dict:
                image_list.append(key + self.cirrus_dict[key])

            out_vrt = './outvrt.vrt'
            out_image = './cirrus_composite.tif'
            out_ds = gdal.BuildVRT(out_vrt, image_list, separate=True)
            out_ds = gdal.Translate(out_image, out_ds)
            image_list.clear()
            os.system('rm ./outvrt.vrt')

        if self.args.snow_ice:
            print('Building snow_ice composite...')
            for key in self.snow_ice_dict:
                image_list.append(key + self.snow_ice_dict[key])

            out_vrt = './outvrt.vrt'
            out_image = './snow_ice_composite.tif'
            out_ds = gdal.BuildVRT(out_vrt, image_list, separate=True)
            out_ds = gdal.Translate(out_image, out_ds)
            image_list.clear()
            os.system('rm ./outvrt.vrt')


def parse_args():
    parser = argparse.ArgumentParser(
        description='Search through current directory and all subdirectories. Unpack Landsat-8'
                    'quality bands based on flags of your choice. Optionally created a quality'
                    'band \'layer stack\' for each Landsat-8 scene. \n')

    parser.add_argument('-c', '--clear-terrain',
                        action='store_const',
                        const='-c',
                        required=False,
                        help='The -c flag will create a new GeoTiff with clear terrain values '
                             '(2720, 2724, 2728, 2732)'
                             'from the Landsat-8 BQA band, and a composite image of the new GeoTiffs. '
                             'This band summarizes pixels with no detected atmospheric interference, but'
                             'may include radiometric saturation. '
                             'This flag alone is probably enough for most cases. \n')
    parser.add_argument('-f', '--fill',
                        action='store_const',
                        const='-f',
                        required=False,
                        help='The -f flag will create a new GeoTIFF with fill value (1) from the'
                             'Landsat-8 BQA band, and a composite image of the new GeoTiffs. '
                             'This is unnecessary for most uses. \n')
    parser.add_argument('-t', '--terrain-occlusion',
                        action='store_const',
                        const='-t',
                        required=False,
                        help='The -t flag will create a new GeoTIFF with terrain occlusion value (2)'
                             'from the Landsat-8 BQA band, and a composite image of the new GeoTiffs. \n')
    parser.add_argument('-r', '--radiometric-saturation',
                        required=False,
                        action='store_const',
                        const='-r',
                        help='The -r flag will create a new GeoTIFF with radiometric saturation values '
                             '(2724, 2728, 2732, 2804, 2808, 2812, 3748, 3752, 3756, 6820, 6824, 6828)'
                             'from the Landsat-8 BQA band, and a composite image of the new GeoTiffs. \n')
    parser.add_argument('-cl', '--clouds',
                        required=False,
                        action='store_const',
                        const='-cl',
                        help='The -cl flag will create a new GeoTIFF with cloud values '
                             '(2800, 2804, 2808, 2812, 6896) from the Landsat-8 BQA band, '
                             'and a composite image of the new GeoTiffs. \n')
    parser.add_argument('-cc', '--cloud-confidence',
                        required=False,
                        action='store_const',
                        const='-cc',
                        help='The -cc flag will create a new GeoTIFF with cloud confidence values'
                             '(2752, 2800, 2804, 2808, 2812, 6896) from the Landsat-8 BQA band, '
                             'and a composite image of the new GeoTiffs. \n')
    parser.add_argument('-cs', '--cloud-shadow',
                        required=False,
                        action='store_const',
                        const='-cs',
                        help='The -cs flag will create a new GeoTIFF with cloud shadow values (2976, 7072)'
                             'from the Landsat-8 BQA band, and a composite image of the new GeoTiffs. \n')
    parser.add_argument('-ci', '--cirrus',
                        required=False,
                        action='store_const',
                        const='-ci',
                        help='The -ci flag will create a new GeoTIFF with cirrus cloud values '
                             '(6816, 6820, 6824, 6828, 6896, 7072) from the Landsat-8 BQA band, '
                             'and a composite image of the new GeoTiffs. \n')
    parser.add_argument('-s', '--snow-ice',
                        required=False,
                        action='store_const',
                        const='-s',
                        help='The -s flag will create a new GeoTIFF with snow and ice values '
                             '(3756, 3752, 3748, 3744) from the Landsat-8 BQA band, '
                             'and a composite image of the new GeoTiffs. \n')
    args = parser.parse_args()

    if len(sys.argv) == 1:
        print('Type landsat_L1_qa_tool -h for help options')
        quit()

    return args


def main():

    args = parse_args()                 # parse command line arguments
    qc = QualityBandConverter(args)     # initialize a QualityBandConverter
    qc.find_bqa_files()                 # find all Landsat-8 BQA files in current dir and all subdirs
    qc.split_qa_bands()                 # make new quality bands based on command line args
    qc.build_composites()               # build QA band composites based on command line args
    print('Done!')


if __name__ == '__main__':
    main()
