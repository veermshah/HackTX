import streamlit as st 
import openai
import cv2

def barcode():
    st.title("Add Items")
    

def inventory():
    st.title("Inventory")
    # Alex add here
    
    
def suggestion():
    st.title("Recipe Suggester")
    if st.button("Suggest a Recipe"):
        API_KEY = "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"
        openai.api_key = API_KEY
        prompt = "Suggest a single recipe using the following ingredients: " + "apple, banana, orange, sugar"
        
        messages = [
            {"role": "assistant", "content": prompt}
        ]
        
        # Make the API call
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.9
        )
        
        # Get the generated sentence from the response
        recipe = response['choices'][0]['message']['content']
        st.subheader(recipe)
        
st.sidebar.image("pantry.jpg")
page = st.sidebar.selectbox("Select Page", ["Add Items", "Inventory", "Recipe Suggester"])

# Display selected page
if page == "Add Items":
    barcode()
elif page == "Inventory":
    inventory()
else:
    suggestion()