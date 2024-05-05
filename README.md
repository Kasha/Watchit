Watchit Sensor Data Monitor and invalid data notification Microservices

Watchit Sensor Monitor, Data Feeder, and validation Microservice. Invalid data notification Microservice FastAPI+AsyncIO HTTP RESTFul API and Swagger: API Documentation (Simulator)


**Watchit Sensor Data Monitoring and Alerting 
microservices:**

**Main Service:**
Sensor-monitor-service

FastAPI dynamic routing for available and valid sensors (configured in config.yaml)

**http://127.0.0.1:8000/watchit/sensors/tempraturesensor
http://127.0.0.1:8000/watchit/sensors/humiditysensor
http://127.0.0.1:8000/watchit/sensors/pressuresensor
http://127.0.0.1:8000/watchit/sensors/n2osensor**

**Run from PyCharm (See attached video)**
https://youtu.be/3UbuQRdmeRU
watchit\microservices\monitor-sensors-service\main.py

**Run from Terminal:**
watchit\microservices\monitor-sensors-service\
1. python ./main.py (windows) python3 ./main.py (Linux)
2. uvicorn main:app --port 8000  --reload

**Swagger docs and feeder: http://127.0.0.1:8000/docs**

**Internal Service:**
Alert-notifier-service
http://127.0.0.1:8001/watchit/notify/
**!!! It should be access-limited from main Service (CORS and original)**

**Run from PyCharm (See attached video)**
https://youtu.be/3UbuQRdmeRU
\watchit\microservices\alert-notifier-service\main.py

**Run from Terminal:**
\watchit\microservices\alert-notifier-service\
1. python ./main.py (windows) python3 ./main.py (Linux)
2. uvicorn main:app --port 8001  --reload 

**Swagger docs and feeder: http://127.0.0.1:8001/docs**

**Technology**:
FastAPI + Asyncio (for IO bound processing)+ aiohttp for Asynchronous HTTP Client/Server HTTP RESTFull API
And Micro Services http communication + Swagger: API Documentation & Design Tools
Exception handling for Runtime errors and HTTP responses + handlers for http exceptions.
Custom exceptions

Logger with handlers for catching routing activities
Logger for invalid data notification writing

MyPy, Pydentic for typo and annotations and validations

**Coding guidelines:**
Domain Driven Design (Domain+Client+Service infrastructure and design)
Google guidelines (small and readable functions)

**Installed but not used:**

PyLint and Coverage for future code analyzer and test coverage
PyTest for future End To End, Integration, Unit Test (Including monkey patch for URL and runtime classes data mock-ups)

