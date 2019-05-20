'''

Python Script to detect imprinted text on pill images using AWS Rekognition.
Set up for passing just 1 image. 
Will need to be refactored to pass 2 images based on URL or JSON given by WEB.

Source code:
https://github.com/labs12-rxid/DS/blob/master/text_detection_AWSRekognition.ipynb
'''

import urllib.request
import json
import re
import boto3
import numpy as np
from dotenv import load_dotenv
import os
import cv2

load_dotenv()

key_id = os.getenv("AWS_ACCESS_KEY_ID")
secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
reg_ion = os.getenv("AWS_DEFAULT_REGION")
client=boto3.client('rekognition', region_name=reg_ion,
                    aws_access_key_id=key_id,
                    aws_secret_access_key=secret_key)

# Filter to increase image contrast
def add_contrast(image_path):

    #-----Reading the image-----------------------------------------------------
    img = cv2.imread(image_path, 1)

    #-----Converting image to LAB Color model----------------------------------- 
    lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    #-----Splitting the LAB image to different channels-------------------------
    l, a, b = cv2.split(lab)

    #-----Applying CLAHE to L-channel-------------------------------------------
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl = clahe.apply(l)

    #-----Merge the CLAHE enhanced L-channel with the a and b channel-----------
    limg = cv2.merge((cl,a,b))

    #-----Converting image from LAB Color model to RGB model--------------------
    image_contrast = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    
    return image_contrast


# Text  Dectection Function

def post_rekog(pic_json, elem_limit=3, con_fidence=70):
   
    # -------------Getting list of image file names -------------
    imageURL_list = pic_json.get("image_locations")
    # print(f'imageURL_list {imageURL_list}')
    
    # ------------- Text from image(s) uploaded by user -------------
    all_text = []
    # ------------- text read from image(s) with contrast filter -------------
    all_filter_text = []
    
    ctr1 = 10000
    ctr2 = 10001
    for imageURL in imageURL_list:
        if imageURL != "":
            # ------------- Saving image URL locally -------------
            ctr1 += 2
            temp_img = str(ctr1) + ".jpg"
            urllib.request.urlretrieve(imageURL, temp_img)
            imageFile = './' + temp_img
            
            # ------------- Detecting text from original image ------------
            
            with open(imageFile, 'rb') as image:
                # !!!!!!  WRAP THIS IN A TRY / CATCH !!!!!!!!!
                response = client.detect_text(Image={'Bytes': image.read()})
                
#                 response2 = 

            # ------------- Detected Text (List of Dictionaries) -------------
            textDetections=response['TextDetections']

            # ------------- Parsing Through Detected Text and 
            # Making list of Unique Sets of Text Dectected -------------
            text_found = []

            for text in textDetections:
                if text['Confidence'] > con_fidence:
                    text_found.append(text['DetectedText'])
#                     print(text['Confidence'])
#             print(f'text_found: {text_found}')
            
            text_set = list(set(text_found))

            # ------------- Appending detected text in image to "all_text" list --------
            all_text.append(text_set) 
            
            # ------------- Detecting text from filtered image ------------
            
            filtered_img = add_contrast(imageFile)
            
            # ------------- Saving image URL locally -------------
            ctr2 += 2
            temp_img = str(ctr2) + ".jpg"
            cv2.imwrite(temp_img, filtered_img)
            imageFile2 = './' + temp_img
            
            with open(imageFile2, 'rb') as image:
                # !!!!!!  WRAP THIS IN A TRY / CATCH !!!!!!!!!
                response2 = client.detect_text(Image={'Bytes': image.read()}) 

            # ------------- Detected Text (List of Dictionaries) -------------
            textDetections2=response2['TextDetections']

            # ------------- Parsing Through Detected Text and 
            # Making list of Unique Sets of Text Dectected -------------
            text_found2 = []

            for text in textDetections2:
                if text['Confidence'] > con_fidence:
                    text_found2.append(text['DetectedText'])
#                     print(text['Confidence'])
#             print(f'text_found: {text_found}')
            
            text_set2 = list(set(text_found2))

            # ------------- Appending detected text in image to "all_text" list ------
            all_filter_text.append(text_set2) 
            
            # ------------------------------------------------------------
            
        else:
            continue
            
    # ------------- Flattening 'all_text' (list of lists) into 1 list -------------
    text_list = [text for sublist in all_text for text in sublist]
    text_list = list(set(text_list))
    
    text_list2 = [text for sublist in all_filter_text for text in sublist]
    text_list2 = list(set(text_list2))
#     print(f'text_list: {text_list}')
#     print(f'text_list2: {text_list2}')

    # ------------- Splitting any text blob that may have digits and numbers together ----
    unique_list = []
    for each in text_list:
        num_split = re.findall(r'[A-Za-z]+|\d+', each)
        unique_list.append(num_split)
        
    unique_list2 = []
    for each in text_list2:
        num_split = re.findall(r'[A-Za-z]+|\d+', each)
        unique_list2.append(num_split)

    # ------------- Flattening again into one list with just unique values -------------
    unique_list = [text for sublist in unique_list for text in sublist]
    unique_list = list(set(unique_list))
    
    unique_list2 = [text for sublist in unique_list for text in sublist]
    unique_list2 = list(set(unique_list))
    # print(len(unique_list))
    
    # ------------- Return 'final_list' -------------
    final_list = set(unique_list + unique_list2)

    # If 'final_list' is empty return and empty set and break
    if len(final_list) == 0:
        return {} 

    if len(final_list) > elem_limit:
        final_list = set(list(final_list)[:elem_limit])
    return final_list


# __________ M A I N ________________________
if __name__ == '__main__':
    #data = {"image_locations": ["https://s3.us-east-2.amazonaws.com/firstpythonbucketac60bb97-95e1-43e5-98e6-0ca294ec9aad/adderall.jpg", ""]}
    #data = {"image_locations": ["https://raw.githubusercontent.com/ed-chin-git/ed-chin-git.github.io/master/sample_pill_image.jpg", ""]}
    data = {"image_locations": ["https://s3.us-east-2.amazonaws.com/firstpythonbucketac60bb97-95e1-43e5-98e6-0ca294ec9aad/img2b.JPG",
                                "https://s3.us-east-2.amazonaws.com/firstpythonbucketac60bb97-95e1-43e5-98e6-0ca294ec9aad/img2b.JPG"]}
    print(post_rekog(data,4,80))

    


