import gradio as gr
<<<<<<< HEAD
from PIL import Image

def display_image():
    image_path = "path/to/your/image.jpg"  # Set your image path here
    image = Image.open(image_path)
    return image

img_window = gr.Image()
iface = gr.Interface(fn=display_image, inputs=[], outputs=img_window)

iface.launch()
=======
import time

def slowly_reverse(word, progress=gr.Progress()):
    progress(0, desc="Starting")
    time.sleep(1)
    progress(0.05)
    new_string = ""
    for letter in progress.tqdm(word, desc="Reversing"):
        time.sleep(0.25)
        new_string = letter + new_string
    return new_string

demo = gr.Interface(slowly_reverse, gr.Text(), gr.Text())

demo.launch()
>>>>>>> 93bbb3bf06d675fe821036466f01e32d2245e7af
