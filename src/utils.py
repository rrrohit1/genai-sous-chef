from google import genai
from PIL import Image
import io
import re
import pyttsx3
import config
import json
from google.api_core import retry
from google import genai
from google.genai import types
from io import BytesIO

is_retriable = lambda e: (isinstance(e, genai.errors.APIError) and e.code in {429, 503})

genai.models.Models.generate_content = retry.Retry(
    predicate=is_retriable)(genai.models.Models.generate_content)
client = genai.Client(api_key=config.GOOGLE_API_KEY)


def get_dict_from_response(response):
    try:
        # Extract JSON from the response
        return json.loads(response.text.strip("```json\n").strip("```"))
    except json.JSONDecodeError as e:
        # Handle the case where the response is not valid JSON
        print(e)
        return None

def detect_ingredients(image_path):
    """
    Detects ingredients present in an image using a generative AI model.

    Args:
        image_path (str): The file path to the image to be analyzed.

    Returns:
        list: A list of ingredients detected in the image.

    Note:
        - This function requires the `genai` library to be configured with a valid API key.
        - The generative model used is "gemini-pro-vision".
        - Ensure the image file exists and is accessible at the specified path.
    """
    img = Image.open(image_path)
    prompt = """What food ingredients do you see in this photo?
                Return ONLY a simple comma-separated list of ingredients without any additional text, explanations, or formatting.
                For example: "tomatoes, onions, garlic, chicken" or "flour, sugar, eggs, milk"
                Do not include any commentary, introductions, or conclusions.
            """

    response = client.models.generate_content(model=config.MODEL_NAME, contents=[prompt, img])
    raw_text = response.text

    raw_ingredients = [i.strip().lower() for i in raw_text.split(",") if i.strip()]
    return raw_ingredients

def normalize_ingredients(raw_ingredients):
    """
    Normalize a list of raw ingredient names by mapping variants to a standard form.

    This function takes a list of raw ingredient names, removes non-alphabetic characters,
    converts them to lowercase, and maps known variants to a standard form based on a predefined
    mapping. If an ingredient does not match any known variants, it is included as-is in the
    normalized list.

    Args:
        raw_ingredients (list of str): A list of raw ingredient names to be normalized.

    Returns:
        list of str: A list of unique normalized ingredient names.
    """
    mapping = {"bell pepper": ["capsicum", "bellpepper"], "tomato": ["cherry tomato", "roma tomato"]}
    normalized = []
    for item in raw_ingredients:
        clean_item = re.sub(r"[^a-zA-Z ]", "", item).lower()
        found = False
        for key, variants in mapping.items():
            if clean_item in variants or clean_item == key:
                normalized.append(key)
                found = True
                break
        if not found:
            normalized.append(clean_item)
    return list(set(normalized))

def generate_recipe(ingredients):
    """
    Generates a recipe based on the provided list of ingredients using a generative AI model.

    Args:
        ingredients (list of str): A list of ingredient names to be used in the recipe.

    Returns:
        dict: The generated recipe is returned as a dictionary.

    Note:
        - This function requires the `genai` library to be configured with a valid API key.
        - The generative model used is "gemini-pro".
    """
    prompt = f"""
    You are a professional chef AI. Given these ingredients: {', '.join(ingredients)},
    generate a creative and tasty recipe in the following format:
    dict: The generated recipe is returned as a dictionary containing:
            - title (str): The title of the recipe.
            - cooking_time (str): The estimated cooking time.
            - ingredients (list of str): A list of ingredients with quantities.
            - instructions (list of str): Step-by-step instructions for the recipe.
            - tip (str): A tip for enhancing the dish.
    Example:
        {{"tite": "Spaghetti Aglio e Olio",
         "cooking_time": "20 minutes",
         "ingredients": ["spaghetti: 200g", "garlic: 4 cloves", "olive oil: 50ml"],
         "instructions": ["Boil water.", "Add spaghetti.", "Sauté garlic."],
         "tip": "Use fresh parsley for garnish."}}
    Only return the recipe in the specified format without any additional text or explanations.
    """
    response = client.models.generate_content(
    model=config.MODEL_NAME,
    contents=prompt)

    response_dict = get_dict_from_response(response)
    return response_dict


def generate_step_images(recipe):
    """
    Generate images for each step in a recipe using Gemini's multimodal model.

    Args:
        recipe (dict): Must contain a list of instruction steps under the key "instructions".

    Returns:
        list of PIL.Image.Image: Images representing each recipe step.

    Notes:
        - Uses 'gemini-2.0-flash-exp-image-generation'.
        - Text responses are printed; images are returned.
        - Assumes a configured Gemini client named `client`.
    """

    images = []
    for step in recipe["instructions"]:
        image_response = client.models.generate_content(
            model="gemini-2.0-flash-exp-image-generation",
            contents=f"Generate an image for this step: {step}",
            config=types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE'],
            # system_instruction="You are a helpful assistant that generates images for cooking instructions. You will help me create images for each step of the recipe.",
            ))

        for part in image_response.candidates[0].content.parts:
            if part.text is not None:
                print(part.text)
            elif part.inline_data is not None:
                image = Image.open(BytesIO((part.inline_data.data)))
                # image.save(response["title"] + "/" + step + ".jpg")
                images.append(image)
                # print("Image saved for step:", step)
    return images

def get_nutrition_info(recipe):
    """
        Calculate the approximate total nutritional values for a given recipe.
        This function uses a nutritionist AI model to estimate the nutritional 
        content of a recipe based on its list of ingredients. The output is a 
        dictionary containing the total protein, fat, carbohydrates, and calories 
        for the entire recipe.
        Args:
            recipe (dict): A dictionary containing recipe details. It must include 
                        a key 'ingredients', which is a list of ingredients 
                        used in the recipe.
        Returns:
            dict: A dictionary with the following keys and their corresponding 
                nutritional values (rounded to the nearest whole number):
    """
    nutrient_PROMPT = f""" 
                    You are a nutritionist AI. Given the following list of ingredients: {recipe['ingredients']}, 
                    calculate the approximate total nutritional values for the entire recipe. Return only a dictionary with the following keys:
                    - "protein (in g)"
                    - "fat (in g)"
                    - "carbohydrates (in g)"
                    - "calories (in kcal)"
                
                    Round all values to the nearest whole number. Do not include any explanation—just return the dictionary.
                    Example output: 
                    {{
                        "protein (in g)": 18,
                        "fat (in g)": 22, 
                        "carbohydrates (in g)": 45, 
                        "calories (in kcal)": 450 
                    }}
                    """

    nutrient_response = client.models.generate_content(
        model=config.MODEL_NAME,
        contents=nutrient_PROMPT)
    nutrient_response_dict = get_dict_from_response(nutrient_response)
    return nutrient_response_dict

def narrate_recipe(recipe_text):
    """
    Converts the given recipe text into speech using a text-to-speech engine.

    Args:
        recipe_text (str): The text of the recipe to be narrated.

    Returns:
        None
    """
    engine = pyttsx3.init()
    engine.say(recipe_text)
    engine.runAndWait()



######### Plots #########
import matplotlib.pyplot as plt

def show_images_with_text(images, texts):
    n = len(images)
    fig, axs = plt.subplots(n, 2, figsize=(10, 2 * n))
    if n == 1:
        axs = [axs]  # Ensure it's iterable when n=1

    for i in range(n):
        # Show text
        axs[i][0].axis('off')
        axs[i][0].text(0.01, 0.5, texts[i], fontsize=12, va='center', wrap=True)

        # Show image
        axs[i][1].imshow(images[i])
        axs[i][1].axis('off')

    plt.tight_layout()
    plt.show()
