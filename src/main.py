from utils import *

if __name__ == "__main__":
    ingredients = detect_ingredients("data/pantry_sample.jpg")

    normalized = normalize_ingredients(ingredients)

    recipe = generate_recipe(normalized)

    visuals = generate_step_images(recipe)

    narration = narrate_recipe(recipe)