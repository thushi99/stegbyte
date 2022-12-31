#!/usr/bin/python3

import cv2
import numpy as np
import pyfiglet
from termcolor import colored
import base64
import os
import platform
  
motdBanner = pyfiglet.figlet_format("STEGCURITY")
print(motdBanner)
print(colored('- Created by:', 'red'), colored('Thushi', 'green'))
print("-"*56)


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


#Decode the encoded text within the image and print the message in bae64 format as external file
def decodeText():
    image_name = input("Enter Image You Want To Extract : ")
    image = cv2.imread(image_name)

    text = showData(image)

    message_bytes = text.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    encoded_message = base64_bytes.decode('ascii')

    f = open(image_name + ".txt", "a")
    f.write(encoded_message)
    f.close()       
    return encoded_message


#List the Png files
def listPngFiles():
    findOS = platform.system()
    if findOS=='Windows':
        exeCmd=os.system("dir *.png")
    else:
        exeCmd=os.system("ls -a *.png")
    return exeCmd
    

#Main function for the tool
def steganography():
    userinput = input("\nSelect an Option\n\n 1. Encode \n 2. Decode \n 3. List PNG image files \n 4. Quit \n\nEnter Option : ")
    if userinput == "1":
        encodeText()

    elif userinput == "2":
        final_data=decodeText()
        print("\nDecoded Data : ",final_data)
    
    elif userinput == "3":
        output=listPngFiles()

    elif userinput == "4":
        print(colored('\nSee you again...Bye...\n\n','blue'),end = '')
    
    elif userinput.isnumeric()==False:
        print("\nEnter a Number")
        print(colored('\n '+'-'*28,'yellow'))
        print(colored('| WARNING!!! Enter a Number. |','yellow'))
        print(colored(' '+'-'*28,'yellow'))
    
    else:
        print(colored('\n '+'-'*40,'yellow'))
        print(colored('| WARNING!!! Please enter correct value. |','yellow'))
        print(colored(' '+'-'*40 +'\n','yellow'))
        
steganography()