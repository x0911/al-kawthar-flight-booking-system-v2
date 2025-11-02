# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
from backend.database import get_connection

class BookingsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.sort_column = 'booking_date'
        self.sort_direction = 'DESC'
        self.setup_ui()
        self.load_bookings()
        
    def setup_ui(self):
      """Create bookings management interface"""
      self.configure(bg='white')
      
      # Header with buttons
      header_frame = tk.Frame(self, bg='white')
      header_frame.pack(fill=tk.X, padx=20, pady=10)
      
      title = tk.Label(
          header_frame,
          text="Bookings Management",
          font=('Arial', 18, 'bold'),
          bg='white',
          fg='#2c3e50'
      )
      title.pack(side=tk.LEFT)
      
      # Action buttons
      button_frame = tk.Frame(header_frame, bg='white')
      button_frame.pack(side=tk.RIGHT)
      
      refresh_btn = ttk.Button(
          button_frame,
          text="Refresh",
          command=self.load_bookings
      )
      refresh_btn.pack(side=tk.LEFT, padx=5)
      
      add_btn = ttk.Button(
          button_frame,
          text="New Booking",
          command=self.add_booking
      )
      add_btn.pack(side=tk.LEFT, padx=5)
      
      # Search frame
      search_frame = tk.Frame(self, bg='white')
      search_frame.pack(fill=tk.X, padx=20, pady=10)
      
      tk.Label(search_frame, text="Search:", bg='white').pack(side=tk.LEFT)
      
      self.search_var = tk.StringVar()
      search_entry = ttk.Entry(
          search_frame, 
          textvariable=self.search_var,
          width=30
      )
      search_entry.pack(side=tk.LEFT, padx=5)
      search_entry.bind('<KeyRelease>', self.on_search)
      
      # Bookings table
      table_frame = tk.Frame(self, bg='white')
      table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
      
      # Create treeview with scrollbar - CORRECTED COLUMNS
      columns = ('booking_ref', 'passenger_name', 'flight_number', 
                'route', 'booking_date', 'seat_count', 'total_price', 'status')
      
      self.tree = ttk.Treeview(
          table_frame, 
          columns=columns,
          show='headings',
          height=15
      )
      
      # Define headings - CORRECTED MAPPING
      self.tree.heading('booking_ref', text='Booking Ref.')
      self.tree.heading('passenger_name', text='Passenger')
      self.tree.heading('flight_number', text='Flight')
      self.tree.heading('route', text='Route')
      self.tree.heading('booking_date', text='Booking Date')
      self.tree.heading('seat_count', text='Seats')
      self.tree.heading('total_price', text='Total Price')
      self.tree.heading('status', text='Status')
      
      # Configure columns - CORRECTED WIDTHS
      self.tree.column('booking_ref', width=100)
      self.tree.column('passenger_name', width=150)
      self.tree.column('flight_number', width=80)
      self.tree.column('route', width=150)
      self.tree.column('booking_date', width=120)
      self.tree.column('seat_count', width=60)
      self.tree.column('total_price', width=100)
      self.tree.column('status', width=100)
      
      # Scrollbar
      scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
      self.tree.configure(yscrollcommand=scrollbar.set)
      
      self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
      scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
      
      # Bind double-click event
      self.tree.bind('<Double-1>', self.on_booking_select)
        
    def load_bookings(self):
      """Load bookings from database"""
      try:
          conn = get_connection()
          cursor = conn.cursor()
          
          # Load bookings with related data (FIXED QUERY)
          cursor.execute("""
              SELECT 
                  b.booking_reference,
                  p.name as passenger_name,
                  f.flight_number,
                  o_airport.airport_code || ' → ' || d_airport.airport_code as route,
                  b.booking_date,
                  b.seat_count,
                  b.total_price,
                  t.status
              FROM bookings b
              JOIN tickets t ON b.id = t.booking_id
              JOIN passengers p ON t.passenger_id = p.id
              JOIN flights f ON t.flight_id = f.id
              JOIN airports o_airport ON f.origin_airport_id = o_airport.id
              JOIN airports d_airport ON f.destination_airport_id = d_airport.id
              GROUP BY b.id  -- Group to avoid duplicate bookings
              ORDER BY b.booking_date DESC
          """)
          
          bookings = cursor.fetchall()
          conn.close()
          
          # Clear existing data
          for item in self.tree.get_children():
              self.tree.delete(item)
          
          # Populate treeview
          for booking in bookings:
              booking_values = tuple(booking)
              self.tree.insert('', tk.END, values=booking_values)
              
          # Show message if no bookings
          if not bookings:
              self.tree.insert('', tk.END, values=(
                  "No bookings found", "", "", "", "", "", "", "", ""
              ))
              
      except Exception as e:
          messagebox.showerror("Database Error", f"Failed to load bookings: {e}")
    
    def on_search(self, event):
      """Handle search functionality"""
      try:
          search_term = self.search_var.get().lower().strip()
          
          if not search_term:
              self.load_bookings()
              return
              
          conn = get_connection()
          cursor = conn.cursor()
          
          cursor.execute("""
              SELECT 
                  b.booking_reference,
                  p.name as passenger_name,
                  f.flight_number,
                  o_airport.airport_code || ' → ' || d_airport.airport_code as route,
                  b.booking_date,
                  b.seat_count,
                  b.total_price,
                  t.status
              FROM bookings b
              JOIN tickets t ON b.id = t.booking_id
              JOIN passengers p ON t.passenger_id = p.id
              JOIN flights f ON t.flight_id = f.id
              JOIN airports o_airport ON f.origin_airport_id = o_airport.id
              JOIN airports d_airport ON f.destination_airport_id = d_airport.id
              WHERE b.booking_reference LIKE ? OR 
                    p.name LIKE ? OR 
                    f.flight_number LIKE ? OR
                    t.status LIKE ?
              GROUP BY b.id
              ORDER BY b.booking_date DESC
          """, (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
          
          bookings = cursor.fetchall()
          conn.close()
          
          # Clear existing data
          for item in self.tree.get_children():
              self.tree.delete(item)
          
          # Populate treeview
          for booking in bookings:
              booking_values = tuple(booking)
              self.tree.insert('', tk.END, values=booking_values)
              
          if not bookings:
              self.tree.insert('', tk.END, values=(
                  "No bookings found", "", "", "", "", "", "", "", ""
              ))
              
      except Exception as e:
          messagebox.showerror("Search Error", f"Failed to search bookings: {e}")
    
    def on_booking_select(self, event):
        """Handle booking selection (double-click)"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            booking_data = item['values']
            if booking_data and len(booking_data) >= 2 and booking_data[0] != "No bookings found":
                self.view_booking_details(booking_data)
    
    def view_booking_details(self, booking_data):
        """Show booking details popup"""
        details_window = tk.Toplevel(self)
        details_window.title("Booking Details")
        details_window.geometry("500x400")
        
        # Set icon
        from frontend.window_utils import set_window_icon
        set_window_icon(details_window)
        
        # Center the window
        self.center_window(details_window)
        
        # Booking details
        details_frame = tk.Frame(details_window, padx=20, pady=20)
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        labels = [
            ("Booking ID:", booking_data[0]),
            ("Ticket Number:", booking_data[1]),
            ("Passenger:", booking_data[2]),
            ("Flight:", booking_data[3]),
            ("Route:", booking_data[4]),
            ("Booking Date:", booking_data[5]),
            ("Seat Count:", booking_data[6]),
            ("Total Price:", f"${booking_data[7]}"),
            ("Status:", booking_data[8])
        ]
        
        for i, (label, value) in enumerate(labels):
            tk.Label(details_frame, text=label, font=('Arial', 10, 'bold')).grid(
                row=i, column=0, sticky='w', pady=5)
            tk.Label(details_frame, text=value).grid(
                row=i, column=1, sticky='w', pady=5, padx=(10, 0))
        
        # Action buttons
        button_frame = tk.Frame(details_frame)
        button_frame.grid(row=len(labels), column=0, columnspan=2, pady=20)
        
        if booking_data[8] == 'confirmed':
            ttk.Button(button_frame, text="Cancel Booking", 
                      command=lambda: self.cancel_booking(booking_data[0], details_window)).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Close", 
                  command=details_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def cancel_booking(self, booking_id, window):
        """Cancel a booking"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute("UPDATE tickets SET status = 'cancelled' WHERE booking_id = ?", (booking_id,))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Booking cancelled successfully!")
            window.destroy()
            self.load_bookings()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to cancel booking: {e}")
    
    def add_booking(self):
        """Open add booking dialog"""
        booking_window = tk.Toplevel(self)
        booking_window.title("Create New Booking")
        booking_window.geometry("600x700")
        
        # Set icon
        from frontend.window_utils import set_window_icon
        set_window_icon(booking_window)
        
        # Center the window
        self.center_window(booking_window)
        
        form_frame = tk.Frame(booking_window, padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Form title
        title = tk.Label(
            form_frame,
            text="Create New Booking",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50'
        )
        title.pack(pady=(0, 20))
        
        # Main content frame with scrollbar
        main_frame = tk.Frame(form_frame)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Get data for dropdowns
        passengers = self.get_passengers()
        flights = self.get_available_flights()
        classes = self.get_classes()
        terminals = self.get_terminals()
        
        self.booking_widgets = {}
        current_row = 0
        
        # Passenger Selection
        tk.Label(
            scrollable_frame, 
            text="Passenger:", 
            font=('Arial', 11, 'bold'),
            foreground='#2c3e50'
        ).grid(row=current_row, column=0, sticky='w', pady=(10, 5))
        
        passenger_names = [f"{p['passport']} - {p['name']}" for p in passengers]
        passenger_var = tk.StringVar()
        passenger_cb = ttk.Combobox(
            scrollable_frame,
            values=passenger_names,
            textvariable=passenger_var,
            state='readonly',
            width=40,
            font=('Arial', 10)
        )
        passenger_cb.grid(row=current_row, column=1, sticky='w', pady=(10, 5), padx=(10, 0))
        passenger_cb.set("Select Passenger")
        self.booking_widgets['passenger'] = {
            'widget': passenger_cb,
            'var': passenger_var,
            'data': passengers
        }
        current_row += 1
        
        # Flight Selection
        tk.Label(
            scrollable_frame, 
            text="Flight:", 
            font=('Arial', 11, 'bold'),
            foreground='#2c3e50'
        ).grid(row=current_row, column=0, sticky='w', pady=5)
        
        flight_options = [f"{f['number']} - {f['route']} ({f['date']} {f['time']})" for f in flights]
        flight_var = tk.StringVar()
        flight_cb = ttk.Combobox(
            scrollable_frame,
            values=flight_options,
            textvariable=flight_var,
            state='readonly',
            width=40,
            font=('Arial', 10)
        )
        flight_cb.grid(row=current_row, column=1, sticky='w', pady=5, padx=(10, 0))
        flight_cb.set("Select Flight")
        self.booking_widgets['flight'] = {
            'widget': flight_cb,
            'var': flight_var,
            'data': flights
        }
        
        # Flight details display
        flight_details = tk.Label(
            scrollable_frame,
            text="",
            font=('Arial', 9),
            foreground='#666',
            wraplength=400,
            justify=tk.LEFT
        )
        flight_details.grid(row=current_row + 1, column=1, sticky='w', pady=(2, 10), padx=(10, 0))
        self.booking_widgets['flight_details'] = flight_details
        
        # Update flight details when flight is selected
        flight_cb.bind('<<ComboboxSelected>>', lambda e: self.update_flight_details())
        current_row += 2
        
        # Class Selection
        tk.Label(
            scrollable_frame, 
            text="Class:", 
            font=('Arial', 11, 'bold'),
            foreground='#2c3e50'
        ).grid(row=current_row, column=0, sticky='w', pady=10)
        
        class_names = [f"{c['name']} - ${c['price']}" for c in classes]
        class_var = tk.StringVar()
        class_cb = ttk.Combobox(
            scrollable_frame,
            values=class_names,
            textvariable=class_var,
            state='readonly',
            width=25,
            font=('Arial', 10)
        )
        class_cb.grid(row=current_row, column=1, sticky='w', pady=10, padx=(10, 0))
        class_cb.set("Select Class")
        self.booking_widgets['class'] = {
            'widget': class_cb,
            'var': class_var,
            'data': classes
        }
        current_row += 1
        
        # Terminal Selection
        tk.Label(
            scrollable_frame, 
            text="Terminal:", 
            font=('Arial', 11, 'bold'),
            foreground='#2c3e50'
        ).grid(row=current_row, column=0, sticky='w', pady=10)
        
        terminal_names = [f"{t['number']} - {t['name']}" for t in terminals]
        terminal_var = tk.StringVar()
        terminal_cb = ttk.Combobox(
            scrollable_frame,
            values=terminal_names,
            textvariable=terminal_var,
            state='readonly',
            width=25,
            font=('Arial', 10)
        )
        terminal_cb.grid(row=current_row, column=1, sticky='w', pady=10, padx=(10, 0))
        terminal_cb.set("Select Terminal")
        self.booking_widgets['terminal'] = {
            'widget': terminal_cb,
            'var': terminal_var,
            'data': terminals
        }
        current_row += 1
        
        # Seat Number
        tk.Label(
            scrollable_frame, 
            text="Seat Number:", 
            font=('Arial', 11, 'bold'),
            foreground='#2c3e50'
        ).grid(row=current_row, column=0, sticky='w', pady=10)
        
        seat_var = tk.StringVar()
        seat_entry = ttk.Entry(
            scrollable_frame,
            textvariable=seat_var,
            width=15,
            font=('Arial', 10)
        )
        seat_entry.grid(row=current_row, column=1, sticky='w', pady=10, padx=(10, 0))
        self.booking_widgets['seat'] = {
            'widget': seat_entry,
            'var': seat_var
        }
        
        # Seat format helper
        seat_helper = tk.Label(
            scrollable_frame,
            text="Format: 15A, 5B, etc.",
            font=('Arial', 8),
            foreground='#999'
        )
        seat_helper.grid(row=current_row, column=1, sticky='w', pady=(0, 5), padx=(150, 0))
        current_row += 1
        
        # Number of Seats
        tk.Label(
            scrollable_frame, 
            text="Number of Seats:", 
            font=('Arial', 11, 'bold'),
            foreground='#2c3e50'
        ).grid(row=current_row, column=0, sticky='w', pady=10)
        
        seats_var = tk.StringVar(value="1")
        seats_spin = ttk.Spinbox(
            scrollable_frame,
            from_=1,
            to=10,
            textvariable=seats_var,
            width=5,
            font=('Arial', 10)
        )
        seats_spin.grid(row=current_row, column=1, sticky='w', pady=10, padx=(10, 0))
        self.booking_widgets['seats_count'] = {
            'widget': seats_spin,
            'var': seats_var
        }
        current_row += 1
        
        # Price Calculation Display
        price_frame = tk.Frame(scrollable_frame, relief='solid', bd=1, bg='#f8f9fa')
        price_frame.grid(row=current_row, column=0, columnspan=2, sticky='ew', pady=15, padx=5)
        price_frame.grid_columnconfigure(1, weight=1)
        
        tk.Label(
            price_frame,
            text="Price Calculation:",
            font=('Arial', 11, 'bold'),
            foreground='#2c3e50',
            bg='#f8f9fa'
        ).grid(row=0, column=0, sticky='w', pady=5, padx=10)
        
        price_display = tk.Label(
            price_frame,
            text="Select class and seats to see price",
            font=('Arial', 10),
            foreground='#666',
            bg='#f8f9fa'
        )
        price_display.grid(row=0, column=1, sticky='w', pady=5, padx=10)
        self.booking_widgets['price_display'] = price_display
        
        # Bind events for price calculation
        class_cb.bind('<<ComboboxSelected>>', lambda e: self.calculate_price())
        seats_spin.bind('<KeyRelease>', lambda e: self.calculate_price())
        seats_spin.bind('<ButtonRelease>', lambda e: self.calculate_price())
        current_row += 1
        
        # Validation message
        validation_msg = tk.Label(
            scrollable_frame,
            text="",
            font=('Arial', 9),
            foreground='red',
            wraplength=400
        )
        validation_msg.grid(row=current_row, column=0, columnspan=2, pady=10)
        self.booking_widgets['validation'] = validation_msg
        current_row += 1
        
        # Buttons
        button_frame = tk.Frame(scrollable_frame)
        button_frame.grid(row=current_row, column=0, columnspan=2, pady=20)
        
        ttk.Button(
            button_frame,
            text="Create Booking",
            command=lambda: self.create_booking(booking_window),
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Cancel",
            command=booking_window.destroy,
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        # Pack the scrollable area
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Store the window reference
        self.booking_window = booking_window
    
    def center_window(self, window):
        """Center a window on the screen"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
    def get_passengers(self):
        """Get list of passengers from database"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, passport_number, name FROM passengers ORDER BY name")
            passengers = []
            for row in cursor.fetchall():
                passengers.append({
                    'id': row[0],
                    'passport': row[1],
                    'name': row[2]
                })
            conn.close()
            return passengers
        except Exception as e:
            print(f"Error getting passengers: {e}")
            return []

    def get_available_flights(self):
        """Get list of available flights"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    f.id, f.flight_number, 
                    o.airport_code, d.airport_code,
                    f.departure_date, f.departure_time,
                    f.status
                FROM flights f
                JOIN airports o ON f.origin_airport_id = o.id
                JOIN airports d ON f.destination_airport_id = d.id
                WHERE f.status = 'scheduled'
                ORDER BY f.departure_date, f.departure_time
            """)
            flights = []
            for row in cursor.fetchall():
                flights.append({
                    'id': row[0],
                    'number': row[1],
                    'route': f"{row[2]} → {row[3]}",
                    'date': row[4],
                    'time': row[5],
                    'status': row[6]
                })
            conn.close()
            return flights
        except Exception as e:
            print(f"Error getting flights: {e}")
            return []

    def get_classes(self):
        """Get list of available classes with sample prices"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM classes ORDER BY id")
            classes = []
            # Sample prices - in real app, these would come from database
            prices = {'Economy': 450, 'Business': 850, 'First': 1200}
            for row in cursor.fetchall():
                classes.append({
                    'id': row[0],
                    'name': row[1],
                    'price': prices.get(row[1], 500)
                })
            conn.close()
            return classes
        except Exception as e:
            print(f"Error getting classes: {e}")
            return []

    def get_terminals(self):
        """Get list of terminals"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, number, name FROM terminals ORDER BY number")
            terminals = []
            for row in cursor.fetchall():
                terminals.append({
                    'id': row[0],
                    'number': row[1],
                    'name': row[2] or f"Terminal {row[1]}"
                })
            conn.close()
            return terminals
        except Exception as e:
            print(f"Error getting terminals: {e}")
            return []

    def update_flight_details(self):
        """Update flight details display when flight is selected"""
        flight_var = self.booking_widgets['flight']['var']
        flight_data = self.booking_widgets['flight']['data']
        details_label = self.booking_widgets['flight_details']
        
        selected_text = flight_var.get()
        if selected_text and selected_text != "Select Flight":
            # Find the selected flight data
            for flight in flight_data:
                flight_option = f"{flight['number']} - {flight['route']} ({flight['date']} {flight['time']})"
                if flight_option == selected_text:
                    details_label.config(
                        text=f"Flight {flight['number']} | {flight['route']} | {flight['date']} {flight['time']} | {flight['status']}",
                        foreground='#2c3e50'
                    )
                    break

    def calculate_price(self):
        """Calculate and display total price"""
        class_var = self.booking_widgets['class']['var']
        seats_var = self.booking_widgets['seats_count']['var']
        price_display = self.booking_widgets['price_display']
        class_data = self.booking_widgets['class']['data']
        
        try:
            class_text = class_var.get()
            seats = int(seats_var.get())
            
            if class_text and class_text != "Select Class":
                # Extract price from class text "Business - $850"
                for cls in class_data:
                    class_option = f"{cls['name']} - ${cls['price']}"
                    if class_option == class_text:
                        total_price = cls['price'] * seats
                        price_display.config(
                            text=f"${cls['price']} × {seats} seat(s) = ${total_price}",
                            foreground='#27ae60'
                        )
                        return
            
            price_display.config(
                text="Select class and seats to see price",
                foreground='#666'
            )
        except ValueError:
            price_display.config(
                text="Invalid number of seats",
                foreground='red'
            )

    def create_booking(self, window):
        """Create the booking in database"""
        try:
            # Get all values
            passenger_data = self.get_selected_passenger()
            flight_data = self.get_selected_flight()
            class_data = self.get_selected_class()
            terminal_data = self.get_selected_terminal()
            seat_number = self.booking_widgets['seat']['var'].get().strip().upper()
            seats_count = int(self.booking_widgets['seats_count']['var'].get())
            
            # Validate all fields
            validation_msg = self.booking_widgets['validation']
            
            if not passenger_data:
                validation_msg.config(text="Please select a passenger")
                return
                
            if not flight_data:
                validation_msg.config(text="Please select a flight")
                return
                
            if not class_data:
                validation_msg.config(text="Please select a class")
                return
                
            if not terminal_data:
                validation_msg.config(text="Please select a terminal")
                return
                
            if not seat_number:
                validation_msg.config(text="Please enter a seat number")
                return
                
            if seats_count < 1:
                validation_msg.config(text="Please enter valid number of seats")
                return
            
            # Calculate total price
            total_price = class_data['price'] * seats_count
            
            # Generate booking reference and ticket number
            import random
            booking_ref = f"BRN{random.randint(1000, 9999)}"
            ticket_number = f"TKT{random.randint(10000, 99999)}"
            
            # Save to database
            conn = get_connection()
            cursor = conn.cursor()
            
            # Create booking
            cursor.execute("""
                INSERT INTO bookings 
                (user_id, flight_id, seat_count, booking_date, total_price, booking_reference)
                VALUES (?, ?, ?, date('now'), ?, ?)
            """, (1, flight_data['id'], seats_count, total_price, booking_ref))
            
            booking_id = cursor.lastrowid
            
            # Create ticket
            cursor.execute("""
                INSERT INTO tickets 
                (ticket_number, passenger_id, flight_id, booking_id, class_id, terminal_id, seat_number, price, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'confirmed')
            """, (ticket_number, passenger_data['id'], flight_data['id'], booking_id, 
                class_data['id'], terminal_data['id'], seat_number, class_data['price']))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo(
                "Success", 
                f"Booking created successfully!\n\n"
                f"Booking Reference: {booking_ref}\n"
                f"Ticket Number: {ticket_number}\n"
                f"Total: ${total_price}"
            )
            
            window.destroy()
            self.load_bookings()  # Refresh the bookings list
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create booking: {e}")

    def get_selected_passenger(self):
        """Get the selected passenger data"""
        passenger_var = self.booking_widgets['passenger']['var']
        passenger_data = self.booking_widgets['passenger']['data']
        
        selected_text = passenger_var.get()
        if selected_text and selected_text != "Select Passenger":
            for passenger in passenger_data:
                passenger_option = f"{passenger['passport']} - {passenger['name']}"
                if passenger_option == selected_text:
                    return passenger
        return None

    def get_selected_flight(self):
        """Get the selected flight data"""
        flight_var = self.booking_widgets['flight']['var']
        flight_data = self.booking_widgets['flight']['data']
        
        selected_text = flight_var.get()
        if selected_text and selected_text != "Select Flight":
            for flight in flight_data:
                flight_option = f"{flight['number']} - {flight['route']} ({flight['date']} {flight['time']})"
                if flight_option == selected_text:
                    return flight
        return None

    def get_selected_class(self):
        """Get the selected class data"""
        class_var = self.booking_widgets['class']['var']
        class_data = self.booking_widgets['class']['data']
        
        selected_text = class_var.get()
        if selected_text and selected_text != "Select Class":
            for cls in class_data:
                class_option = f"{cls['name']} - ${cls['price']}"
                if class_option == selected_text:
                    return cls
        return None

    def get_selected_terminal(self):
        """Get the selected terminal data"""
        terminal_var = self.booking_widgets['terminal']['var']
        terminal_data = self.booking_widgets['terminal']['data']
        
        selected_text = terminal_var.get()
        if selected_text and selected_text != "Select Terminal":
            for terminal in terminal_data:
                terminal_option = f"{terminal['number']} - {terminal['name']}"
                if terminal_option == selected_text:
                    return terminal
        return None