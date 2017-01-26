# Solar Correlation Map
A new way to visualize correlations. 

## Installation

Install the solar correlation map with:
``pip install solar-correlation-map``


## Basic usage
``python -m solar_correlation_map CSV_FILE_PATH SUN_VARIABLE [IMAGE_FILE_NAME]``


The csv file must have a header that includes the variable/column names in the first line.

The sun variable is the dependentant variable in the center of solar system.

The image file name is optional and can be used to change the default file name "solar.png".


## Example
``python -m solar_correlation_map jedi.csv JEDI jedi.png``

![solar correlation map](https://github.com/Zapf-Consulting/solar-correlation-map/blob/master/solar.png "Solar Correlation Map example")

[Zapf Consulting](http://www.zapf-consulting.com/)


