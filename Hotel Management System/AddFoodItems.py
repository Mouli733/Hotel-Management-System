from db_connection import get_db

class AddFoodItems:
    def __init__(self):
        self.food_items = [
            {"pizza": 10.99},
            {"burger": 8.99},
            {"fries": 3.99},
            {"salad": 6.99},
            {"soda": 2.99},
            {"water": 1.99}
        ]
        self.customer_selected = []
        self.quantity = []

    def print_item_list(self, items):
        for count, item in enumerate(items, start=1):
            item_name = list(item.keys())[0]
            print(f"{count}. {item_name} - ${item[item_name]:.2f}")

    def customer_food_selection(self):
        while True:
            try:
                print("\n------Select a food item from the menu below---------")
                self.print_item_list(self.food_items)
                selection = int(input("Select the food item you want to add (or 0 to finish): "))
                if selection == 0:
                    print("\n------Done with the selection-------")
                    self.printing_only_items()
                    break
                elif 1 <= selection <= len(self.food_items):
                    selected_item = self.food_items[selection - 1]
                    self.customer_selected.append(selected_item)
                    quantity = int(input("Enter the quantity of the selected item: "))
                    self.quantity.append(quantity)
                    print(f"\nYou have selected: {list(selected_item.keys())[0]} with the quantity {quantity}")
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def printing_only_items(self):
        for item, quantity in zip(self.customer_selected, self.quantity):
            item_name = list(item.keys())[0]
            item_price = list(item.values())[0]
            print(f"{item_name} = {quantity} @ ${item_price:.2f} each")

    def save_food_selection(self, booking_id):
        db = get_db()
        for item, qty in zip(self.customer_selected, self.quantity):
            item_name = list(item.keys())[0]
            item_price = list(item.values())[0]
            db.food_orders.insert_one({
                "booking_id": booking_id,
                "item": item_name,
                "quantity": qty,
                "price_per_unit": item_price,
                "total_price": item_price * qty
            })
        print(f"Food selection saved for booking ID: {booking_id}")