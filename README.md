# orchard-backend

This is the implementation of the backend for the orchard restaurant assessment dataset.

# How it works and what it does

This repo:

1. Creates an SQLite database based on the https://nycopendata.socrata.com/api/views/xx67-kt59/rows.csv?accessType=DOWNLOAD dataset.
2. Starts an endpoint to retrieve top 10 restaurants (based on the date of grading and no worse than a grade of 'B') based on the cuisine provided.

# Installation

1. Install the dependencies.
   This project uses Python 3, so all the modules have to be Python 3 version.
   
   Run:
   
   `pip install pandas sqlalchemy flask`
   
   This should install all the necessary dependencies for Python.
   
   Also, make sure your machine has an Apache server up and running.
   
   If it doesn't, consider following the following instructions:
   
   On Ubuntu:
      sudo apt install apache2
      sudo service apache2 start
   Macs come with Apache server by default, but in case it is not running, run the command:
      sudo apachectl -k start
   On Windows:
      Watch this video https://www.youtube.com/watch?v=A_NGnq31d18
   
 2. Create the database:
    Make sure the dataset is in the same directpory with the python scripts(in the repo directory.)
    Then run: <br/>
    `python db.py`
    This will create the database file as well as initialize the model for the database.<br/>
    Then run:
    `python etl_job.py`
    This will load the data into the database with the following schema:<br/>
    
      # restaurant model 
      `class Restaurant(Base): <br/> 
          __tablename__ = 'restaurants' <br/>
          id = Column(Integer, primary_key=True, autoincrement=False) <br/>
          name = Column(String)  <br/>
          boro = Column(String)  <br/>
          building = Column(String) <br/>
          street = Column(String)   <br/>
          zip = Column(Integer)    <br/>
          phone = Column(String)    <br/>
          cuisine = Column(String)  <br/>
        `

      # inspection model
      `class Inspection(Base):   <br/>
          __tablename__ = 'inspections' <br/>
          id = Column(Integer, primary_key=True) <br/>
          rest_id = Column(Integer, ForeignKey(Restaurant.id)) <br/>
          inspection_date = Column(Date)  <br/>
          action = Column(String)    <br/>
          violation_code = Column(String)   <br/>
          violation_desc = Column(String)   <br/>
          is_critical = Column(Boolean)     <br/>
          score = Column(Integer)          <br/>
          grade = Column(String)           <br/>
          grade_date = Column(Date)       <br/>
          record_date = Column(Date)       <br/>
          inspection_type = Column(String) <br/>
       `
          
  3.    Finally, to start the endpoint handler, run:
       `python microservices.py`
       This will start the backend running.  <br/>
       The service is available at route: `http://host:port/best-places?cuisine=YOUR_CUISINE`
       
       # NOTE
       If you want the app to run on a specific port, change this line in microservices.py:
            app.run(host='0.0.0.0')
       To
            app.run(host='0.0.0.0', port=YOUR_PORT)
