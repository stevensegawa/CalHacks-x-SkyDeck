import gradio as gr
from claude_calorie_counter import calorie_count
from PIL import Image
from numpy import asarray
# import matplotlib.pyplot as plt

# Formats frontend
def calorie_counter():
    # plt.imsave('converted_img.png', input_imgarr, cmap='Greys') -- use to convert nparray to filepath
    # Load the image and convert into numpy array
    img = Image.open('images/converted_img.png')
    numpydata = asarray(img)

    response = calorie_count('images/converted_img.png')
    return [numpydata, response]

demo = gr.Interface(calorie_counter, inputs=[], outputs=["image", "textbox"])
if __name__ == "__main__":
    demo.launch()