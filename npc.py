from datetime import datetime

class Customer:
    def __init__(self, customer_id, customer_type, balance):
        """Give the customer an ID and a type(golden, regular). 
        
        Their basket is an instance of the ShoppingCart class and the list is their puchase history."""
        self.customer_id = customer_id
        self.customer_type = customer_type
        self.basket = ShoppingCart()
        self.purchase_history = []
        self.balance = balance

    def __repr__(self):
        """Provide a representation of the customer object."""
        return f'Customer ID: {self.customer_id}\nType: {self.customer_type}'

    def view_purchase_history(self):
        """Let the customer view their purchase history.
        
        Prints out the purchase history in reverse order aka from newest to oldest."""
        print(f'{self.customer_id} Purchase History:')
        if len(self.purchase_history) == 0:
            print('No recent purchases.')
        for purchase in self.purchase_history[::-1]:
            print(purchase)

    def make_purchase(self, shop):
        """Make the purchase using the calculate_total_cost class in the ShoppingCart class.

        If Golden Customer get 10% discount."""
        total_cost = round(self.basket.calculate_total_cost(), 2)
        if self.customer_type == 'golden customer':
            total_cost *= 0.9

        if total_cost > self.balance:
            raise ValueError(f'Customer {self.customer_id} Purchase failed: Insufficient funds.')

        """Save the purchase date and details.
        
        Also save the details of the Eshop by calling the Eshop process_purchase function."""
        purchase_date = datetime.now().strftime("%d.%m.%Y")
        purchase_details = f'Purchase date: {purchase_date}\nItems: {self.basket}\nTotal Cost: {total_cost}'
        self.purchase_history.append(purchase_details)
        shop.process_purchase(self, total_cost)
        print(f'{self.customer_id} Purchase successful!')

    def get_customer_balance(self):
        """Stat check."""
        return f'{self.customer_id} Current balance: {round(self.balance, 2)}'


class Item:
    def __init__(self, name, price, quantity):
        """Give a name a price and quantity to an item in the EShop."""
        self.name = name
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        """Represent the item in string form."""
        return f'{self.name}: {self.price}\nquantity left: {self.quantity}'

class ShoppingCart:
    """A shopping cart for the customer to use."""
    def __init__(self):
        self.items = []

    def __repr__(self):
        """Represent the entire shopping cart."""
        return ', '.join([f'{item.name} ({quantity})' for item, quantity in self.items])

    def add_item(self, item: Item, quantity=1):
        """Add an item into the shopping cart with a default quantity of 1."""
        self.items.append((item, quantity))

    def remove_item(self, item: Item):
        """Remove a specific item from the shopping cart."""
        for x, (cart_item, _) in enumerate(self.items):
            if cart_item == item:
                del self.items[x]
                break

    def increase_quantity(self, item: Item, quantity):
        """Increase the quantity of a specific item in the shopping cart."""
        for x, (cart_item, cart_quantity) in enumerate(self.items):
            if cart_item == item:
                self.items[x] = (cart_item, cart_quantity + quantity)
                break

    def decrease_quantity(self, item: Item, quantity):
        """Vice versa."""
        for x, (cart_item, cart_quantity) in enumerate(self.items):
            if cart_item == item:
                if cart_quantity - quantity <= 0:
                    del self.items[x]
                else:
                    self.items[x] = (cart_item, cart_quantity - quantity)
                break

    def calculate_total_cost(self):
        """Calculate total cost of the shopping cart."""
        return sum(item.price * quantity for item, quantity in self.items)


class EShop:
    def __init__(self):
        """The online shop.
        
        Has list of the items, customers and purchase records."""
        self.items = []
        self.customers = []
        self.purchase_records = []

    def __repr__(self):
        """Represent all the items currently in the EShop and the number of customers."""
        return f'EShop Details:\nItems: {", ".join(str(item) for item in self.items)}\nCustomers: {len(self.customers)}'\

    def add_item(self, item: Item):
        """Add an item to the shop's inventory."""
        self.items.append(item)

    def add_customer(self, customer: Customer):
        """Add a customer."""
        self.customers.append(customer)

    def process_purchase(self, customer: Customer, total_cost):
        """Process a purchase made by a customer."""
        total_cost = round(total_cost, 2)
        self.purchase_records.append((customer, total_cost))
        self.decrease_customer_balance(customer, total_cost)
        self.decrease_item_quantities(customer.basket)

    def decrease_customer_balance(self, customer: Customer, amount):
        """Decrease customer balance after a purchase."""
        customer.balance -= amount

    def decrease_item_quantities(self, basket: ShoppingCart):
        """Decrease item quantities from the EShop."""
        for item, quantity in basket.items:
            for shop_item in self.items:
                if shop_item.name == item.name:
                    shop_item.quantity -= quantity
                    break
    
    def shop_purchase_history(self):
        print('EShop purchase history:')
        for purchase in self.purchase_records[::-1]:
            print(purchase)


if __name__ == '__main__':
    """Default test."""
    # Create an instance of the EShop
    shop = EShop()

    # Create some items and add them to the shop
    item1 = Item('$11 milk', 10.99, 5)
    item2 = Item('post-inflation chips', 5.99, 10)
    item3 = Item('bread buy 6 get 1 free', 7.49, 3)
    shop.add_item(item1)
    shop.add_item(item2)
    shop.add_item(item3)

    # Create some customers and add them to the shop
    customer1 = Customer('Timothy', 'regular', 100.0)
    customer2 = Customer('Carl', 'golden customer', 200.0)
    customer3 = Customer('My dad (went for milk)', 'regular', 150.0)
    customer4 = Customer('King Alexander I of Yugoslavia', 'golden customer', 300.0)
    shop.add_customer(customer1)
    shop.add_customer(customer2)
    shop.add_customer(customer3)
    shop.add_customer(customer4)

    # Add items to customers' shopping carts
    customer1.basket.add_item(item1, 2)
    customer2.basket.add_item(item2, 3)
    customer3.basket.add_item(item1, 1)
    customer3.basket.add_item(item3, 2)
    customer4.basket.add_item(item2, 4)
    customer4.basket.add_item(item3, 1)

    # Test view_purchase_history method
    customer1.view_purchase_history()

    customer2.view_purchase_history()

    customer3.view_purchase_history()

    customer4.view_purchase_history()

    # Test make_purchase method
    try:
        customer1.make_purchase(shop)
    except ValueError as e:
        print(str(e))

    try:
        customer2.make_purchase(shop)
    except ValueError as e:
        print(str(e))

    try:
        customer3.make_purchase(shop)
    except ValueError as e:
        print(str(e))

    try:
        customer4.make_purchase(shop)
    except ValueError as e:
        print(str(e))

    # Test view_purchase_history method
    customer1.view_purchase_history()

    customer2.view_purchase_history()

    customer3.view_purchase_history()

    customer4.view_purchase_history()

    # Test updated balances and item quantities
    print(customer1.get_customer_balance())
    print(customer2.get_customer_balance())
    print(customer3.get_customer_balance())
    print(customer4.get_customer_balance())

    print('Item 1 Quantity:', item1.quantity)
    print('Item 2 Quantity:', item2.quantity)
    print('Item 3 Quantity:', item3.quantity)

    # Print EShop representation
    print(shop)

    # Print EShop purchase history
    shop.shop_purchase_history()



if __name__ == '__main__':
    """Edge case."""
    # Create an instance of the EShop
    shop = EShop()

    # Create an item and add it to the shop
    item1 = Item('Item 1', 10.99, 5)
    shop.add_item(item1)

    # Create a customer and add them to the shop with a low balance
    customer = Customer(1, 'regular', 5.0)
    shop.add_customer(customer)

    # Add the item to the customer's shopping cart
    customer.basket.add_item(item1)

    # Print customer balance and item quantity
    print(f'\n\n\n{customer.get_customer_balance()}')
    print('Item Quantity:', item1.quantity)

    # Test make_purchase method with insufficient funds
    try:
        customer.make_purchase(shop)
    except ValueError as e:
        print(str(e))

    # Print updated balance and item quantity
    print(customer.get_customer_balance())
    print('Item Quantity:', item1.quantity)

    # Print EShop representation
    print(shop)

    # Print EShop purchase history
    shop.shop_purchase_history()