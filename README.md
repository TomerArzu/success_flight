# Success Flight Application
* Success Flight application's input is csv file that you can find in this repository under `data_and_mocks\airport_flight_data.csv`
* The csv contains data about flight from some airport.
* The airport cannot contain 20 successful flights
* Flight is 'success' if the difference between arrival and departure time is equal or grater then 3 hours and if there is no more then 20 successful flights ordered by arrival time.
* The application knows to receive the csv, parse it and calculate if flight is 'success'.
* In the initialization time of the application, it orders the existing data and defines flight that are 'success'.
* Once initialization is done the API is ready to use.
* By the API the client can get flight by id, get all flights and append new flights to the csv.
* When the client asks for the all list the response will contain the ordered file data.
* If the client wish to add flights, the application will calculate if the new flight is 'success' and update the data in the csv file


## How To use

### Running The App

1. run it in local env:
    1. clone project
    2. create and activate python virtual env
    3. make sure port 5002 is available
    4. run `app.py` with python command `python app.py`
    5. use `localhost:5000` as base url

2. run in docker image.
    1. clone project
    2. change to the cloned dir `cd <path to cloned project dir>`
    3. build docker image from docker file 'docker build -t success_flight .'
    4. make sure port 5000 is available
    5. run docker container: `docker run -p 5000:5000 success_flight`

### API

**NOTE: API is available only if the data file exists and parsed in the initialization**

* GET `/flight/<flight_id>`:
    * args - flight_id: string - id of flight.
    * returns the payload of exists flight in csv, otherwise error.
    * expected errors:
        * FLIGHT_DATA.FLIGHT_NOT_FOUND - where flight is not found in csv.
        * DATA_SOURCE_ERROR.FILE_NOT_FOUND - data source was not found (can be if csv file deleted or moved)
        * DATA_SOURCE_FORMAT_ERROR.UNWOUND_TYPE - some data is corrupted and not match to the given format (can be if
          csv file changed after initialization)
        * DATA_SOURCE_FORMAT_ERROR.UNEXPECTED_LINE_HEADER - headers are not match to the given format  (can be if csv
          file changed after initialization)

* GET `/flights`:
    * returns list of flights.
    * expected errors:
        * FLIGHT_DATA.FLIGHT_NOT_FOUND - where flight is not found in csv.
        * DATA_SOURCE_ERROR.FILE_NOT_FOUND - data source was not found (can be if csv file deleted or moved)
        * DATA_SOURCE_FORMAT_ERROR.UNWOUND_TYPE - some data is corrupted and not match to the given format (can be if
          csv file changed after initialization)
        * DATA_SOURCE_FORMAT_ERROR.UNEXPECTED_LINE_HEADER - headers are not match to the given format  (can be if csv
          file changed after initialization)


* POST `/flights`:
    * body (example below):
    ```json
    {
        "flights": [
            {
                "flight ID": "string",
                "Arrival": "string of time (format: %HH:%MM)",
                "Departure": "string of time (format: %HH:%MM)"
            }
        ]
    }
    ```
  * 200 for success, otherwise error.
  * expected errors:
    * BAD_REQUEST.INVALID_BODY_MESSAGE - The request body is not valid
    * DATA_SOURCE_ERROR.FILE_NOT_FOUND - data source was not found (can be if csv file deleted or moved)
    * DATA_SOURCE_FORMAT_ERROR.UNWOUND_TYPE - some data is corrupted and not match to the given format (can be if csv file changed after initialization)
    * DATA_SOURCE_FORMAT_ERROR.UNEXPECTED_LINE_HEADER - headers are not match to the given format  (can be if csv file changed after initialization)

### request example:
* example of request to `POST /flights`:
    ```json
    {
        "flights": [
            {
                "flight1 ID": "T04",
                "Arrival": "07:45",
                "Departure": "08:30"
            }
        ]
    }
    ```
### response examples
* example of response for `GET /flight/T04`:
   ```json
   {
       "message": {
           "flight ID": "T04",
           "Arrival": "07:45",
           "Departure": "08:30",
           "success": "fail"
       }
   }
   ```

* example of response for `GET /flights`:
   ```json
   {
    "message": [
        {
            "flight ID": "G86",
            "Arrival": "07:30",
            "Departure": "14:00",
            "success": "success"
        },
        {
            "flight ID": "T01",
            "Arrival": "07:45",
            "Departure": "08:30",
            "success": "fail"
        },
        {
            "flight ID": "T04",
            "Arrival": "07:45",
            "Departure": "08:30",
            "success": "fail"
        },
        {
            "flight ID": "C23",
            "Arrival": "08:00",
            "Departure": "17:00",
            "success": "success"
        }
    ]
  }
   ```

* example of `FLIGHT_DATA.FLIGHT_NOT_FOUND` error:

    ```json
    {
      "error_code": "FLIGHT_DATA.FLIGHT_NOT_FOUND",
      "status_code": 404,
      "error_message": "Flight Data was not found"
    }
    ```

* example of `DATA_SOURCE_ERROR.FILE_NOT_FOUND` error:

    ```json
    {
      "error_code": "DATA_SOURCE_ERROR.FILE_NOT_FOUND",
      "status_code": 409,
      "error_message": "Could not find data source in the provided path `data_and_mocks/airport_flight_data1.csv`, please check if data source exists"
    }
    ```

* example of `DATA_SOURCE_FORMAT_ERROR.UNEXPECTED_LINE_HEADER` error:

    ```json
    {
      "error_code": "DATA_SOURCE_FORMAT_ERROR.UNEXPECTED_LINE_HEADER",
      "status_code": 409,
      "error_message": "Wrong field in csv file. field name Departure is not one of defiled fieldsFields name must be: data_and_mocks/airport_flight_data1.csv"
    }
    ```

* example of `DATA_SOURCE_FORMAT_ERROR.UNWOUND_TYPE` error:

    ```json
    {
      "error_code": "DATA_SOURCE_FORMAT_ERROR.UNEXPECTED_LINE_HEADER",
      "status_code": 409,
      "error_message": "Wrong field in csv file. field name Departure is not one of defiled fieldsFields name must be: data_and_mocks/airport_flight_data1.csv"
    }
    ```
* example of `BAD_REQUEST.INVALID_BODY_MESSAGE` error:

    ```json
    {
      "error_message": "The request body is not valid",
      "error_code": "BAD_REQUEST.INVALID_BODY_MESSAGE"
    }
  ```


  