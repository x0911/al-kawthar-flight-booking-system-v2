# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox, ttk

from frontend.window_utils import set_window_icon

from backend.database import get_connection

# Try to import tkcalendar, with fallback
try:
    from tkcalendar import DateEntry
    TKCALENDAR_AVAILABLE = True
except ImportError:
    TKCALENDAR_AVAILABLE = False
    print("Warning: tkcalendar not available. Using fallback date entry.")

class FlightsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.sort_column = 'flight_number'  # Default sort column
        self.sort_direction = 'ASC'  # Default sort direction
        self.setup_ui()
        self.load_flights()
        
    def setup_ui(self):
        """Create flights management interface"""
        self.configure(bg='white')
        
        # Header with buttons
        header_frame = tk.Frame(self, bg='white')
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        title = tk.Label(
            header_frame,
            text="Flights Management",
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
            command=self.load_flights
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        add_btn = ttk.Button(
            button_frame,
            text="Add Flight",
            command=self.add_flight
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
        
        # Flights table
        table_frame = tk.Frame(self, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create treeview with scrollbar
        columns = ('flight_id', 'flight_number', 'origin', 'destination', 
                  'departure', 'arrival', 'status')
        
        self.tree = ttk.Treeview(
            table_frame, 
            columns=columns,
            show='headings',
            height=15
        )
        
        # Define headings with sort indicators
        self.tree.heading('flight_id', text='ID', command=lambda: self.sort_treeview('f.id'))
        self.tree.heading('flight_number', text='Flight Number', command=lambda: self.sort_treeview('f.flight_number'))
        self.tree.heading('origin', text='Origin', command=lambda: self.sort_treeview('o_airport.name'))
        self.tree.heading('destination', text='Destination', command=lambda: self.sort_treeview('d_airport.name'))
        self.tree.heading('departure', text='Departure', command=lambda: self.sort_treeview('f.departure_date'))
        self.tree.heading('arrival', text='Arrival', command=lambda: self.sort_treeview('f.arrival_date'))
        self.tree.heading('status', text='Status', command=lambda: self.sort_treeview('f.status'))
        
        # Configure columns
        self.tree.column('flight_id', width=50)
        self.tree.column('flight_number', width=120)
        self.tree.column('origin', width=150)
        self.tree.column('destination', width=150)
        self.tree.column('departure', width=150)
        self.tree.column('arrival', width=150)
        self.tree.column('status', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double-click event
        self.tree.bind('<Double-1>', self.on_flight_select)
        
        # Update sort indicator on initial load
        self.update_sort_indicator()
        
    def sort_treeview(self, column):
        """Sort treeview by column"""
        # Toggle sort direction if clicking the same column
        if self.sort_column == column:
            self.sort_direction = 'DESC' if self.sort_direction == 'ASC' else 'ASC'
        else:
            # New column, default to ascending
            self.sort_column = column
            self.sort_direction = 'ASC'
        
        # Update the sort indicator and reload data
        self.update_sort_indicator()
        self.load_flights()
        
    def update_sort_indicator(self):
        """Update column headers to show sort direction"""
        # Remove any existing sort indicators
        for col in self.tree['columns']:
            current_text = self.tree.heading(col)['text']
            # Remove any existing arrows
            clean_text = current_text.replace(' ▲', '').replace(' ▼', '')
            self.tree.heading(col, text=clean_text)
        
        # Add arrow to current sort column
        if self.sort_column == 'f.id':
            current_text = self.tree.heading('flight_id')['text']
            arrow = ' ▲' if self.sort_direction == 'ASC' else ' ▼'
            self.tree.heading('flight_id', text=current_text + arrow)
        elif self.sort_column == 'f.flight_number':
            current_text = self.tree.heading('flight_number')['text']
            arrow = ' ▲' if self.sort_direction == 'ASC' else ' ▼'
            self.tree.heading('flight_number', text=current_text + arrow)
        elif self.sort_column == 'o_airport.name':
            current_text = self.tree.heading('origin')['text']
            arrow = ' ▲' if self.sort_direction == 'ASC' else ' ▼'
            self.tree.heading('origin', text=current_text + arrow)
        elif self.sort_column == 'd_airport.name':
            current_text = self.tree.heading('destination')['text']
            arrow = ' ▲' if self.sort_direction == 'ASC' else ' ▼'
            self.tree.heading('destination', text=current_text + arrow)
        elif self.sort_column == 'f.departure_date':
            current_text = self.tree.heading('departure')['text']
            arrow = ' ▲' if self.sort_direction == 'ASC' else ' ▼'
            self.tree.heading('departure', text=current_text + arrow)
        elif self.sort_column == 'f.arrival_date':
            current_text = self.tree.heading('arrival')['text']
            arrow = ' ▲' if self.sort_direction == 'ASC' else ' ▼'
            self.tree.heading('arrival', text=current_text + arrow)
        elif self.sort_column == 'f.status':
            current_text = self.tree.heading('status')['text']
            arrow = ' ▲' if self.sort_direction == 'ASC' else ' ▼'
            self.tree.heading('status', text=current_text + arrow)
        
    def load_flights(self):
        """Load flights from database with current sort"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Build the query with sorting
            query = """
                SELECT 
                    f.id, 
                    f.flight_number, 
                    o_airport.name as origin, 
                    d_airport.name as destination,
                    f.departure_date || ' ' || f.departure_time as departure,
                    f.arrival_date || ' ' || f.arrival_time as arrival,
                    f.status
                FROM flights f
                LEFT JOIN airports o_airport ON f.origin_airport_id = o_airport.id
                LEFT JOIN airports d_airport ON f.destination_airport_id = d_airport.id
                ORDER BY {} {}
            """.format(self.sort_column, self.sort_direction)
            
            cursor.execute(query)
            flights = cursor.fetchall()
            conn.close()
            
            # Clear existing data
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Populate treeview - convert sqlite3.Row to tuple
            for flight in flights:
                flight_values = tuple(flight)
                self.tree.insert('', tk.END, values=flight_values)
                
            # Show message if no flights
            if not flights:
                self.tree.insert('', tk.END, values=("No flights found", "", "", "", "", "", ""))
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load flights: {e}")
    
    def on_search(self, event):
      """Handle search functionality"""
      try:
          search_term = self.search_var.get().lower().strip()
          
          if not search_term:
              # If search is empty, show all flights
              self.load_flights()
              return
              
          # Filter flights based on search term
          conn = get_connection()
          cursor = conn.cursor()
          
          cursor.execute("""
              SELECT 
                  f.id, 
                  f.flight_number, 
                  o_airport.name as origin, 
                  d_airport.name as destination,
                  f.departure_date || ' ' || f.departure_time as departure,
                  f.arrival_date || ' ' || f.arrival_time as arrival,
                  f.status
              FROM flights f
              LEFT JOIN airports o_airport ON f.origin_airport_id = o_airport.id
              LEFT JOIN airports d_airport ON f.destination_airport_id = d_airport.id
              WHERE f.flight_number LIKE ? OR 
                    o_airport.name LIKE ? OR 
                    d_airport.name LIKE ? OR
                    f.status LIKE ?
              ORDER BY f.departure_date, f.departure_time
          """, (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
          
          flights = cursor.fetchall()
          conn.close()
          
          # Clear existing data
          for item in self.tree.get_children():
              self.tree.delete(item)
          
          # Populate treeview - convert sqlite3.Row to tuple
          for flight in flights:
              flight_values = tuple(flight)
              self.tree.insert('', tk.END, values=flight_values)
              
          # Show message if no results
          if not flights:
              self.tree.insert('', tk.END, values=("No flights found", "", "", "", "", "", ""))
              
      except Exception as e:
          messagebox.showerror("Search Error", f"Failed to search flights: {e}")
    
    def on_flight_select(self, event):
      """Handle flight selection (double-click)"""
      selection = self.tree.selection()
      if not selection:
          return  # No selection
      
      try:
          item = self.tree.item(selection[0])
          flight_data = item['values']
          
          # Debug: Print what we're actually getting
          print(f"Flight data received: {flight_data}")
          print(f"Number of elements: {len(flight_data)}")
          print(f"Data types: {[type(x) for x in flight_data]}")
          
          # Validate we have enough data
          if not flight_data or len(flight_data) < 7:
              messagebox.showwarning(
                  "Incomplete Data", 
                  f"Flight data is incomplete. Expected 7 columns, got {len(flight_data) if flight_data else 0}."
              )
              return
              
          self.view_flight_details(flight_data)
          
      except Exception as e:
          messagebox.showerror("Error", f"Failed to load flight details: {e}")
    
    def view_flight_details(self, flight_data):
      """Show flight details popup"""
      # Check if we have enough data
      if len(flight_data) < 7:
          messagebox.showerror("Error", "Incomplete flight data. Cannot display details.")
          return
          
      details_window = tk.Toplevel(self)
      details_window.title("Flight Details")
      details_window.geometry("400x300")
      
      # Set icon for details window too
      set_window_icon(details_window)
      
      # Center the window (manual calculation instead of eval)
      self.center_window(details_window)
      
      # Flight details
      details_frame = tk.Frame(details_window, padx=20, pady=20)
      details_frame.pack(fill=tk.BOTH, expand=True)
      
      labels = [
          ("Flight ID:", flight_data[0]),
          ("Flight Number:", flight_data[1]),
          ("Origin:", flight_data[2]),
          ("Destination:", flight_data[3]),
          ("Departure:", flight_data[4]),
          ("Arrival:", flight_data[5]),
          ("Status:", flight_data[6])
      ]
      
      for i, (label, value) in enumerate(labels):
          tk.Label(details_frame, text=label, font=('Arial', 10, 'bold')).grid(
              row=i, column=0, sticky='w', pady=5)
          tk.Label(details_frame, text=value).grid(
              row=i, column=1, sticky='w', pady=5, padx=(10, 0))
    
    def add_flight(self):
      """Open add flight dialog with proper date/time pickers"""
      add_window = tk.Toplevel(self)
      add_window.title("Add New Flight")
      add_window.geometry("550x600")  # Slightly wider for the helper text
      
      # Set icon for the dialog window too
      set_window_icon(add_window)
      
      # Center the window
      self.center_window(add_window)
      
      form_frame = tk.Frame(add_window, padx=20, pady=20)
      form_frame.pack(fill=tk.BOTH, expand=True)
      
      # Form fields
      tk.Label(form_frame, text="Add New Flight", font=('Arial', 16, 'bold')).grid(
          row=0, column=0, columnspan=2, pady=(0, 20))
      
      # Get airports for dropdowns
      airports = self.get_airports()
      airport_names = [f"{airport['code']} - {airport['name']}" for airport in airports]
      
      from datetime import datetime, timedelta
      current_date = datetime.now()
      default_departure = current_date + timedelta(days=1)
      default_arrival = default_departure + timedelta(hours=2)
      
      # Flight Number field with helper label
      tk.Label(form_frame, text="Flight Number:", font=('Arial', 10)).grid(
          row=1, column=0, sticky='w', pady=10)

      flight_frame = tk.Frame(form_frame)
      flight_frame.grid(row=1, column=1, sticky='w', pady=10, padx=(10, 0))

      self.flight_number_entry = ttk.Entry(flight_frame, width=15, font=('Arial', 10))
      self.flight_number_entry.pack(side=tk.LEFT)

      # Helper label to show formatted flight number
      self.flight_number_helper = tk.Label(
          flight_frame, 
          text=" → Will be saved as: AK", 
          font=('Arial', 9), 
          fg='gray'
      )
      self.flight_number_helper.pack(side=tk.LEFT, padx=5)

      # Update helper text when user types
      self.flight_number_entry.bind('<KeyRelease>', self.update_flight_number_helper)

      # Store the flight number entry
      self.entry_widgets = {}
      self.entry_widgets["Flight Number:"] = self.flight_number_entry
      self.airport_data = airports
      
      # Rest of the fields
      fields = [
          ("Origin Airport:", "combobox"),
          ("Destination Airport:", "combobox"),
          ("Departure Date:", "date_picker"),
          ("Departure Time:", "time_picker"),
          ("Arrival Date:", "date_picker"),
          ("Arrival Time:", "time_picker")
      ]
      
      row = 2  # Start from row 2 since flight number is at row 1
      for label, widget_type in fields:
          tk.Label(form_frame, text=label, font=('Arial', 10)).grid(
              row=row, column=0, sticky='w', pady=10)
          
          if widget_type == "combobox":
              combobox = ttk.Combobox(
                  form_frame, 
                  values=airport_names, 
                  width=40, 
                  font=('Arial', 10),
                  state='readonly'
              )
              combobox.grid(row=row, column=1, sticky='w', pady=10, padx=(10, 0))
              combobox.set("")
              self.entry_widgets[label] = combobox
              
          elif widget_type == "date_picker":
              if TKCALENDAR_AVAILABLE:
                  # Use tkcalendar DateEntry
                  if "Departure Date:" in self.entry_widgets:
                      default_date = default_arrival
                  else:
                      default_date = default_departure
                      
                  date_entry = DateEntry(
                      form_frame,
                      width=20,
                      background='darkblue',
                      foreground='white',
                      borderwidth=2,
                      date_pattern='yyyy-mm-dd',
                      mindate=current_date,
                      font=('Arial', 10)
                  )
                  date_entry.set_date(default_date)
                  date_entry.grid(row=row, column=1, sticky='w', pady=10, padx=(10, 0))
                  self.entry_widgets[label] = date_entry
              else:
                  # Fallback: Simple date entry with validation
                  date_entry = ttk.Entry(form_frame, width=25, font=('Arial', 10))
                  date_entry.grid(row=row, column=1, sticky='w', pady=10, padx=(10, 0))
                  if "Departure Date:" in self.entry_widgets:
                      date_entry.insert(0, default_arrival.strftime("%Y-%m-%d"))
                  else:
                      date_entry.insert(0, default_departure.strftime("%Y-%m-%d"))
                  self.entry_widgets[label] = date_entry
                  
                  # Add placeholder text
                  date_entry.config(foreground='black')
                  date_entry.bind('<FocusIn>', lambda e, entry=date_entry: self.on_date_focus_in(entry))
                  date_entry.bind('<FocusOut>', lambda e, entry=date_entry: self.on_date_focus_out(entry))
              
          elif widget_type == "time_picker":
              time_frame = tk.Frame(form_frame)
              time_frame.grid(row=row, column=1, sticky='w', pady=10, padx=(10, 0))
              
              # Hour spinbox
              hour_label = tk.Label(time_frame, text="Hour:", font=('Arial', 9))
              hour_label.pack(side=tk.LEFT)
              
              default_hour = "08" if "Departure Time:" not in self.entry_widgets else "10"
              hour_var = tk.StringVar(value=default_hour)
              hour_spin = ttk.Spinbox(
                  time_frame,
                  from_=0,
                  to=23,
                  width=3,
                  textvariable=hour_var,
                  format="%02.0f",
                  font=('Arial', 10)
              )
              hour_spin.pack(side=tk.LEFT, padx=5)
              
              # Minute spinbox
              minute_label = tk.Label(time_frame, text="Min:", font=('Arial', 9))
              minute_label.pack(side=tk.LEFT, padx=(10, 0))
              
              minute_var = tk.StringVar(value="00")
              minute_spin = ttk.Spinbox(
                  time_frame,
                  from_=0,
                  to=55,
                  width=3,
                  textvariable=minute_var,
                  format="%02.0f",
                  increment=5,
                  font=('Arial', 10)
              )
              minute_spin.pack(side=tk.LEFT, padx=5)
              
              # Store time widgets
              time_widgets = {
                  'hour_spin': hour_spin,
                  'minute_spin': minute_spin,
                  'hour_var': hour_var,
                  'minute_var': minute_var
              }
              self.entry_widgets[label] = time_widgets
              
          row += 1
      
      # Validation label
      self.validation_label = tk.Label(
          form_frame, 
          text="", 
          fg='red', 
          font=('Arial', 9),
          wraplength=400
      )
      self.validation_label.grid(row=row, column=0, columnspan=2, pady=10)
      row += 1
      
      # Buttons
      button_frame = tk.Frame(form_frame)
      button_frame.grid(row=row, column=0, columnspan=2, pady=20)
      
      ttk.Button(button_frame, text="Save Flight", 
                command=lambda: self.validate_and_save_flight(add_window)).pack(side=tk.LEFT, padx=5)
      ttk.Button(button_frame, text="Cancel", 
                command=add_window.destroy).pack(side=tk.LEFT, padx=5)
      
    def get_airports(self):
      """Get list of airports from database"""
      try:
          conn = get_connection()
          cursor = conn.cursor()
          
          cursor.execute("""
              SELECT id, airport_code, name 
              FROM airports 
              ORDER BY airport_code
          """)
          
          airports = []
          for row in cursor.fetchall():
              airports.append({
                  'id': row[0],
                  'code': row[1],
                  'name': row[2]
              })
          
          conn.close()
          return airports
          
      except Exception as e:
          messagebox.showerror("Database Error", f"Failed to load airports: {e}")
          return []
        
    def validate_and_save_flight(self, window):
      """Validate form data and save flight"""
      try:
          # Get form values
          flight_number_input = self.entry_widgets["Flight Number:"].get().strip()
          origin_text = self.entry_widgets["Origin Airport:"].get().strip()
          destination_text = self.entry_widgets["Destination Airport:"].get().strip()
          
          # Get date values (handle both tkcalendar and fallback)
          dep_date_widget = self.entry_widgets["Departure Date:"]
          if TKCALENDAR_AVAILABLE and hasattr(dep_date_widget, 'get_date'):
              dep_date = dep_date_widget.get_date().strftime("%Y-%m-%d")
          else:
              dep_date = self.get_date_from_widgets(dep_date_widget)
              if not dep_date:
                  self.validation_label.config(text="Please select a valid departure date!")
                  return
          
          arr_date_widget = self.entry_widgets["Arrival Date:"]
          if TKCALENDAR_AVAILABLE and hasattr(arr_date_widget, 'get_date'):
              arr_date = arr_date_widget.get_date().strftime("%Y-%m-%d")
          else:
              arr_date = self.get_date_from_widgets(arr_date_widget)
              if not arr_date:
                  self.validation_label.config(text="Please select a valid arrival date!")
                  return
          
          # Get time values from spinboxes
          dep_time_widgets = self.entry_widgets["Departure Time:"]
          dep_time = f"{dep_time_widgets['hour_var'].get()}:{dep_time_widgets['minute_var'].get()}"
          
          arr_time_widgets = self.entry_widgets["Arrival Time:"]
          arr_time = f"{arr_time_widgets['hour_var'].get()}:{arr_time_widgets['minute_var'].get()}"
          
          # Validate required fields
          if not all([flight_number_input, origin_text, destination_text, dep_date, arr_date]):
              self.validation_label.config(text="All fields are required!")
              return
          
          # Process and validate flight number
          flight_number = self.process_flight_number(flight_number_input)
          if not flight_number:
              self.validation_label.config(text="Please enter a valid flight number (numbers only)")
              return
          
          # Check if flight number already exists
          if self.flight_number_exists(flight_number, dep_date):
              self.validation_label.config(text=f"Flight {flight_number} already exists on {dep_date}!")
              return
          
          # Validate date format (for fallback)
          if not TKCALENDAR_AVAILABLE:
              if not self.is_valid_date(dep_date) or not self.is_valid_date(arr_date):
                  self.validation_label.config(text="Please use YYYY-MM-DD format for dates!")
                  return
          
          # Validate airport selection
          origin_airport = self.get_airport_from_selection(origin_text)
          destination_airport = self.get_airport_from_selection(destination_text)
          
          if not origin_airport:
              self.validation_label.config(text="Please select a valid origin airport!")
              return
              
          if not destination_airport:
              self.validation_label.config(text="Please select a valid destination airport!")
              return
          
          # Validate that origin and destination are different
          if origin_airport['id'] == destination_airport['id']:
              self.validation_label.config(text="Origin and destination airports cannot be the same!")
              return
          
          # Validate date/time logic
          from datetime import datetime
          try:
              dep_datetime = datetime.strptime(f"{dep_date} {dep_time}", "%Y-%m-%d %H:%M")
              arr_datetime = datetime.strptime(f"{arr_date} {arr_time}", "%Y-%m-%d %H:%M")
              
              if arr_datetime <= dep_datetime:
                  self.validation_label.config(text="Arrival must be after departure!")
                  return
                  
          except ValueError as e:
              self.validation_label.config(text=f"Invalid date/time: {e}")
              return
          
          # If all validations pass, save the flight
          self.save_flight_to_database(
              flight_number, origin_airport['id'], destination_airport['id'],
              dep_date, dep_time, arr_date, arr_time, window
          )
          
      except Exception as e:
          messagebox.showerror("Error", f"Validation error: {e}")
    
    def save_flight(self, window):
        """Save new flight to database"""
        try:
            # This would save to database in a real app
            # For now, just show a message and close
            messagebox.showinfo("Success", "Flight saved successfully!")
            window.destroy()
            self.load_flights()  # Refresh the list
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save flight: {e}")
    
    def center_window(self, window):
        """Center a window on the screen"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
    def debug_flight_data(self):
      """Debug method to check what data we're getting"""
      try:
          conn = get_connection()
          cursor = conn.cursor()
          
          cursor.execute("""
              SELECT 
                  f.id, 
                  f.flight_number, 
                  o_airport.name as origin, 
                  d_airport.name as destination,
                  f.departure_date || ' ' || f.departure_time as departure,
                  f.arrival_date || ' ' || f.arrival_time as arrival,
                  f.status
              FROM flights f
              LEFT JOIN airports o_airport ON f.origin_airport_id = o_airport.id
              LEFT JOIN airports d_airport ON f.destination_airport_id = d_airport.id
              LIMIT 1
          """)
          
          sample_flight = cursor.fetchone()
          conn.close()
          
          if sample_flight:
              print("Sample flight data structure:")
              print(f"Type: {type(sample_flight)}")
              print(f"Number of columns: {len(sample_flight)}")
              
              # Convert to tuple for display
              flight_tuple = tuple(sample_flight)
              print(f"As tuple: {flight_tuple}")
              
              for i, value in enumerate(flight_tuple):
                  print(f"Column {i}: {value} (type: {type(value)})")
          else:
              print("No flights found in database")
              
      except Exception as e:
          print(f"Debug error: {e}")
          
    def get_airport_from_selection(self, selection_text):
      """Extract airport ID from combobox selection"""
      if not selection_text:
          return None
      
      # Selection format: "DXB - Dubai International Airport"
      for airport in self.airport_data:
          expected_format = f"{airport['code']} - {airport['name']}"
          if selection_text == expected_format:
              return airport
      
      return None

    def is_valid_date(self, date_str):
        """Basic date format validation"""
        import re
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        return bool(re.match(pattern, date_str))

    def is_valid_time(self, time_str):
        """Basic time format validation"""
        import re
        pattern = r'^\d{2}:\d{2}$'
        return bool(re.match(pattern, time_str))

    def save_flight_to_database(self, flight_number, origin_id, destination_id, 
                              dep_date, dep_time, arr_date, arr_time, window):
        """Save the new flight to database"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Get a plane and branch (for demo - in real app you'd let user choose)
            cursor.execute("SELECT id FROM planes LIMIT 1")
            plane_id = cursor.fetchone()[0]
            cursor.execute("SELECT id FROM branches LIMIT 1")
            branch_id = cursor.fetchone()[0]
            
            cursor.execute("""
                INSERT INTO flights 
                (flight_number, plane_id, branch_id, origin_airport_id, destination_airport_id,
                departure_date, departure_time, arrival_date, arrival_time, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (flight_number, plane_id, branch_id, origin_id, destination_id,
                  dep_date, dep_time, arr_date, arr_time, 'scheduled'))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", f"Flight {flight_number} created successfully!")
            window.destroy()
            self.load_flights()  # Refresh the list
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save flight: {e}")
            
    def on_date_focus_in(self, entry):
      """Handle focus in for date entry (fallback)"""
      if entry.get() == "YYYY-MM-DD":
          entry.delete(0, tk.END)
          entry.config(foreground='black')

    def on_date_focus_out(self, entry):
        """Handle focus out for date entry (fallback)"""
        if not entry.get():
            entry.insert(0, "YYYY-MM-DD")
            entry.config(foreground='black')
            
    def cleanup(self):
        """Clean up resources when frame is destroyed"""
        # Unbind any events if needed
        try:
            self.tree.unbind('<Double-1>')
        except:
            pass
    def process_flight_number(self, flight_number_input):
      """Process flight number input and add AK prefix"""
      # Remove any existing AK prefix and whitespace
      cleaned_input = flight_number_input.upper().replace('AK', '').strip()
      
      # Check if it's all numbers
      if cleaned_input.isdigit():
          return f"AK{cleaned_input}"
      else:
          return None

    def flight_number_exists(self, flight_number, date):
        """Check if a flight number already exists on the given date"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT COUNT(*) FROM flights 
                WHERE flight_number = ? AND departure_date = ?
            """, (flight_number, date))
            
            count = cursor.fetchone()[0]
            conn.close()
            
            return count > 0
            
        except Exception as e:
            print(f"Error checking flight existence: {e}")
            return False

    def get_date_from_widgets(self, date_widgets):
        """Extract date from fallback date widgets"""
        try:
            year = date_widgets['year_var'].get()
            month_str = date_widgets['month_var'].get()
            month = month_str.split(' - ')[0]  # Extract "02" from "02 - Feb"
            day = date_widgets['day_var'].get()
            
            return f"{year}-{month}-{day}"
        except:
            return None
          
    def update_flight_number_helper(self, event):
      """Update the helper text to show formatted flight number"""
      try:
          input_text = self.flight_number_entry.get().strip()
          if input_text.isdigit():
              self.flight_number_helper.config(
                  text=f" → Will be saved as: AK{input_text}", 
                  fg='green'
              )
          else:
              self.flight_number_helper.config(
                  text=" → Enter numbers only", 
                  fg='red'
              )
      except:
          pass