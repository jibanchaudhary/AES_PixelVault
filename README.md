# **AES_PixelVault**

AES PixelVault is a comprehensive data encryption system that handles both encryption and decryption, as well as encoding and decoding. It secures text files (such as PDFs) by first encrypting the content using AES, converting the text into binary, and encoding these 0s and 1s into black and white pixels within video frames. The encoded frames are concatenated into a video for secure storage. The project also includes a decryption and decoding module to reverse the process, extracting the original data from the video. This novel approach merges cryptography with video processing for a unique and secure method of data storage and retrieval.

##**Features**
* AES Encryption: Secure text encryption using AES-128 with CBC mode.
* Binary Encoding: Converts encrypted data into binary, mapping it to black and white pixels.
* Video Encoding: Encodes binary data into video frames, creating a video for secure storage.
* Decryption and Decoding: Reverses the process to retrieve and decrypt the original data.


##**Steps**

###Encryption and Encoding

1. Extracts text from the input PDF file.
2. Encrypts the text using AES encryption.
3. Converts the encrypted data into binary form.
4. Encodes binary data as black and white pixels in image frames.
5. Combines the frames into a video file for storage.
   
###Decryption and Decoding

1. Extracts frames from the video.
2. Decodes the binary data from the frames.
3. Converts the binary data back into the encrypted text.
4. Decrypts the text using the AES key and IV to retrieve the original content.


##**Encrypted Image Frame**
A sample image frame showing the encrypted binary data in pixel form:

![AILA_0](https://github.com/user-attachments/assets/99d491d4-1d8d-4ffa-99ec-2feb57f043f1)


##**Encrypted Video**
The generated video with multiple frames encoding the encrypted data:

https://github.com/user-attachments/assets/4d3002eb-20fd-42a8-b2e4-c8b0d3c2f1ef


##**Decrypted Text**
The original text extracted from the video after decryption:

<img width="644" alt="image" src="https://github.com/user-attachments/assets/e265aec7-74b1-4bc6-b454-b1352775b35f">

###**License**

This project is licensed under the MIT License. Feel free to modify and enhance it!





