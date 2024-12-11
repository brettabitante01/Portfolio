import pandas as pd

# Load the product data
file_path = 'sample_flooring_products.csv'  # Ensure the file is in the same directory
flooring_data = pd.read_csv(file_path)

history = []  # To keep track of user interactions

# Functions
def get_product_details(product_name=None, flooring_type=None):
    """Fetch product details based on product name or flooring type."""
    if product_name:
        product = flooring_data[flooring_data['Product Name'].str.contains(product_name, case=False, na=False)]
    elif flooring_type:
        product = flooring_data[flooring_data['Type'].str.contains(flooring_type, case=False, na=False)]
    else:
        return "Please specify a product name or type."
    
    if not product.empty:
        return product[['Product Name', 'Type', 'Price per Sq Ft', 'Installation Cost per Sq Ft']].to_dict(orient='records')
    return "Sorry, no matching products found."

def calculate_cost(product_name, area_size):
    """Calculate material, installation, and total costs for a product."""
    product = flooring_data[flooring_data['Product Name'].str.contains(product_name, case=False, na=False)]
    if product.empty:
        return "Sorry, we couldn't find that product."
    
    product = product.iloc[0]  # Get the first matching product
    material_cost = product['Price per Sq Ft'] * area_size
    installation_cost = product['Installation Cost per Sq Ft'] * area_size
    total_cost = material_cost + installation_cost
    
    if area_size < 1000:
        total_cost = max(total_cost, 250)  # Apply minimum charge for small areas
    
    return {
        "Product Name": product['Product Name'],
        "Area Size (sq ft)": area_size,
        "Material Cost": f"${material_cost:.2f}",
        "Installation Cost": f"${installation_cost:.2f}",
        "Total Cost": f"${total_cost:.2f}"
    }

# Chatbot Function
def chatbot():
    """Main chatbot interaction loop."""
    print("\nHello! Welcome to the Flooring Chatbot. 👋")
    print("I can assist you with product details, pricing, and installation costs.")
    print("Type 'help' to see all the commands or 'exit' to end the conversation.\n")
    
    while True:
        user_input = input("How can I assist you today? ").strip().lower()
        
        if user_input == "exit":
            print("\nThanks for chatting with me! Have a great day. 😊")
            break
        
        elif user_input == "list":
            print("\nHere are some of our available products:")
            print(flooring_data[['Product Name', 'Type', 'Price per Sq Ft']])
        
        elif user_input == "filter":
            flooring_type = input("\nWhat type of flooring are you looking for? (e.g., Hardwood, Tile): ").strip()
            products = get_product_details(flooring_type=flooring_type)
            if isinstance(products, list):
                print("\nHere are the products that match your filter:")
                for product in products:
                    print(f"{product['Product Name']} - ${product['Price per Sq Ft']}/sq ft")
            else:
                print(products)
        
        elif user_input == "product":
            product_name = input("\nWhat product would you like more details about? ").strip()
            details = get_product_details(product_name=product_name)
            history.append(f"Inquired about product: {product_name}.")
            print("\nProduct Details:")
            print(details if details != "Sorry, no matching products found." else details)
        
        elif user_input == "cost":
            product_name = input("\nWhich product do you want to calculate the cost for? ").strip()
            if flooring_data['Product Name'].str.contains(product_name, case=False, na=False).any():
                try:
                    area_size = float(input("Please enter the area size in square feet: "))
                    if area_size > 0:
                        cost = calculate_cost(product_name, area_size)
                        history.append(f"Calculated cost for {product_name}: {cost}.")
                        print("\nCost Details:")
                        for key, value in cost.items():
                            print(f"{key}: {value}")
                    else:
                        print("The area size must be a positive number.")
                except ValueError:
                    print("Oops! Please enter a valid number for the area size.")
            else:
                print("Sorry, we couldn't find that product.")
        
        elif user_input == "help":
            print("""
Here's a list of commands you can use:
- 'list': Show all available products
- 'filter': Filter products by type (e.g., Hardwood, Tile)
- 'product': Get detailed information about a specific product
- 'cost': Calculate the cost of material and installation
- 'summary': View a summary of your interactions
- 'save': Save the conversation history to a file
- 'exit': End the chat session
            """)
        
        elif user_input == "summary":
            if history:
                print("\nHere's a summary of your interactions with me:")
                for entry in history:
                    print(f"- {entry}")
            else:
                print("\nYou haven't had any interactions yet.")
        
        elif user_input == "save":
            with open("chatbot_conversation.txt", "w") as file:
                file.write("\n".join(history))
            print("\nYour conversation has been saved as 'chatbot_conversation.txt'.")
        
        else:
            print("\nI'm sorry, I didn't quite get that. Type 'help' for a list of commands.")

# Run the chatbot
chatbot()
