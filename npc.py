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
        """Make the purchase using the calculate_total_cost method in the ShoppingCart class.

        If Golden Customer gets a 10% discount."""
        total_cost = round(self.basket.calculate_total_cost(), 2)
        if self.customer_type == 'golden customer':
            total_cost *= 0.9

        if total_cost > self.balance:
            raise ValueError(f'Customer {self.customer_id} Purchase failed: Insufficient funds.')

        for item, quantity in self.basket.items:
            for shop_item in shop.items:
                if shop_item.name == item.name:
                    if quantity > shop_item.quantity:
                        raise ValueError(f'Customer {self.customer_id} Purchase failed: Insufficient quantity for {item.name}.')
                    break

        """Save the purchase date and details.

        Also save the details of the Eshop by calling the Eshop process_purchase method."""
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


def test_customer_make_purchase():
    # Create an instance of EShop
    shop = EShop()

    # Create an instance of Customer
    customer = Customer("C1", "regular customer", 100.0)

    # Create some items and add them to the EShop
    item1 = Item("Item1", 10.0, 5)
    item2 = Item("Item2", 20.0, 3)
    shop.add_item(item1)
    shop.add_item(item2)

    # Add items to the customer's shopping cart
    customer.basket.add_item(item1, 1)
    customer.basket.add_item(item2, 1)

    # Make a purchase
    customer.make_purchase(shop)

    # Assert the customer's purchase history is updated
    assert len(customer.purchase_history) == 1

    # Assert the customer's balance is updated
    assert customer.balance == 70.0

    # Assert the item quantities are updated in the EShop
    assert item1.quantity == 4
    assert item2.quantity == 2


def test_customer_make_purchase_insufficient_funds():
    # Create an instance of EShop
    shop = EShop()

    # Create an instance of Customer with insufficient funds
    customer = Customer("C2", "golden customer", 5.0)

    # Create an item and add it to the EShop
    item = Item("Item1", 10.0, 5)
    shop.add_item(item)

    # Add the item to the customer's shopping cart
    customer.basket.add_item(item)

    # Make a purchase with insufficient funds
    try:
        customer.make_purchase(shop)
    except ValueError as e:
        # Assert the correct exception is raised
        assert str(e) == "Customer C2 Purchase failed: Insufficient funds."

    # Assert the customer's purchase history is not updated
    assert len(customer.purchase_history) == 0

    # Assert the customer's balance is unchanged
    assert customer.balance == 5.0

    # Assert the item quantity is unchanged in the EShop
    assert item.quantity == 5


def test_customer_make_purchase_edge_case():
    # Create an instance of EShop
    shop = EShop()

    # Create an instance of Customer
    customer = Customer("C3", "golden customer", 100.0)

    # Create an item and add it to the EShop
    item = Item("Item1", 10.0, 5)
    shop.add_item(item)

    # Add the item to the customer's shopping cart with a quantity greater than available stock
    customer.basket.add_item(item, 10)

    # Make a purchase with quantity greater than available stock
    try:
        customer.make_purchase(shop)
    except ValueError as e:
        # Assert the correct exception is raised
        assert str(e) == f"Customer C3 Purchase failed: Insufficient quantity for {item.name}."

    # Assert the customer's purchase history is not updated
    assert len(customer.purchase_history) == 0

    # Assert the customer's balance is unchanged
    assert customer.balance == 100.0

    # Assert the item quantity is unchanged in the EShop
    assert item.quantity == 5

# Run the tests
test_customer_make_purchase()
test_customer_make_purchase_insufficient_funds()
test_customer_make_purchase_edge_case()