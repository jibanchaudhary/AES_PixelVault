# Extracting each frame from the video
import cv2
import os
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

file_name = input("Enter the name of the file for decryption : ")


# Directory paths
video_path="" # Path of the video saved
key_dir = "" # Path of the key directory where key and IV will be stored

#Reading the key and IV values
def read_key(dir):
    key_path = os.path.join(dir, f"Key_value_{file_name}.txt")
    with open(key_path, 'r') as key_file:
        key_hex = key_file.read().strip()
        key = bytes.fromhex(key_hex)
        print(key)
        print("Key read successfully.")
        
    IV_path = os.path.join(dir, f"IV_value_{file_name}.txt")
    with open(IV_path, 'r') as IV_file:
        IV_hex = IV_file.read().strip()
        IV = bytes.fromhex(IV_hex)
        print(IV)
        print("IV read successfully.")
    
    return key,IV

key,IV = read_key(key_dir)


#Extracting the Frames from the video
def extract_frames(video_path):
    frames = []
    cap = cv2.VideoCapture(video_path)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        grey_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        frames.append(grey_frame)
    cap.release()
    return frames
frames = extract_frames(video_path)
# print(frames)
print(f"Length of the frames={len(frames)}")


# Decode the Binary data from each frames
def decode_to_binary(frame, threshold=128):
    binary_data = ""
    height, width = frame.shape[:2]
    for y in range(height):  
        for x in range(width):
            pixel_value = frame[y, x] 
            binary_data += '0' if pixel_value < threshold else '1'
    return binary_data

binary_data = ""
for frame in frames:
    binary_data += decode_to_binary(frame)
print(f"Sample Binary Data: {binary_data[:128]}")  

binary_data = binary_data.rstrip('0')


# Conversion from Binary_to_encrypted_text
def binary_to_encrypted_text(binary_data):
    encrypted_bytes = bytearray()
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        if len(byte) < 8:
            break  
        encrypted_bytes.append(int(byte, 2))
    return bytes(encrypted_bytes)

encrypted_text = binary_to_encrypted_text(binary_data)
print(len(encrypted_text))


# Decrypting the text
def decrypt_text(encrypted_text,key,IV):
    cipher = AES.new(key,AES.MODE_CBC,IV)
    padded_text = cipher.decrypt(encrypted_text)
    decrypted_text = unpad(padded_text, AES.block_size).decode('utf-8', errors='replace')

    return decrypted_text

text = decrypt_text(encrypted_text,key,IV)
print(text)
print("CONVERSION SUCCESSFUL!!!!!!!!!!!!!!!!!")

output_txt_file="extracted_text.txt"
with open(output_txt_file,'w', encoding='utf-8') as file:
    file.write(text)

