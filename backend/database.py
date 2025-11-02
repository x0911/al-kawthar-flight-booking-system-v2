# -*- coding: utf-8 -*-
# backend/database.py
import sqlite3

DB_NAME = "al_kawthar_flights.db"

def get_connection():
    """Create and return a new database connection."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # allows dictionary-like access
    return conn

def initialize_database():
    """Create tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Create lookup tables first (no foreign key dependencies)
    
    # Countries table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS countries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL
    )
    """)

    # Genders table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS genders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
    """)

    # Classes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS classes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT
    )
    """)

    # Plane types table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS plane_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        manufacturer TEXT NOT NULL,
        model TEXT NOT NULL
    )
    """)

    # Branches table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS branches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        address TEXT NOT NULL,
        phone_number TEXT NOT NULL
    )
    """)

    # Terminals table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS terminals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        number TEXT NOT NULL,
        name TEXT
    )
    """)

    # Airports table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS airports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        airport_code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        country_id INTEGER NOT NULL,
        FOREIGN KEY (country_id) REFERENCES countries(id)
    )
    """)

    # Planes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS planes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tail_number TEXT UNIQUE NOT NULL,
        plane_type_id INTEGER NOT NULL,
        FOREIGN KEY (plane_type_id) REFERENCES plane_types(id)
    )
    """)

    # Users table - MOVED BEFORE BOOKINGS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT,
        is_admin INTEGER DEFAULT 0
    )
    """)

    # Employees table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_number TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        address TEXT NOT NULL,
        phone_number TEXT NOT NULL,
        job TEXT NOT NULL,
        branch_id INTEGER NOT NULL,
        FOREIGN KEY (branch_id) REFERENCES branches(id)
    )
    """)

    # Passengers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS passengers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        passport_number TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        gender_id INTEGER NOT NULL,
        nationality_country_id INTEGER NOT NULL,
        FOREIGN KEY (gender_id) REFERENCES genders(id),
        FOREIGN KEY (nationality_country_id) REFERENCES countries(id)
    )
    """)

    # Junction table: Plane available classes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS plane_available_classes (
        plane_type_id INTEGER NOT NULL,
        class_id INTEGER NOT NULL,
        PRIMARY KEY (plane_type_id, class_id),
        FOREIGN KEY (plane_type_id) REFERENCES plane_types(id),
        FOREIGN KEY (class_id) REFERENCES classes(id)
    )
    """)

    # Junction table: Airport terminals
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS airport_terminals (
        airport_id INTEGER NOT NULL,
        terminal_id INTEGER NOT NULL,
        PRIMARY KEY (airport_id, terminal_id),
        FOREIGN KEY (airport_id) REFERENCES airports(id),
        FOREIGN KEY (terminal_id) REFERENCES terminals(id)
    )
    """)

    # Flights table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS flights (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flight_number TEXT NOT NULL,
        plane_id INTEGER NOT NULL,
        branch_id INTEGER NOT NULL,
        origin_airport_id INTEGER NOT NULL,
        destination_airport_id INTEGER NOT NULL,
        departure_date TEXT NOT NULL,
        departure_time TEXT NOT NULL,
        arrival_date TEXT NOT NULL,
        arrival_time TEXT NOT NULL,
        status TEXT DEFAULT 'scheduled',
        FOREIGN KEY (plane_id) REFERENCES planes(id),
        FOREIGN KEY (branch_id) REFERENCES branches(id),
        FOREIGN KEY (origin_airport_id) REFERENCES airports(id),
        FOREIGN KEY (destination_airport_id) REFERENCES airports(id)
    )
    """)

    # Create bookings table - NOW AFTER USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        flight_id INTEGER NOT NULL,
        seat_count INTEGER NOT NULL,
        booking_date TEXT NOT NULL,
        total_price REAL NOT NULL,
        booking_reference TEXT UNIQUE NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(flight_id) REFERENCES flights(id)
    )
    """)

    # Create tickets table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_number TEXT UNIQUE NOT NULL,
        passenger_id INTEGER NOT NULL,
        flight_id INTEGER NOT NULL,
        booking_id INTEGER NOT NULL,
        class_id INTEGER NOT NULL,
        terminal_id INTEGER NOT NULL,
        seat_number TEXT NOT NULL,
        price REAL NOT NULL,
        status TEXT DEFAULT 'confirmed',
        FOREIGN KEY(passenger_id) REFERENCES passengers(id),
        FOREIGN KEY(flight_id) REFERENCES flights(id),
        FOREIGN KEY(booking_id) REFERENCES bookings(id),
        FOREIGN KEY(class_id) REFERENCES classes(id),
        FOREIGN KEY(terminal_id) REFERENCES terminals(id)
    )
    """)

    # Crew assignments table (bonus - many-to-many between employees and flights)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crew_assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER NOT NULL,
        flight_id INTEGER NOT NULL,
        role TEXT NOT NULL,
        FOREIGN KEY (employee_id) REFERENCES employees(id),
        FOREIGN KEY (flight_id) REFERENCES flights(id),
        UNIQUE(employee_id, flight_id)
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Airline management database initialized successfully!")

if __name__ == "__main__":
    initialize_database()