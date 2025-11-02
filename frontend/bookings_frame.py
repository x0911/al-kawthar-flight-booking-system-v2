# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
from backend.database import get_connection

class BookingsFrame(tk.Frame):
    def __init__(self, parent, language_manager):
        super().__init__(parent)
        self.language_manager = language_manager
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
          text=self.language_manager.get_text('booking_management'),
          font=('Arial', 18, 'bold'),
          bg='white',
          fg='#2c3e50',
          anchor='w' if not self.language_manager.is_rtl() else 'e'
      )
      if self.language_manager.is_rtl():
          title.pack(side=tk.RIGHT)
      else:
          title.pack(side=tk.LEFT)
      
      # Action buttons
      button_frame = tk.Frame(header_frame, bg='white')
      if self.language_manager.is_rtl():
          button_frame.pack(side=tk.LEFT)
      else:
          button_frame.pack(side=tk.RIGHT)
      
      refresh_btn = ttk.Button(
          button_frame,
          text=self.language_manager.get_text('refresh'),
          command=self.load_bookings
      )
      refresh_btn.pack(side=tk.LEFT, padx=5)
      
      add_btn = ttk.Button(
          button_frame,
          text=self.language_manager.get_text('new_booking'),
          command=self.add_booking
      )
      add_btn.pack(side=tk.LEFT, padx=5)
      
      # Search frame
      search_frame = tk.Frame(self, bg='white')
      search_frame.pack(fill=tk.X, padx=20, pady=10)
      
      search_label = tk.Label(search_frame, text=self.language_manager.get_text('search') + ":", bg='white')
      if self.language_manager.is_rtl():
          search_label.pack(side=tk.RIGHT)
      else:
          search_label.pack(side=tk.LEFT)
      
      self.search_var = tk.StringVar()
      search_entry = ttk.Entry(
          search_frame, 
          textvariable=self.search_var,
          width=30
      )
      if self.language_manager.is_rtl():
          search_entry.pack(side=tk.RIGHT, padx=5)
      else:
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
      self.tree.heading('booking_ref', text=self.language_manager.get_text('booking_id'))
      self.tree.heading('passenger_name', text=self.language_manager.get_text('passenger_name'))
      self.tree.heading('flight_number', text=self.language_manager.get_text('flight'))
      self.tree.heading('route', text=self.language_manager.get_text('route'))
      self.tree.heading('booking_date', text=self.language_manager.get_text('booking_date'))
      self.tree.heading('seat_count', text=self.language_manager.get_text('seat_number'))
      self.tree.heading('total_price', text=self.language_manager.get_text('price'))
      self.tree.heading('status', text=self.language_manager.get_text('booking_status'))
      
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
      
      if self.language_manager.is_rtl():
          scrollbar.pack(side=tk.LEFT, fill=tk.Y)
          self.tree.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
      else:
          self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
          scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
      
      # Bind double-click event
      self.tree.bind('<Double-1>', self.on_booking_select)
      
      # Apply RTL to all widgets (AFTER all widgets are created)
      self.language_manager.apply_rtl_layout(self)
        
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
                  self.language_manager.get_text('no_bookings_found'), "", "", "", "", "", "", ""
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
                  self.language_manager.get_text('no_bookings_found'), "", "", "", "", "", "", ""
              ))
              
      except Exception as e:
          messagebox.showerror("Search Error", f"Failed to search bookings: {e}")
    
    def on_booking_select(self, event):
        """Handle booking selection (double-click)"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            booking_data = item['values']
            # Check if we have valid booking data (not the "no bookings found" message)
            if (booking_data and len(booking_data) >= 1 and 
                booking_data[0] != self.language_manager.get_text('no_bookings_found')):
                self.view_booking_details(booking_data)
    
    def view_booking_details(self, booking_data):
        """Show booking details popup"""
        # Check if we have enough data
        if len(booking_data) < 8:
            messagebox.showerror("Error", "Incomplete booking data. Cannot display details.")
            return
            
        details_window = tk.Toplevel(self)
        details_window.title(self.language_manager.get_text('booking_details'))
        details_window.geometry("500x400")
        
        # Set icon
        from frontend.window_utils import set_window_icon
        set_window_icon(details_window)
        
        # Center the window
        self.center_window(details_window)
        
        # Apply RTL to details window
        if self.language_manager.is_rtl():
            self.language_manager.apply_rtl_layout(details_window)
        
        # Booking details
        details_frame = tk.Frame(details_window, padx=20, pady=20)
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create labels based on available data
        labels = [
            (self.language_manager.get_text('booking_id') + ":", booking_data[0]),
            (self.language_manager.get_text('passenger_name') + ":", booking_data[1]),
            (self.language_manager.get_text('flight') + ":", booking_data[2]),
            (self.language_manager.get_text('route') + ":", booking_data[3]),
            (self.language_manager.get_text('booking_date') + ":", booking_data[4]),
            (self.language_manager.get_text('seat_count') + ":", booking_data[5]),
            (self.language_manager.get_text('total_price') + ":", f"${booking_data[6]}"),
        ]
        
        # Add status if available (index 7)
        if len(booking_data) > 7:
            labels.append((self.language_manager.get_text('status') + ":", booking_data[7]))
        
        for i, (label, value) in enumerate(labels):
            label_widget = tk.Label(details_frame, text=label, font=('Arial', 10, 'bold'))
            value_widget = tk.Label(details_frame, text=value)
            
            if self.language_manager.is_rtl():
                label_widget.grid(row=i, column=1, sticky='e', pady=5, padx=(0, 10))
                value_widget.grid(row=i, column=0, sticky='w', pady=5)
            else:
                label_widget.grid(row=i, column=0, sticky='w', pady=5)
                value_widget.grid(row=i, column=1, sticky='w', pady=5, padx=(10, 0))
        
        # Action buttons
        button_frame = tk.Frame(details_frame)
        button_frame.grid(row=len(labels), column=0, columnspan=2, pady=20)
        
        # Only show cancel button if status is available and is 'confirmed'
        if len(booking_data) > 7 and booking_data[7] == 'confirmed':
            cancel_btn = ttk.Button(button_frame, text=self.language_manager.get_text('cancel_booking'), 
                    command=lambda: self.cancel_booking(booking_data[0], details_window))
            cancel_btn.pack(side=tk.LEFT, padx=5)
        
        close_btn = ttk.Button(button_frame, text=self.language_manager.get_text('close'), 
                command=details_window.destroy)
        close_btn.pack(side=tk.LEFT, padx=5)
    
    def cancel_booking(self, booking_ref, window):
        """Cancel a booking"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Update the tickets status for this booking reference
            cursor.execute("""
                UPDATE tickets 
                SET status = 'cancelled' 
                WHERE booking_id IN (
                    SELECT id FROM bookings WHERE booking_reference = ?
                )
            """, (booking_ref,))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", self.language_manager.get_text('booking_cancelled_success'))
            window.destroy()
            self.load_bookings()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to cancel booking: {e}")
    
    def add_booking(self):
        """Open add booking dialog"""
        booking_window = tk.Toplevel(self)
        booking_window.title(self.language_manager.get_text('create_new_booking'))
        booking_window.geometry("600x700")
        
        # Set icon
        from frontend.window_utils import set_window_icon
        set_window_icon(booking_window)
        
        # Center the window
        self.center_window(booking_window)
        
        # Apply RTL to booking window
        if self.language_manager.is_rtl():
            self.language_manager.apply_rtl_layout(booking_window)
        
        form_frame = tk.Frame(booking_window, padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Form title
        title = tk.Label(
            form_frame,
            text=self.language_manager.get_text('create_new_booking'),
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
        passenger_label = tk.Label(
            scrollable_frame, 
            text=self.language_manager.get_text('select_passenger') + ":", 
            font=('Arial', 11, 'bold'),
            foreground='#2c3e50'
        )
        if self.language_manager.is_rtl():
            passenger_label.grid(row=current_row, column=1, sticky='e', pady=(10, 5))
        else:
            passenger_label.grid(row=current_row, column=0, sticky='w', pady=(10, 5))
        
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
        if self.language_manager.is_rtl():
            passenger_cb.grid(row=current_row, column=0, sticky='e', pady=(10, 5), padx=(0, 10))
        else:
            passenger_cb.grid(row=current_row, column=1, sticky='w', pady=(10, 5), padx=(10, 0))
        passenger_cb.set(self.language_manager.get_text('select_passenger'))
        self.booking_widgets['passenger'] = {
            'widget': passenger_cb,
            'var': passenger_var,
            'data': passengers
        }
        current_row += 1
        
        # Flight Selection
        flight_label = tk.Label(
            scrollable_frame, 
            text=self.language_manager.get_text('select_flight') + ":", 
            font=('Arial', 11, 'bold'),
            foreground='#2c3e50'
        )
        if self.language_manager.is_rtl():
            flight_label.grid(row=current_row, column=1, sticky='e', pady=5)
        else:
            flight_label.grid(row=current_row, column=0, sticky='w', pady=5)
        
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
        if self.language_manager.is_rtl():
            flight_cb.grid(row=current_row, column=0, sticky='e', pady=5, padx=(0, 10))
        else:
            flight_cb.grid(row=current_row, column=1, sticky='w', pady=5, padx=(10, 0))
        flight_cb.set(self.language_manager.get_text('select_flight'))
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
            justify=tk.LEFT if not self.language_manager.is_rtl() else tk.RIGHT
        )
        if self.language_manager.is_rtl():
            flight_details.grid(row=current_row + 1, column=0, sticky='e', pady=(2, 10), padx=(0, 10))
        else:
            flight_details.grid(row=current_row + 1, column=1, sticky='w', pady=(2, 10), padx=(10, 0))
        self.booking_widgets['flight_details'] = flight_details
        
        # Update flight details when flight is selected
        flight_cb.bind('<<ComboboxSelected>>', lambda e: self.update_flight_details())
        current_row += 2
        
        # Class Selection
        class_label = tk.Label(
            scrollable_frame, 
            text=self.language_manager.get_text('seat_class') + ":", 
            font=('Arial', 11, 'bold'),
            foreground='#2c3e50'
        )
        if self.language_manager.is_rtl():
            class_label.grid(row=current_row, column=1, sticky='e', pady=10)
        else:
            class_label.grid(row=current_row, column=0, sticky='w', pady=10)
        
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
        if self.language_manager.is_rtl():
            class_cb.grid(row=current_row, column=0, sticky='e', pady=10, padx=(0, 10))
        else:
            class_cb.grid(row=current_row, column=1, sticky='w', pady=10, padx=(10, 0))
        class_cb.set(self.language_manager.get_text('select_class'))
        self.booking_widgets['class'] = {
            'widget': class_cb,
            'var': class_var,
            'data': classes
        }
        current_row += 1
        
        # Terminal Selection
        terminal_label = tk.Label(
            scrollable_frame, 
            text=self.language_manager.get_text('terminal') + ":", 
            font=('Arial', 11, 'bold'),
            foreground='#2c3e50'
        )
        if self.language_manager.is_rtl():
            terminal_label.grid(row=current_row, column=1, sticky='e', pady=10)
        else:
            terminal_label.grid(row=current_row, column=0, sticky='w', pady=10)
        
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
        if self.language_manager.is_rtl():
            terminal_cb.grid(row=current_row, column=0, sticky='e', pady=10, padx=(0, 10))
        else:
            terminal_cb.grid(row=current_row, column=1, sticky='w', pady=10, padx=(10, 0))
        terminal_cb.set(self.language_manager.get_text('select_terminal'))
        self.booking_widgets['terminal'] = {
            'widget': terminal_cb,
            'var': terminal_var,
            'data': terminals
        }
        current_row += 1
        
        # Seat Number
        seat_label = tk.Label(
            scrollable_frame, 
            text=self.language_manager.get_text('seat_number') + ":", 
            font=('Arial', 11, 'bold'),
            foreground='#2c3e50'
        )
        if self.language_manager.is_rtl():
            seat_label.grid(row=current_row, column=1, sticky='e', pady=10)
        else:
            seat_label.grid(row=current_row, column=0, sticky='w', pady=10)
        
        seat_var = tk.StringVar()
        seat_entry = ttk.Entry(
            scrollable_frame,
            textvariable=seat_var,
            width=15,
            font=('Arial', 10)
        )
        if self.language_manager.is_rtl():
            seat_entry.grid(row=current_row, column=0, sticky='e', pady=10, padx=(0, 10))
        else:
            seat_entry.grid(row=current_row, column=1, sticky='w', pady=10, padx=(10, 0))
        self.booking_widgets['seat'] = {
            'widget': seat_entry,
            'var': seat_var
        }
        
        # Seat format helper
        seat_helper = tk.Label(
            scrollable_frame,
            text=self.language_manager.get_text('seat_format_helper'),
            font=('Arial', 8),
            foreground='#999'
        )
        if self.language_manager.is_rtl():
            seat_helper.grid(row=current_row, column=0, sticky='e', pady=(0, 5), padx=(0, 150))
        else:
            seat_helper.grid(row=current_row, column=1, sticky='w', pady=(0, 5), padx=(150, 0))
        current_row += 1
        
        # Number of Seats
        seats_label = tk.Label(
            scrollable_frame, 
            text=self.language_manager.get_text('number_of_seats') + ":", 
            font=('Arial', 11, 'bold'),
            foreground='#2c3e50'
        )
        if self.language_manager.is_rtl():
            seats_label.grid(row=current_row, column=1, sticky='e', pady=10)
        else:
            seats_label.grid(row=current_row, column=0, sticky='w', pady=10)
        
        seats_var = tk.StringVar(value="1")
        seats_spin = ttk.Spinbox(
            scrollable_frame,
            from_=1,
            to=10,
            textvariable=seats_var,
            width=5,
            font=('Arial', 10)
        )
        if self.language_manager.is_rtl():
            seats_spin.grid(row=current_row, column=0, sticky='e', pady=10, padx=(0, 10))
        else:
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
        
        price_label = tk.Label(
            price_frame,
            text=self.language_manager.get_text('price_calculation') + ":",
            font=('Arial', 11, 'bold'),
            foreground='#2c3e50',
            bg='#f8f9fa'
        )
        if self.language_manager.is_rtl():
            price_label.grid(row=0, column=1, sticky='e', pady=5, padx=10)
        else:
            price_label.grid(row=0, column=0, sticky='w', pady=5, padx=10)
        
        price_display = tk.Label(
            price_frame,
            text=self.language_manager.get_text('select_class_seats_for_price'),
            font=('Arial', 10),
            foreground='#666',
            bg='#f8f9fa'
        )
        if self.language_manager.is_rtl():
            price_display.grid(row=0, column=0, sticky='w', pady=5, padx=10)
        else:
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
        
        create_btn = ttk.Button(
            button_frame,
            text=self.language_manager.get_text('create_booking'),
            command=lambda: self.create_booking(booking_window),
            width=15
        )
        create_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = ttk.Button(
            button_frame,
            text=self.language_manager.get_text('cancel'),
            command=booking_window.destroy,
            width=15
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
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
        if selected_text and selected_text != self.language_manager.get_text('select_flight'):
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
            
            if class_text and class_text != self.language_manager.get_text('select_class'):
                # Extract price from class text "Business - $850"
                for cls in class_data:
                    class_option = f"{cls['name']} - ${cls['price']}"
                    if class_option == class_text:
                        total_price = cls['price'] * seats
                        price_display.config(
                            text=f"${cls['price']} × {seats} {self.language_manager.get_text('seat_s')} = ${total_price}",
                            foreground='#27ae60'
                        )
                        return
            
            price_display.config(
                text=self.language_manager.get_text('select_class_seats_for_price'),
                foreground='#666'
            )
        except ValueError:
            price_display.config(
                text=self.language_manager.get_text('invalid_seat_count'),
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
                validation_msg.config(text=self.language_manager.get_text('select_passenger_validation'))
                return
                
            if not flight_data:
                validation_msg.config(text=self.language_manager.get_text('select_flight_validation'))
                return
                
            if not class_data:
                validation_msg.config(text=self.language_manager.get_text('select_class_validation'))
                return
                
            if not terminal_data:
                validation_msg.config(text=self.language_manager.get_text('select_terminal_validation'))
                return
                
            if not seat_number:
                validation_msg.config(text=self.language_manager.get_text('enter_seat_number'))
                return
                
            if seats_count < 1:
                validation_msg.config(text=self.language_manager.get_text('invalid_seat_count'))
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
                f"{self.language_manager.get_text('booking_created_success')}\n\n"
                f"{self.language_manager.get_text('booking_reference')}: {booking_ref}\n"
                f"{self.language_manager.get_text('ticket_number')}: {ticket_number}\n"
                f"{self.language_manager.get_text('total')}: ${total_price}"
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
        if selected_text and selected_text != self.language_manager.get_text('select_passenger'):
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
        if selected_text and selected_text != self.language_manager.get_text('select_flight'):
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
        if selected_text and selected_text != self.language_manager.get_text('select_class'):
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
        if selected_text and selected_text != self.language_manager.get_text('select_terminal'):
            for terminal in terminal_data:
                terminal_option = f"{terminal['number']} - {terminal['name']}"
                if terminal_option == selected_text:
                    return terminal
        return None