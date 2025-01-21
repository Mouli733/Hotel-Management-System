import random
import string

class RoomSelection:
    def customer_selection(self, selection):
        if selection == 1:
            self.room_type = "single bed"
            return 1000
        elif selection == 2:
            self.room_type = "king size"
            return 2000
        elif selection == 3:
            self.room_type = "queen size"
            return 3000
        else:
            print("Invalid selection. Please select a valid room (1-3).")
            return 0

    def generate_id(self, length=10):
        first_part = "".join(random.choices(string.ascii_uppercase, k=length - 5))
        second_part = "".join(random.choices(string.digits, k=5))
        return first_part + second_part