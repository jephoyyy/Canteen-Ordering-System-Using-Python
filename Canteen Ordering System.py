import time # Para sa queue time / timer ng order
from datetime import datetime  # Para makuha ang real-time date and time para sa receipts

# Product storage (similar sa database tables)
menu = {
    "Beverages": {
        1: ("Lemon", 15),
        2: ("Iced Tea", 20),
        3: ("Coffee", 50),
        4: ("Gulaman", 10),
        5: ("Bottled Water", 10),
        6: ("Softdrinks", 15)
    },
    "Snacks": {
        1: ("Corndog", 25),
        2: ("Burger", 30),
        3: ("Turon", 15),
        4: ("Ice Cream", 20),
        5: ("Donut", 20),
        6: ("Siopao", 25),
        7: ("Siomai", 20),
        8: ("Chicken Fillet", 35)
    },
    "Meals": {
        1: ("Sisig", 70),
        2: ("Pares", 60),
        3: ("Siomai Rice", 35),
        4: ("Tapsilog", 40),
        5: ("Pastil", 25),
        6: ("BBQ", 25),
        7: ("Hotsilog", 40),
        8: ("Longsilog", 40)
    }
}

session_orders = []      # Dynamic Arrays, declared na ang array is nag sstart ng empty list
order_history = []       
order_count = 0          # Order number counter
customer_id_counter = 1  # Auto-increment customer ID start siya sa 1

def simulate_order_timer(order_number, item_name): #Function for Queue/Timer para sa order
    print(f"\nPreparing Order #{order_number} ({item_name})...")
    for i in range(3, 0, -1): # For loop nag sstart sa 3 decrement ng 1 kada 1 second
        print(f"Ready in {i}...")
        time.sleep(1)
    print("Order READY!\n")

def show_menu(category):
    global order_count #since asa labas ang order_count at gusto natin siyang baguhin, gumamit tayo ng global keyword
    items = menu[category]

    while True:
        print("\n--- " + category + " ---") 
        for pid in items: #For loop print for list of all products per category
            name, price = items[pid]
            print(f"{pid}. {name} - ₱{price}")

        try:
            choice = int(input("\nChoose item (0 to go back): ")) #User's Input
            if choice == 0: # Decision making statements
                return
            if choice not in items: # If wala sa range ng options 
                print("Invalid item.")
                continue #Para bumalik sa pag pili ng items

            qty = int(input("Quantity: "))
            name, price = items[choice]
            total = price * qty # Operation para makuha ang total 

            order_count += 1 #increment sa order_count
            simulate_order_timer(order_count, name)

            session_orders.append({ #taga store ng values na nakuha 
                "name": name,
                "qty": qty,
                "total": total
            })

            print(f"Added to cart: {qty} x {name}")
            break # stop ng loop

        except ValueError: # Error Handling if may mag-exist na error.
            print("Invalid input!")

def finish_ordering(customer_id): #Function for option 5
    if not session_orders: #Check if may laman ang cart or session
        print("No orders yet!")
        return

    grand_total = 0 

    print("\n=== SESSION RECEIPT ===") #header

    for item in session_orders:
        print(f'{item["qty"]} x {item["name"]} .... ₱{item["total"]}')
        grand_total += item["total"]

        order_history.append({ #taga store ng order history para sa admin view
            "customer_id": customer_id,
            "item_name": item["name"],
            "quantity": item["qty"],
            "total": item["total"],
            "order_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S") #Kunin ang real time & date upon ordering and i format sa readable form
        })

    print("-----------------------------")
    print("TOTAL: ₱" + str(grand_total)) #Convert ang int to string

    session_orders.clear() #Para ma-reset at hindi mag halo ang order ng previous customer sa current customer

def user_mode(): #Functiom for option 1 sa unang menu
    global customer_id_counter #Pare ma access ang nasa labas ng variable na may assigned value

    # assign unique customer ID sa bawat user
    customer_id = customer_id_counter
    customer_id_counter += 1

    print(f"\nYour Customer ID: {customer_id}")

    while True:
        print("\n--- USER MENU ---") #Menu after choosing User's Menu
        print("[1] Beverages\n[2] Snacks\n[3] Meals\n[4] Back\n[5] Finish Order")

        choice = input("Choose: ")
        #All parameter here goes to their specific category.
        if choice == "1":
            show_menu("Beverages")
        elif choice == "2":
            show_menu("Snacks")
        elif choice == "3":
            show_menu("Meals")
        elif choice == "4":
            return
        elif choice == "5":
            finish_ordering(customer_id) #Tinawag yung function na ginawa for option 5
        else:
            print("Invalid choice!")

def admin_mode(): #Function for option 2 sa unang menu
    password = input("\nEnter admin password: ")

    if password != "pogiako123": #dito pwede mag change ng password
        print("Wrong password.")
        return

    while True:
        print("\n=== ADMIN VIEW ===")
        print("[1] View ALL Orders\n[2] View Orders by Customer ID\n[3] Back")

        choice = input("Choose: ")

        if choice == "1":
            if not order_history:
                print("No orders found.")
            else:
                print("\n--- ALL ORDERS ---")
                for i, order in enumerate(order_history, start=1): #nagbibigay ng index number habang nag-i-iterate sa list.
                    print(
                        f"#{i} | Customer {order['customer_id']} | "
                        f"{order['item_name']} x{order['quantity']} | ₱{order['total']} | {order['order_time']}"
                    )

        elif choice == "2":
            try:
                cid = int(input("Enter Customer ID: "))
                found = False #Check if may order ang customer

                print(f"\n--- ORDERS OF CUSTOMER {cid} ---")

                for order in order_history:
                    if order["customer_id"] == cid:
                        found = True
                        print(
                            f"{order['item_name']} x{order['quantity']} | ₱{order['total']} | {order['order_time']}"
                        )

                if not found:
                    print("No orders found for this customer.")

            except ValueError: #Error handling
                print("Invalid ID.")

        elif choice == "3":
            return #Exit
        else:
            print("Invalid choice!")

while True:
    print("\n=== CANTEEN ORDERING SYSTEM ===")
    print("[1] User Mode\n[2] Admin Mode\n[3] Exit")

    mode = input("Choose: ")

    if mode == "1":
        user_mode() #call ng function
    elif mode == "2":
        admin_mode()
    elif mode == "3":
        print("Goodbye!")
        break #Terminate
    else:
        print("Invalid input!")
