import streamlit as st

# Custom CSS to add a border to the container
st.markdown(
    """
    <style>
    div[data-testid="stContainer"] {
        border: 2px solid #e6e9ef;
        padding: 20px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 1. Create a box-like container
with st.container():
    st.subheader("Configuration Settings")

    # 2. Add widgets inside the container
    text_input_value = st.text_input("Enter some text:", value="Default Text")
    select_box_option = st.selectbox("Select an option:", ["Option A", "Option B", "Option C"])
    additional_text = st.text_area("Enter additional information", "Initial information")

# 3. Print the values outside the container
st.subheader("Values Entered:")
st.write(f"Text Input: {text_input_value}")
st.write(f"Select Box Option: {select_box_option}")
st.write(f"Additional Text: {additional_text}")