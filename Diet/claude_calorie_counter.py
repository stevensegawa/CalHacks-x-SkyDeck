from anthropic import AnthropicBedrock
from PIL import Image
import base64

def calorie_count(img_path):
    # Convert the file path to processable image data
    image_type = "image/png"
    pil_image = Image.open(img_path)
    compressed_img = pil_image.convert("P", palette=Image.ADAPTIVE, colors=256)
    compressed_img.save("images/converted_img.png", optimize=True)
    local_image_path = 'images/converted_img.png'

    with open(local_image_path, "rb") as image_file:
        image_content = image_file.read()
    image_data = base64.b64encode(image_content).decode("utf-8")

    client = AnthropicBedrock(
        aws_access_key="AKIA3JQGRBJNQA7UBWWT",
        aws_secret_key="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",
        aws_region="us-east-1",
    )

    message = client.messages.create(
        model="anthropic.claude-3-5-sonnet-20240620-v1:0",
        max_tokens=10000,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": image_type,
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": "Give me a bullet pointed list of all the individual food ingredients in this dish with the approximate proportion like tablespoons, ounces, cups, etc. in parenthesis. Next to each bullet point, predict how many calories it contributes to the meal. At the end, provide a predicted total calorie count of the meal. Don't add any formatting to text (bold, italics, etc.). Don't explain anything, just give the bullet points, measurements, calories, and total calories."
                    }
                ],
            }
        ],
    )
    return message.content[0].text

if __name__ == "__main__":
    text_response = calorie_count('images/food.png')
    print(text_response)