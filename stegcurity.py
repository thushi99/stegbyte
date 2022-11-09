#!/usr/bin/python3

import cv2
import numpy as np
import pyfiglet
from termcolor import colored
  
banner = pyfiglet.figlet_format("STEGCURITY")
#print(banner)
print(colored(banner, 'white'))
print(colored('- Sri Lanka Institute of Information Technology (SLIIT)\n- Information Security Project - IE3092\n- Done by:', 'blue'))
print(colored('\tM.Thushitharan - IT19983370\n\tS.Kaviseshan - IT20070144', 'green'))
print("")
#print("--------------------------------------------------------")
print(colored('--------------------------------------------------------', 'grey'))


def data2binary(data):
    if type(data) == str:
        return ''.join([format(ord(i),"08b") for i in data])
    elif type(data) == bytes or type(data) == np.ndarray:
        return [format(i,"08b") for i in data]


def hideData(image,secret_data):
    secret_data += "#####"      

    data_index = 0
    binary_data = data2binary(secret_data)
    data_length = len(binary_data)
    
    for values in image:
        for pixel in values:
            
            r,g,b = data2binary(pixel)

            if data_index < data_length:
                pixel[0] = int(r[:-1] + binary_data[data_index])
                data_index += 1
            if data_index < data_length:
                pixel[1] = int(g[:-1] + binary_data[data_index])
                data_index += 1
            if data_index < data_length:
                pixel[2] = int(b[:-1] + binary_data[data_index])
                data_index += 1
            if data_index >= data_length:
                break

    return image
            
    
def encode_text():
    image_name = input("Enter Cover Image Name : ")
    image = cv2.imread(image_name)

    data = input("Enter The Text You Want To Hide : ")
    if data == 0:
        raise ValueError("Data is Empty ... ")

    file_name = input("Enter The Encoded Image Name : ")

    encoded_data = hideData(image,data)
    cv2.imwrite(file_name,encoded_data) 

def show_data(image):
    binary_data = ""
    for values in image:
        for pixel in values:
            r,g,b = data2binary(pixel)
            
            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]

    all_bytes = [binary_data[i: i+8] for i in range (0,len(binary_data),8)]

    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte,2))
        if decoded_data[-5:] == "#####":
            break

    return decoded_data[:-5]



def decode_text():
    image_name = input("Enter Image You Want To Extract : ")
    image = cv2.imread(image_name)

    text=show_data(image)       
    return text

def stegnography():
    userinput = int(input("\nSelect an Option\n\n 1. Encode \n 2. Decode \n 3. Quit Program \n\n Enter Option : "))
    if userinput == 1:
        encode_text()
    elif userinput == 2:
        final_data=decode_text()
        print("\nDecoded Data : ",final_data)
    elif userinput == 3:
        print("\nSee you again...Bye...", end = ' ')
    else:
        print("\nWARNING!!! Please enter correct value.")
        
        

stegnography()
