# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox, ttk

from frontend.dashboard_frame import DashboardFrame
from frontend.login_frame import LoginFrame


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.current_frame = None
        self.setup_window()
        self.show_login()
        
    def setup_window(self):
        """Configure the main window"""
        self.root.title("Al Kawthar Flights Management System")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Center the window on screen
        self.root.eval('tk::PlaceWindow . center')
        
    def show_login(self):
        """Show login screen"""
        self.clear_window()
        self.current_frame = LoginFrame(self.root, self.login_successful)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
    def show_dashboard(self, user_data):
        """Show main dashboard after successful login"""
        self.clear_window()
        self.current_frame = DashboardFrame(self.root, user_data, self.logout)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def login_successful(self, user_data):
        """Callback for successful login"""
        self.show_dashboard(user_data)
        
    def logout(self):
        """Logout and return to login screen"""
        self.show_login()
        
    def clear_window(self):
        """Clear all widgets from window"""
        # Safely cleanup current frame if it has a cleanup method
        if self.current_frame and hasattr(self.current_frame, 'cleanup'):
            try:
                self.current_frame.cleanup()
            except Exception as e:
                print(f"Cleanup error (ignored): {e}")
        
        # Clear all widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.current_frame = None