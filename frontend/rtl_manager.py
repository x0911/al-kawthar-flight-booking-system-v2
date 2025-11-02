# -*- coding: utf-8 -*-
# frontend/rtl_manager.py

import tkinter as tk
from tkinter import ttk

class RTLManager:
    @staticmethod
    def configure_rtl_layout(widget, language):
        """Configure RTL layout for Arabic language"""
        if language == 'arabic':
            # For containers, change packing direction
            if isinstance(widget, (tk.Frame, tk.LabelFrame)):
                # This will affect how children are packed
                pass
            
    @staticmethod
    def apply_rtl_to_frame(frame, language):
        """Apply RTL layout to a frame and its children"""
        if language != 'arabic':
            return
            
        try:
            # Recursively apply RTL to all widgets
            for widget in frame.winfo_children():
                RTLManager.apply_rtl_to_widget(widget, language)
                RTLManager.apply_rtl_to_frame(widget, language)  # Recursive call for containers
        except:
            pass
    
    @staticmethod
    def apply_rtl_to_widget(widget, language):
        """Apply RTL settings to individual widget"""
        if language != 'arabic':
            return
            
        try:
            if isinstance(widget, (tk.Label, tk.Button)):
                # Change text alignment to right
                widget.config(anchor='e', justify='right')
            elif isinstance(widget, ttk.Entry):
                # Change text alignment to right
                widget.config(justify='right')
            elif isinstance(widget, ttk.Combobox):
                # Change text alignment to right
                widget.config(justify='right')
            elif isinstance(widget, ttk.Treeview):
                # Change column alignment to right
                for col in widget['columns']:
                    widget.heading(col, anchor='e')
        except:
            pass