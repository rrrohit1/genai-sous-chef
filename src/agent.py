from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
from utils import generate_recipe, generate_step_images, get_nutrition_info, show_images_with_text
import config # TEXT_MODEL_NAME, IMAGE_MODEL_NAME
import pprint
import __main__

# Step 1: Define the state schema
class RecipeState(TypedDict):
    ingredients: Annotated[list[str], "The user provided ingredients."]
    text_model: Annotated[str, "Gemini model for text generation."]
    image_model: Annotated[str, "Gemini model for image generation."]
    recipe: Annotated[dict, "The generated recipe dictionary."]
    step_images: Annotated[list, "List of step-wise PIL images."]
    nutrition_info: Annotated[dict, "Nutritional information dictionary."]

# Step 2: Define the nodes
def recipe_node(state: RecipeState) -> RecipeState:
    recipe = generate_recipe(state["ingredients"], selected_model=state["text_model"])
    return {**state, "recipe": recipe}

def image_node(state: RecipeState) -> RecipeState:
    images = generate_step_images(state["recipe"], selected_model=state["image_model"])
    step_texts = state["recipe"]["instructions"]

    if hasattr(__main__, '__file__') and __main__.__file__.endswith("main.py"):
        show_images_with_text(images, step_texts)

    return {**state, "step_images": images}

def nutrition_node(state: RecipeState) -> RecipeState:
    nutrition = get_nutrition_info(state["recipe"], selected_model=state["text_model"])
    return {**state, "nutrition_info": nutrition}

# Step 3: Create LangGraph workflow
def build_graph():
    builder = StateGraph(RecipeState)

    builder.add_node("generate_recipe", recipe_node)
    builder.add_node("generate_images", image_node)
    builder.add_node("get_nutrition", nutrition_node)

    builder.set_entry_point("generate_recipe")
    builder.add_edge("generate_recipe", "generate_images")
    builder.add_edge("generate_images", "get_nutrition")
    builder.add_edge("get_nutrition", END)

    return builder.compile()

# Step 4: Run the graph
if __name__ == "__main__":
    graph = build_graph()
    ingredients = ["tomato", "onion", "bell pepper", "garlic"]
    final_state = graph.invoke({
        "ingredients": ingredients,
        "text_model": config.TEXT_MODEL_NAME,
        "image_model": config.IMAGE_MODEL_NAME
    })

    print("\n🔹 Final Recipe Output:\n")
    pprint.pprint(final_state["recipe"])
    print("\n🧠 Nutrition Info:\n")
    pprint.pprint(final_state["nutrition_info"])
    print("\n🖼️ Images for each step were shown above (if running from CLI).\n")
