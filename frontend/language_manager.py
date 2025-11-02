# -*- coding: utf-8 -*-
# frontend/language_manager.py

import tkinter as tk
from tkinter import ttk

class LanguageManager:
    def __init__(self):
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
                
                # Flight management specific translations
                'flight_number': 'Flight Number',
                'origin': 'Origin', 
                'destination': 'Destination',
                'departure': 'Departure',
                'arrival': 'Arrival', 
                'status': 'Status',
                'origin_airport': 'Origin Airport',
                'destination_airport': 'Destination Airport',
                'departure_date': 'Departure Date',
                'departure_time': 'Depature Time', 
                'arrival_date': 'Arrival Date',
                'arrival_time': 'Arrival Time',
                'save_flight': 'Save Flight',
                'cancel': 'Cancel',
                'hour': 'Hour',
                'minute': 'Minute',
                'will_be_saved_as': 'Will be saved as',
                'enter_numbers_only': 'Enter numbers only',
                'select_valid_departure_date': 'Please select a valid departure date!',
                'select_valid_arrival_date': 'Please select a valid arrival date!',
                'all_fields_required': 'All fields are required!',
                'enter_valid_flight_number': 'Please enter a valid flight number (numbers only)',
                'flight_already_exists': 'Flight {} already exists on {}!',
                'use_yyyy_mm_dd_format': 'Please use YYYY-MM-DD format for dates!',
                'select_valid_origin_airport': 'Please select a valid origin airport!',
                'select_valid_destination_airport': 'Please select a valid destination airport!',
                'origin_destination_different': 'Origin and destination airports cannot be the same!',
                'arrival_after_departure': 'Arrival must be after departure!',
                
                # Booking management specific translations
                'booking_id': 'Booking ID',
                'passenger_name': 'Passenger Name',
                'flight': 'Flight',
                'booking_date': 'Booking Date',
                'seat_number': 'Seat Number',
                'booking_status': 'Booking Status',
                'add_booking': 'Add Booking',
                'edit_booking': 'Edit Booking',
                'delete_booking': 'Delete Booking',
                'view_details': 'View Details',
                'total_bookings': 'Total Bookings',
                'confirmed': 'Confirmed',
                'pending': 'Pending',
                'cancelled': 'Cancelled',
                'select_passenger': 'Select Passenger',
                'select_flight': 'Select Flight',
                'seat_class': 'Seat Class',
                'economy': 'Economy',
                'business': 'Business',
                'first_class': 'First Class',
                'price': 'Price',
                'payment_status': 'Payment Status',
                'paid': 'Paid',
                'unpaid': 'Unpaid',
                'notes': 'Notes',
                'save_booking': 'Save Booking',
                'update_booking': 'Update Booking',
                
                # Additional booking management translations
                'no_bookings_found': 'No bookings found',
                'booking_details': 'Booking Details',
                'close': 'Close',
                'cancel_booking': 'Cancel Booking',
                'booking_cancelled_success': 'Booking cancelled successfully!',
                'create_new_booking': 'Create New Booking',
                'select_class': 'Select Class',
                'select_terminal': 'Select Terminal',
                'terminal': 'Terminal',
                'number_of_seats': 'Number of Seats',
                'seat_format_helper': 'Format: 15A, 5B, etc.',
                'price_calculation': 'Price Calculation',
                'select_class_seats_for_price': 'Select class and seats to see price',
                'invalid_seat_count': 'Invalid number of seats',
                'create_booking': 'Create Booking',
                'select_passenger_validation': 'Please select a passenger',
                'select_flight_validation': 'Please select a flight',
                'select_class_validation': 'Please select a class',
                'select_terminal_validation': 'Please select a terminal',
                'enter_seat_number': 'Please enter a seat number',
                'booking_created_success': 'Booking created successfully!',
                'booking_reference': 'Booking Reference',
                'ticket_number': 'Ticket Number',
                'total': 'Total',
                'seat_s': 'seat(s)',
                'route': 'Route',
                'seat_count': 'Seat Count',
                'total_price': 'Total Price',
                'today_passengers': "Today's Passengers",
                'revenue': "Revenue",
                'recent_activity': "Recent Activity",
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
                
                # Flight management specific translations
                'flight_number': 'رقم الرحلة',
                'origin': 'المغادرة', 
                'destination': 'الوجهة',
                'departure': 'وقت المغادرة',
                'arrival': 'وقت الوصول', 
                'status': 'الحالة',
                'origin_airport': 'مطار المغادرة',
                'destination_airport': 'مطار الوصول',
                'departure_date': 'تاريخ المغادرة',
                'departure_time': 'وقت المغادرة', 
                'arrival_date': 'تاريخ الوصول',
                'arrival_time': 'وقت الوصول',
                'save_flight': 'حفظ الرحلة',
                'cancel': 'إلغاء',
                'hour': 'ساعة',
                'minute': 'دقيقة',
                'will_be_saved_as': 'سيتم حفظه كـ',
                'enter_numbers_only': 'أدخل أرقام فقط',
                'select_valid_departure_date': 'الرجاء اختيار تاريخ مغادرة صحيح!',
                'select_valid_arrival_date': 'الرجاء اختيار تاريخ وصول صحيح!',
                'all_fields_required': 'جميع الحقول مطلوبة!',
                'enter_valid_flight_number': 'الرجاء إدخال رقم رحلة صحيح (أرقام فقط)',
                'flight_already_exists': 'الرحلة {} موجودة بالفعل في {}!',
                'use_yyyy_mm_dd_format': 'الرجاء استخدام صيغة YYYY-MM-DD للتواريخ!',
                'select_valid_origin_airport': 'الرجاء اختيار مطار مغادرة صحيح!',
                'select_valid_destination_airport': 'الرجاء اختيار مطار وصول صحيح!',
                'origin_destination_different': 'لا يمكن أن يكون مطار المغادرة والوصول متماثلين!',
                'arrival_after_departure': 'يجب أن يكون وقت الوصول بعد وقت المغادرة!',
                
                # Booking management specific translations
                'booking_id': 'رقم الحجز',
                'passenger_name': 'اسم المسافر',
                'flight': 'الرحلة',
                'booking_date': 'تاريخ الحجز',
                'seat_number': 'رقم المقعد',
                'booking_status': 'حالة الحجز',
                'add_booking': 'إضافة حجز',
                'edit_booking': 'تعديل الحجز',
                'delete_booking': 'حذف الحجز',
                'view_details': 'عرض التفاصيل',
                'total_bookings': 'إجمالي الحجوزات',
                'confirmed': 'مؤكد',
                'pending': 'قيد الانتظار',
                'cancelled': 'ملغى',
                'select_passenger': 'اختر المسافر',
                'select_flight': 'اختر الرحلة',
                'seat_class': 'فئة المقعد',
                'economy': 'اقتصادية',
                'business': 'رجال الأعمال',
                'first_class': 'الدرجة الأولى',
                'price': 'السعر',
                'payment_status': 'حالة الدفع',
                'paid': 'مدفوع',
                'unpaid': 'غير مدفوع',
                'notes': 'ملاحظات',
                'save_booking': 'حفظ الحجز',
                'update_booking': 'تحديث الحجز',
                
                # Additional booking management translations
                'no_bookings_found': 'لم يتم العثور على حجوزات',
                'booking_details': 'تفاصيل الحجز',
                'close': 'إغلاق',
                'cancel_booking': 'إلغاء الحجز',
                'booking_cancelled_success': 'تم إلغاء الحجز بنجاح!',
                'create_new_booking': 'إنشاء حجز جديد',
                'select_class': 'اختر الفئة',
                'select_terminal': 'اختر المحطة',
                'terminal': 'المحطة',
                'number_of_seats': 'عدد المقاعد',
                'seat_format_helper': 'الصيغة: 15A, 5B, إلخ',
                'price_calculation': 'حساب السعر',
                'select_class_seats_for_price': 'اختر الفئة والمقاعد لرؤية السعر',
                'invalid_seat_count': 'عدد مقاعد غير صالح',
                'create_booking': 'إنشاء الحجز',
                'select_passenger_validation': 'الرجاء اختيار مسافر',
                'select_flight_validation': 'الرجاء اختيار رحلة',
                'select_class_validation': 'الرجاء اختيار فئة',
                'select_terminal_validation': 'الرجاء اختيار محطة',
                'enter_seat_number': 'الرجاء إدخال رقم المقعد',
                'booking_created_success': 'تم إنشاء الحجز بنجاح!',
                'booking_reference': 'رقم مرجع الحجز',
                'ticket_number': 'رقم التذكرة',
                'total': 'المجموع',
                'seat_s': 'مقعد(مقاعد)',
                'route': 'الطريق',
                'seat_count': 'عدد المقاعد',
                'total_price': 'السعر الإجمالي',
                'today_passengers': "مسافرو اليوم",
                'revenue': "الإيرادات",
                'recent_activity': "النشاط الأخير"
            },
        }
    
    def set_language(self, language):
        """Change the application language"""
        if language in self.translations:
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
        return list(self.translations.keys())
    
    def is_rtl(self):
        """Check if current language is RTL (Arabic)"""
        return self.current_language == 'arabic'
    
    def apply_rtl_layout(self, widget):
        """Apply RTL layout to widget if current language is Arabic"""
        if not self.is_rtl():
            return
            
        try:
            self._apply_rtl_recursive(widget)
        except Exception as e:
            print(f"Error applying RTL layout: {e}")
    
    def _apply_rtl_recursive(self, widget):
        """Recursively apply RTL layout to widget and its children"""
        try:
            # Apply RTL to current widget
            self._apply_rtl_to_single_widget(widget)
            
            # Apply to all children recursively
            for child in widget.winfo_children():
                self._apply_rtl_recursive(child)
                
        except:
            pass  # Ignore errors for widgets that can't be processed
    
    def _apply_rtl_to_single_widget(self, widget):
        """Apply RTL settings to a single widget"""
        try:
            if isinstance(widget, (tk.Label, tk.Button)):
                widget.config(anchor='e', justify='right')
            elif isinstance(widget, (ttk.Entry, ttk.Combobox)):
                widget.config(justify='right')
            elif isinstance(widget, ttk.Treeview):
                # Change column alignment to right
                for col in widget['columns']:
                    widget.heading(col, anchor='e')
        except:
            pass