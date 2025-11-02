# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
from backend.database import get_connection

class PassengersFrame(tk.Frame):
    def __init__(self, parent, language_manager):
        super().__init__(parent)
        self.language_manager = language_manager
        self.setup_ui()
        self.load_passengers()
        
    def setup_ui(self):
        """Create passengers management interface"""
        self.configure(bg='white')
        
        # Header with buttons
        header_frame = tk.Frame(self, bg='white')
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        title = tk.Label(
            header_frame,
            text=self.language_manager.get_text('passengers_management'),
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
            command=self.load_passengers
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        add_btn = ttk.Button(
            button_frame,
            text=self.language_manager.get_text('add_passenger'),
            command=self.add_passenger
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
        
        # Passengers table
        table_frame = tk.Frame(self, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create treeview with scrollbar
        columns = ('passenger_id', 'passport', 'name', 'gender', 'nationality')
        
        self.tree = ttk.Treeview(
            table_frame, 
            columns=columns,
            show='headings',
            height=15
        )
        
        # Define headings
        self.tree.heading('passenger_id', text='ID')
        self.tree.heading('passport', text=self.language_manager.get_text('passport_number'))
        self.tree.heading('name', text=self.language_manager.get_text('passenger_name'))
        self.tree.heading('gender', text=self.language_manager.get_text('gender'))
        self.tree.heading('nationality', text=self.language_manager.get_text('nationality'))
        
        # Configure columns
        self.tree.column('passenger_id', width=50)
        self.tree.column('passport', width=120)
        self.tree.column('name', width=150)
        self.tree.column('gender', width=80)
        self.tree.column('nationality', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        if self.language_manager.is_rtl():
            scrollbar.pack(side=tk.LEFT, fill=tk.Y)
            self.tree.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        else:
            self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind events
        self.tree.bind('<Double-1>', self.on_passenger_view)
        
        # Context menu for right-click actions
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(
            label=self.language_manager.get_text('view_details'),
            command=self.view_selected_passenger
        )
        self.context_menu.add_command(
            label=self.language_manager.get_text('edit_passenger'),
            command=self.edit_selected_passenger
        )
        self.tree.bind('<Button-3>', self.show_context_menu)
        
        # Apply RTL to all widgets (AFTER all widgets are created)
        self.language_manager.apply_rtl_layout(self)
        
    def load_passengers(self):
        """Load passengers from database"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    p.id,
                    p.passport_number,
                    p.name,
                    g.name as gender,
                    c.name as nationality
                FROM passengers p
                JOIN genders g ON p.gender_id = g.id
                JOIN countries c ON p.nationality_country_id = c.id
                ORDER BY p.name
            """)
            
            passengers = cursor.fetchall()
            conn.close()
            
            # Clear existing data
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Populate treeview
            for passenger in passengers:
                passenger_values = tuple(passenger)
                self.tree.insert('', tk.END, values=passenger_values)
                
            # Show message if no passengers
            if not passengers:
                self.tree.insert('', tk.END, values=(
                    self.language_manager.get_text('no_passengers_found'), "", "", "", ""
                ))
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load passengers: {e}")
    
    def on_search(self, event):
        """Handle search functionality"""
        try:
            search_term = self.search_var.get().lower().strip()
            
            if not search_term:
                self.load_passengers()
                return
                
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    p.id,
                    p.passport_number,
                    p.name,
                    g.name as gender,
                    c.name as nationality
                FROM passengers p
                JOIN genders g ON p.gender_id = g.id
                JOIN countries c ON p.nationality_country_id = c.id
                WHERE p.passport_number LIKE ? OR 
                      p.name LIKE ? OR
                      g.name LIKE ? OR
                      c.name LIKE ?
                ORDER BY p.name
            """, (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
            
            passengers = cursor.fetchall()
            conn.close()
            
            # Clear existing data
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Populate treeview
            for passenger in passengers:
                passenger_values = tuple(passenger)
                self.tree.insert('', tk.END, values=passenger_values)
                
            if not passengers:
                self.tree.insert('', tk.END, values=(
                    self.language_manager.get_text('no_passengers_found'), "", "", "", ""
                ))
                
        except Exception as e:
            messagebox.showerror("Search Error", f"Failed to search passengers: {e}")
    
    def show_context_menu(self, event):
        """Show context menu on right-click"""
        selection = self.tree.identify_row(event.y)
        if selection:
            self.tree.selection_set(selection)
            self.context_menu.post(event.x_root, event.y_root)
    
    def get_selected_passenger(self):
        """Get the selected passenger data"""
        selection = self.tree.selection()
        if not selection:
            return None
            
        item = self.tree.item(selection[0])
        passenger_data = item['values']
        
        # Check if it's a valid passenger (not the "no passengers found" message)
        if (passenger_data and len(passenger_data) >= 1 and 
            passenger_data[0] != self.language_manager.get_text('no_passengers_found')):
            return passenger_data
        return None
    
    def view_selected_passenger(self):
        """View selected passenger details"""
        passenger_data = self.get_selected_passenger()
        if passenger_data:
            self.view_passenger_details(passenger_data)
    
    def edit_selected_passenger(self):
        """Edit selected passenger"""
        passenger_data = self.get_selected_passenger()
        if passenger_data:
            self.edit_passenger(passenger_data)
    
    def on_passenger_view(self, event):
        """Handle passenger double-click (view details)"""
        passenger_data = self.get_selected_passenger()
        if passenger_data:
            self.view_passenger_details(passenger_data)
    
    def view_passenger_details(self, passenger_data):
        """Show passenger details in a 2-tab dialog"""
        details_window = tk.Toplevel(self)
        details_window.title(self.language_manager.get_text('passenger_details'))
        details_window.geometry("700x500")
        
        # Center the window
        self.center_window(details_window)
        
        # Apply RTL to details window
        if self.language_manager.is_rtl():
            self.language_manager.apply_rtl_layout(details_window)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(details_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Passenger Details
        details_frame = ttk.Frame(notebook)
        notebook.add(details_frame, text=self.language_manager.get_text('passenger_details'))
        
        # Tab 2: Passenger Bookings
        bookings_frame = ttk.Frame(notebook)
        notebook.add(bookings_frame, text=self.language_manager.get_text('passenger_bookings'))
        
        # Load passenger details for tab 1
        self.load_passenger_details_tab(details_frame, passenger_data[0])
        
        # Load passenger bookings for tab 2
        self.load_passenger_bookings_tab(bookings_frame, passenger_data[0])
    
    def load_passenger_details_tab(self, parent, passenger_id):
        """Load passenger details in the details tab"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    p.passport_number,
                    p.name,
                    g.name as gender,
                    c.name as nationality,
                    c.code as country_code
                FROM passengers p
                JOIN genders g ON p.gender_id = g.id
                JOIN countries c ON p.nationality_country_id = c.id
                WHERE p.id = ?
            """, (passenger_id,))
            
            passenger = cursor.fetchone()
            conn.close()
            
            if not passenger:
                tk.Label(parent, text=self.language_manager.get_text('passenger_not_found')).pack(pady=20)
                return
            
            # Create details display
            details_container = tk.Frame(parent)
            details_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            labels = [
                (self.language_manager.get_text('passport_number') + ":", passenger[0]),
                (self.language_manager.get_text('passenger_name') + ":", passenger[1]),
                (self.language_manager.get_text('gender') + ":", passenger[2]),
                (self.language_manager.get_text('nationality') + ":", passenger[3]),
                (self.language_manager.get_text('country_code') + ":", passenger[4])
            ]
            
            for i, (label, value) in enumerate(labels):
                label_widget = tk.Label(details_container, text=label, font=('Arial', 11, 'bold'))
                value_widget = tk.Label(details_container, text=value, font=('Arial', 11))
                
                if self.language_manager.is_rtl():
                    label_widget.grid(row=i, column=1, sticky='e', pady=8, padx=(0, 10))
                    value_widget.grid(row=i, column=0, sticky='w', pady=8)
                else:
                    label_widget.grid(row=i, column=0, sticky='w', pady=8)
                    value_widget.grid(row=i, column=1, sticky='w', pady=8, padx=(10, 0))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load passenger details: {e}")
    
    def load_passenger_bookings_tab(self, parent, passenger_id):
        """Load passenger bookings in the bookings tab"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    b.booking_reference,
                    f.flight_number,
                    o_airport.airport_code || ' → ' || d_airport.airport_code as route,
                    b.booking_date,
                    t.ticket_number,
                    cls.name as class,
                    t.seat_number,
                    t.price,
                    t.status
                FROM tickets t
                JOIN bookings b ON t.booking_id = b.id
                JOIN flights f ON t.flight_id = f.id
                JOIN airports o_airport ON f.origin_airport_id = o_airport.id
                JOIN airports d_airport ON f.destination_airport_id = d_airport.id
                JOIN classes cls ON t.class_id = cls.id
                WHERE t.passenger_id = ?
                ORDER BY b.booking_date DESC
            """, (passenger_id,))
            
            bookings = cursor.fetchall()
            conn.close()
            
            if not bookings:
                tk.Label(parent, text=self.language_manager.get_text('no_bookings_found')).pack(pady=20)
                return
            
            # Create bookings table
            table_frame = tk.Frame(parent)
            table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Create treeview for bookings
            columns = ('booking_ref', 'flight', 'route', 'booking_date', 'ticket', 'class', 'seat', 'price', 'status')
            
            tree = ttk.Treeview(
                table_frame, 
                columns=columns,
                show='headings',
                height=10
            )
            
            # Define headings
            tree.heading('booking_ref', text=self.language_manager.get_text('booking_reference'))
            tree.heading('flight', text=self.language_manager.get_text('flight'))
            tree.heading('route', text=self.language_manager.get_text('route'))
            tree.heading('booking_date', text=self.language_manager.get_text('booking_date'))
            tree.heading('ticket', text=self.language_manager.get_text('ticket_number'))
            tree.heading('class', text=self.language_manager.get_text('seat_class'))
            tree.heading('seat', text=self.language_manager.get_text('seat_number'))
            tree.heading('price', text=self.language_manager.get_text('price'))
            tree.heading('status', text=self.language_manager.get_text('status'))
            
            # Configure columns
            tree.column('booking_ref', width=100)
            tree.column('flight', width=80)
            tree.column('route', width=120)
            tree.column('booking_date', width=100)
            tree.column('ticket', width=100)
            tree.column('class', width=80)
            tree.column('seat', width=60)
            tree.column('price', width=80)
            tree.column('status', width=80)
            
            # Scrollbar
            scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            if self.language_manager.is_rtl():
                scrollbar.pack(side=tk.LEFT, fill=tk.Y)
                tree.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
            else:
                tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Populate bookings
            for booking in bookings:
                booking_values = tuple(booking)
                tree.insert('', tk.END, values=booking_values)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load passenger bookings: {e}")
    
    def add_passenger(self):
        """Open add passenger dialog"""
        add_window = tk.Toplevel(self)
        add_window.title(self.language_manager.get_text('add_passenger'))
        add_window.geometry("500x400")
        
        # Center the window
        self.center_window(add_window)
        
        # Apply RTL to add window
        if self.language_manager.is_rtl():
            self.language_manager.apply_rtl_layout(add_window)
        
        form_frame = tk.Frame(add_window, padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Form title
        title = tk.Label(
            form_frame,
            text=self.language_manager.get_text('add_passenger'),
            font=('Arial', 16, 'bold'),
            fg='#2c3e50'
        )
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Get data for dropdowns
        genders = self.get_genders()
        countries = self.get_countries()
        
        self.passenger_widgets = {}
        current_row = 1
        
        # Passport Number
        passport_label = tk.Label(form_frame, text=self.language_manager.get_text('passport_number') + ":", font=('Arial', 10))
        if self.language_manager.is_rtl():
            passport_label.grid(row=current_row, column=1, sticky='e', pady=10)
        else:
            passport_label.grid(row=current_row, column=0, sticky='w', pady=10)
        
        passport_var = tk.StringVar()
        passport_entry = ttk.Entry(form_frame, textvariable=passport_var, width=25, font=('Arial', 10))
        if self.language_manager.is_rtl():
            passport_entry.grid(row=current_row, column=0, sticky='e', pady=10, padx=(0, 10))
        else:
            passport_entry.grid(row=current_row, column=1, sticky='w', pady=10, padx=(10, 0))
        self.passenger_widgets['passport'] = passport_var
        current_row += 1
        
        # Name
        name_label = tk.Label(form_frame, text=self.language_manager.get_text('passenger_name') + ":", font=('Arial', 10))
        if self.language_manager.is_rtl():
            name_label.grid(row=current_row, column=1, sticky='e', pady=10)
        else:
            name_label.grid(row=current_row, column=0, sticky='w', pady=10)
        
        name_var = tk.StringVar()
        name_entry = ttk.Entry(form_frame, textvariable=name_var, width=25, font=('Arial', 10))
        if self.language_manager.is_rtl():
            name_entry.grid(row=current_row, column=0, sticky='e', pady=10, padx=(0, 10))
        else:
            name_entry.grid(row=current_row, column=1, sticky='w', pady=10, padx=(10, 0))
        self.passenger_widgets['name'] = name_var
        current_row += 1
        
        # Gender
        gender_label = tk.Label(form_frame, text=self.language_manager.get_text('gender') + ":", font=('Arial', 10))
        if self.language_manager.is_rtl():
            gender_label.grid(row=current_row, column=1, sticky='e', pady=10)
        else:
            gender_label.grid(row=current_row, column=0, sticky='w', pady=10)
        
        gender_var = tk.StringVar()
        gender_cb = ttk.Combobox(
            form_frame,
            values=[g['name'] for g in genders],
            textvariable=gender_var,
            state='readonly',
            width=23,
            font=('Arial', 10)
        )
        if self.language_manager.is_rtl():
            gender_cb.grid(row=current_row, column=0, sticky='e', pady=10, padx=(0, 10))
        else:
            gender_cb.grid(row=current_row, column=1, sticky='w', pady=10, padx=(10, 0))
        if genders:
            gender_cb.set(genders[0]['name'])
        self.passenger_widgets['gender'] = {
            'widget': gender_cb,
            'var': gender_var,
            'data': genders
        }
        current_row += 1
        
        # Nationality
        nationality_label = tk.Label(form_frame, text=self.language_manager.get_text('nationality') + ":", font=('Arial', 10))
        if self.language_manager.is_rtl():
            nationality_label.grid(row=current_row, column=1, sticky='e', pady=10)
        else:
            nationality_label.grid(row=current_row, column=0, sticky='w', pady=10)
        
        nationality_var = tk.StringVar()
        nationality_cb = ttk.Combobox(
            form_frame,
            values=[c['name'] for c in countries],
            textvariable=nationality_var,
            state='readonly',
            width=23,
            font=('Arial', 10)
        )
        if self.language_manager.is_rtl():
            nationality_cb.grid(row=current_row, column=0, sticky='e', pady=10, padx=(0, 10))
        else:
            nationality_cb.grid(row=current_row, column=1, sticky='w', pady=10, padx=(10, 0))
        if countries:
            nationality_cb.set(countries[0]['name'])
        self.passenger_widgets['nationality'] = {
            'widget': nationality_cb,
            'var': nationality_var,
            'data': countries
        }
        current_row += 1
        
        # Validation message
        validation_msg = tk.Label(
            form_frame,
            text="",
            font=('Arial', 9),
            foreground='red',
            wraplength=400
        )
        validation_msg.grid(row=current_row, column=0, columnspan=2, pady=10)
        self.passenger_widgets['validation'] = validation_msg
        current_row += 1
        
        # Buttons
        button_frame = tk.Frame(form_frame)
        button_frame.grid(row=current_row, column=0, columnspan=2, pady=20)
        
        save_btn = ttk.Button(
            button_frame,
            text=self.language_manager.get_text('save_passenger'),
            command=lambda: self.save_passenger(add_window),
            width=15
        )
        save_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = ttk.Button(
            button_frame,
            text=self.language_manager.get_text('cancel'),
            command=add_window.destroy,
            width=15
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def edit_passenger(self, passenger_data):
        """Open edit passenger dialog"""
        edit_window = tk.Toplevel(self)
        edit_window.title(self.language_manager.get_text('edit_passenger'))
        edit_window.geometry("500x400")
        
        # Center the window
        self.center_window(edit_window)
        
        # Apply RTL to edit window
        if self.language_manager.is_rtl():
            self.language_manager.apply_rtl_layout(edit_window)
        
        form_frame = tk.Frame(edit_window, padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Form title
        title = tk.Label(
            form_frame,
            text=self.language_manager.get_text('edit_passenger'),
            font=('Arial', 16, 'bold'),
            fg='#2c3e50'
        )
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Get data for dropdowns
        genders = self.get_genders()
        countries = self.get_countries()
        
        self.passenger_widgets = {}
        current_row = 1
        
        # Passport Number (read-only for editing)
        passport_label = tk.Label(form_frame, text=self.language_manager.get_text('passport_number') + ":", font=('Arial', 10))
        if self.language_manager.is_rtl():
            passport_label.grid(row=current_row, column=1, sticky='e', pady=10)
        else:
            passport_label.grid(row=current_row, column=0, sticky='w', pady=10)
        
        passport_var = tk.StringVar(value=passenger_data[1])
        passport_entry = ttk.Entry(form_frame, textvariable=passport_var, width=25, font=('Arial', 10), state='readonly')
        if self.language_manager.is_rtl():
            passport_entry.grid(row=current_row, column=0, sticky='e', pady=10, padx=(0, 10))
        else:
            passport_entry.grid(row=current_row, column=1, sticky='w', pady=10, padx=(10, 0))
        self.passenger_widgets['passport'] = passport_var
        self.passenger_widgets['passenger_id'] = passenger_data[0]
        current_row += 1
        
        # Name
        name_label = tk.Label(form_frame, text=self.language_manager.get_text('passenger_name') + ":", font=('Arial', 10))
        if self.language_manager.is_rtl():
            name_label.grid(row=current_row, column=1, sticky='e', pady=10)
        else:
            name_label.grid(row=current_row, column=0, sticky='w', pady=10)
        
        name_var = tk.StringVar(value=passenger_data[2])
        name_entry = ttk.Entry(form_frame, textvariable=name_var, width=25, font=('Arial', 10))
        if self.language_manager.is_rtl():
            name_entry.grid(row=current_row, column=0, sticky='e', pady=10, padx=(0, 10))
        else:
            name_entry.grid(row=current_row, column=1, sticky='w', pady=10, padx=(10, 0))
        self.passenger_widgets['name'] = name_var
        current_row += 1
        
        # Gender
        gender_label = tk.Label(form_frame, text=self.language_manager.get_text('gender') + ":", font=('Arial', 10))
        if self.language_manager.is_rtl():
            gender_label.grid(row=current_row, column=1, sticky='e', pady=10)
        else:
            gender_label.grid(row=current_row, column=0, sticky='w', pady=10)
        
        gender_var = tk.StringVar(value=passenger_data[3])
        gender_cb = ttk.Combobox(
            form_frame,
            values=[g['name'] for g in genders],
            textvariable=gender_var,
            state='readonly',
            width=23,
            font=('Arial', 10)
        )
        if self.language_manager.is_rtl():
            gender_cb.grid(row=current_row, column=0, sticky='e', pady=10, padx=(0, 10))
        else:
            gender_cb.grid(row=current_row, column=1, sticky='w', pady=10, padx=(10, 0))
        self.passenger_widgets['gender'] = {
            'widget': gender_cb,
            'var': gender_var,
            'data': genders
        }
        current_row += 1
        
        # Nationality
        nationality_label = tk.Label(form_frame, text=self.language_manager.get_text('nationality') + ":", font=('Arial', 10))
        if self.language_manager.is_rtl():
            nationality_label.grid(row=current_row, column=1, sticky='e', pady=10)
        else:
            nationality_label.grid(row=current_row, column=0, sticky='w', pady=10)
        
        nationality_var = tk.StringVar(value=passenger_data[4])
        nationality_cb = ttk.Combobox(
            form_frame,
            values=[c['name'] for c in countries],
            textvariable=nationality_var,
            state='readonly',
            width=23,
            font=('Arial', 10)
        )
        if self.language_manager.is_rtl():
            nationality_cb.grid(row=current_row, column=0, sticky='e', pady=10, padx=(0, 10))
        else:
            nationality_cb.grid(row=current_row, column=1, sticky='w', pady=10, padx=(10, 0))
        self.passenger_widgets['nationality'] = {
            'widget': nationality_cb,
            'var': nationality_var,
            'data': countries
        }
        current_row += 1
        
        # Validation message
        validation_msg = tk.Label(
            form_frame,
            text="",
            font=('Arial', 9),
            foreground='red',
            wraplength=400
        )
        validation_msg.grid(row=current_row, column=0, columnspan=2, pady=10)
        self.passenger_widgets['validation'] = validation_msg
        current_row += 1
        
        # Buttons
        button_frame = tk.Frame(form_frame)
        button_frame.grid(row=current_row, column=0, columnspan=2, pady=20)
        
        update_btn = ttk.Button(
            button_frame,
            text=self.language_manager.get_text('update_passenger'),
            command=lambda: self.update_passenger(edit_window),
            width=15
        )
        update_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = ttk.Button(
            button_frame,
            text=self.language_manager.get_text('cancel'),
            command=edit_window.destroy,
            width=15
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def save_passenger(self, window):
        """Save new passenger to database"""
        try:
            # Get form values
            passport = self.passenger_widgets['passport'].get().strip()
            name = self.passenger_widgets['name'].get().strip()
            gender_name = self.passenger_widgets['gender']['var'].get()
            nationality_name = self.passenger_widgets['nationality']['var'].get()
            
            # Validate all fields
            validation_msg = self.passenger_widgets['validation']
            
            if not all([passport, name, gender_name, nationality_name]):
                validation_msg.config(text=self.language_manager.get_text('all_fields_required'))
                return
            
            # Get gender and country IDs
            gender_id = None
            for gender in self.passenger_widgets['gender']['data']:
                if gender['name'] == gender_name:
                    gender_id = gender['id']
                    break
            
            country_id = None
            for country in self.passenger_widgets['nationality']['data']:
                if country['name'] == nationality_name:
                    country_id = country['id']
                    break
            
            if not gender_id or not country_id:
                validation_msg.config(text=self.language_manager.get_text('invalid_gender_or_country'))
                return
            
            # Save to database
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO passengers 
                (passport_number, name, gender_id, nationality_country_id)
                VALUES (?, ?, ?, ?)
            """, (passport, name, gender_id, country_id))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", self.language_manager.get_text('passenger_saved_success'))
            window.destroy()
            self.load_passengers()  # Refresh the list
            
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                messagebox.showerror("Error", self.language_manager.get_text('passport_already_exists'))
            else:
                messagebox.showerror("Error", f"Failed to save passenger: {e}")
    
    def update_passenger(self, window):
        """Update passenger in database"""
        try:
            # Get form values
            passenger_id = self.passenger_widgets['passenger_id']
            name = self.passenger_widgets['name'].get().strip()
            gender_name = self.passenger_widgets['gender']['var'].get()
            nationality_name = self.passenger_widgets['nationality']['var'].get()
            
            # Validate all fields
            validation_msg = self.passenger_widgets['validation']
            
            if not all([name, gender_name, nationality_name]):
                validation_msg.config(text=self.language_manager.get_text('all_fields_required'))
                return
            
            # Get gender and country IDs
            gender_id = None
            for gender in self.passenger_widgets['gender']['data']:
                if gender['name'] == gender_name:
                    gender_id = gender['id']
                    break
            
            country_id = None
            for country in self.passenger_widgets['nationality']['data']:
                if country['name'] == nationality_name:
                    country_id = country['id']
                    break
            
            if not gender_id or not country_id:
                validation_msg.config(text=self.language_manager.get_text('invalid_gender_or_country'))
                return
            
            # Update database
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE passengers 
                SET name = ?, gender_id = ?, nationality_country_id = ?
                WHERE id = ?
            """, (name, gender_id, country_id, passenger_id))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", self.language_manager.get_text('passenger_updated_success'))
            window.destroy()
            self.load_passengers()  # Refresh the list
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update passenger: {e}")
    
    def get_genders(self):
        """Get list of genders from database"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM genders ORDER BY name")
            genders = []
            for row in cursor.fetchall():
                genders.append({
                    'id': row[0],
                    'name': row[1]
                })
            conn.close()
            return genders
        except Exception as e:
            print(f"Error getting genders: {e}")
            return []
    
    def get_countries(self):
        """Get list of countries from database"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM countries ORDER BY name")
            countries = []
            for row in cursor.fetchall():
                countries.append({
                    'id': row[0],
                    'name': row[1]
                })
            conn.close()
            return countries
        except Exception as e:
            print(f"Error getting countries: {e}")
            return []
    
    def center_window(self, window):
        """Center a window on the screen"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))