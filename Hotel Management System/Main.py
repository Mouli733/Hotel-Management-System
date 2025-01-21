import random
import string
from AddFoodItems import AddFoodItems
from CustomerBill import CustomerBill
from CustomerDetails import CustomerDetails
from db_connection import get_bill_by_booking_id, get_customer_details_by_booking_id, get_db, get_food_selection_by_booking_id

class Main:
    def __init__(self):
        print("-------Welcome to the Hotel Grand-------")

    def get_customer_details(self):
        """Get customer details from the user."""
        name = input("Enter your name: ")
        while True:
            try:
                age = int(input("Enter your age: "))
                if age > 0:
                    break
                else:
                    print("Age must be a positive number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid age.")

        gender = input("Enter your Gender: ")
        phone = input("Enter your Phone number: ")
        while len(phone) != 10 or not phone.isdigit():
            print("Invalid phone number. Please enter a 10-digit number.")
            phone = input("Enter your Phone number: ")

        print("Available rooms are \n 1. Single bed -- 1000 \n 2. King size -- 2000 \n 3. Queen size -- 3000")
        while True:
            try:
                room_type = int(input("Select your Room Type (1-3): "))
                if 1 <= room_type <= 3:
                    break
                else:
                    print("Invalid room type. Please select a valid option (1-3).")
            except ValueError:
                print("Invalid input. Please enter a number.")

        while True:
            try:
                days_stay = int(input("Enter number of days you want to stay: "))
                if days_stay > 0:
                    break
                else:
                    print("Days stay must be a positive number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        booking_id = self.generate_id()
        return name, age, gender, phone, room_type, days_stay, booking_id

    def generate_id(self, length=10):
        """Generate a unique booking ID."""
        first_part = "".join(random.choices(string.ascii_uppercase, k=length - 5))
        second_part = "".join(random.choices(string.digits, k=5))
        return first_part + second_part
    
    def view_bills(self):
        db = get_db()
        if db is not None:
            booking_id = input("Enter the booking ID to view the bill: ")
            bill = db.bills.find_one({"booking_id": booking_id})
            if bill:
                print(f"Booking ID: {bill['booking_id']}")
                print(f"Name: {bill['name']}")
                print(f"Room Type: {bill['room_type']}")
                print(f"Days Stay: {bill['days_stay']}")
                print(f"Room Charge: ${bill['room_charge']:.2f}")
                print(f"Food Charge: ${bill['food_charge']:.2f}")
                print(f"Total Bill: ${bill['total_bill']:.2f}")
                if 'food_items' in bill:
                    print("Food Items:")
                    for item in bill['food_items']:
                        print(f"{item['item']} (x{item['quantity']}) - ${item['price'] * item['quantity']:.2f}")
                print("\n")
            else:
                print("No bill found for the given booking ID.")
        else:
            print("Database connection failed.")

    def run(self):
        """Main loop to handle user choices."""
        while True:
            print("-----Select your choice to continue for hotel booking-----\n 1. Select the Room \n 2. For Food selection \n 3. Customer details \n 4. Generate Bill \n 5. View Bills \n 6. Exit")
            try:
                n = int(input("\nEnter your choice: "))

                if n == 1:
                    name, age, gender, phone, room_type, days_stay, booking_id = self.get_customer_details()
                    customer_details = CustomerDetails(name, age, gender, phone, room_type, days_stay, booking_id)
                    customer_details.print_customer_details()
                    customer_details.save_to_db()

                elif n == 2:
                    booking_id = input("Enter your booking ID to continue: ")
                    customer_data = get_customer_details_by_booking_id(booking_id)
                    if customer_data:
                        food_items = AddFoodItems()
                        food_items.customer_food_selection()
                        food_items.save_food_selection(booking_id)
                    else:
                        print("No customer found with this booking ID.")

                elif n == 3:
                    booking_id = input("Enter booking ID to retrieve details: ")
                    customer_data = get_customer_details_by_booking_id(booking_id)
                    if customer_data:
                        print("Customer Details:")
                        print(customer_data)
                        print("Food Orders:")
                        food_orders = get_food_selection_by_booking_id(booking_id)
                        print(food_orders)
                        print("Bill Details:")
                        bill_details = get_bill_by_booking_id(booking_id)
                        print(bill_details)
                    else:
                        print("No customer found with this booking ID.")

                elif n == 4:
                    booking_id = input("Enter your booking ID to generate the bill: ")
                    customer_data = get_customer_details_by_booking_id(booking_id)
                    if customer_data:
                        customer_details = CustomerDetails(
                            name=customer_data["name"],
                            age=customer_data["age"],
                            gender=customer_data["gender"],
                            phone=customer_data["phone"],
                            room_type=customer_data["room_type"],
                            days_stay=customer_data["days_stay"],
                            booking_id=customer_data["booking_id"]
                        )
                        food_items = AddFoodItems().customer_selected
                        food_quantity = AddFoodItems().quantity
                        bill = CustomerBill(customer_details)
                        bill.customer_selected = food_items
                        bill.quantity = food_quantity
                        bill.display_total_bill()
                        bill.save_bill_to_db()
                    else:
                        print("No customer found with this booking ID.")

                elif n== 5:
                    self.view_bills()

                elif n == 6:
                    print("Thank you for visiting Hotel Grand")
                    break

                else:
                    print("Invalid choice. Please select a valid option.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    Main().run()