# IMPROVEMENTS by Levente Stieber
I have researched best practices and coding conventions in Python and Flask, to have a better idea of how to optimize the code. Tried to make use of my existing knowledge and my freshly gained knowledge to be able to recognize possibilities for improvement, for example assigning multiple variables at once on one line, which is a python-specific feature.
Apart from this, I wrote a lot of comments throughout the code to explain what is happening.
Here are some points that I improved in the code (excluding the comments):

__init__.py:
- I put all the blueprints in one list, then looped through the list to register all of them. 
- Apart from that, according to Flask and Python best practices, separated the app creation and the running. This can be useful when using the app in different environments (development, testing, etc)

auth.py, place.py, routes.py:
- Most modifications were done in these files.
- When assigning multiple variables at once, instead of doing it in new line everytime, now I am assigning them at once (for example: email, password = None, None)
- I am saving the content type request to a variable, as it is reused often 
- Saving the possible content types in variables, on module level (contents_xml = ('application/xml', 'text/xml'), content_json = 'application/json')
- Then I am checking the content type using these variables
- Instead of checking statements separately, but giving the same response for them, i am aggregating those into one if statement (if not name or not start or not end or not user_id)
- Variable assignments were the same in both possibilities for the if statement, so I put them outside the statement (for example user = User.query.filter_by(id=request_id))
- Schema validations for XML were checking for False, but Json was checking for True, so I fixed that

response_builder.py:
- Deleted the unnecessary commented codes that were left there

## End of section. From here, the Readme file starts
# data-processing-api

In our project, we were striving for the implementation of a route planning application. In the application, the user is able to input their desired points, and ask for a route planning. The app then creates a route plan for the user with the help of API calls. The idea was based on our original project done last year, the E-Grips. It was an insertable handlebar made to make sure biking can be done more safely, as the bike grip vibrates when you have to take  a turn, alerting you and making sure you do not lose track of your route. 
In this document, the necessary steps to ensure the program works properly will be described.

# Prerequisites, requirements:
* Python 3 (latest version 3 is recommended) 
* Flask (2.2.2 is recommended and used in the project) 
* Flask-SQLAlchemy (3.0.3 is recommended and used in the project)
* bcrypt (4.0.1 is recommended and used in the project)
* SQLAlchemy (2.0.6 is recommended and used in the project)
* JSONSchema (4.17.3 is recommended and use in the project)
* LXML (4.9.2 is recommended and use in the project)
* Windows 10 or 11 
* Editor (VSC, VS2019 or any relevant editor) 
* The provided route planning application 
* Postman API platform

# Installation:
* Install Python 3 from Microsoft Store
* Open Command prompt to install python modules. If you experience any issues related to privileges during installation, then close the command prompt and run it as administrator.
* pip install flask
* pip install Flask-SQLAlchemy
* pip install SQLAlchemy
* pip install jsonschema
* pip install lxml
* pip install bcrypt
* navigate to the foler where the "\_\_init\_\_.py" file is located
* run "python \_\_init\_\_.py" (if this command is not working use the following: "python .\\_\_init\_\_.py" )
* if necessary allow access to the internet on both public and private networks
* if the server is running the following messages appears:
Serving Flask app '\_\_init\_\_'
  Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
  Running on all addresses (0.0.0.0)
  Running on http://127.0.0.1:5000
  Running on http://192.168.178.207:5000
*use the two address to access the api (http://127.0.0.1:5000 is the recommended)

(After installing if there are errors regarding missing packages make sure you have all of these packages from this list and install accordingly:
* attrs             22.2.0
* bcrypt            4.0.1
* cffi              1.15.1
* click             8.1.3
* colorama          0.4.5
* cryptography      39.0.2
* Flask             2.2.2
* Flask-Login       0.6.2
* Flask-MySQLdb     1.0.1
* Flask-SQLAlchemy  3.0.3
* greenlet          2.0.2
* itsdangerous      2.1.2
* Jinja2            3.1.2
* jsonschema        4.17.3
* jwt               1.3.1
* lxml              4.9.2
* MarkupSafe        2.1.1
* mysqlclient       2.1.1
* pycparser         2.21
* pyrsistent        0.19.3
* SQLAlchemy        2.0.6
* typing_extensions 4.5.0
* Werkzeug          2.2.2
)

# Database and login to app

The database is created via a toolkit, called flask-SQLAlchemy. The initialization and creation of it is included in the api, so it does not need to be done manually. The database file  "db.sqlite" is created under the instance folder. By default the file is already there, thus, when running the app there wont be a new generated. If you need a new file just delete "db.sqlite" as it will create a new after starting the api.
When running the application, the user is given the opportunity to log in or register a new account. 
Note that the email must be in a valid email format, and the password can contain only letters and number, and has to be exactly 8 characters long. 
* Register a new account and remember your details 
* Switch to the login page and provide your information  
Apart from the user credentials, also places and routes will be saved in the database, where everything can be updated or deleted by admin.

With the help of Postman, we are able to make the API request and see the structure of a request body. 

Steps: 
* First, it needs to be installed. You can do that here: https://www.postman.com/downloads/ 
Then open it, and follow these steps: 
* Click on Collections tab in the top left corner and then the "Import" button (a bit right to the collections) 
* In the import window, select the "Import File" tab and click on "Choose Files" to select the JSON files. These can be found in the “json,xml request,response postman” folder we provided. 
* Once you have selected the JSON file, click on "Import" to import it into Postman. 
* These will be now imported as collections in Postman. You can view the collection in the "Collections" tab.

Note: Pictures of the requests and their bodies can be also viewed in the folder "api_request_bodies".

FOR MORE INFORMATION PLEASE CHECK THE DATA PROCESSING MANUAL AND APPLICATION MANUAL.
