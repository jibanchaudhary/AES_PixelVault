import os
import cv2
import fitz
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

# Directory path
file_name = input("Enter the name of the file : ")
frame_size = 1280*720
img_dir ="" # Path for image directory
output_dir = ""# Path for Output video directory
key_dir = "" # Path of the key directory where key and IV will be stored

pdf_path = "AILA_cases.pdf"

# AES Key to encrypt the text and IV(Initialization vector) to ramdomise the pattern(16 bytes)
key = get_random_bytes(16)
IV = get_random_bytes(16)


# Function for extracting data from the pdf
def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_no in range(doc.page_count):
        page = doc.load_page(page_no)
        text+= page.get_text()
    return text

text_data = extract_text(pdf_path)


# Encrypt and pad the text using AES
def encrypt_text(text,key,IV):
    cipher = AES.new(key,AES.MODE_CBC,IV)
    padded_text = pad(text.encode(),AES.block_size)
    encrypted_text = cipher.encrypt(padded_text)
    return encrypted_text

encrypted_text = encrypt_text(text_data, key, IV)
print(f"Encryption successful! Encrypted text length: {len(encrypted_text)}")


#converting the text_data into binary 0s and 1s
def text_to_binary(text):
    binary_text = "".join(format(byte,'08b')for byte in text) 
    return binary_text
binary_text = text_to_binary(encrypted_text)
print(len(binary_text))


# Define the frame size
def create_frames(binary_data,frame_num,width=1280,height = 720):
    img = Image.new('1',(width,height))
    pixels = img.load()

    for i in range(len(binary_data)):
        x = i % width
        y = i//width
        if y < height:
            pixels[x,y]=0 if binary_data[i] == '0' else 1
    img.save(os.path.join(img_dir,f"{file_name}_{frame_num}.png"))
    
    img.show()

frame_count = (len(binary_text)+frame_size-1)//frame_size
for i in range(frame_count):
    frame_data = binary_text[i* frame_size: (i+1)*frame_size]
    if len(frame_data) < frame_size:
        frame_data = frame_data.ljust(frame_size, '0')
    create_frames(frame_data, i)


# Creating a video concatinating the frames
def create_video(frame_count, output_path, file_name, frame_rate=10):
    frame_size = (1280, 720)  # Use the correct frame size
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, frame_size, isColor=False)
    
    for i in range(frame_count):
        frame_path = os.path.join(img_dir,f"{file_name}_{i}.png")
        frame = cv2.imread(frame_path, cv2.IMREAD_GRAYSCALE)  
        if frame is None:
            print(f"Error: unable to read frame {i}.")
            continue
        out.write(frame)
    
    out.release()

output_path = os.path.join(output_dir, f"output_video_{file_name}.mp4")
create_video(frame_count, output_path, file_name) 


key_path=os.path.join(key_dir,f"Key_value_{file_name}.txt")
with open(key_path,'w') as key_file:
    key_file.write(key.hex())
IV_path=os.path.join(key_dir,f"IV_value_{file_name}.txt")
with open(IV_path,'w') as IV_file:
    IV_file.write(IV.hex())
print(key)
print(IV)


