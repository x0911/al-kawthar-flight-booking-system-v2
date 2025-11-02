# -*- coding: utf-8 -*-
# frontend/language_manager.py

class LanguageManager:
    def __init__(self, font_manager):
        self.font_manager = font_manager
        self.current_language = 'english'
        self.translations = self.load_translations()
    
    def load_translations(self):
        """Load all language translations"""
        return {
            'english': {
                'app_title': 'Al Kawthar Flights',
                'login_title': 'Management System Login',
                'username': 'Username',
                'password': 'Password',
                'login_button': 'Login',
                'demo_credentials': 'For demo: Use any credentials',
                'dashboard': 'Dashboard',
                'flights': 'Flights',
                'bookings': 'Bookings',
                'passengers': 'Passengers',
                'reports': 'Reports',
                'logout': 'Logout',
                'welcome': 'Welcome, {}',
                'flight_management': 'Flights Management',
                'booking_management': 'Bookings Management',
                'refresh': 'Refresh',
                'add_flight': 'Add Flight',
                'new_booking': 'New Booking',
                'search': 'Search',
            },
            'arabic': {
                'app_title': 'طيران الكوثر',
                'login_title': 'نظام إدارة التسجيل',
                'username': 'اسم المستخدم',
                'password': 'كلمة المرور',
                'login_button': 'تسجيل الدخول',
                'demo_credentials': 'للتجربة: استخدم أي بيانات دخول',
                'dashboard': 'لوحة التحكم',
                'flights': 'الرحلات',
                'bookings': 'الحجوزات',
                'passengers': 'المسافرون',
                'reports': 'التقارير',
                'logout': 'تسجيل الخروج',
                'welcome': 'أهلاً بك، {}',
                'flight_management': 'إدارة الرحلات',
                'booking_management': 'إدارة الحجوزات',
                'refresh': 'تحديث',
                'add_flight': 'إضافة رحلة',
                'new_booking': 'حجز جديد',
                'search': 'بحث',
            },
        }
    
    def set_language(self, language):
        """Change the application language"""
        if language in self.translations:
            # Update font manager first
            success = self.font_manager.set_language(language)
            if success:
                self.current_language = language
                return True
        return False
    
    def get_text(self, key, *args):
        """Get translated text for the current language"""
        translation = self.translations.get(self.current_language, {})
        text = translation.get(key, key)  # Fallback to key if not found
        
        # Format with arguments if provided
        if args:
            try:
                text = text.format(*args)
            except:
                pass  # Keep original text if formatting fails
        
        return text
    
    def get_supported_languages(self):
        """Get list of supported languages"""
        return self.font_manager.get_supported_languages()