from AddFoodItems import AddFoodItems
from RoomSelection import RoomSelection
from db_connection import get_db


class CustomerBill(AddFoodItems, RoomSelection):
    def __init__(self, customer_details):
        super().__init__()
        self.customer_details = customer_details
        self.food_charge = 0

    def calculate_food_charge(self):
        self.food_charge = sum(item[list(item.keys())[0]] * qty for item, qty in zip(self.customer_selected, self.quantity))
        return self.food_charge

    def display_total_bill(self):
        room_charge = self.calculate_room_charge()
        food_charge = self.calculate_food_charge()
        total_bill = room_charge + food_charge
        print(f"Room Charge: ${room_charge:.2f}")
        print(f"Food Charge: ${food_charge:.2f}")
        print("Food Items:")
        for item, qty in zip(self.customer_selected, self.quantity):
            item_name = list(item.keys())[0]
            item_price = list(item.values())[0]
            print(f"{item_name} (x{qty}) - ${item_price * qty:.2f}")
        print(f"Total Bill: ${total_bill:.2f}")

    def calculate_room_charge(self):
        room_prices = {1: 1000, 2: 2000, 3: 3000}  # Room prices
        room_type = self.customer_details.room_type  # Access instance variable
        days_stay = self.customer_details.days_stay  # Access instance variable
        return room_prices.get(room_type, 0) * days_stay

    def save_bill_to_db(self):
        db = get_db()
        total_food_cost = self.calculate_food_charge()
        room_charge = self.calculate_room_charge()
        total_bill = room_charge + total_food_cost
        db.bills.insert_one({
            "booking_id": self.customer_details.booking_id,
            "name": self.customer_details.name,
            "room_type": self.customer_details.get_room_type_string(),
            "days_stay": self.customer_details.days_stay,
            "room_charge": room_charge,
            "food_charge": total_food_cost,
            "total_bill": total_bill,
            "food_items": [{"item": list(item.keys())[0], "quantity": qty, "price": list(item.values())[0]} for item, qty in zip(self.customer_selected, self.quantity)]
        })
        print(f"Bill saved for booking ID: {self.customer_details.booking_id}")