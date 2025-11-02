# -*- coding: utf-8 -*-
class Flight:
    def __init__(self, flight_id, flight_number, origin, destination, 
                 departure_date, departure_time, arrival_date, arrival_time, status):
        self.flight_id = flight_id
        self.flight_number = flight_number
        self.origin = origin
        self.destination = destination
        self.departure_date = departure_date
        self.departure_time = departure_time
        self.arrival_date = arrival_date
        self.arrival_time = arrival_time
        self.status = status

class Passenger:
    def __init__(self, passenger_id, passport_number, name, gender, nationality):
        self.passenger_id = passenger_id
        self.passport_number = passport_number
        self.name = name
        self.gender = gender
        self.nationality = nationality

class Ticket:
    def __init__(self, ticket_id, ticket_number, passenger_name, flight_number, 
                 seat_number, price, status):
        self.ticket_id = ticket_id
        self.ticket_number = ticket_number
        self.passenger_name = passenger_name
        self.flight_number = flight_number
        self.seat_number = seat_number
        self.price = price
        self.status = status