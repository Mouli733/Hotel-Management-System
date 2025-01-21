from pymongo import MongoClient

def get_db():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client.hotel_management
        return db
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def get_customer_details_by_booking_id(booking_id):
    db = get_db()
    if db is not None:
        try:
            customer_data = db.customers.find_one({"booking_id": booking_id})
            if customer_data:
                print("Customer Details:")
                print(f"Name: {customer_data['name']}")
                print(f"Age: {customer_data['age']}")
                print(f"Gender: {customer_data['gender']}")
                print(f"Phone: {customer_data['phone']}")
                print(f"Room Type: {customer_data['room_type']}")
                print(f"Days Stay: {customer_data['days_stay']}")
                print(f"Booking ID: {customer_data['booking_id']}")
                return customer_data
            else:
                print(f"No customer found with booking ID: {booking_id}")
                return None
        except Exception as e:
            print(f"Error retrieving customer data: {e}")
            return None
    else:
        print("Database connection failed.")
        return None

def get_food_selection_by_booking_id(booking_id):
    db = get_db()
    if db is not None:
        try:
            food_orders = db.food_orders.find({"booking_id": booking_id})
            print("\nFood Orders:")
            for food in food_orders:
                print(f"{food['item']} (x{food['quantity'] }) - ${food['total_price']:.2f}")
            return list(food_orders)
        except Exception as e:
            print(f"Error retrieving food selection: {e}")
            return []
    else:
        print("Database connection failed.")
        return []

def get_bill_by_booking_id(booking_id):
    db = get_db()
    if db is not None:
        try:
            bill_data = db.bills.find_one({"booking_id": booking_id})
            if bill_data:
                print("\nBill Details:")
                print(f"Name: {bill_data['name']}")
                print(f"Room Type: {bill_data['room_type']}")
                print(f"Room Charge: ${bill_data['room_charge']:.2f}")
                print(f"Food Charge: ${bill_data['food_charge']:.2f}")
                print(f"Total Bill: ${bill_data['total_bill']:.2f}")
                return bill_data
            else:
                print(f"No bill found for booking ID: {booking_id}")
                return None
        except Exception as e:
            print(f"Error retrieving bill data: {e}")
            return None
    else:
        print("Database connection failed.")
        return None