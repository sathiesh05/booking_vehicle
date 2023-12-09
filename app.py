from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('home.html')

class TransportBookingSystem:
    def __init__(self):
        self.db_connection = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password="1234567890!@#$%^&*()",
            database="transport_booking"
        )
        self.cursor = self.db_connection.cursor(buffered=True)  # Use buffered cursor for result iteration
        self.initialize_database()

    def initialize_database(self):
        create_vehicles_table = """
            CREATE TABLE IF NOT EXISTS vehicles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                vehicle_type VARCHAR(10) NOT NULL,
                available_vehicle INT NOT NULL,
                capacity INT,
                charges INT NOT NULL
            )
        """
        self.cursor.execute(create_vehicles_table)

        create_bookings_table = """
            CREATE TABLE IF NOT EXISTS bookings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(30) NOT NULL,
                email VARCHAR(40) NOT NULL,
                phone varchar(14) NOT NULL,
                vehicle_type VARCHAR(10) NOT NULL,
                num_seats INT NOT NULL,
                starting_location VARCHAR(50) NOT NULL,
                ending_location VARCHAR(50) NOT NULL
            )
        """
        self.cursor.execute(create_bookings_table)

        # Insert initial data if the table is empty
        check_empty_query = "SELECT COUNT(*) FROM vehicles"
        self.cursor.execute(check_empty_query)
        if self.cursor.fetchone()[0] == 0:
            initial_vehicle_data = [
                ('Car', 10, 7, 100),
                ('Bus', 12, 30, 150),
                ('Van', 15, 10, 90)
            ]
            insert_vehicle_query = "INSERT INTO vehicles (vehicle_type, available_vehicle, capacity, charges) VALUES (%s, %s, %s, %s)"
            self.cursor.executemany(insert_vehicle_query, initial_vehicle_data)

        self.db_connection.commit()

    def display_available_vehicles(self):
        query = "SELECT id, vehicle_type, available_vehicle, capacity, charges FROM vehicles WHERE available_vehicle > 0"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def book_vehicle(self, name, email, phone, vehicle_type, num_seats, starting_location, ending_location):
        check_availability_query = "SELECT available_vehicle FROM vehicles WHERE vehicle_type = %s"
        self.cursor.execute(check_availability_query, (vehicle_type,))
        available_seats = self.cursor.fetchone()

        if available_seats and available_seats[0] > 0:
            # Reduce available vehicles by 1
            update_query = "UPDATE vehicles SET available_vehicle = available_vehicle - 1 WHERE vehicle_type = %s"
            self.cursor.execute(update_query, (vehicle_type,))

            # Insert booking details with phone number
            insert_booking_query = """
                INSERT INTO bookings (name, email, phone, vehicle_type, num_seats, starting_location, ending_location)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            booking_data = (name, email, phone, vehicle_type, num_seats, starting_location, ending_location)
            self.cursor.execute(insert_booking_query, booking_data)

            self.db_connection.commit()
            return "Booking Confirmed. You have booked a vehicle."

        else:
            return "Booking failed. Please check availability."
            

    def __del__(self):
        if self.db_connection.is_connected():
            self.cursor.close()
            self.db_connection.close()

@app.route('/index', methods=['GET', 'POST'])
def index():
    transport_system = TransportBookingSystem()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        vehicle_type = request.form['vehicle_type']
        num_seats = int(request.form['num_seats'])
        starting_location = request.form['starting_location']
        ending_location = request.form['ending_location']

        result_message = transport_system.book_vehicle(name, email, phone, vehicle_type, num_seats, starting_location, ending_location)
        
        if "Booking Confirmed" in result_message:
            return redirect(url_for('booking_confirmation'))
        # Fetch available vehicles for display
        vehicles = transport_system.display_available_vehicles()

        # Pass result_message and vehicles to the template
        return render_template('index.html', result_message=result_message, vehicles=vehicles)

    # Fetch available vehicles for display
    vehicles = transport_system.display_available_vehicles()
    return render_template('index.html', vehicles=vehicles)

@app.route('/booking_confirmation')
def booking_confirmation():
    return render_template('booking_confirmation.html')

if __name__ == "__main__":
    app.run(debug=True)
