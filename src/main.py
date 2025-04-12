from utils import *
import argparse

def main():
    parser = argparse.ArgumentParser(description="Generate a recipe from a list of ingredients.")
    parser.add_argument("--ingredients", nargs="+", required=True, help="List of ingredients")
    args = parser.parse_args()

    # ingredients = detect_ingredients("data/pantry_sample.jpg")

    # normalized = normalize_ingredients(ingredients)

    # recipe = generate_recipe(normalized)

    print("\nGenerating recipe...\n")
    recipe = generate_recipe(args.ingredients)
    
    return recipe

    # visuals = generate_step_images(recipe)

    # narration = narrate_recipe(recipe)


if __name__ == "__main__":
    main()
