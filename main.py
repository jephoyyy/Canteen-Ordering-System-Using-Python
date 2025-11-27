import time # package used for queue time order
from datetime import datetime # package use for real-time date and time for overall view of all order

menu = { # this is where we store our products that is available to the system
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
        1: ('Sisig', 70),
        2: ('Pares', 60),
        3: ('Siomai Rice', 35),
        4: ('Tapsilog', 40),
        5: ('Pastil', 25),
        6: ('BBQ', 25),
        7: ('Hotsilog', 40),
        8: ('Longsilog', 40)
    }
}

session_orders = []
order_history = []
order_count = 0

def simulate_order_timer(order_number, item_name):
    print("\nOrder #" + str(order_number) + " (" + item_name + ") is being prepared...")
    for i in range(3, 0, -1): # loops 3 time and print the output below 3 times with 1 second delay
        print("Order #" + str(order_number) + " ready in " + str(i) + "...")
        time.sleep(1) # 1 second delay for timer
    print("Order is READY!\n")

def show_menu(category):
    global order_count

    items = menu[category]

    print("\n--- " + category.upper() + " ---")
    for id in items:
        name = items[id][0]
        price = items[id][1]
        print(str(id) + ". " + name + " - ₱" + str(price))

    try:
        order = int(input("\nEnter item number to order (0 to go back): "))
        if order == 0:
            return

        qty = int(input("Enter quantity: "))

        if order not in items:
            print("Invalid item number!")
            return

        name = items[order][0]
        price = items[order][1]
        total = price * qty

        order_count += 1
        simulate_order_timer(order_count, name)

        session_orders.append({
            "name": name,
            "qty": qty,
            "total": total
        })

        print("Added to cart: " + str(qty) + " x " + name + " (₱" + str(total) + ")")

    except ValueError:
        print("Invalid input!")


def finish_ordering():
    if len(session_orders) == 0:
        print("You haven't ordered anything yet!")
        return

    grand_total = 0
    print("\n=== SESSION RECEIPT ===")

    for item in session_orders:
        line = str(item["qty"]) + " x " + item["name"] + " ........ ₱" + str(item["total"])
        print(line)
        grand_total += item["total"]

        order_history.append({
            "item_name": item["name"],
            "quantity": item["qty"],
            "total": item["total"],
            "order_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    print("-----------------------------")
    print("GRAND TOTAL: ₱" + str(grand_total))
    print("Thank you for ordering!\n")

    session_orders.clear()

def user_mode(): #will show if user chose the number 1 option at the start menu
    while True:
        print("\n[1] Beverages\n[2] Snacks\n[3] Meals\n[4] Exit\n[5] Finish Ordering")
        choice = input("Choose a category: ")

        if choice == "1":
            show_menu("Beverages")
        elif choice == "2":
            show_menu("Snacks")
        elif choice == "3":
            show_menu("Meals")
        elif choice == "4":
            print("Returning to main menu...")
            return
        elif choice == "5":
            finish_ordering()
        else:
            print("Invalid choice!")

def admin_mode(): #will show if user chose the number 2 option at the start menu
    password = input("Enter admin password: ") 

    if password != "pogiako123": #you can change the password here!!
        print("Incorrect password!")
        return

    print("\n=== ALL ORDERS (ADMIN VIEW) ===") # this is where the all order history will show.

    if len(order_history) == 0: #if no orders are made during the whole run up
        print("No orders yet.")
        return

    for i in range(len(order_history)):
        order = order_history[i]
        line = ("Order #" + str(i + 1) +
                " | " + order["item_name"] +
                " x" + str(order["quantity"]) +
                " | ₱" + str(order["total"]) +
                " | " + order["order_time"])

        print(line)

while True: # the first menu that will appear upon starting up the system
    print("\n=== CANTEEN ORDERING SYSTEM ===")
    print("[1] User Mode")
    print("[2] Admin Mode")
    print("[3] Exit")
    mode = input("Choose mode: ")

    if mode == "1":
        user_mode()
    elif mode == "2":
        admin_mode() 
    elif mode == "3":
        print("Exiting system. Goodbye!")
        break
    else:
        print("Invalid choice!")

