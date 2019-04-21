## Background

Landsat-8 Level 1 scenes come with a quality assessment band (BQA) that shows various forms of atmospheric and other interference present in the image.

The accompanying BQA file is a GeoTIFF with bit-packed values corresponding to an internal USGS numbering scheme. You can learn about these values and the BQA band in general by reading the USGS overview located [here](https://www.usgs.gov/land-resources/nli/landsat/landsat-collection-1-level-1-quality-assessment-band?qt-science_support_page_related_con=0#qt-science_support_page_related_con). There is also a more in-depth PDF titled 'Landsat Quality Assessment (QA) Tools User's Guide'.

## Usage

This CLI tool may be useful to you if you are working with Landsat-8 quality assessment data in Python 3.

This tool is written to search the directory where it is run, and all sub-directories for Landsat-8 BQA bands. It then 'unpacks' the bit packed BQA raster and creates a new GeoTIFF for each USGS quality measure that the user specifies. Finally, the tool takes the new quality bands for each scene and creates a composite image stack for each quality control measure.

For example, you can take a directory of Landsat-8 scenes, pull out all cloudy pixels, and create a composite image showing all cloudy pixels in the stack.

This is helpful for time series analysis because you can identify atmospheric interference over time.

Flags correspond to each quality assessment layer identified by USGS.
The following will produce individual BQA band files for every quality assessment type identified by USGS and then build composites from each quality assessment type.

```commandline
cd /filepath/to/top_dir_for_landsat_scenes
landsat_L1_qa_tool -c -f -t -r -cl -cc -cs -ci -s
```

Quality assessment types:
```commandline
-c --clear-terrain
-f --fill
-t --terrain-occlusion
-r --radiometric-saturation
-cl --clouds
-cc --cloud-confidence
-cs --cloud-shadow
-ci --cirrus
-s --snow-ice
```
