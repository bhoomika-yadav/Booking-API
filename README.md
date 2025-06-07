# Booking-API

Overview
This project is a simple backend API for a fictional fitness studio offering classes like Yoga, Zumba, and HIIT. It allows clients to view available classes, book spots, and retrieve their bookings.

Built with Python and Django REST Framework, it uses SQLite as an in-memory database for simplicity.

Features
GET /classes/
Retrieves a list of upcoming fitness classes with details: name, date/time, instructor, and available slots.

POST /
Book a spot in a class by providing class_id, client_name, and client_email. Validates slot availability and prevents overbooking.

GET /bookings/
Retrieve all bookings made by a specific email address.

Timezone Management
Classes are created in Indian Standard Time (IST). All date/time values are timezone-aware and adjust accordingly.

Error Handling & Validation
Handles missing or invalid data, and prevents booking when no slots are available.

Unit Tests
Includes basic tests for API endpoints validating core functionalities.

Setup Instructions

Prerequisites:
Python 3.8+
pip (Python package manager)



Run the development server:
python manage.py runserver

Usage Examples

Get all classes
curl -X GET http://127.0.0.1:8000/classes/

Book a class
curl -X POST http://127.0.0.1:8000/ -H "Content-Type: application/json" -d '{
  "class_id": 1,
  "client_name": "John Doe",
  "client_email": "john@example.com"
}'

Get bookings by email
curl -X GET "http://127.0.0.1:8000/bookings/?email=john@example.com"

Project Structure:

models.py - Defines FitnessClass and Booking models.
serializers.py - Serializers for API input/output validation.
views.py - API endpoint logic and booking validation.
urls.py - URL routes for the API.
tests.py - Automated tests for API endpoints.

