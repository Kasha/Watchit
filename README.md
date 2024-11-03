# Watchit Sensor Data Monitoring and Notification Microservices

This project provides a set of **FastAPI** microservices for monitoring sensor data, validating it, and notifying on any invalid data. Built with **AsyncIO** for efficient asynchronous handling, this RESTful API supports dynamic routing and is managed with **Poetry** for streamlined dependency management.

Example Project

## Microservices Overview

1. **Sensor Monitor Service** (`monitor-sensors-service`)
   - The main microservice for monitoring data from configured sensors (as specified in `config.yaml`).
   - Supports dynamic routing to provide sensor-specific endpoints:
     - `http://127.0.0.1:8000/watchit/sensors/tempraturesensor`
     - `http://127.0.0.1:8000/watchit/sensors/humiditysensor`
     - `http://127.0.0.1:8000/watchit/sensors/pressuresensor`
     - `http://127.0.0.1:8000/watchit/sensors/n2osensor`
   - **Swagger Documentation**: [API Documentation](http://127.0.0.1:8000/docs)

2. **Alert Notifier Service** (`alert-notifier-service`)
   - Internal service for handling notifications about invalid data from the main service.
   - Should be access-limited to authorized calls from the main Sensor Monitor Service (using CORS and origin restrictions).
   - **Endpoint**: `http://127.0.0.1:8001/watchit/notify`
   - **Swagger Documentation**: [API Documentation](http://127.0.0.1:8001/docs)

## Getting Started

### Prerequisites

- **Python 3.8+**
- **Poetry**: Install with `pip install poetry` if not already installed.

### Installation Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository_url>
   ```

2. **Sensor Monitor Service Setup**
   - Navigate to the microservice directory:
     ```bash
     cd microservices/monitor-sensors-service/monitor_sensors_service
     ```
   - Initialize Poetry, activate the virtual environment, and install dependencies:
     ```bash
     poetry shell
     poetry install
     ```
   - To run the service:
     ```bash
     uvicorn main:app --port 8000 --reload
     ```

3. **Alert Notifier Service Setup**
   - Navigate to the microservice directory:
     ```bash
     cd microservices/alert-notifier-service/alert_notifier_service
     ```
   - Initialize Poetry, activate the virtual environment, and install dependencies:
     ```bash
     poetry shell
     poetry install
     ```
   - To run the service:
     ```bash
     uvicorn main:app --port 8001 --reload
     ```

### Running from PyCharm

1. Set the namespace for each service (`monitor_sensors_service` or `alert_notifier_service`) in **PyCharm**.
2. Open the terminal within PyCharm and follow the above installation steps.

**Video Tutorial**: [Setup and Run Instructions](https://youtu.be/3UbuQRdmeRU)

## Key Technologies

- **FastAPI**: For creating RESTful API endpoints.
- **AsyncIO** + **aiohttp**: For asynchronous client-server communication.
- **Swagger**: Integrated API documentation.
- **Poetry**: For dependency and environment management.
- **MyPy** and **Pydantic**: For type-checking and data validation.

### Logging and Exception Handling

- Configured logging for route activities and invalid data alerts.
- Custom exception handling for HTTP responses and runtime errors.

### Design and Code Standards

- **Domain-Driven Design (DDD)**: Separates domain, client, and service logic.
- **Google Style Guide**: Emphasis on small, readable functions.

## Planned Enhancements

- **PyLint** and **Coverage**: For future code analysis and test coverage.
- **PyTest**: For planned End-to-End, Integration, and Unit Testing (includes mock-ups for URL and runtime data).

## License

This project is licensed under the [MIT License](LICENSE).