


class Product:
    def __init__(self, name, price, stock, sku):
        self.name = name
        self.price = price
        self.stock = stock
        self.sku = sku

    def __str__(self):
        return f"Name: {self.name}, Price: ${self.price}, Stock: {self.stock}, SKU: {self.sku}"


class Inventory:
    def __init__(self):
        self.products = {}

    def add_product(self, product):
        if product.sku in self.products:
            print("A product with this SKU already exists.")
            return

        self.products[product.sku] = product

    def view_products(self):
        if not self.products:
            print("Inventory is empty.")
            return

        for sku, product in self.products.items():
            print(product)

    def sell_product(self, sku, quantity):
        if sku not in self.products:
            print("Product not found.")
            return

        product = self.products[sku]

        if quantity <= 0:
            print("Quantity must be greater than zero.")
        elif quantity > product.stock:
            print("Not enough stock available.")
        else:
            product.stock -= quantity
            total = quantity * product.price
            print(f"Sale complete. Total: ${total}")

    def restock_product(self, sku, quantity):
        if sku not in self.products:
            print("Product not found.")
            return

        if quantity <= 0:
            print("Quantity must be greater than zero.")
            return

        product = self.products[sku]
        product.stock += quantity
        print("Restocked. New stock:", product.stock)

    def remove_product(self, sku):
        if sku not in self.products:
            print("Product not found.")
            return False

        del self.products[sku]
        print("Product removed.")
        return True

    def low_stock_products(self, threshold):
        result = []

        for sku, product in self.products.items():
            if product.stock < threshold:
                result.append(product)

        return result

    def products_under_price(self, max_price):
        return [
            product
            for sku, product in self.products.items()
            if product.price < max_price
        ]

    def total_inventory_value(self):
        total = 0

        for sku, product in self.products.items():
            total += product.price * product.stock

        return total

    def generate_report(self, threshold):
        total = self.total_inventory_value()
        low_stock = self.low_stock_products(threshold)

        print("Total Inventory Value: $", total)
        print("Low Stock Products (below", threshold, "):")

        if not low_stock:
            print("No low-stock products.")
        else:
            for p in low_stock:
                print(p)

    def save_inventory(self):
        with open("inventory.txt", "w") as file:
            for sku, product in self.products.items():
                file.write(
                    f"{sku}|{product.name}|{product.price}|{product.stock}\n"
                )

    def load_inventory(self):
        try:
            with open("inventory.txt", "r") as file:
                for line in file:
                    if not line.strip():
                        continue

                    sku, name, price, stock = line.strip().split("|")
                    product = Product(name, float(price), int(stock), sku)
                    self.products[sku] = product

        except FileNotFoundError:
            print("No saved inventory found. Starting with an empty inventory.")


# Create one Inventory object
inventory = Inventory()
inventory.load_inventory()

while True:
    print("\n1. Add a Product")
    print("2. View Products")
    print("3. Remove a Product")
    print("4. Restock")
    print("5. Sell")
    print("6. Low Stock Products")
    print("7. Products Under Price")
    print("8. Total Inventory Value")
    print("9. Generate Report")
    print("10. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        try:
            name = input("Enter the product name: ")
            price = float(input("Enter the product price: "))
            stock = int(input("Enter the product stock: "))
            sku = input("Enter the product SKU: ")

            if price < 0 or stock < 0:
                print("Price and stock cannot be negative.")
                continue

            product = Product(name, price, stock, sku)
            inventory.add_product(product)

            if sku in inventory.products and inventory.products[sku] is product:
                inventory.save_inventory()
                print("Product added.")

        except ValueError:
            print("Please enter a valid number for price and stock.")

    elif choice == "2":
        inventory.view_products()

    elif choice == "3":
        sku = input("Enter the SKU of the product to remove: ")
        removed = inventory.remove_product(sku)

        if removed:
            inventory.save_inventory()

    elif choice == "4":
        try:
            sku = input("Enter the SKU of the product to restock: ")
            quantity = int(input("Enter the quantity to restock: "))

            inventory.restock_product(sku, quantity)
            inventory.save_inventory()

        except ValueError:
            print("Please enter a valid whole number for quantity.")

    elif choice == "5":
        try:
            sku = input("Enter the SKU of the product to sell: ")
            quantity = int(input("Enter the quantity to sell: "))

            inventory.sell_product(sku, quantity)
            inventory.save_inventory()

        except ValueError:
            print("Please enter a valid whole number for quantity.")

    elif choice == "6":
        try:
            threshold = int(input("Enter the stock threshold: "))
            low_stock = inventory.low_stock_products(threshold)

            if not low_stock:
                print("No low-stock products found.")
            else:
                for p in low_stock:
                    print(p)

        except ValueError:
            print("Please enter a valid whole number for threshold.")

    elif choice == "7":
        try:
            max_price = float(input("Enter the maximum price: "))
            products = inventory.products_under_price(max_price)

            if not products:
                print("No products found under that price.")
            else:
                for p in products:
                    print(p)

        except ValueError:
            print("Please enter a valid number for price.")

    elif choice == "8":
        total = inventory.total_inventory_value()
        print("Total Inventory Value: $", total)

    elif choice == "9":
        try:
            threshold = int(input("Enter the stock threshold: "))
            inventory.generate_report(threshold)

        except ValueError:
            print("Please enter a valid whole number for threshold.")

    elif choice == "10":
        inventory.save_inventory()
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Please enter a number from 1 to 10.")

