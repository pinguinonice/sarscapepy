# sarscapepy
A Python module to read and interprete H3 SARscape 5.5X Data.

## Animation of time series

Visualize SBAS and PSI results as a gif animation


![prediction example](examples/example_animatedDef/animation.gif)

see example_animatedDef

## Read and display
Import a PSI or SBAS result shapefile.
Interpolate to raster with  variable gridding and distance.


## Temporal reampling
Temporal resample SBAS or PSI results, i.e. to bring them on an equal time axis.
![prediction example](examples/example_show_temporalResample/image.png)

see example_show_temporalResample

## Show Aquisition timeline
Diplay the Aquisitiontimes of a SBAS or PSI result.

![prediction example](examples/example_show_acquisitionTimes/image.png)


## Show deformation History for a a point

Click on Map and display the deformation History for this point.

![prediction example](examples/example_show_deformationHistoryForOnePoint/image.png)


## Decomposition 
Decomposition of two orbit observation into vertical and horizontal components.

Vertical (Up-Down):
![prediction example](examples/example_decomposition_and_animate_two_LOS/animation_vertPSI.gif)

Horizontal (West-East):
![prediction example](examples/example_decomposition_and_animate_two_LOS/animation.gif)

see example_decomposition_and_animate_two_LOS

## Export as shapefile
Export results as shapefile.

To display in external GIS.

