# BizCardX-Extracting-Business-Card-Data-with-OCR

**Project overview:** BizCardX is a user-friendly python application built using Streamlit, EasyOCR, OpenCV, Regex functions and SQL Database. The tool uses the OCR technology to recognize text on business cards and extract the data and stores the data into the database after classification using Regular expressions. The tool also provides access to modify the data. The extracted information would be displayed in a clean and organized manner.

------------------------------------------------------------------------------------------------------


Quick Configuration Guide:
-----------------------------
To get the quick access to the different packages of python:
Create a virtual evnironment under the folder in which you are creating python(.py) file in Visual Studio Code and install below packages in cmd prompt and import them:

- import streamlit as st
- from streamlit_option_menu import option_menu
- import easyocr
- from PIL import Image
- import pandas as pd
- import re
- import psycopg2
- import cv2
- import time
- import numpy as np
- import matplotlib.pyplot as plt
- import os
- import io

-----------------------------------------------------------------------------------------------------

**Features:**
---------------------------

- Extracts text information from business card images using EasyOCR.
- Utilizes OpenCV for image preprocessing, such as resizing, cropping, and enhancing.
- Uses regular expressions (RegEx) to parse and extract specific fields like name, designation, company, contact details, etc.
- Stores the extracted information in a MySQL database for easy retrieval and analysis.
- Provides a user-friendly interface built with Streamlit to upload images, extract information, and view/update the database.

-----------------------------------------------------------------------------------------------------

**Usage:**
-------------------------------------
1.Run the Streamlit application:
streamlit run bizcard.py

2.Access the application in the browser at http://localhost:8501.

3.Upload a business card image to extract the information.

4.The application will preprocess the image using OpenCV by resizing, cropping, and enhancing it.

5.The processed image will be passed to EasyOCR for text extraction. 

6.The extracted information will be displayed on the screen can be stored in the SQL database.

7.Use the provided options to view, update, or delete the extracted data in the database.

------------------------------------------------------------------------------------------------------

**Technologies Used:**
---------------------------

- Streamlit
- Streamlit_lottie
- Python
- RegEx
- EasyOCR
- OpenCV
- PostgreSQL
--------------------------------------------------------------------------------------------------------

**Acknowledgments:**
------------------------------

- Streamlit - For building interactive web applications with ease.
- EasyOCR - For text extraction from images.
- OpenCV - For image preprocessing and manipulation.
- PostgreSQL - For the database management system.

