# Analyzing-Coronavirus-Covid-19

Graphing data is stored at Johns Hopkins University and obtained through covid-data-api. Data is updated after 24 hours.

To build for a given country, you must first import
```python
from utils import *
```

pass the list of countries to the plot_locations () function
```python
locations = ['world', 'US', 'China', 'Russia']
plot_locations(df, locations)
```
you can see the list of available countries as follows 
```python
api.show_available_countries()
```
