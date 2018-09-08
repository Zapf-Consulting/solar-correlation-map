# Solar Correlation Map
A new way to visualize correlations. 

## Basic usage
``python solar_corr.py CSV_FILE_PATH SUN_VARIABLE [IMAGE_FILE_NAME]``


The csv file must have a header that includes the variable/column names in the first line.

The csv file is your original data set, you do not need to create a correlation matrix yourself, we got you covered. 

Currently we do not support factor variables, please transform them beforehand. 

The sun variable is the dependentant variable in the center of solar system.

The image file name is optional and can be used to change the default file name "solar.png".


## Example
``python solar_corr.py jedi.csv JEDI jedi.png``

![solar correlation map](https://github.com/Zapf-Consulting/solar-correlation-map/blob/master/solar.png "Solar Correlation Map example")

[Zapf Consulting](http://www.zapf-consulting.com/)


