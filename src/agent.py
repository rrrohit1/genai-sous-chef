from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
from utils import generate_recipe, generate_step_images, get_nutrition_info
import pprint

# Step 1: Define the state schema
class RecipeState(TypedDict):
    ingredients: Annotated[list[str], "The user provided ingredients."]
    recipe: Annotated[dict, "The generated recipe dictionary."]
    step_images: Annotated[list, "List of step-wise PIL images."]
    nutrition_info: Annotated[dict, "Nutritional information dictionary."]

# Step 2: Define the nodes
def recipe_node(state: RecipeState) -> RecipeState:
    recipe = generate_recipe(state["ingredients"])
    return {**state, "recipe": recipe}

def image_node(state: RecipeState) -> RecipeState:
    images = generate_step_images(state["recipe"])
    return {**state, "step_images": images}

def nutrition_node(state: RecipeState) -> RecipeState:
    nutrition = get_nutrition_info(state["recipe"])
    return {**state, "nutrition_info": nutrition}

# Step 3: Create LangGraph workflow
def build_graph():
    builder = StateGraph(RecipeState)

    # Add nodes
    builder.add_node("generate_recipe", recipe_node)
    builder.add_node("generate_images", image_node)
    builder.add_node("get_nutrition", nutrition_node)

    # Set flow
    builder.set_entry_point("generate_recipe")
    builder.add_edge("generate_recipe", "generate_images")
    builder.add_edge("generate_images", "get_nutrition")
    builder.add_edge("get_nutrition", END)

    return builder.compile()

# Step 4: Run the graph
if __name__ == "__main__":
    graph = build_graph()
    ingredients = ["tomato", "onion", "bell pepper", "garlic"]  # Example input
    final_state = graph.invoke({"ingredients": ingredients})

    print("\n Final Recipe Output:\n")
    pprint.pprint(final_state["recipe"])
    print("\n Nutrition Info:\n")
    pprint.pprint(final_state["nutrition_info"])
    print("\n Generated images for each step available in `final_state['step_images']`\n")
