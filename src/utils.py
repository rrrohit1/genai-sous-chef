from google import genai
from PIL import Image
import io
import re
import pyttsx3
import config

from google.api_core import retry
from google import genai

is_retriable = lambda e: (isinstance(e, genai.errors.APIError) and e.code in {429, 503})

genai.models.Models.generate_content = retry.Retry(
    predicate=is_retriable)(genai.models.Models.generate_content)
client = genai.Client(api_key=config.GOOGLE_API_KEY)

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
    genai.configure(api_key=config.GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-pro-vision")
    with open(image_path, "rb") as f:
        img_bytes = f.read()
    image = Image.open(io.BytesIO(img_bytes))
    response = model.generate_content(["What ingredients do you see in this image?", image])
    return response.text.split("\n")

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
        str: The generated recipe as a text string.

    Note:
        - This function requires the `genai` library to be configured with a valid API key.
        - The generative model used is "gemini-pro".
    """
    prompt = f"""
    You are a professional chef AI. Given these ingredients: {', '.join(ingredients)},
    generate a creative and tasty recipe. Include:
    - A title
    - Estimated cooking time
    - Ingredients with quantities
    - Step-by-step instructions
    - A tip for enhancement
    """
    response = client.models.generate_content(
    model=config.MODEL_NAME,
    contents=prompt)
    return response.text

def generate_step_images(recipe_text):
    """
    Generates a list of images corresponding to each step in a recipe.

    This function uses a generative AI model to create visual representations
    of each step in the provided recipe text. The recipe text is split into
    individual steps, and an image is generated for each step.

    Args:
        recipe_text (str): A string containing the recipe steps, where each
            step is separated by a period and a space (". ").

    Returns:
        list of tuple: A list of tuples, where each tuple contains a recipe
        step (str) and the corresponding generated image (object).

    Example:
        recipe_text = "Chop the onions. Sauté the onions in a pan."
        images = generate_step_images(recipe_text)
        # images = [
        #     ("Chop the onions", <image_object>),
        #     ("Sauté the onions in a pan", <image_object>)
        # ]
    """
    genai.configure(api_key=config.GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-pro-vision")
    steps = [s.strip() for s in recipe_text.split(". ") if s]
    images = []
    for step in steps:
        image = model.generate_content([f"Generate an image of: {step}"])
        images.append((step, image))
    return images

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
