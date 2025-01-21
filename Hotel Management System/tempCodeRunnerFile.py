    db = get_db()
        if db is not None:
            bills = db.bills.find()
            if bills:
                for bill in bills:
                    print(f"Booking ID: {bill['booking_id']}")
                    print(f"Name: {bill['name']}")
                    print(f"Room Type: {bill['room_type']}")
                    print(f"Days Stay: {bill['days_stay']}")
                    print(f"Room Charge: ${bill['room_charge']:.2f}")
                    print(f"Food Charge: ${bill['food_charge']:.2f}")
                    print(f"Total Bill: ${bill['total_bill']:.2f}")
                    print("Food Items:")
                    for item in bill['food_items']:
                        print(f"{item['item']} (x{item['quantity']}) - ${item['price'] * item['quantity']:.2f}")
                    print("\n")
            else:
                print("No bills found.")
        else:
            print("Database connection failed.")