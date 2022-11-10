#!/usr/bin/python3

import cv2
import numpy as np
import pyfiglet
from termcolor import colored
  
motdBanner = pyfiglet.figlet_format("STEGCURITY")
print(motdBanner)
print(colored('- Sri Lanka Institute of Information Technology (SLIIT)\n- Information Security Project - IE3092\n- Done by:', 'red'))
print(colored('\tM.Thushitharan - IT19983370\n\tS.Kaviseshan - IT20070144', 'green'))
print("--------------------------------------------------------")


#Converting Image data to Binary data
def imgData2Binary(data):
    if type(data) == str:
        return ''.join([format(ord(i),"08b") for i in data])
    elif type(data) == bytes or type(data) == np.ndarray:
        return [format(i,"08b") for i in data]


#Hiding the secret text within the image
def hideData(image,secretData):
    secretData += "#####"      

    dataIndex = 0
    binaryData = imgData2Binary(secretData)
    dataLength = len(binaryData)
    
    for values in image:
        for pixel in values:
            
            r,g,b = imgData2Binary(pixel)

            if dataIndex < dataLength:
                pixel[0] = int(r[:-1] + binaryData[dataIndex])
                dataIndex += 1
            if dataIndex < dataLength:
                pixel[1] = int(g[:-1] + binaryData[dataIndex])
                dataIndex += 1
            if dataIndex < dataLength:
                pixel[2] = int(b[:-1] + binaryData[dataIndex])
                dataIndex += 1
            if dataIndex >= dataLength:
                break

    return image
            

#Encoding the Image    
def encodeText():
    image_name = input("Enter Cover Image Name : ")
    image = cv2.imread(image_name)

    data = input("Enter The Text You Want To Hide : ")
    if data == 0:
        raise ValueError("Data is Empty ... ")

    file_name = input("Enter The Encoded Image Name : ")

    encoded_data = hideData(image,data)
    cv2.imwrite(file_name,encoded_data) 


#Show the data which encoded within the image
def showData(image):
    binaryData = ""
    for values in image:
        for pixel in values:
            r,g,b = imgData2Binary(pixel)
            
            binaryData += r[-1]
            binaryData += g[-1]
            binaryData += b[-1]

    all_bytes = [binaryData[i: i+8] for i in range (0,len(binaryData),8)]

    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte,2))
        if decoded_data[-5:] == "#####":
            break

    return decoded_data[:-5]


#Decode the encoded text within the image
def decodeText():
    image_name = input("Enter Image You Want To Extract : ")
    image = cv2.imread(image_name)

    text=showData(image)       
    return text


#Main function for the tool
def stegnography():
    userinput = int(input("\nSelect an Option\n\n 1. Encode \n 2. Decode \n 3. Quit Program \n\n Enter Option : "))
    if userinput == 1:
        encodeText()
    elif userinput == 2:
        final_data=decodeText()
        print("\nDecoded Data : ",final_data)
    elif userinput == 3:
        print(colored('\nSee you again...Bye...\n\n','blue'),end = '')
    else:
        print(colored('\n ---------------------------------------- ','yellow'))
        print(colored('| WARNING!!! Please enter correct value. |','yellow'))
        print(colored(' ---------------------------------------- \n','yellow'))
        
        

stegnography()
