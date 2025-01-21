from pymongo import MongoClient
from db_connection import get_db

class CustomerDetails:
    def __init__(self, name, age, gender, phone, room_type, days_stay, booking_id):
        self.name = name
        self.age = age
        self.gender = gender
        self.phone = phone
        self.room_type = room_type  # This is an integer
        self.days_stay = days_stay
        self.booking_id = booking_id

    def get_room_type_string(self):
        # Map room_type integer to its string representation
        room_type_mapping = {
            1: "single bed",
            2: "king size",
            3: "queen size"
        }
        return room_type_mapping.get(self.room_type, "unknown room type")

    def print_customer_details(self):
        print("----You have booked your Room Successfully with booking_id:", self.booking_id, "------")
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Gender: {self.gender}")
        print(f"Phone Number: {self.phone}")
        print(f"Room Type: {self.get_room_type_string()}")  # Use the mapped string
        print(f"Days Stay: {self.days_stay}")
        print(f"Booking ID: {self.booking_id}")

    def save_to_db(self):
        db = get_db()
        customer_data = {
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "phone": self.phone,
            "room_type": self.room_type,
            "days_stay": self.days_stay,
            "booking_id": self.booking_id
        }
        db.customers.insert_one(customer_data)
        print(f"Customer details saved successfully for booking ID: {self.booking_id}")