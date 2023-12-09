import gradio as gr
from PIL import Image

def display_image():
    image_path = "path/to/your/image.jpg"  # Set your image path here
    image = Image.open(image_path)
    return image

img_window = gr.Image()
iface = gr.Interface(fn=display_image, inputs=[], outputs=img_window)

iface.launch()
