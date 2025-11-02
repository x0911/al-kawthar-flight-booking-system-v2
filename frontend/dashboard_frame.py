# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk


class DashboardFrame(tk.Frame):
    def __init__(self, parent, user_data, logout_callback):
        super().__init__(parent)
        self.user_data = user_data
        self.logout_callback = logout_callback
        self.setup_ui()
        
    def setup_ui(self):
        """Create dashboard interface"""
        self.configure(bg='#f8f9fa')
        
        # Header
        header_frame = tk.Frame(self, bg='#2c3e50', height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # App title and user info
        title_label = tk.Label(
            header_frame,
            text="Al Kawthar Flights - Management System",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        user_label = tk.Label(
            header_frame,
            text=f"Welcome, {self.user_data['username']}",
            font=('Arial', 11),
            fg='white',
            bg='#2c3e50'
        )
        user_label.pack(side=tk.RIGHT, padx=20, pady=20)
        
        # Main content area
        main_container = tk.Frame(self, bg='#f8f9fa')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left sidebar - Navigation
        sidebar = tk.Frame(main_container, bg='#34495e', width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        sidebar.pack_propagate(False)
        
        # Navigation buttons
        nav_buttons = [
            ("📊 Dashboard", self.show_dashboard),
            ("🛫 Flights", self.show_flights),
            ("🎫 Bookings", self.show_bookings),
            ("👥 Passengers", self.show_passengers),
            ("📈 Reports", self.show_reports)
        ]
        
        for text, command in nav_buttons:
            btn = tk.Button(
                sidebar,
                text=text,
                font=('Arial', 11),
                fg='white',
                bg='#34495e',
                relief='flat',
                anchor='w',
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
            text="🚪 Logout",
            font=('Arial', 11),
            fg='white',
            bg='#e74c3c',
            relief='flat',
            anchor='w',
            command=self.logout,
            padx=20,
            pady=15
        )
        logout_btn.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Right content area
        self.content_frame = tk.Frame(main_container, bg='white', relief='solid', bd=1)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Show default dashboard content
        self.show_dashboard_content()
        
    def show_dashboard_content(self):
        """Display dashboard content"""
        self.clear_content()
        
        # Dashboard title
        title = tk.Label(
            self.content_frame,
            text="Dashboard Overview",
            font=('Arial', 18, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title.pack(pady=20)
        
        # Stats cards
        stats_frame = tk.Frame(self.content_frame, bg='white')
        stats_frame.pack(pady=10, padx=20, fill=tk.X)
        
        stats_data = [
            ("Total Flights", "24", "#3498db"),
            ("Active Bookings", "156", "#2ecc71"),
            ("Today's Passengers", "42", "#e74c3c"),
            ("Revenue", "$12,450", "#f39c12")
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
            text="Recent Activity",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='#2c3e50',
            anchor='w'
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
                anchor='w'
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
      flights_frame = FlightsFrame(self.content_frame)
      flights_frame.pack(fill=tk.BOTH, expand=True)
    
    def show_bookings(self):
        """Show bookings management view"""
        self.clear_content()
        
        # Use the actual BookingsFrame instead of placeholder
        from frontend.bookings_frame import BookingsFrame
        bookings_frame = BookingsFrame(self.content_frame)
        bookings_frame.pack(fill=tk.BOTH, expand=True)
    
    def show_passengers(self):
        """Show passengers management view"""
        self.clear_content()
        
        title = tk.Label(
            self.content_frame,
            text="Passengers Management",
            font=('Arial', 18, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title.pack(pady=20)
        
        # Placeholder for passengers content
        placeholder = tk.Label(
            self.content_frame,
            text="Passengers management system will be implemented here\n\n"
                 "Features:\n"
                 "• View passenger list\n"
                 "• Register new passengers\n"
                 "• Update passenger information\n"
                 "• View passenger history",
            font=('Arial', 12),
            bg='white',
            fg='#7f8c8d',
            justify=tk.LEFT
        )
        placeholder.pack(expand=True)
    
    def show_reports(self):
        """Show reports view"""
        self.clear_content()
        
        title = tk.Label(
            self.content_frame,
            text="Reports & Analytics",
            font=('Arial', 18, 'bold'),
            bg='white',
            fg='#2c3e50'
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
            justify=tk.LEFT
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
        # This frame doesn't have any special cleanup needs,
        # but we include the method for consistency
        pass