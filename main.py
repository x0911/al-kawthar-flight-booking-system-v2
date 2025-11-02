# -*- coding: utf-8 -*-
import tkinter as tk
import os
from frontend.main_window import MainWindow

def main():
    """Main application entry point"""
    try:
        # Initialize database
        from backend.database import initialize_database
        from backend.seeder import insert_sample_data

        initialize_database()
        insert_sample_data()
        
        # Create and run the application
        root = tk.Tk()
        
        # Set app icon
        set_app_icon(root)
        
        app = MainWindow(root)
        root.mainloop()
        
    except Exception as e:
        print(f"Failed to start application: {e}")
        input("Press Enter to exit...")

def set_app_icon(root):
    """Set the application icon"""
    try:
        icon_paths = ['images/icon.ico', 'icon.ico']
        for path in icon_paths:
            if os.path.exists(path):
                root.iconbitmap(path)
                print(f"✅ App icon set: {path}")
                return
        print("⚠️ No icon file found")
    except Exception as e:
        print(f"⚠️ Could not set app icon: {e}")

if __name__ == "__main__":
    main()