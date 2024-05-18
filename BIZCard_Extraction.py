import streamlit as st
from streamlit_option_menu import option_menu
import easyocr
from PIL import Image
import pandas as pd
import re
import psycopg2
import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
import os
import io


#Function to extract the data from the Business card

# INITIALIZING THE EasyOCR READER
reader = easyocr.Reader(['en'])

mydb = psycopg2.connect(host="localhost",
                        user="postgres",
                        password="12345678",
                        database="BiZCard_Data",
                        port = "5432"
                        )

mycursor = mydb.cursor() 


#Function to extract the Card holder name

def card_holder(result):
  for i in result:
    return result[0]


#Function to extract the Designation

def designation(result):
   for i in result:
      return result[1]
   
#Function to extract the Phone numbers

def phone(result):
   num = []
   for i in result:
      if re.findall(r'^[+]', i):
         num.append(i)
      elif re.findall(r'^\d{3}-\d{3}-\d{4}$', i):
         num.append(i)
   return num

#Function to extract the Email id

def email(result):
   for i in result:
      if (re.findall(r'[\w\.-]+@[\w\.-]+',i)):
         return i
      
#Function to extract the website

def website(result):
    for ind,i in enumerate(result):
       if "www " in i.lower() or "www." in i.lower():
          return i
                    
       elif "WWW" in i:
          return result[4] +"." + result[5]



#Function to extract the address

def address(result):
  for i in result:
    if(re.findall(r'^123+\s[\w\.-]+',i)):
      return i[0:10]

#Function to extract the domain
 
def domain(result):
    name_pattern = r'^[A-Za-z]+ [A-Za-z]+$|^[A-Za-z]+$|^[A-Za-z]+ & [A-Za-z]+$'
    name_data = []  # empty list
    for i in result:
        if re.findall(name_pattern, i):
            if i not in 'WWW':
                name_data.append(i)
    if len(name_data) == 3:
        company = name_data[2]
    else:
        company = name_data[2] + ' ' + name_data[3]
    return company


#Function to extract the district

def district(result):
  for i in result:
    if(re.search(r'^123+\s',i)):
      if len(i[10:20])> 6:
        return i[13:21].replace(";","").replace(",", "")
    elif (re.search(r'\bErode\b',i)):
      return i.replace(";","").replace(",", "")
  return "Not Available"    


#Function to extract the pincode

def pincode(result):
    pincode = None
    for i in result:
        pincode_match = re.search(r'(\d{6})|\b(\d{3}\s*\d{3})\b', i)
        if pincode_match:
            pincode = pincode_match.group(0).replace(' ', '')
    return pincode
    

#Function to extract the state

def state(result): 
    for i in result:
        match = re.search(r'TamilNadu', i)
        if match:
            return match.group()
    return "Not found"

def img_to_binary(file):
            img_byte_array = io.BytesIO()
            Image.fromarray(image).save(img_byte_array, format='PNG')
            return img_byte_array.getvalue()
  

def data(img):
          data = {}
          data['Name'] = card_holder(img)
          data['Designation'] = designation(img)
          data['Company'] = domain(img)
          data['Contact'] = phone(img)
          data['Email'] = email(img)
          data['Website'] = website(img)
          data['Area'] = address(img)
          data['City'] = district(img)
          data['State'] = state(img)
          data['Pincode'] = pincode(img)
          data["Image"] = img_to_binary(img)
          return data
      

#Streamlit part

img =Image.open(r"C:\Users\rajub\OneDrive\Desktop\logo_ocr.png")

st.set_page_config(page_title="BizcardX_OCR", page_icon=img, layout="wide", initial_sidebar_state="expanded")

st.markdown("<h2 style='text-align: center; color: orange;'>Business Card Data Extraction with OCR</h2>", unsafe_allow_html=True)

with st.sidebar:
    st.write("# :orange[BizCardX] :label:")
    st.write("")
    st.sidebar.image(r"C:\Users\rajub\OneDrive\Desktop\sidebar.png", use_column_width=True)
    st.write("")
    st.write("")
    selected = option_menu(None,
                            options = ["Home", "Upload & Extract", "Modify/ Delete"],
                            icons= ["house", "cloud-upload", "pencil-square"],
                            styles={"icon": {"color": "white"}})
                            
    
    
if selected == "Home":
    
    col1, col2 = st.columns((1.5,1))
    
    with col1:
       st.write("")
       st.write("")
       st.write("##### Welcome to the BizCardX: Extracting Business Card Data with OCR project!")
       st.write("##### This Python-based tool is designed to digitize the scanned Business card image and store the data in database for easy access and Modification")
       st.write("##### This tool also uses image processing technology, which helps to improve image quality to enable advanced automation and development of Models")
       
    with col2:
       st.write("")
       st.write("")
       img1 = Image.open(r"C:\Users\rajub\OneDrive\Desktop\text.png")
       
       st.image(img1, width=400)
       
       

    col3, col4 = st.columns((0.5,1))

    with col3:
       st.write("")
       st.write("")
       img2 = Image.open(r"C:\Users\rajub\OneDrive\Desktop\ocr.png")
       st.image(img2, width=300)
    
    with col4:
       st.write("")
       st.write("##### :orange[Data Extraction:] Utilizes the Optical Character Recognition(OCR) technology, EasyOCR which is flexible and easy to use for data entry automation and image analysis")
       st.write("##### EasyOCR enables computers to identify and extract text from images and is a Multi-language support, pretrained text detection and identification Model")
       st.write("")            
       st.write("##### :orange[Streamlit Interface:] Provides a streamlined web interface powered by Streamlit providing options for easy data Extraction, storage, and Modification.")
    
    

if selected == "Upload & Extract":

    uploaded = st.file_uploader("Upload the Image", type= ["png","jpg","jpeg"])

    if uploaded is not None:
       def save_card(uploaded):
            if not os.path.exists("uploaded"):
              os.makedirs("uploaded")
            with open(os.path.join("uploaded",uploaded.name), "wb") as f:
                f.write(uploaded.getbuffer())  

       save_card(uploaded)

       def image_preview(image,res): 
            for (bbox, text, prob) in res: 
              # unpack the bounding box
                (tl, tr, br, bl) = bbox
                tl = (int(tl[0]), int(tl[1]))
                tr = (int(tr[0]), int(tr[1]))
                br = (int(br[0]), int(br[1]))
                bl = (int(bl[0]), int(bl[1]))
                cv2.rectangle(image, tl, br, (0, 255, 0), 2)
                cv2.putText(image, text, (tl[0], tl[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            
            return image

        
       
      #Displaying the uploaded image
       col5, col6 = st.columns((1,1))
       with col5:
          
        file_bytes = uploaded.read()
        nparr = np.frombuffer(file_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        st.write("")
        st.write("##### :orange[The Uploaded card]")
        st.write("")
        st.write("")
        st.write("")
        st.image(image,channels='BGR', width=500)

       
      #Displaying the card with the highlights
       with col6:
               
               if st.button(':orange[Process Image]'):
                  with st.spinner('Please wait..Processing Image.....'):
                     time.sleep(2)  


                  st.set_option('deprecation.showPyplotGlobalUse', False)
                  saved_img = os.getcwd()+ "\\" + "uploaded"+ "\\"+ uploaded.name
                  image = cv2.imread(saved_img)
                  res = reader.readtext(saved_img)
                  st.markdown("##### :orange[Processed Image]")
                  processed_image = image_preview(image, res)
                  plt.figure(figsize=(15, 15))
                  plt.axis('off')
                  plt.imshow(processed_image)
                  st.pyplot()

               saved_img = os.getcwd()+ "\\" + "uploaded"+ "\\"+ uploaded.name
               result = reader.readtext(saved_img,detail = 0,paragraph=False)
               Data = data(result)
               df = pd.DataFrame(Data) 

               

    if st.button(" :orange[Extract data]"):
          
      st.success("Data Extracted successfully")
      
      st.write(df)

    
    if st.button(" :orange[Upload to Database]"):

      mydb = psycopg2.connect(host="localhost",
                        user="postgres",
                        password="12345678",
                        database="BiZCard_Data",
                        port = "5432"
                        )

      mycursor = mydb.cursor()
      
      Name_insert = df['Name'].iloc[0]

      query = '''SELECT Name from bizcard where Name = %s'''
      mycursor.execute(query, (Name_insert,))
      existing_name = mycursor.fetchone()

      if len(df) == 2:
        df1 = df.groupby(['Name','Designation','Company','Email','Website','Area','City','State','Pincode','Image'], as_index=False).agg({'Contact':','.join})
      else:
        df1 = df  

      if existing_name:
            st.error("Information of the given Business card already exists")
      else:
            #for index, row in df.iterrows():
            sql = '''INSERT INTO bizcard(Name,Designation,Company,Contact,Email,Website,Area,City,State,Pincode,Image)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                
            

            values = (df1['Name'].iloc[0],
                        df1['Designation'].iloc[0],
                        df1['Company'].iloc[0],
                        df1['Contact'].iloc[0],
                        df1['Email'].iloc[0],
                        df1['Website'].iloc[0],
                        df1['Area'].iloc[0],
                        df1['City'].iloc[0],
                        df1['State'].iloc[0],
                        df1['Pincode'].iloc[0],
                        df1['Image'].iloc[0])
            

            mycursor.execute(sql, values)
            mydb.commit()

            st.success("Uploaded to database successfully!")
       
if selected == "Modify/ Delete":
    
    option = option_menu(None, ['View card', "Update", "Delete"],
                                 icons=["image", "pencil-fill", 'exclamation-diamond'], orientation= "horizontal", default_index=0)


    mydb = psycopg2.connect(host="localhost",
                        user="postgres",
                        password="12345678",
                        database="BiZCard_Data",
                        port = "5432"
                        )

    mycursor = mydb.cursor()       
    mycursor.execute("SELECT * FROM bizcard")
    result1 = mycursor.fetchall()

    #convert into dataframe using pandas
    df2=pd.DataFrame(result1, columns=['name','designation','company','contact','email','website','city','area','state','pincode','image'])
    st.write(df2)

    if option=='View card':
            left,col1, right = st.columns([2,0.5, 2.5])
            with left:
                mycursor.execute("SELECT Name, Designation, Company FROM bizcard")
                rows = mycursor.fetchall()
                
                row_name = [row[0] for row in rows]
                row_designation = [row[1] for row in rows]
                row_company = [row[2] for row in rows]

                # Display the selection box
                selected_company = st.selectbox("Select Company", row_company)
                selected_name = st.selectbox("Select Name", row_name)     #selection box for avoiding the user input
                selected_designation = st.selectbox("Select Designation", row_designation)

                if st.button(" :orange[Show card]"):
                    with right:
                        sql = "SELECT image FROM bizcard WHERE name = %s AND designation = %s AND company = %s"
                        mycursor.execute(sql, (selected_name, selected_designation, selected_company))
                        result = mycursor.fetchone()

                        # Check if image data exists
                        if result is not None:
                            
                            # Retrieve the image data from the result
                            image_data = result[0]

                            # Create a file-like object from the image data
                            nparr = np.frombuffer(image_data, np.uint8)
                            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                            st.image(image, width=400)
      
                        if result is None:
                            st.error("No card is present with the given information")


    if option=='Update': 
                
        column1,column2 = st.columns(2, gap="large")
        with column1:
            mycursor.execute("SELECT name FROM bizcard")
            result = mycursor.fetchall()
            business_cards = {}

            for row in result:
                business_cards[row[0]] = row[0]
            selected_card = st.selectbox("Select a card holder name to update", list(business_cards.keys()))
            st.markdown("#### Update or modify any data below")
            mycursor.execute("select name, designation, company, contact, email, website, area, city, state, pincode from bizcard WHERE name= %s",
                            (selected_card,))
            result = mycursor.fetchone()

            # DISPLAYING ALL THE INFORMATIONS
            name = st.text_input("Name", result[0])
            designation = st.text_input("Designation", result[1])
            company = st.text_input("Company", result[2])
            contact = st.text_input("Contact", result[3])
            email = st.text_input("Email", result[4])
            
        with column2:
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            website = st.text_input("Website", result[5])
            area = st.text_input("Area", result[6])
            city = st.text_input("City", result[7])
            state = st.text_input("State", result[8])
            pincode = st.text_input("Pincode", result[9])

        if st.button(" :orange[Save changes]"):
            # Update the information for the selected business card in the database
            mycursor.execute("""UPDATE bizcard SET name=%s, designation=%s, company=%s, 
                                contact=%s, email=%s, website=%s, area=%s, city=%s, state=%s, pincode=%s
                            WHERE name=%s""", (name, designation, company, contact, email, website, area, city, state, pincode, selected_card))
            mydb.commit()
            st.success("Information updated in database successfully.")
        
        if st.button(" :orange[View updated data]"):
            
            mycursor.execute("select name, designation, company, contact, email, website, area, city, state, pincode from bizcard")

            updated_df = pd.DataFrame(mycursor.fetchall(),columns=["Name","Designation","Company","Contact","Email","Website","Area","City","State","Pincode"])

            st.write(updated_df)                 

    # Define the username and password
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "password"

    # Authentication function
    def authenticate(username, password):
        return username == ADMIN_USERNAME and password == ADMIN_PASSWORD
    

    if option=='Delete': 
                
        column1,column2 = st.columns(2, gap="large")

        with column1:
            mycursor.execute("SELECT name FROM bizcard")
            result = mycursor.fetchall()

            business_cards = {}

            for row in result:
                business_cards[row[0]] = row[0]

            selected_card = st.selectbox("Select a card holder name to Delete", list(business_cards.keys()))

            st.write(f"#### :orange[You have selected :green[**{selected_card}'s**] card to delete]")

            st.write("#### Do you want to proceed to delete this card?")

            # Display authentication form
            form = st.form(key='authentication_form')
            username = form.text_input("Username")
            password = form.text_input("Password", type="password")
            submit_button = form.form_submit_button("Authenticate")

            # If form is submitted
            if submit_button:
                if authenticate(username, password):
                    # If authentication is successful, proceed with deletion
                    mycursor.execute(f"DELETE FROM bizcard WHERE name='{selected_card}'")
                    mydb.commit()
                    st.success("Business card information deleted from database.")
                else:
                    st.error("Invalid username or password. Deletion aborted.")
