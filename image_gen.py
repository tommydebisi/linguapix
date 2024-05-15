import base64
import os
import requests
from modernmt import ModernMT


mmt = ModernMT("A864DC0E-CA4A-02D4-8BAC-0557155941C5")

def translate_and_generate_image(text, source_lang, size='medium'):
    """
    Translate text from Fon or Yoruba to English and generate an image from the translated text.

    Args:
        text (str): The text in Fon or Yoruba to be translated.
        source_lang (str): The source language code ('fon' for Fon, 'yor' for Yoruba).
        size (str, optional): The size of the image. Default is 'medium'.
            Available options: 'small', 'medium', 'big', 'landscape', 'portrait'.
        samples (int, optional): Number of samples to generate. Default is 1.

    Returns:
        list of bytes: List of image data in bytes format.
    """
    translated_text = translate_text(text, source_lang)
    images = generate_image_from_text(translated_text, size, 1)
    return images
def translate_text(text, source_lang):
    """
    Translate text from Fon, Yoruba, French, or English to English. If the source language is English, the text is returned as is.

    Args:
        text (str): The text to be translated.
        source_lang (str): The source language full name ('Fon', 'Yoruba', 'French', 'English').

    Returns:
        str: The translated text in English or the original text if the source language is English.
    """
    # Mapping full language names to their respective codes
    language_codes = {
        'Fon': 'fon',
        'Yoruba': 'yo',
        'French': 'fr',
        'English': 'en'
    }

    # Convert full language name to language code
    if source_lang in language_codes:
        lang_code = language_codes[source_lang]
    else:
        raise ValueError("Unsupported language. Please use 'Fon', 'Yoruba', 'French', or 'English'.")

    # If the source language is English, return the text as is
    if lang_code == 'en':
        return text

    # Assuming 'mmt' is a predefined object or function for translation
    translation = mmt.translate(lang_code, "en", text)
    print(translation.translation)
    return translation.translation



def generate_image_from_text(prompt, size='medium', samples=1):
    size = size.lower()
    engine_id = "stable-diffusion-v1-6"
    api_host = os.getenv('API_HOST', 'https://api.stability.ai')
    api_key = 'sk-Umh3hsQ1zQzl22JjXHKYPrTRQ6tkADEi3KtE8plqBlQIkBFc'

    if api_key is None:
        raise Exception("Missing Stability API key.")

    sizes = {
        'small': {'height': 512, 'width': 512},
        'medium': {'height': 1024, 'width': 1024},
        'large': {'height': 1536, 'width': 1536},
        'landscape': {'height': 768, 'width': 1024},
        'portrait': {'height': 1024, 'width': 768},
    }

    if size not in sizes:
        raise ValueError("Invalid size. Please choose from: small, medium, big, landscape, portrait.")

    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 7,
            "height": sizes[size]['height'],
            "width": sizes[size]['width'],
            "samples": samples,
            "steps": 30,
        },
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()

    images = []
    for i, image in enumerate(data["artifacts"]):
        images.append(base64.b64decode(image["base64"]))

    return images[0]



