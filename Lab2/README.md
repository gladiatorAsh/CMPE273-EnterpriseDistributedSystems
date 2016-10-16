# README #

requirements.txt contains all dependencies

### What is this repository for? ###

"""
This is a simple example as Lab2 to show the basics of writing a Http api using Spyne. 

Input:

````code
curl "http://localhost:8000/checkcrime?lat=37.334164&lon=-121.884301&radius=1"
````
Output:

````javascript
[
  {
    "total_crime": 50,
    "the_most_dangerous_streets": [
      "00 BLOCK OF VIRGINIA LN",
      "2700 BLOCK OF 25TH AV",
      "4400 BLOCK OF CAMDEN ST"
    ],
    "crime_type_count": {
      "assault": 4,
      "arrest": 2,
      "burglary": 6,
      "robbery": 8,
      "theft": 1,
      "other": 27
    },
    "event_time_count": {
      "12:01am-3am": 3,
      "3:01am-6am": 0,
      "6:01am-9am": 0,
      "9:01am-12noon": 0,
      "12:01pm-3pm": 0,
      "3:01pm-6pm": 0,
      "6:01pm-9pm": 0,
      "9:01pm-12midnight": 47
    }
  }
]
````

### Remarks ###

* As no tests have been provided as of now, using most_common method of python to   display most common places of crimes after splitting on '&' character.
* May be updated if tests are created showing different common places probably by splitting on additional characters like 'AND'
