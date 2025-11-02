# -*- coding: utf-8 -*-
import os
import tempfile

def set_window_icon(window):
    """Set the application icon for any window"""
    try:
        icon_paths = [
            'images/icon.ico',
            'icon.ico',
            'frontend/images/icon.ico',
            'backend/images/icon.ico',
        ]
        
        for icon_path in icon_paths:
            if os.path.exists(icon_path):
                window.iconbitmap(icon_path)
                return
        
        # Check for generated icon
        temp_dir = tempfile.gettempdir()
        generated_icon = os.path.join(temp_dir, 'al_kawthar_icon.ico')
        if os.path.exists(generated_icon):
            window.iconbitmap(generated_icon)
            
    except Exception as e:
        print(f"Could not set window icon: {e}")