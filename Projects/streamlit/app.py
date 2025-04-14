import streamlit as st

#text/title
st.title("Streamlit Tutorials")

st.header("This is a header")
st.subheader("This is a subheader")
st.write("This is a write")
st.text("This is a text")
st.markdown("**This is a markdown**")
st.success("This is a success")
st.info("This is an info")
st.warning("This is a warning")
st.error("This is an error")
st.exception("NameError: name 'name' is not defined")
st.code("print('Hello World')", language='python')
st.latex(r'''a^2 + b^2 = c^2''')
st.json({"name": "John", "age": 30, "city": "New York"})
st.write(range(10))

from PIL import Image
img = Image.open("../../Data/img.png")
#st.image(img, caption="This is an image", width=250)
if st.checkbox("Show image"):
    st.image(img, caption="This is an image", width=250)

if st.button("Click me"):
    st.write("Button clicked")

status = st.radio("Select status", ("Active", "Inactive"))

if status == "Active":
    st.write("Active")
else:
    st.write("Inactive")

# Selectbox
options = ["Option 1", "Option 2", "Option 3"]
# selected_option = st.selectbox("Select an option", options)
# st.write("You selected:", selected_option)
# Multiselect
selected_options = st.multiselect("Select multiple options", options)
st.write("You selected:", selected_options)
# Slider
value = st.slider("Select a value", 0, 100, 50)
st.write("You selected:", value)
# Range slider
value_range = st.slider("Select a range", 0, 100, (25, 75))
st.write("You selected:", value_range)
# Date input
import datetime
today = datetime.date.today()
date = st.date_input("Select a date", today)
st.write("You selected:", date)
# Time input
import datetime
time = st.time_input("Select a time", datetime.time(12, 0))
st.write("You selected:", time)
# File uploader
uploaded_file = st.file_uploader("Upload a file", type=["csv", "txt"])
if uploaded_file is not None:
    file_content = uploaded_file.read()
    st.write("File content:", file_content)

# Text input
text_input = st.text_input("Enter some text", "Default text")
st.write("You entered:", text_input)
# Text area
text_area = st.text_area("Enter some text", "Default text")
st.write("You entered:", text_area)
# Password input
password = st.text_input("Enter a password", type="password")
st.write("You entered:", password)
# Checkbox
checkbox = st.checkbox("Check me")
st.write("Checkbox checked:", checkbox)
# Radio button
radio = st.radio("Select an option", ["Optiossssns 1", "Option 2", "Option 3"])
st.write("You selected:", radio)

# Progress bar
import time
progress_bar = st.progress(0)
# for i in range(100):
#     time.sleep(0.1)
#     progress_bar.progress(i + 1)
# # Spinner
# with st.spinner("Loading..."):
#     time.sleep(2)
# Sidebar
st.sidebar.title("Sidebar")
st.sidebar.write("This is a sidebar")
# Sidebar selectbox
sidebar_options = ["Option 1", "Option 2", "Option 3"]
sidebar_selected_option = st.sidebar.selectbox("Select an option", sidebar_options)
st.sidebar.write("You selected:", sidebar_selected_option)
# Sidebar slider
sidebar_values = st.sidebar.slider("Select a value", 0, 100, 50, key="sidebar_slider_1")
st.sidebar.write("You selected:", sidebar_values)
# Sidebar range slider
sidebar_value_range = st.sidebar.slider("Select a range", 0, 100, (25, 75), key="sidebar_slider_2")
st.sidebar.write("You selected:", sidebar_value_range)
# Sidebar date input
sidebar_date = st.sidebar.date_input("Select a date", today, key="sidebar_date_1")
st.sidebar.write("You selected:", sidebar_date)
# Sidebar time input
sidebar_time = st.sidebar.time_input("Select a time", datetime.time(12, 0), key="sidebar_time_1")
st.sidebar.write("You selected:", sidebar_time)
# Sidebar file uploader
sidebar_uploaded_file = st.sidebar.file_uploader("Upload a file", type=["csv", "txt"], key="sidebar_file_uploader_1")
if sidebar_uploaded_file is not None:
    sidebar_file_content = sidebar_uploaded_file.read()
    st.sidebar.write("File content:", sidebar_file_content)
# Sidebar text input
sidebar_text_input = st.sidebar.text_input("Enter some text", "Default text", key="sidebar_text_input_1")
st.sidebar.write("You entered:", sidebar_text_input)
# Sidebar text area
sidebar_text_area = st.sidebar.text_area("Enter some text", "Default text", key="sidebar_text_area_1")
st.sidebar.write("You entered:", sidebar_text_area)
# Sidebar password input
sidebar_password = st.sidebar.text_input("Enter a password", type="password", key="sidebar_password_1")
st.sidebar.write("You entered:", sidebar_password)
# Sidebar checkbox
sidebar_checkbox = st.sidebar.checkbox("Check me", key="sidebar_checkbox_1")
st.sidebar.write("Checkbox checked:", sidebar_checkbox)
# Sidebar radio button
sidebar_radio = st.sidebar.radio("Select an option", ["Option 1", "Option 2", "Option 3"], key="sidebar_radio_1")
st.sidebar.write("You selected:", sidebar_radio)
