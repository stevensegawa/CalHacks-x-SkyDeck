from openai import OpenAI
import base64
import requests

def calorie_count(image_path):
    # OpenAI API Key
    api_key = 'sk-proj-sY9f35luVvB3WBqBtnZZT3BlbkFJdeUiFzlLeMqZ4VHA2rTh'

    # Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4o",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": "Give me a bullet pointed list of all the individual food ingredients in this dish with the approximate proportion like tablespoons, ounces, cups, etc. in parenthesis. Next to each bullet point, predict how many calories it contributes to the meal. At the end, provide a predicted total calorie count of the meal. Don't add any formatting to text (bold, italics, etc.)"
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()['choices'][0]['message']['content']

if __name__ == "__main__":
    text_response = calorie_count('images/food.png')
    print(text_response)