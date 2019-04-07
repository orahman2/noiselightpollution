# Read-me file

### Description
This repository contians the the user interface code along the various scripts used to 
  - Download data from 3rd party websites
  - Enrich traffic files with various attributes including pollution
  - Perform linear regression
  - Perform logarithmic regression
  - Perform multivariate regression
  - Prepare files for the above types of regression

### Folder structure

The user interface code contains two main folders, namely public which contains root level files and metadate, and src which contains the source code. Within src, App.Test.js contains all the test files, whereas the statistics folder contains all the code to do with the statistics part of the website.

A flat hierarchy has been chosen for the scripts so that the 'utils' file containing commonly used methods and 'constants' file containing data that is static can be re-used. Python requires third party libraries to import modules from parent directories.

### Prerequisites
To run the User Interface, the following software needs to be installed:
  - Latest version of Node.js

All other dependencies will be downloaded via node package manager.

The scripts requires the following libraries to be installed:
  - Python 3.6.6
  - Pip (Package manager)

All of the following libraries used are available through Pip:
  - shapely
  - json
  - simplejson
  - enum34
  - pyopenssl
  - geojson
  - scipy
  - sklearn
  - pandas
  - statsmodels
  - numpy
  - matplotlib

### Usage

To launch the user interface, run the following commands:
```
npm install
npm run dev
```

The commands listed above may take a few minutes depending on your internet connection and machine specifications. Alternatively, the deployed version can be accessed on https://noiselightpollution.herokuapp.com/ .

For the data processing, QGIS (an open source Geographic Information System tool) was used to stitch together and filter geo-encoded data spatially. Given this, and the fact that the scripts are used for various different purposes and run for a very long time, and require data sets that special access needs to be requested for, instructions haven't been explicity given to run these. However, a dependency diagram on how the two main workflows occur is given below. 
## Noise Pollution Workflow
![Noise Pollution Workflow](./noise_pollution_workflow.png?raw=true)
## Light Pollution Workflow
![Light Pollution Workflow](./light_pollution_workflow.png?raw=true)
It is recommended that you don't try and run them as it could easily take more than hours to do so, and the process won't be entirely automatic.  Different data sets are enriched differently for different purposes.

### Credits

[Open Government licence](http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) applies to all data sets provided by the UK Government-related sources, with older versions applying to the older data sets. The following data sources been used in this project:
| Data | Credits |
| ------ | ------ |
| Light Pollution | Earth Observation Group, NOAA National Centers for Environmental Information (NCEI). |
| Noise Pollution | © Crown 2019 copyright Defra via uk-air.defra.gov.uk, licenced under the Open Government Licence (OGL). |
| Data Processing Software | QGIS, Creative Commons Attribution-ShareAlike 3.0 licence (CC BY-SA) |
| Traffic Data | Contains OS data © Crown copyright and database right 2017 |
| Pubs | Contains OS data © Crown copyright and database right (2019), Contains Royal Mail data © Royal Mail copyright and Database right (2019), Contains National Statistics data © Crown copyright and database right (2019), Data produced by Land Registry © Crown copyright (2019), Contains Environment Agency data licensed under the Open Government Licence v3.0, Everything else © GetTheData Publishing Limited (2019) |
| Tube | Open Government Licence with specific amendments for Transport for London |
| Tube Analytics | Greater London Authority |
| Population | Contains OS data © Crown copyright and database right 2011, Contains Royal Mail data © Royal Mail copyright and database right 2011, Contains National Statistics data © Crown copyright and database right 2011 |
| London geographical boundaries |  Contains OS data © Crown copyright and database right 2019, Contains National Statistics data © Crown copyright and database right 2019 |