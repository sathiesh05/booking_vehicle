# Transport Booking System

This is a simple web application built using Flask and MySQL that allows users to book vehicles for transportation. Users can view available vehicles, make bookings, and receive confirmation.

## Features

- View available vehicles with details (type, availability, capacity, charges).
- Book a vehicle by providing user details and trip information.
- Confirmation of bookings with a dedicated confirmation page.

## Requirements

- Python 3.x
- Flask
- MySQL
- MySQL Connector for Python

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd transport_booking_system
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**

   ```bash
   pip install Flask mysql-connector-python
   ```

4. **Set up the MySQL database:**

   - Create a database named `transport_booking`.
   - Use the following credentials in the `app.py` file:

     ```python
     user="root"
     password="1234567890!@#$%^&*()"
     ```

5. **Run the application:**

   ```bash
   python app.py
   ```

   The application will run on `http://127.0.0.1:5000/`.

## File Structure

```
.
├── app.py                   # Main application file
├── templates                # Folder containing HTML templates
│   ├── home.html           # Home page template
│   ├── index.html          # Booking page template
│   └── booking_confirmation.html  # Booking confirmation page
└── static                  # Folder for static files (images, CSS)
    └── PSG.jpg             # Example image for the website
```

## Usage

- **Home Page:** Provides an overview and a button to navigate to the booking page.
- **Booking Page:** Displays available vehicles and a form for booking a vehicle.
- **Booking Confirmation Page:** Displays a confirmation message after a successful booking.

## Contribution

If you'd like to contribute to this project, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
