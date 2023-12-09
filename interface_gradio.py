import gradio as gr
from face_recog import compare, take_picture
from database import write_to_database, read_from_database
from PIL import Image


theme = gr.themes.Base(
    primary_hue="green",
    secondary_hue="red",
)


alpha_mode = True


if not alpha_mode:
    from stm32 import lock_signal_stm32, unlock_signal_stm32
    write_to_database(1, None)
    write_to_database(2, None)
else:
    # write_to_database(1, None)
    # write_to_database(2, 'img_database/1.jpg')
    pass

def load_image(image_path):
        image = Image.open("img_database/23.jpg")
        return image

def lock(locker_number):
    print(f"Lock scanning {locker_number=}")
    saved_path = take_picture()
    print("Showing the image to the user")
    gr.Interface(fn=load_image, inputs="text", outputs=img_window).launch()
    write_to_database(locker_number=1, path=saved_path)

    print(f"sending lock signal  {locker_number=}")
    if not alpha_mode:
        if unlock_signal_stm32(locker_number=1):
            print("unlocked successful")
        else:
            print("fuckkkkk")
    return f"Locker {locker_number} is locked", load_image(saved_path)


def unlock(locker_number):
    print(f"Unlock scanning  {locker_number=}")
    saved_path = read_from_database(locker_number=1)
    comapare_path = take_picture()
    print(comapare_path)
    x = compare(target=saved_path, input=comapare_path)
    if x:
        print(f"sending unlock signal  {locker_number=}")
        if not alpha_mode:
            if unlock_signal_stm32(locker_number=1):
                print("unlocked successful")
            else:
                print("fuckkkkk")
            pass
    else:
        print("wrong user")
        # gradio prompt the user
    return f"Locker {locker_number} is locked", load_image(comapare_path)


def locker1():
    if read_from_database(1):  # if path of saved image exist
        return unlock(1)
    else:
        return lock(1)


def locker2():
    if read_from_database(2):  # if path of saved image exist
        return unlock(2)
    else:
        return lock(2)


# Create the blocks for the interface
with gr.Blocks(theme=theme) as demo:
    gr.Markdown("# Lock it up system")
    gr.Markdown("Brought to you by Tinapat Limsila")

    with gr.Row():
        with gr.Column():
            # Second column content
            # You can add elements here for the right side
            # gr.Image(type="pil")
            # gr.Button("Take Picture", elem_id="take", variant="primary")
            img_window = gr.Image(elem_id="img_window", type="pil")
            with gr.Row():
                gr.Button("Accept", elem_id="accept", variant="primary")
                gr.Button("Retry", elem_id="retry", variant="secondary")

        with gr.Column():
            # First column content
            txt_3 = gr.Textbox(value="", label="Output")
            with gr.Row():
                btn1 = gr.Button("1", elem_id="btn1", variant="primary").click(
                    locker1, outputs=[txt_3, img_window]
                )
                btn2 = gr.Button("2", elem_id="btn2", variant="primary").click(
                    locker2, outputs=[txt_3, img_window]
                )
            gr.Markdown("---")
            gr.Markdown("## Rate")
            gr.Markdown("10 THB/hour")
            gr.Markdown("---")


    # The output from the lock_system function is not used here since we are just creating a static UI.
    # We would normally call a function when a button is clicked to process some input and return an output.
    # output = gr.Textbox(label="System Response")

# The interface does not take any input and will not call the lock_system function.
# The interface is just a static representation of the UI design.
demo.launch()
