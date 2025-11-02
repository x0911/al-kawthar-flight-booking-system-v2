# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox, ttk


class LoginFrame(tk.Frame):
    def __init__(self, parent, login_callback, language_manager):
        super().__init__(parent)
        self.login_callback = login_callback
        self.language_manager = language_manager
        self.setup_ui()
        
    def setup_ui(self):
        """Create login interface"""
        self.configure(bg='#ffffff')
        
        # Main container
        container = tk.Frame(self, bg='#ffffff', padx=40, pady=40)
        container.pack(expand=True)
        
        # Title
        title_label = tk.Label(
            container, 
            text=self.language_manager.get_text('app_title'), 
            font=('Arial', 24, 'bold'),
            fg='#2c3e50',
            bg='#ffffff'
        )
        title_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(
            container,
            text=self.language_manager.get_text('login_title'),
            font=('Arial', 14),
            fg='#7f8c8d',
            bg='#ffffff'
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Login form
        form_frame = tk.Frame(container, bg='#ffffff')
        form_frame.pack(pady=20)
        
        # Username
        tk.Label(form_frame, text=self.language_manager.get_text('username'), font=('Arial', 11), 
                bg='#ffffff', fg='#2c3e50').grid(row=0, column=0, sticky='w', pady=5)
        self.username_entry = ttk.Entry(form_frame, font=('Arial', 11), width=25)
        self.username_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # Password
        tk.Label(form_frame, text=self.language_manager.get_text('password'), font=('Arial', 11), 
                bg='#ffffff', fg='#2c3e50').grid(row=1, column=0, sticky='w', pady=5)
        self.password_entry = ttk.Entry(form_frame, show='*', font=('Arial', 11), width=25)
        self.password_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # Login button
        login_btn = ttk.Button(
            container,
            text=self.language_manager.get_text('login_button'),
            command=self.attempt_login,
            width=20
        )
        login_btn.pack(pady=20)
        
        # Demo credentials note
        demo_label = tk.Label(
            container,
            text=self.language_manager.get_text('demo_credentials'),
            font=('Arial', 9),
            fg='#95a5a6',
            bg='#ffffff'
        )
        demo_label.pack(pady=(10, 0))
        
        # Language selector
        self.create_language_selector(container)
        
        # Bind Enter key to login - but only for these specific widgets
        self.username_entry.bind('<Return>', lambda e: self.attempt_login())
        self.password_entry.bind('<Return>', lambda e: self.attempt_login())
        
    def create_language_selector(self, parent):
        """Create language selection dropdown"""
        lang_frame = tk.Frame(parent, bg='#ffffff')
        lang_frame.pack(pady=(20, 0))
        
        tk.Label(lang_frame, text="Language / اللغة:", 
                font=('Arial', 9),
                bg='#ffffff', fg='#666').pack(side=tk.LEFT)
        
        lang_var = tk.StringVar(value=self.language_manager.current_language)
        lang_cb = ttk.Combobox(
            lang_frame,
            values=['english', 'arabic'],
            textvariable=lang_var,
            state='readonly',
            width=10,
            font=('Arial', 9)
        )
        lang_cb.pack(side=tk.LEFT, padx=5)
        
        lang_cb.bind('<<ComboboxSelected>>', 
                    lambda e: self.change_language(lang_var.get()))
        
    def change_language(self, language):
        """Change application language"""
        if self.language_manager.set_language(language):
            # Recreate the UI with new language
            self.setup_ui()
        
    def attempt_login(self):
        """Attempt to login user"""
        try:
            username = self.username_entry.get().strip()
            password = self.password_entry.get().strip()
            
            if not username or not password:
                messagebox.showwarning("Input Error", "Please enter both username and password")
                return
                
            # For demo purposes, accept any non-empty credentials
            user_data = {
                'username': username,
                'is_admin': True  # Demo admin access
            }
            
            self.login_callback(user_data)
            
        except Exception as e:
            # Handle the case where widgets might not exist anymore
            print(f"Login attempt error: {e}")
            
    def cleanup(self):
        """Clean up bindings when frame is destroyed"""
        try:
            self.username_entry.unbind('<Return>')
            self.password_entry.unbind('<Return>')
        except:
            pass  # Widgets might already be destroyed