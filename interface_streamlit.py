import gradio as gr
from face_recog import compare, take_picture
from database import write_to_database, read_from_database
from PIL import Image


global st

alpha_mode = True


def print(text):
    st.session_state.debug.append(text)


if not alpha_mode:
    from stm32 import lock_signal_stm32, unlock_signal_stm32

    write_to_database(1, None)
    write_to_database(2, None)
else:
    # write_to_database(1, None)
    # write_to_database(2, 'img_database/1.jpg')
    pass


def lock(locker_number):
    global st
    print(f"Lock scanning {locker_number=}")
    saved_path = take_picture()

    print("Showing the image to the user")
    write_to_database(locker_number, path=saved_path)

    st.session_state.current_image = saved_path

    print(f"sending lock signal  {locker_number=}")
    if not alpha_mode:
        if unlock_signal_stm32(locker_number=1):
            print("unlocked successful")
        else:
            print("fuckkkkk")
    return f"Locker {locker_number} is locked"


def unlock(locker_number):
    global st
    print(f"Unlock scanning  {locker_number=}")
    saved_path = read_from_database(locker_number)
    comapare_path = take_picture()
    st.session_state["image"] = comapare_path

    st.session_state.current_image = comapare_path

    x = compare(target=saved_path, input=comapare_path)
    if x:
        print(f"sending unlock signal  {locker_number=}")
        write_to_database(locker_number)
        if not alpha_mode:
            if unlock_signal_stm32(locker_number=1):
                print("unlocked successful")
            else:
                print("fuckkkkk")
            pass

    else:
        print("wrong user")
        # gradio prompt the user
    return f"Locker {locker_number} is locked"


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


import streamlit as st
from PIL import Image
import time

# Custom theme colors
st.set_page_config(page_title="Lock it up system", layout="wide")
primaryColor = "#1c1c1c"
backgroundColor = "#262730"
secondaryBackgroundColor = "#404148"
textColor = "#fafafa"
font = "sans serif"

# Presets
st.session_state["image"] = "img_database/0.jpg"
st.session_state["rows"] = 0


# Header
st.title("Lock it up system")
st.caption("Brought to you by Tinapat Limsila")

# Initialize the session state for the image if it doesn't exist
if "current_image" not in st.session_state:
    st.session_state.current_image = "img_database/1.jpg"  # default image

if "debug" not in st.session_state:
    st.session_state.debug = ["Debug:       "]  # default image


def fuck():
    # Update the session state to the new image
    st.session_state.current_image = "img_database/2.jpg"


# Image and Button layout
col1, col2 = st.columns(2)
with col1:
    coln1, coln2 = st.columns(2)
    with coln1:
        st.button("Accept")
    with coln2:
        st.button("Retry")

    # x = st.image(Image.open(st.session_state['image']), use_column_width=True)
    st.image(st.session_state.current_image, caption="Displayed Image")


with col2:
    st.header("A dog")
    st.write("")  # This can be used for spacing
    coln1, coln2 = st.columns(2)
    with coln1:
        st.button("Locker 1", on_click=locker1)
    with coln2:
        st.button("Locker 2", on_click=locker2)
    # Additional UI Elements
    st.write("Rate")
    st.write("10 THB/hour")
    time.sleep(2)

for i in st.session_state.debug:
    st.write(i)
