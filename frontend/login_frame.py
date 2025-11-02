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
        
        # Apply RTL layout if Arabic
        if self.language_manager.is_rtl():
            self.apply_rtl_layout()
        
        # Main container
        container = tk.Frame(self, bg='#ffffff', padx=40, pady=40)
        container.pack(expand=True)
        
        # Title
        title_label = tk.Label(
            container, 
            text=self.language_manager.get_text('app_title'), 
            font=('Arial', 24, 'bold'),
            fg='#2c3e50',
            bg='#ffffff',
            anchor='center'
        )
        title_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(
            container,
            text=self.language_manager.get_text('login_title'),
            font=('Arial', 14),
            fg='#7f8c8d',
            bg='#ffffff',
            anchor='center'
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Login form
        form_frame = tk.Frame(container, bg='#ffffff')
        form_frame.pack(pady=20)
        
        # Username
        username_label = tk.Label(form_frame, text=self.language_manager.get_text('username'), font=('Arial', 11), 
                bg='#ffffff', fg='#2c3e50')
        username_label.grid(row=0, column=0, sticky='w' if not self.language_manager.is_rtl() else 'e', pady=5)
        
        self.username_entry = ttk.Entry(form_frame, font=('Arial', 11), width=25)
        self.username_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # Password
        password_label = tk.Label(form_frame, text=self.language_manager.get_text('password'), font=('Arial', 11), 
                bg='#ffffff', fg='#2c3e50')
        password_label.grid(row=1, column=0, sticky='w' if not self.language_manager.is_rtl() else 'e', pady=5)
        
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
            bg='#ffffff',
            anchor='center'
        )
        demo_label.pack(pady=(10, 0))
        
        # Language selector
        self.create_language_selector(container)
        
        # Apply RTL to all widgets
        self.language_manager.apply_rtl_layout(self)
        
        # Bind Enter key to login - but only for these specific widgets
        self.username_entry.bind('<Return>', lambda e: self.attempt_login())
        self.password_entry.bind('<Return>', lambda e: self.attempt_login())
        
    def apply_rtl_layout(self):
        """Apply RTL specific layout changes"""
        # For RTL, we might want to adjust the overall layout
        pass
        
    def create_language_selector(self, parent):
        """Create language selection dropdown"""
        lang_frame = tk.Frame(parent, bg='#ffffff')
        lang_frame.pack(pady=(20, 0))
        
        lang_label = tk.Label(lang_frame, text="Language / اللغة:", 
                font=('Arial', 9),
                bg='#ffffff', fg='#666')
        
        if self.language_manager.is_rtl():
            lang_label.pack(side=tk.RIGHT)
        else:
            lang_label.pack(side=tk.LEFT)
        
        lang_var = tk.StringVar(value=self.language_manager.current_language)
        lang_cb = ttk.Combobox(
            lang_frame,
            values=['english', 'arabic'],
            textvariable=lang_var,
            state='readonly',
            width=10,
            font=('Arial', 9)
        )
        
        if self.language_manager.is_rtl():
            lang_cb.pack(side=tk.RIGHT, padx=5)
        else:
            lang_cb.pack(side=tk.LEFT, padx=5)
        
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
            # Update all labels and buttons
            for widget in self.winfo_children():
                self.update_widget_texts(widget)
            
            # Apply RTL layout changes
            if self.language_manager.is_rtl():
                self.apply_rtl_layout()
            self.language_manager.apply_rtl_layout(self)
            
            # Update form labels alignment
            self.update_form_alignment()
                
        except Exception as e:
            print(f"Error updating login UI texts: {e}")
            # Fallback: recreate the UI
            self.destroy_ui()
            self.setup_ui()
    
    def update_form_alignment(self):
        """Update form labels alignment for RTL/LTR"""
        # Find the form frame and update label alignment
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame):  # This should be the form frame
                        for form_child in child.winfo_children():
                            if isinstance(form_child, tk.Label):
                                if self.language_manager.is_rtl():
                                    form_child.config(anchor='e')
                                else:
                                    form_child.config(anchor='w')
    
    def update_widget_texts(self, widget):
        """Recursively update widget texts"""
        try:
            # Update labels
            if isinstance(widget, tk.Label):
                current_text = widget.cget('text')
                
                # Map current text to translation keys
                text_mapping = {
                    'Al Kawthar Flights': self.language_manager.get_text('app_title'),
                    'طيران الكوثر': self.language_manager.get_text('app_title'),
                    'Management System Login': self.language_manager.get_text('login_title'),
                    'نظام إدارة التسجيل': self.language_manager.get_text('login_title'),
                    'Username': self.language_manager.get_text('username'),
                    'اسم المستخدم': self.language_manager.get_text('username'),
                    'Password': self.language_manager.get_text('password'),
                    'كلمة المرور': self.language_manager.get_text('password'),
                    'Login': self.language_manager.get_text('login_button'),
                    'تسجيل الدخول': self.language_manager.get_text('login_button'),
                    'For demo: Use any credentials': self.language_manager.get_text('demo_credentials'),
                    'للتجربة: استخدم أي بيانات دخول': self.language_manager.get_text('demo_credentials'),
                    'Language / اللغة:': 'Language / اللغة:'
                }
                
                if current_text in text_mapping:
                    widget.config(text=text_mapping[current_text])
                
                # Update text alignment for RTL
                if self.language_manager.is_rtl():
                    if widget.cget('anchor') != 'center':  # Don't change centered titles
                        widget.config(anchor='e', justify='right')
                else:
                    if widget.cget('anchor') != 'center':
                        widget.config(anchor='w', justify='left')
            
            # Update buttons
            elif isinstance(widget, ttk.Button):
                current_text = widget.cget('text')
                if current_text in ['Login', 'تسجيل الدخول']:
                    widget.config(text=self.language_manager.get_text('login_button'))
            
            # Update combobox
            elif isinstance(widget, ttk.Combobox):
                if self.language_manager.is_rtl():
                    widget.config(justify='right')
                else:
                    widget.config(justify='left')
            
            # Recursively check children
            for child in widget.winfo_children():
                self.update_widget_texts(child)
                
        except Exception as e:
            # Ignore errors for widgets that might be destroyed
            pass
        
    def destroy_ui(self):
        """Destroy all UI elements before recreation"""
        # Unbind events first
        self.cleanup()
        
        # Destroy all child widgets
        for widget in self.winfo_children():
            widget.destroy()
        
    def attempt_login(self):
        """Attempt to login user"""
        try:
            username = self.username_entry.get().strip()
            password = self.password_entry.get().strip()
            
            if not username or not password:
                # Use translated message for input error
                if self.language_manager.is_rtl():
                    messagebox.showwarning("خطأ في الإدخال", "الرجاء إدخال اسم المستخدم وكلمة المرور")
                else:
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
            if hasattr(self, 'username_entry'):
                self.username_entry.unbind('<Return>')
            if hasattr(self, 'password_entry'):
                self.password_entry.unbind('<Return>')
        except:
            pass  # Widgets might already be destroyed