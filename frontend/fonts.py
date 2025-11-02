# -*- coding: utf-8 -*-
# frontend/fonts.py

import tkinter as tk
import tkinter.font as tkfont
import os

class FontManager:
    def __init__(self, root):
        self.root = root
        self.current_language = 'english'  # Default language
        self.setup_fonts()
    
    def setup_fonts(self):
        """Setup font system with language support"""
        # Define font mappings for different languages
        self.language_fonts = {
            'english': {
                'family': 'Open Sans',
                'files': {
                    'regular': 'fonts/open-sans/OpenSans-Regular.ttf',
                    'bold': 'fonts/open-sans/OpenSans-Bold.ttf',
                    'semibold': 'fonts/open-sans/OpenSans-SemiBold.ttf',
                    'light': 'fonts/open-sans/OpenSans-Light.ttf'
                }
            },
            'arabic': {
                'family': 'Arial',  # Good Arabic support
                'files': {}  # Use system font for Arabic
            },
            'french': {
                'family': 'Open Sans',
                'files': {
                    'regular': 'fonts/open-sans/OpenSans-Regular.ttf',
                    'bold': 'fonts/open-sans/OpenSans-Bold.ttf'
                }
            },
            'spanish': {
                'family': 'Open Sans', 
                'files': {
                    'regular': 'fonts/open-sans/OpenSans-Regular.ttf',
                    'bold': 'fonts/open-sans/OpenSans-Bold.ttf'
                }
            }
            # Add more languages as needed
        }
        
        self.load_fonts_for_language(self.current_language)
    
    def load_fonts_for_language(self, language):
        """Load appropriate fonts for the selected language"""
        self.current_language = language
        font_config = self.language_fonts.get(language, self.language_fonts['english'])
        
        try:
            # Try to use the specified font family
            available_fonts = tkfont.families()
            
            if font_config['family'] in available_fonts:
                print(f"✅ Using {font_config['family']} for {language}")
                self.create_font_objects(font_config['family'])
            else:
                # Fallback to Arial for better language support
                print(f"🔧 {font_config['family']} not found, using Arial for {language}")
                self.create_font_objects('Arial')
                
        except Exception as e:
            print(f"⚠️ Error loading fonts for {language}: {e}")
            self.create_font_objects('Arial')
    
    def create_font_objects(self, font_family):
        """Create font objects for the given font family"""
        # Regular weight
        self.primary_regular = tkfont.Font(family=font_family, size=10, weight="normal")
        self.primary_bold = tkfont.Font(family=font_family, size=10, weight="bold")
        self.primary_semibold = tkfont.Font(family=font_family, size=10, weight="bold")  # Approximate semi-bold
    
    def set_language(self, language):
        """Change the language and update fonts"""
        if language in self.language_fonts:
            self.load_fonts_for_language(language)
            return True
        else:
            print(f"⚠️ Language '{language}' not supported, keeping current language")
            return False
    
    def get_supported_languages(self):
        """Get list of supported languages"""
        return list(self.language_fonts.keys())
    
    # Font size properties (same interface for all languages)
    @property
    def title_large(self):
        font = self.primary_bold.copy()
        font.configure(size=18)
        return font
    
    @property
    def title_medium(self):
        font = self.primary_bold.copy()
        font.configure(size=16)
        return font
    
    @property
    def title_small(self):
        font = self.primary_bold.copy()
        font.configure(size=14)
        return font
    
    @property
    def heading(self):
        font = self.primary_bold.copy()
        font.configure(size=12)
        return font
    
    @property
    def body_large(self):
        font = self.primary_regular.copy()
        font.configure(size=11)
        return font
    
    @property
    def body_medium(self):
        font = self.primary_regular.copy()
        font.configure(size=10)
        return font
    
    @property
    def body_small(self):
        font = self.primary_regular.copy()
        font.configure(size=9)
        return font
    
    @property
    def button_large(self):
        font = self.primary_semibold.copy()
        font.configure(size=11)
        return font
    
    @property
    def button_medium(self):
        font = self.primary_regular.copy()
        font.configure(size=10)
        return font
    
    @property
    def label_bold(self):
        font = self.primary_bold.copy()
        font.configure(size=10)
        return font
    
    @property
    def label_normal(self):
        font = self.primary_regular.copy()
        font.configure(size=10)
        return font
    
    @property
    def input_text(self):
        font = self.primary_regular.copy()
        font.configure(size=10)
        return font