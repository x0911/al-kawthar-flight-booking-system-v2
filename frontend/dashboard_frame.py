# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk


class DashboardFrame(tk.Frame):
    def __init__(self, parent, user_data, logout_callback, language_manager):
        super().__init__(parent)
        self.user_data = user_data
        self.logout_callback = logout_callback
        self.language_manager = language_manager
        self.setup_ui()
        
    def setup_ui(self):
        """Create dashboard interface"""
        self.configure(bg='#f8f9fa')
        
        # Apply RTL layout if Arabic
        if self.language_manager.is_rtl():
            self.apply_rtl_layout()
        
        # Header
        header_frame = tk.Frame(self, bg='#2c3e50', height=80)
        if self.language_manager.is_rtl():
            header_frame.pack(fill=tk.X, padx=0, pady=0, side=tk.TOP, anchor='ne')
        else:
            header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # App title and user info
        title_label = tk.Label(
            header_frame,
            text=self.language_manager.get_text('app_title') + " - Management System",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        if self.language_manager.is_rtl():
            title_label.pack(side=tk.RIGHT, padx=20, pady=20)
        else:
            title_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        user_label = tk.Label(
            header_frame,
            text=self.language_manager.get_text('welcome', self.user_data['username']),
            font=('Arial', 11),
            fg='white',
            bg='#2c3e50'
        )
        if self.language_manager.is_rtl():
            user_label.pack(side=tk.LEFT, padx=20, pady=20)
        else:
            user_label.pack(side=tk.RIGHT, padx=20, pady=20)
        
        # Language selector in header
        # self.create_header_language_selector(header_frame)
        
        # Main content area
        main_container = tk.Frame(self, bg='#f8f9fa')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left sidebar - Navigation
        sidebar = tk.Frame(main_container, bg='#34495e', width=200)
        if self.language_manager.is_rtl():
            sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        else:
            sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        sidebar.pack_propagate(False)
        
        # Navigation buttons
        nav_buttons = [
            (self.language_manager.get_text('dashboard'), self.show_dashboard),
            (self.language_manager.get_text('flights'), self.show_flights),
            (self.language_manager.get_text('bookings'), self.show_bookings),
            (self.language_manager.get_text('passengers'), self.show_passengers),
            (self.language_manager.get_text('reports'), self.show_reports)
        ]
        
        for text, command in nav_buttons:
            btn = tk.Button(
                sidebar,
                text=text,
                font=('Arial', 11),
                fg='white',
                bg='#34495e',
                relief='flat',
                anchor='w' if not self.language_manager.is_rtl() else 'e',
                command=command,
                padx=20,
                pady=15
            )
            btn.pack(fill=tk.X)
            
            # Add hover effect
            def on_enter(e, button=btn):
                button.configure(bg='#3498db')
                
            def on_leave(e, button=btn):
                button.configure(bg='#34495e')
                
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
        
        # Logout button at bottom of sidebar
        logout_btn = tk.Button(
            sidebar,
            text=self.language_manager.get_text('logout'),
            font=('Arial', 11),
            fg='white',
            bg='#e74c3c',
            relief='flat',
            anchor='w' if not self.language_manager.is_rtl() else 'e',
            command=self.logout,
            padx=20,
            pady=15
        )
        logout_btn.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Right content area
        self.content_frame = tk.Frame(main_container, bg='white', relief='solid', bd=1)
        if self.language_manager.is_rtl():
            self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        else:
            self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Apply RTL to all widgets
        self.language_manager.apply_rtl_layout(self)
        
        # Show default dashboard content
        self.show_dashboard_content()
        
    def apply_rtl_layout(self):
        """Apply RTL specific layout changes"""
        # Configure the main frame for RTL
        pass
        
    def create_header_language_selector(self, header_frame):
        """Create language selector in header"""
        lang_frame = tk.Frame(header_frame, bg='#2c3e50')
        if self.language_manager.is_rtl():
            lang_frame.pack(side=tk.LEFT, padx=10, pady=20)
        else:
            lang_frame.pack(side=tk.RIGHT, padx=10, pady=20)
        
        lang_var = tk.StringVar(value=self.language_manager.current_language)
        lang_cb = ttk.Combobox(
            lang_frame,
            values=['english', 'arabic'],
            textvariable=lang_var,
            state='readonly',
            width=10,
            font=('Arial', 9)
        )
        lang_cb.pack()
        
        lang_cb.bind('<<ComboboxSelected>>', 
                    lambda e: self.change_language(lang_var.get()))
        
    def change_language(self, language):
        """Change application language"""
        if self.language_manager.set_language(language):
            # Update UI texts without recreating the entire interface
            self.update_ui_texts()
        
    def update_ui_texts(self):
        """Update all UI texts with current language"""
        try:
            # Update header texts
            for widget in self.winfo_children():
                if isinstance(widget, tk.Frame) and widget.cget('bg') == '#2c3e50':  # Header frame
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Label):
                            current_text = child.cget('text')
                            if 'Al Kawthar' in current_text or 'طيران الكوثر' in current_text:
                                child.config(text=self.language_manager.get_text('app_title') + " - Management System")
                            elif 'Welcome' in current_text or 'أهلاً بك' in current_text:
                                child.config(text=self.language_manager.get_text('welcome', self.user_data['username']))
            
            # Update navigation buttons
            self.update_navigation_texts()
            
            # Update content area based on current view
            self.update_content_texts()
            
            # Apply RTL layout changes
            if self.language_manager.is_rtl():
                self.apply_rtl_layout()
            self.language_manager.apply_rtl_layout(self)
            
        except Exception as e:
            print(f"Error updating dashboard UI texts: {e}")
            # Fallback: recreate the UI
            self.destroy_ui()
            self.setup_ui()
    
    def update_navigation_texts(self):
        """Update navigation button texts"""
        # Find sidebar frame
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame) and widget.cget('bg') == '#f8f9fa':  # Main container
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame) and child.cget('bg') == '#34495e':  # Sidebar
                        # Get all buttons in sidebar (excluding logout button)
                        buttons = [w for w in child.winfo_children() if isinstance(w, tk.Button) and w.cget('bg') != '#e74c3c']
                        logout_buttons = [w for w in child.winfo_children() if isinstance(w, tk.Button) and w.cget('bg') == '#e74c3c']
                        
                        # Update navigation buttons in order
                        nav_texts = [
                            self.language_manager.get_text('dashboard'),
                            self.language_manager.get_text('flights'),
                            self.language_manager.get_text('bookings'),
                            self.language_manager.get_text('passengers'),
                            self.language_manager.get_text('reports')
                        ]
                        
                        for i, btn in enumerate(buttons):
                            if i < len(nav_texts):
                                btn.config(text=nav_texts[i])
                                # Update anchor for RTL
                                if self.language_manager.is_rtl():
                                    btn.config(anchor='e')
                                else:
                                    btn.config(anchor='w')
                        
                        # Update logout button
                        for logout_btn in logout_buttons:
                            logout_btn.config(text=self.language_manager.get_text('logout'))
                            if self.language_manager.is_rtl():
                                logout_btn.config(anchor='e')
                            else:
                                logout_btn.config(anchor='w')
                        break
    
    def update_content_texts(self):
        """Update content area texts based on current view"""
        if not hasattr(self, 'content_frame'):
            return
        
        # Get the current content frame children
        content_children = self.content_frame.winfo_children()
        if not content_children:
            return
        
        current_content = content_children[0]
        
        # Update based on content type
        if hasattr(current_content, 'update_language'):
            # If the content frame has an update_language method, use it
            current_content.update_language()
        else:
            # Otherwise, try to update common elements
            self.update_common_content_texts(current_content)

    def update_common_content_texts(self, content_widget):
        """Update common content texts"""
        try:
            # Recursively update all labels in content area
            def update_widget_texts(widget):
                if isinstance(widget, tk.Label):
                    current_text = widget.cget('text')
                    # Update common titles
                    if 'Dashboard' in current_text or 'لوحة التحكم' in current_text:
                        widget.config(text=self.language_manager.get_text('dashboard') + " Overview")
                    elif 'Flights Management' in current_text or 'إدارة الرحلات' in current_text:
                        widget.config(text=self.language_manager.get_text('flight_management'))
                    elif 'Bookings Management' in current_text or 'إدارة الحجوزات' in current_text:
                        widget.config(text=self.language_manager.get_text('booking_management'))
                    elif 'Passengers Management' in current_text or 'إدارة المسافرين' in current_text:
                        widget.config(text=self.language_manager.get_text('passengers') + " Management")
                    elif 'Reports & Analytics' in current_text or 'التقارير والتحليلات' in current_text:
                        widget.config(text=self.language_manager.get_text('reports') + " & Analytics")
                    # Update stats cards
                    elif 'Flights' in current_text and 'Overview' not in current_text:
                        widget.config(text=self.language_manager.get_text('flights'))
                    elif 'Bookings' in current_text and 'Management' not in current_text:
                        widget.config(text=self.language_manager.get_text('bookings'))
                    elif "Today's Passengers" in current_text:
                        widget.config(text=self.language_manager.get_text('today_passengers'))
                    elif "Revenue" in current_text:
                        widget.config(text=self.language_manager.get_text('revenue'))
                    elif "Recent Activity" in current_text or "النشاط الأخير" in current_text:
                        widget.config(text=self.language_manager.get_text('recent_activity'))
                    
                    # Update text alignment for RTL
                    if self.language_manager.is_rtl():
                        widget.config(anchor='e', justify='right')
                    else:
                        widget.config(anchor='w', justify='left')
            
            update_widget_texts(content_widget)
            
        except Exception as e:
            print(f"Error updating content texts: {e}")
    
    def destroy_ui(self):
        """Destroy all UI elements before recreation"""
        # Destroy all child widgets
        for widget in self.winfo_children():
            widget.destroy()
        
    def show_dashboard_content(self):
        """Display dashboard content"""
        self.clear_content()
        
        # Dashboard title
        title = tk.Label(
            self.content_frame,
            text=self.language_manager.get_text('dashboard') + " Overview",
            font=('Arial', 18, 'bold'),
            bg='white',
            fg='#2c3e50',
            anchor='w' if not self.language_manager.is_rtl() else 'e'
        )
        title.pack(pady=20)
        
        # Stats cards
        stats_frame = tk.Frame(self.content_frame, bg='white')
        stats_frame.pack(pady=10, padx=20, fill=tk.X)
        
        stats_data = [
            (self.language_manager.get_text('flights'), "24", "#3498db"),
            (self.language_manager.get_text('bookings'), "156", "#2ecc71"),
            (self.language_manager.get_text('today_passengers'), "42", "#e74c3c"),
            (self.language_manager.get_text('revenue'), "$12,450", "#f39c12")
        ]
        
        for i, (label, value, color) in enumerate(stats_data):
            card = tk.Frame(
                stats_frame,
                bg=color,
                relief='raised',
                bd=1,
                width=150,
                height=100
            )
            if self.language_manager.is_rtl():
                card.pack(side=tk.RIGHT, padx=10, pady=10)
            else:
                card.pack(side=tk.LEFT, padx=10, pady=10)
            card.pack_propagate(False)
            
            # Value
            value_label = tk.Label(
                card,
                text=value,
                font=('Arial', 20, 'bold'),
                bg=color,
                fg='white'
            )
            value_label.pack(expand=True)
            
            # Label
            label_label = tk.Label(
                card,
                text=label,
                font=('Arial', 10),
                bg=color,
                fg='white'
            )
            label_label.pack(pady=(0, 10))
        
        # Recent activity section
        activity_frame = tk.Frame(self.content_frame, bg='white')
        activity_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        activity_label = tk.Label(
            activity_frame,
            text=self.language_manager.get_text('recent_activity'),
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='#2c3e50',
            anchor='w' if not self.language_manager.is_rtl() else 'e'
        )
        activity_label.pack(fill=tk.X, pady=(0, 10))
        
        # Sample activity list
        activities = [
            "New booking AK202 - Dubai to Riyadh",
            "Flight AK101 departed on time",
            "New passenger registered",
            "Payment received for booking #AK789",
            "Flight schedule updated"
        ]
        
        for activity in activities:
            activity_item = tk.Label(
                activity_frame,
                text=f"• {activity}",
                font=('Arial', 10),
                bg='white',
                fg='#7f8c8d',
                anchor='w' if not self.language_manager.is_rtl() else 'e',
                justify='left' if not self.language_manager.is_rtl() else 'right'
            )
            activity_item.pack(fill=tk.X, pady=2)
    
    def show_dashboard(self):
        """Show dashboard view"""
        self.show_dashboard_content()
    
    def show_flights(self):
        """Show flights management view"""
        self.clear_content()
        
        # Use the actual FlightsFrame instead of placeholder
        from frontend.flights_frame import FlightsFrame
        flights_frame = FlightsFrame(self.content_frame, self.language_manager)
        flights_frame.pack(fill=tk.BOTH, expand=True)
    
    def show_bookings(self):
        """Show bookings management view"""
        self.clear_content()
        
        # Use the actual BookingsFrame instead of placeholder
        from frontend.bookings_frame import BookingsFrame
        bookings_frame = BookingsFrame(self.content_frame, self.language_manager)
        bookings_frame.pack(fill=tk.BOTH, expand=True)
    
    def show_passengers(self):
        """Show passengers management view"""
        self.clear_content()
        
        # Use the actual PassengersFrame instead of placeholder
        from frontend.passengers_frame import PassengersFrame
        passengers_frame = PassengersFrame(self.content_frame, self.language_manager)
        passengers_frame.pack(fill=tk.BOTH, expand=True)
    
    def show_reports(self):
        """Show reports view"""
        self.clear_content()
        
        title = tk.Label(
            self.content_frame,
            text=self.language_manager.get_text('reports') + " & Analytics",
            font=('Arial', 18, 'bold'),
            bg='white',
            fg='#2c3e50',
            anchor='w' if not self.language_manager.is_rtl() else 'e'
        )
        title.pack(pady=20)
        
        # Placeholder for reports content
        placeholder = tk.Label(
            self.content_frame,
            text="Reports and analytics will be implemented here\n\n"
                 "Features:\n"
                 "• Revenue reports\n"
                 "• Flight performance\n"
                 "• Passenger statistics\n"
                 "• Booking trends",
            font=('Arial', 12),
            bg='white',
            fg='#7f8c8d',
            justify='left' if not self.language_manager.is_rtl() else 'right'
        )
        placeholder.pack(expand=True)
    
    def clear_content(self):
        """Clear the content area"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def logout(self):
        """Handle logout"""
        self.logout_callback()
        
    def cleanup(self):
        """Clean up resources when frame is destroyed"""
        pass