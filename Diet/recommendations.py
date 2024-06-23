import numpy as np
from openvino.runtime import Core
import random


def get_predictions(user_id=0, num_recommendations=3):
    food_selections = [
        "Spaghetti Carbonara", "Tacos al Pastor", "Sushi", "Pad Thai", "Beef Stroganoff",
        "Chicken Tikka Masala", "Shrimp Scampi", "Lasagna", "Falafel", "Ramen",
        "Bangers and Mash", "Chiles Rellenos", "Chicken Alfredo", "Gyro", "French Onion Soup",
        "Beef Wellington", "Chicken Fajitas", "Moussaka", "Eggs Benedict", "Peking Duck",
        "Paella", "Fish and Chips", "Bibimbap", "Chicken Cordon Bleu", "Pizza Margherita",
        "Lamb Shawarma", "Vegetable Stir Fry", "Pulled Pork Sandwich", "Goulash", "Ratatouille",
        "Miso Soup", "Beef Tacos", "Chicken Parmesan", "Stuffed Peppers", "Huevos Rancheros",
        "Ceviche", "Bruschetta", "Calamari", "Pasta Primavera", "Kung Pao Chicken",
        "Clam Chowder", "Pho", "Gazpacho", "Chicken Satay", "Pulled Chicken Tacos",
        "Biryani", "Beef Bourguignon", "Chana Masala", "Enchiladas", "Chicken Quesadilla",
        "Vegetable Curry", "Samosa", "Fettuccine Alfredo", "Tuna Tartare", "Mushroom Risotto",
        "Shrimp Tacos", "Shakshuka", "Paneer Butter Masala", "Teriyaki Chicken", "Chicken Wings",
        "Salmon Sushi", "Lamb Kebab", "Veggie Burger", "Pasta Carbonara", "Prawn Cocktail",
        "Chicken Caesar Salad", "Pesto Pasta", "Tom Yum Soup", "Churrasco", "Mango Sticky Rice",
        "Pepperoni Pizza", "Shepherd's Pie", "Beef Nachos", "Caesar Salad", "Fried Rice",
        "Mojito Chicken", "Chicken Shawarma", "Eggplant Parmesan", "Hummus", "Roast Beef",
        "Chili Con Carne", "Sichuan Beef", "Vegetable Paella", "Sushi Roll", "Grilled Cheese Sandwich",
        "Chicken Pad See Ew", "Jambalaya", "BBQ Ribs", "Caprese Salad", "Omelette",
        "Chicken Burrito", "Peking Pork", "Coconut Shrimp", "Lamb Vindaloo", "Turkey Sandwich",
        "Beef Burrito", "Margherita Pizza", "Greek Salad", "Chicken Souvlaki", "Hot and Sour Soup",
        "Stuffed Cabbage Rolls", "Lobster Bisque", "Vegetable Soup", "Chicken Pot Pie", "Tzatziki",
        "Baked Ziti", "Bulgogi", "Pasta Bolognese", "Minestrone Soup", "Chicken Fried Rice",
        "Shish Kebab", "Black Bean Soup", "Queso Fundido", "Duck Confit", "Spinach Salad",
        "Pulled Pork", "Shrimp Fried Rice", "Chicken Tenders", "Beef Empanadas", "Chicken Salad",
        "Veggie Wrap", "Fried Chicken", "Prawn Tempura", "Lentil Soup", "Caprese Skewers",
        "Beef Teriyaki", "Chicken Piccata", "Vegetarian Chili", "Fish Tacos", "Egg Salad Sandwich",
        "Chicken Gyro", "Tomato Basil Soup", "Bacon Cheeseburger", "Garlic Shrimp", "Lamb Chops",
        "Buffalo Wings", "Veggie Pizza", "Chicken Marsala", "Crab Cakes", "Fajita",
        "Quiche Lorraine", "Zucchini Noodles", "Chicken Milanese", "Pumpkin Soup", "Beef Fajitas",
        "Cauliflower Tacos", "Clam Linguine", "Cheese Fondue", "Katsu Curry", "Tortilla Soup",
        "Steak Sandwich", "Vegetable Lasagna", "Chicken Gyro Wrap", "BBQ Chicken Pizza", "Egg Drop Soup",
        "Beef Rendang", "Shrimp Linguine", "Chicken Shawarma Wrap", "Pasta Salad", "Fried Calamari",
        "Lamb Curry", "Spicy Tuna Roll", "Chicken Noodle Soup", "Bratwurst", "Vegetarian Quesadilla",
        "Chicken Enchiladas", "Beef Bulgogi", "Gnocchi", "Tom Yum Goong", "Tofu Stir Fry",
        "Pork Chops", "Lamb Rogan Josh", "Chicken Soup", "Veggie Tacos", "Spaghetti Marinara",
        "Stuffed Mushrooms", "Beef Stew", "Crab Rangoon", "Chicken Ramen", "Seafood Paella",
        "Stuffed Zucchini", "Prawn Fried Rice", "BBQ Pulled Chicken", "Lamb Gyro", "Vegetarian Pizza",
        "Chicken Curry", "Shrimp Scampi Pasta", "Pork Belly", "Salmon Salad", "Falafel Wrap",
        "Vegetable Korma", "Chicken Schnitzel", "Prawn Laksa", "Stuffed Tomatoes", "Beef Carpaccio",
        "Pulled Pork Tacos", "Chicken Nachos", "Thai Green Curry", "Vegetable Spring Rolls", "Garlic Bread",
        "Salmon Teriyaki", "Grilled Vegetables", "Chicken Cacciatore", "Stuffed Bell Peppers", "Pork Dumplings",
        "Chicken Pho", "Vegetable Tempura", "Beef Tartar", "Chicken Empanadas", "Spaghetti Bolognese",
        "Veggie Pasta", "Prawn Risotto", "Pork Ribs"]
    # Load the OpenVINO runtime
    core = Core()

    # Load the network
    model_path = "./model/recommendation_model.xml"  # Path to your OpenVINO IR model
    compiled_model = core.compile_model(model_path, "CPU")

    # Get input and output layers
    input_layer_user = compiled_model.input("user_id")
    input_layer_item = compiled_model.input("item_id")
    output_layer = compiled_model.output("output")

    # Run inference
    # go through 10x the number of recommendations needed and take the top tenth of them
    results = []
    max_scores = []
    max_foods = []

    for x in range(num_recommendations*10):
        index = random.randint(0, len(food_selections))
        if len(max_scores) < num_recommendations:
            max_scores.append(compiled_model([user_id, index])[output_layer])
            max_foods.append(food_selections[index])
        else:
            score = compiled_model([user_id, index])[output_layer]
            min_score = min(max_scores)
            if score > min_score:
                min_index = max_scores.index(min_score)
                max_scores[min_index] = score
                max_foods[min_index] = food_selections[index]
    for x in range(num_recommendations):
        results.append({"food": max_foods[x], "score": max_scores[x]})
        
    return results

print(get_predictions())