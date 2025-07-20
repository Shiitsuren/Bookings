# Booking API

A Django REST API for user weekly availability and guest booking of time slots.

## Features
- Users set their weekly availability.
- Guests can book a time slot (15m, 30m, 45m, 1hr) based on user availability.
- Bookings do not overlap and must fit into the available schedule.
- API documented with Swagger (drf-yasg).

## Setup
1. Clone the repo and navigate to the project folder.
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install django djangorestframework drf-yasg
   ```
4. Run migrations:
   ```
   python manage.py migrate
   ```
5. Create a superuser (for admin):
   ```
   python manage.py createsuperuser
   ```
6. Run the server:
   ```
   python manage.py runserver
   ```

## API Endpoints
- `/api/availability/` (GET, POST): List or create weekly availability (auth required)
- `/api/bookings/` (GET, POST): List or create bookings for a user (guest access)
- `/swagger/` or `/redoc/`: API documentation

## Notes
- Bookings are validated to not overlap and must fit within the user's set availability.
- Use the `user` field (user id) when booking a slot as a guest.

## Testing
To run tests:
```
python manage.py test
```

---
No frontend included. See Swagger UI for API usage.
