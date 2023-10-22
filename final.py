import streamlit as st
import openai
import cv2
import requests
from pyzbar.pyzbar import decode
import time
import os

def BarcodeReader(image):
    img = cv2.imread(image)

    detectedBarcodes = decode(img)

    if detectedBarcodes:
        for barcode in detectedBarcodes:
            if barcode.data != "": 
                #return ["Oojami - Time Is Now (Music CD)", "https://images.barcodelookup.com/449/4498117-1.jpg"]
                response = requests.get("https://api.barcodelookup.com/v3/products?barcode=" + barcode.data.decode(
                    "utf-8") + "&formatted=y&key=k2hu41evicezr4pqgu9tui9jth1q4t")
                return [response.json()['products'][0]['title'], response.json()['products'][0]['images'][0]]


def getImage(cam, curtime, boxes, placeholder):
    if page != "Add Items":
        return
    item = None
    while page == "Add Items":
        
        ret, frame = cam.read()
        if not ret:
            print("\nfailed to grab frame\n")
            break
        img_name = "barcode.png"
        cv2.imwrite(img_name, frame)
        item = BarcodeReader(img_name)
        
        if item is not None and (int(round(time.time())) > curtime + 1):
            break
            
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        placeholder.image(rgb_frame, use_column_width=True)
    for b in boxes:
            b.empty()
    getData(item, boxes)
    getImage(cam, int(round(time.time())), boxes, placeholder)

def getData(item,boxes):
    global items
    if item is not None:
        print("getting items\n")
        boxes[0].subheader(body="Your item is")
        boxes[1].markdown(
        f'<div style="display: flex; justify-content: center;"><img src="{item[1]}" width="400" /></div>',
        unsafe_allow_html=True)
        boxes[2].subheader(item[0] + "\n")
        with open('inven.txt', 'a') as file:
            file.write(item[0] + "," + item[1] + "\n")
            file.close()
    

def barcode(curtime):
    print("barcode")
    st.title("Add Items")
    placeholder = st.empty()
    boxes = [st.empty(), st.empty(), st.empty()]
    cam = cv2.VideoCapture(0)
    getImage(cam, curtime, boxes, placeholder)
    cam.release()


def inventory():
    st.title("Inventory")
    st.markdown('<hr style="border: 0; height: 1px; background-color: #ccc;">', unsafe_allow_html=True)
    arr = st.session_state.items
    print(arr)
    with open("inven.txt", "r") as file:
        for line in file:
            i = line.strip().split(",", 1)
            st.markdown(
    f"""
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <div style="font-family: 'Lexend Deca', 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 24px; line-height: 1.5;">
            {i[0]}
        </div>
        <div style="float: right;">
            <img src="{i[1]}" alt="Image" style="width: 100px; max-width: 100%; height: auto;">
        </div>
    </div>
    <hr style="border: 0; height: 1px; background-color: #ccc;">
    """,
    unsafe_allow_html=True
)


def suggestion():
    st.title("Recipe Suggester")
    if st.button("Suggest a Recipe"):
        API_KEY = st.secrets["apikey"]
        openai.api_key = API_KEY
        
        ingredients = ""
        with open("inven.txt", "r") as file:
            for line in file:
                i = line.strip().split(",", 1)
                ingredients = ingredients + i[0] + ", "
            
        prompt = "Suggest a single recipe using the following ingredients: " + ingredients
        print("Prompt: " + prompt)
        
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



st.sidebar.title("Pantry Chef")
st.sidebar.image("pantry.jpg")
page = st.sidebar.selectbox("Select Page", ["Add Items", "Inventory", "Recipe Suggester"])

# items = [["Water Bottle", "https://pizzahampstead.com/wp-content/uploads/2016/09/45.jpg"],
#          ["Bread","https://assets.bonappetit.com/photos/5c62e4a3e81bbf522a9579ce/1:1/w_2240,c_limit/milk-bread.jpg"]]

# Display selected page
if page == "Add Items":
    barcode(int(round(time.time())))
elif page == "Inventory":
    inventory()
else:
    suggestion()
