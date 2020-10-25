# CDR-project
Building a Telecom CDR Data Analytics Project.

## About the data:
It is a real-time data compromising of 16737 rows and 435 Columns in raw and unfiltered format.

## Creating the User Interface

The data was cleaned using using python and its different libraries and creating a UI with table and graphical 
representation based on the filtration of Start date and End date, Group and based on Hourly, Weekly and Daily basis.

The raw data was cleaned and divided in various files, Call_data, Device_data, Service_data.

Dash and its various components were used to create the UI.

```sh
import dash
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table as dt
```

And various tabs were created to show different graphs and data.

## Results

Line Graph
![image](https://user-images.githubusercontent.com/73426895/97107108-c26d4a00-16eb-11eb-96de-b1b9d8496894.png)


![image](https://user-images.githubusercontent.com/73426895/97107238-838bc400-16ec-11eb-84cd-3527b179c943.png)


![image](https://user-images.githubusercontent.com/73426895/97107276-b46bf900-16ec-11eb-8265-0608a60873fd.png)


## Final Notes

What's in the files?

1. Data Cleaning.py has the code to clean the data.
2. Main UI App.py has the code to locally host the solution.


Thank You!










