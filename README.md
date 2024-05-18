# BizCardX-Extracting-Business-Card-Data-with-OCR

**Project overview:** BizCardX is a user-friendly python application built using Streamlit, EasyOCR, OpenCV, Regex functions and SQL Database. The tool uses the OCR technology to recognize text on business cards and extract the data and stores the data into the database after classification using Regular expressions. The tool also provides access to modify the data. The extracted information would be displayed in a clean and organized manner.

____________________________________
**Packages to be imported:**
____________________________________

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

________________________________
**Features:**
________________________________

Extracts text information from business card images using EasyOCR.
Utilizes OpenCV for image preprocessing, such as resizing, cropping, and enhancing.
Uses regular expressions (RegEx) to parse and extract specific fields like name, designation, company, contact details, etc.
Stores the extracted information in a MySQL database for easy retrieval and analysis.
Provides a user-friendly interface built with Streamlit to upload images, extract information, and view/update the database.

