# -*- coding: utf-8 -*-
# backend/seeder.py
import sqlite3

from backend.database import get_connection


def insert_sample_data():
    """Insert sample data for testing purposes."""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        print("🔄 Checking and inserting sample data...")
        
        # Insert sample countries
        countries = [
            ('US', 'United States'),
            ('UK', 'United Kingdom'),
            ('UAE', 'United Arab Emirates'),
            ('SA', 'Saudi Arabia'),
            ('EG', 'Egypt'),
            ('CA', 'Canada'),
            ('FR', 'France'),
            ('DE', 'Germany'),
            ('IT', 'Italy'),
            ('ES', 'Spain'),
            ('JP', 'Japan'),
            ('CN', 'China'),
            ('IN', 'India'),
            ('AU', 'Australia'),
            ('BR', 'Brazil'),
            ('MX', 'Mexico'),
            ('TR', 'Turkey'),
            ('KR', 'South Korea'),
            ('SG', 'Singapore'),
            ('MY', 'Malaysia'),
            ('TH', 'Thailand'),
            ('ZA', 'South Africa'),
            ('NG', 'Nigeria'),
            ('KE', 'Kenya'),
            ('QA', 'Qatar')
        ]
        cursor.executemany("INSERT OR IGNORE INTO countries (code, name) VALUES (?, ?)", countries)
        print("✅ Countries checked/inserted")

        # Insert sample genders
        genders = [('Male',), ('Female',)]
        cursor.executemany("INSERT OR IGNORE INTO genders (name) VALUES (?)", genders)
        print("✅ Genders checked/inserted")

        # Insert sample classes
        classes = [
            ('Economy', 'Standard economy class'),
            ('Business', 'Business class with extra legroom'),
            ('First', 'First class luxury')
        ]
        cursor.executemany("INSERT OR IGNORE INTO classes (name, description) VALUES (?, ?)", classes)
        print("✅ Classes checked/inserted")

        # Insert sample plane types
        plane_types = [
            ('Boeing 737', 'Boeing', '737-800'),
            ('Airbus A320', 'Airbus', 'A320'),
            ('Boeing 777', 'Boeing', '777-300ER'),
            ('Airbus A380', 'Airbus', 'A380-800')
        ]
        cursor.executemany("INSERT OR IGNORE INTO plane_types (name, manufacturer, model) VALUES (?, ?, ?)", plane_types)
        print("✅ Plane types checked/inserted")

        # Insert sample branches
        branches = [
            ('AK-HQ', 'Al Kawthar Headquarters', 'Dubai, UAE', '+971-4-1234567'),
            ('AK-KSA', 'Al Kawthar KSA Branch', 'Riyadh, Saudi Arabia', '+966-11-7654321'),
            ('AK-EGY', 'Al Kawthar Egypt Branch', 'Cairo, Egypt', '+20-2-9876543')
        ]
        cursor.executemany("INSERT OR IGNORE INTO branches (code, name, address, phone_number) VALUES (?, ?, ?, ?)", branches)
        print("✅ Branches checked/inserted")

        # Insert sample terminals
        terminals = [
            ('1', 'Terminal 1'),
            ('2', 'Terminal 2'), 
            ('3', 'Terminal 3'),
            ('N', 'North Terminal'),
            ('S', 'South Terminal')
        ]
        cursor.executemany("INSERT OR IGNORE INTO terminals (number, name) VALUES (?, ?)", terminals)
        print("✅ Terminals checked/inserted")

        # Get country IDs with error checking
        cursor.execute("SELECT id FROM countries WHERE code = 'UAE'")
        uae_result = cursor.fetchone()
        uae_id = uae_result[0] if uae_result else 1
        
        cursor.execute("SELECT id FROM countries WHERE code = 'SA'")
        saudi_result = cursor.fetchone()
        saudi_id = saudi_result[0] if saudi_result else 1
        
        cursor.execute("SELECT id FROM countries WHERE code = 'EG'")
        egypt_result = cursor.fetchone()
        egypt_id = egypt_result[0] if egypt_result else 1
        
        cursor.execute("SELECT id FROM countries WHERE code = 'QA'")
        qatar_result = cursor.fetchone()
        qatar_id = qatar_result[0] if qatar_result else 1

        # Insert sample airports
        airports = [
            ('DXB', 'Dubai International Airport', uae_id),
            ('AUH', 'Abu Dhabi International Airport', uae_id),
            ('RUH', 'King Khalid International Airport', saudi_id),
            ('JED', 'King Abdulaziz International Airport', saudi_id),
            ('MED', 'Prince Mohammad Airport', saudi_id),
            ('CAI', 'Cairo International Airport', egypt_id),
            ('ALY', 'Alexandria International Airport', egypt_id),
            ('DOH', 'Hamad International Airport', qatar_id)
        ]
        cursor.executemany("INSERT OR IGNORE INTO airports (airport_code, name, country_id) VALUES (?, ?, ?)", airports)
        print("✅ Airports checked/inserted")

        # Get airport IDs with error checking
        cursor.execute("SELECT id FROM airports WHERE airport_code = 'DXB'")
        dxb_result = cursor.fetchone()
        dxb_id = dxb_result[0] if dxb_result else 1
        
        cursor.execute("SELECT id FROM airports WHERE airport_code = 'RUH'")
        ruh_result = cursor.fetchone()
        ruh_id = ruh_result[0] if ruh_result else 2
        
        cursor.execute("SELECT id FROM airports WHERE airport_code = 'JED'")
        jed_result = cursor.fetchone()
        jed_id = jed_result[0] if jed_result else 3
        
        cursor.execute("SELECT id FROM airports WHERE airport_code = 'CAI'")
        cai_result = cursor.fetchone()
        cai_id = cai_result[0] if cai_result else 4
        
        cursor.execute("SELECT id FROM airports WHERE airport_code = 'DOH'")
        doh_result = cursor.fetchone()
        doh_id = doh_result[0] if doh_result else 5

        # Get plane type IDs with error checking
        cursor.execute("SELECT id FROM plane_types WHERE name = 'Boeing 737'")
        boeing737_result = cursor.fetchone()
        boeing737_id = boeing737_result[0] if boeing737_result else 1
        
        cursor.execute("SELECT id FROM plane_types WHERE name = 'Airbus A320'")
        a320_result = cursor.fetchone()
        a320_id = a320_result[0] if a320_result else 2
        
        cursor.execute("SELECT id FROM plane_types WHERE name = 'Boeing 777'")
        boeing777_result = cursor.fetchone()
        boeing777_id = boeing777_result[0] if boeing777_result else 3

        # Insert sample planes
        planes = [
            ('AK-001', boeing737_id),
            ('AK-002', boeing737_id),
            ('AK-003', a320_id),
            ('AK-004', a320_id),
            ('AK-005', boeing777_id),
            ('AK-006', boeing777_id)
        ]
        cursor.executemany("INSERT OR IGNORE INTO planes (tail_number, plane_type_id) VALUES (?, ?)", planes)
        print("✅ Planes checked/inserted")

        # Get class IDs with error checking
        cursor.execute("SELECT id FROM classes WHERE name = 'Economy'")
        economy_result = cursor.fetchone()
        economy_id = economy_result[0] if economy_result else 1
        
        cursor.execute("SELECT id FROM classes WHERE name = 'Business'")
        business_result = cursor.fetchone()
        business_id = business_result[0] if business_result else 2
        
        cursor.execute("SELECT id FROM classes WHERE name = 'First'")
        first_result = cursor.fetchone()
        first_id = first_result[0] if first_result else 3

        # Insert plane-class relationships
        plane_classes = [
            (boeing737_id, economy_id),
            (boeing737_id, business_id),
            (a320_id, economy_id),
            (a320_id, business_id),
            (boeing777_id, economy_id),
            (boeing777_id, business_id),
            (boeing777_id, first_id),  # Only 777 has first class
        ]
        cursor.executemany("INSERT OR IGNORE INTO plane_available_classes (plane_type_id, class_id) VALUES (?, ?)", plane_classes)
        print("✅ Plane-class relationships checked/inserted")

        # Get branch ID with error checking
        cursor.execute("SELECT id FROM branches WHERE code = 'AK-HQ'")
        hq_branch_result = cursor.fetchone()
        hq_branch_id = hq_branch_result[0] if hq_branch_result else 1

        # Insert sample employees
        employees = [
            ('EMP-001', 'Ahmed Al-Mansoori', 'Dubai Marina, Dubai', '+971-50-1112233', 'Manager', hq_branch_id),
            ('EMP-002', 'Fatima Al-Qasimi', 'Jumeirah, Dubai', '+971-50-4445566', 'Flight Supervisor', hq_branch_id),
            ('EMP-003', 'Khalid Al-Otaibi', 'Al Olaya, Riyadh', '+966-50-7778889', 'Ground Staff', hq_branch_id),
            ('EMP-004', 'Sarah Johnson', 'Downtown Dubai', '+971-50-9990001', 'Customer Service', hq_branch_id)
        ]
        cursor.executemany("INSERT OR IGNORE INTO employees (employee_number, name, address, phone_number, job, branch_id) VALUES (?, ?, ?, ?, ?, ?)", employees)
        print("✅ Employees checked/inserted")

        # Get gender IDs with error checking
        cursor.execute("SELECT id FROM genders WHERE name = 'Male'")
        male_result = cursor.fetchone()
        male_id = male_result[0] if male_result else 1
        
        cursor.execute("SELECT id FROM genders WHERE name = 'Female'")
        female_result = cursor.fetchone()
        female_id = female_result[0] if female_result else 2

        # Insert sample passengers
        passengers = [
            ('P12345678', 'Mohammed Hassan', male_id, uae_id),
            ('P87654321', 'Aisha Rahman', female_id, saudi_id),
            ('P11223344', 'Omar Khalid', male_id, egypt_id),
            ('P44332211', 'Layla Ahmed', female_id, uae_id),
            ('P55667788', 'Yousef Ibrahim', male_id, qatar_id)
        ]
        cursor.executemany("INSERT OR IGNORE INTO passengers (passport_number, name, gender_id, nationality_country_id) VALUES (?, ?, ?, ?)", passengers)
        print("✅ Passengers checked/inserted")

        # Check if flights already exist before inserting
        cursor.execute("SELECT COUNT(*) FROM flights")
        existing_flights_count = cursor.fetchone()[0]
        
        if existing_flights_count == 0:
            # Get plane IDs with error checking
            cursor.execute("SELECT id FROM planes WHERE tail_number = 'AK-001'")
            plane1_result = cursor.fetchone()
            plane1_id = plane1_result[0] if plane1_result else 1
            
            cursor.execute("SELECT id FROM planes WHERE tail_number = 'AK-003'")
            plane3_result = cursor.fetchone()
            plane3_id = plane3_result[0] if plane3_result else 3

            # Insert sample flights only if none exist
            flights = [
                # Dubai to Riyadh
                ('AK101', plane1_id, hq_branch_id, dxb_id, ruh_id, '2024-02-01', '08:00', '2024-02-01', '10:30', 'scheduled'),
                ('AK102', plane1_id, hq_branch_id, ruh_id, dxb_id, '2024-02-01', '12:00', '2024-02-01', '14:30', 'scheduled'),
                # Dubai to Jeddah
                ('AK201', plane3_id, hq_branch_id, dxb_id, jed_id, '2024-02-01', '14:00', '2024-02-01', '16:45', 'scheduled'),
                ('AK202', plane3_id, hq_branch_id, jed_id, dxb_id, '2024-02-01', '18:30', '2024-02-01', '21:15', 'scheduled'),
                # Dubai to Cairo
                ('AK301', plane1_id, hq_branch_id, dxb_id, cai_id, '2024-02-02', '09:00', '2024-02-02', '11:30', 'scheduled'),
                ('AK302', plane1_id, hq_branch_id, cai_id, dxb_id, '2024-02-02', '13:00', '2024-02-02', '15:30', 'scheduled'),
                # Riyadh to Doha
                ('AK401', plane3_id, hq_branch_id, ruh_id, doh_id, '2024-02-02', '10:30', '2024-02-02', '11:45', 'scheduled'),
                ('AK402', plane3_id, hq_branch_id, doh_id, ruh_id, '2024-02-02', '13:00', '2024-02-02', '14:15', 'scheduled')
            ]
            cursor.executemany("""
                INSERT INTO flights 
                (flight_number, plane_id, branch_id, origin_airport_id, destination_airport_id,
                 departure_date, departure_time, arrival_date, arrival_time, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, flights)
            print("✅ Sample flights inserted")
        else:
            print("✅ Flights already exist - skipping flight insertion")

        # Insert airport-terminal relationships (safe to run multiple times)
        cursor.execute("SELECT id FROM terminals WHERE number = '1'")
        term1_result = cursor.fetchone()
        term1_id = term1_result[0] if term1_result else 1
        
        cursor.execute("SELECT id FROM terminals WHERE number = '2'")
        term2_result = cursor.fetchone()
        term2_id = term2_result[0] if term2_result else 2

        airport_terminals = [
            (dxb_id, term1_id),
            (dxb_id, term2_id),
            (ruh_id, term1_id),
            (jed_id, term1_id),
            (cai_id, term1_id),
            (doh_id, term1_id)
        ]
        cursor.executemany("INSERT OR IGNORE INTO airport_terminals (airport_id, terminal_id) VALUES (?, ?)", airport_terminals)
        print("✅ Airport-terminal relationships checked/inserted")
        
        # Insert sample users
        users = [
            ('admin', 'password123', 'admin@alkawthar.com', 1),
            ('agent1', 'password123', 'agent1@alkawthar.com', 0)
        ]
        cursor.executemany("INSERT OR IGNORE INTO users (username, password, email, is_admin) VALUES (?, ?, ?, ?)", users)
        print("✅ Users checked/inserted")
        
        # Check if tickets already exist before inserting
        cursor.execute("SELECT COUNT(*) FROM tickets")
        existing_tickets_count = cursor.fetchone()[0]
        
        if existing_tickets_count == 0:
            # Get flight ID for bookings
            cursor.execute("SELECT id FROM flights WHERE flight_number = 'AK101'")
            flight1_result = cursor.fetchone()
            if not flight1_result:
                print("⚠️ No flights found for bookings - skipping bookings/tickets")
            else:
                flight1_id = flight1_result[0]

                # Insert sample bookings
                bookings = [
                    (1, flight1_id, 2, '2024-01-10', 900.00, 'BRN001'),
                    (1, flight1_id, 1, '2024-01-11', 450.00, 'BRN002'),
                ]

                cursor.executemany("""
                    INSERT OR IGNORE INTO bookings 
                    (user_id, flight_id, seat_count, booking_date, total_price, booking_reference)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, bookings)
                print("✅ Sample bookings inserted")

                # Get booking IDs with error checking
                cursor.execute("SELECT id FROM bookings WHERE booking_reference = 'BRN001'")
                booking1_result = cursor.fetchone()
                booking1_id = booking1_result[0] if booking1_result else 1
                
                cursor.execute("SELECT id FROM bookings WHERE booking_reference = 'BRN002'") 
                booking2_result = cursor.fetchone()
                booking2_id = booking2_result[0] if booking2_result else 2

                # Get passenger IDs with error checking
                cursor.execute("SELECT id FROM passengers WHERE passport_number = 'P12345678'")
                passenger1_result = cursor.fetchone()
                passenger1_id = passenger1_result[0] if passenger1_result else 1
                
                cursor.execute("SELECT id FROM passengers WHERE passport_number = 'P87654321'")
                passenger2_result = cursor.fetchone()
                passenger2_id = passenger2_result[0] if passenger2_result else 2

                # Get flight IDs with error checking
                cursor.execute("SELECT id FROM flights WHERE flight_number = 'AK101'")
                flight1_result = cursor.fetchone()
                flight1_id = flight1_result[0] if flight1_result else 1
                
                cursor.execute("SELECT id FROM flights WHERE flight_number = 'AK201'")
                flight2_result = cursor.fetchone()
                flight2_id = flight2_result[0] if flight2_result else 2

                # Get terminal ID with error checking
                cursor.execute("SELECT id FROM terminals WHERE number = '1'")
                terminal1_result = cursor.fetchone()
                terminal1_id = terminal1_result[0] if terminal1_result else 1

                # Insert sample tickets
                tickets = [
                    ('TKT-001', passenger1_id, flight1_id, booking1_id, economy_id, terminal1_id, '15A', 450.00, 'confirmed'),
                    ('TKT-002', passenger1_id, flight1_id, booking1_id, economy_id, terminal1_id, '15B', 450.00, 'confirmed'),
                    ('TKT-003', passenger2_id, flight2_id, booking2_id, business_id, terminal1_id, '5B', 850.00, 'confirmed')
                ]

                cursor.executemany("""
                    INSERT INTO tickets 
                    (ticket_number, passenger_id, flight_id, booking_id, class_id, terminal_id, seat_number, price, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, tickets)
                print("✅ Sample tickets inserted")
        else:
            print("✅ Tickets already exist - skipping ticket insertion")

        conn.commit()
        print("🎉 Sample data setup completed successfully!")

    except sqlite3.Error as e:
        print(f"❌ Error inserting sample data: {e}")
        conn.rollback()
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        print(f"❌ Detailed error: {traceback.format_exc()}")
        conn.rollback()
    finally:
        conn.close()