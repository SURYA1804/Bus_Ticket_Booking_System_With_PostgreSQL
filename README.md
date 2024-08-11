# Bus_Ticket_Booking_System_With_PostgreSQL

This Python program provides a user interface for a bus ticket booking system. Users can create accounts, login, browse available seats, book seats, view booking history, and update their information.

# Features:

User Login and Account Creation
View Available Seats for Different Buses
Book Seats and View Discounts
Manage Booking History
Update User Details
Getting Started:

Install Dependencies: You'll need the psycopg2 library to connect to the PostgreSQL database. You can install it using pip install psycopg2.
Database Configuration: Update the connection details in the program code with your PostgreSQL database credentials (host, database name, username, password, and port).
Run the Program: Execute the Python script (python bus_booking_system.py).
User Interface:
The program starts with a login page. Users can either create a new account or login with existing credentials. After successful login, users are presented with a menu for various functionalities:

# View Details:
    See your name 
    mobile number 
    email address.
# Update Details: 
    Edit your name
    mobile number
    email address
    password
# Booking Section:
 # View Available Seats: 
     Browse available seats for different buses.
 # Book Seats: 
   Choose a bus and seat(s), confirm booking, and view the final bill with discounts.
 # View Discount Offers: 
   See available discounts on different bus types and seat categories.
 # View Booked Seats: 
   Check your booked seats across all trips.
 # Booking History: 
    View a list of your previous bus bookings with details like bus name, seat type, price, discount applied, and booking date.
