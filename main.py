# -*- coding: utf-8 -*-
import tkinter as tk
import os
from frontend.main_window import MainWindow
from frontend.fonts import FontManager

# Global font manager instance
font_manager = None

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
        
        # Initialize font manager (global access)
        global font_manager
        font_manager = FontManager(root)
        
        # Set app icon
        set_app_icon(root)
        
        # Set default font for the entire application
        root.option_add('*Font', font_manager.body_medium)
        
        # Configure ttk styles
        configure_styles(root)
        
        app = MainWindow(root)
        root.mainloop()
        
    except Exception as e:
        print(f"Failed to start application: {e}")
        input("Press Enter to exit...")

def configure_styles(root):
    """Configure ttk styles with current font"""
    global font_manager
    style = tk.ttk.Style()
    style.configure('TButton', font=font_manager.button_medium)
    style.configure('TLabel', font=font_manager.label_normal)
    style.configure('TEntry', font=font_manager.input_text)
    style.configure('TCombobox', font=font_manager.input_text)

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