import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import PIL.Image
import numpy as np
from keras.models import load_model
from keras.preprocessing import image as keras_image
from keras.applications.vgg16 import preprocess_input
from tkinter import messagebox
from tkinter import *

#Face Emotion Recognition Inspiration Idea
#https://youtu.be/aoCIoumbWQY?si=SSjJzWe2PdHmK1js
#https://youtu.be/avv9GQ3b6Qg?si=ginbyJzbel0VTQYK

class Emotion:
    # Initialize class attributes
    def __init__(self, name):
        self.name = name
        self.file_path = ''
        self.storefeedback = { }
        self.img = None
        self.image_label = tk.Label(root, bg='lightgrey')   # Label to display the image
        self.image_label.place(x=700, y=100, height=300, width=300)

    def open_image(self):
        # Open and display an image using file dialog
        self.file_path=filedialog.askopenfilename()
        self.img = PIL.Image.open(self.file_path)
        self.img = self.img.resize((400, 400), PIL.Image.BILINEAR)
        photo = ImageTk.PhotoImage(self.img)
        image_label.config(image=photo)
        image_label.image =photo  # Store a reference to prevent garbage collection

    

    def emotions_detector(self):
        if self.file_path not in self.storefeedback: 
            # Load the model and predict emotion from the selected image
            model = load_model(r"D:\\OneDrive\Desktop\\G7_FinalProject\\emotion_detection_model")
            self.img = np.array(self.img)
            self.img = self.img / 255.0  # Normalize the image
            self.img = np.expand_dims(self.img, axis=0)  # Add batch dimension
            predictions = model.predict(self.img)

            # Assuming model outputs probabilities for each emotion class
            emotion_labels = ['Angry', 'Disgusting', 'Fear', 'Happy', 'Sad', 'Surprise']
            predicted_emotion = emotion_labels[np.argmax(predictions)]
            result_label.config(text=f"Predicted Emotion: {predicted_emotion}", font=("Helvetica", 18, "bold"))

#MessageBox Widget
#https://www.geeksforgeeks.org/python-tkinter-messagebox-widget/ 
            
            feedback = messagebox.askyesno("Feedback", "Is this the correct emotion?")
            if feedback:
                messagebox.showinfo("Feedback","Thank you for your feedback.")
            else:
                emotion_window = tk.Tk()
                emotion_window.title("Emotions")
                
                # store feedback
                def save_emotion(emotion):
                    self.storefeedback[self.file_path] = emotion
                    messagebox.showinfo("Saved", f"Image with emotion '{emotion}' saved!")
                    emotion_window.destroy()

                label = tk.Label(emotion_window, text="Please select the correct emotion:")
                label.pack(padx=20, pady=10)

                max_label_length = max(len(emotion) for emotion in emotion_labels)

                # Create buttons for each emotion
                for emotion in emotion_labels:
                    emotion_button = tk.Button(emotion_window, text=emotion.capitalize(), command=lambda e=emotion: save_emotion(e))
                    # Set uniform width for all buttons based on the maximum label length
                    emotion_button.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
                    emotion_button.config(width=max_label_length + 2) 

                emotion_window.mainloop()

        else:
            predicted_emotion = self.storefeedback[self.file_path]
            result_label.config(text=f"Predicted Emotion: {predicted_emotion}", font=("Helvetica", 18, "bold"))
        

    def page2(self):
        # Switch to the second page, setting up UI elements
        global image_label
        global result_label
        string = entry.get()
        if string.strip():
#Switch Between Pages in Python - Tkinter
#https://www.youtube.com/watch?v=qw_XHRJP-vc
            
            username_label = tk.Label(root, text="", bg="white", font=('Helvetica', 18, "bold"))
            username_label.place(x=740, y=100)
            #Remove First Page Widgets
            bg1.destroy()
            start_btn.destroy()
            entry.destroy()

            #2nd Page Background Image
            bg2_img = tk.Label(root, image=bg2)
            bg2_img.place(x=0, y=0)

            msgbox = tk.Label(root, bg='white', width=60, height=36)
            msgbox.place(x=735, y=50)

            
#Button Widget
#https://www.geeksforgeeks.org/python-creating-a-button-in-tkinter/

            #Select Image Button
            btn1 = tk.Button(root, text="Select Image", bg='#453ea3', font=('Helvetica', 20), command=self.open_image)
            btn1.place(x=790, y=500, height=60, width=170)

            #Detect Image Button
            btn2 = tk.Button(root, text="Detect", bg='#4f9383', font=('Helvetica', 20), command=self.emotions_detector)
            btn2.place(x=1000, y=500, height=60, width=100)

            #Display Image
            image_label = tk.Label(root, bg="#e8e1e1")
            image_label.place(x=190, y=150, height=400,width=400)

            #Display Result
            result_label = tk.Label(root, text="", bg="white", font=("Helvetica", 18, "bold"), width = 25, height = 5)
            result_label.place(x=760, y=250)
            
            username_label.config(text=f"Hi, {string}!\nUpload an image to Detect Emotion.")
            username_label.lift()

        else:
            messagebox.showerror("Error", "Input box cannot be empty!")
#Uploading Images
#https://youtu.be/WurCpmHtQc4?si=6i81sr1beAeZZEoR
            
# Create the main window
root = tk.Tk()
root.geometry("1200x700")
root.title("Image Emotion Detection")
root.iconbitmap(r"D:\\OneDrive\\Desktop\\G7_FinalProject\\BaseData\\ICON.ico")

# Create an instance of the Emotion class
Project = Emotion("Project_Group7")

# Load Image
bg = tk.PhotoImage(file=r"D:\\OneDrive\\Desktop\\G7_FinalProject\\BaseData\\background.png")
start = tk.PhotoImage(file=r"D:\\OneDrive\\Desktop\\G7_FinalProject\\BaseData\\start.png")
bg2 = tk.PhotoImage(file=r"D:\\OneDrive\\Desktop\\G7_FinalProject\\BaseData\\bg2.png")

#Background image
bg1 = tk.Label(root, image=bg)
bg1.place(x=0, y=0)

#Navigate to Second Page
start_btn = tk.Button(root, image=start, command=Project.page2)
start_btn.place(x=555, y=425)

#Get User Input
#https://youtu.be/d_MrsYUJPGI?si=--p7WLUQFzxlUgN2

# Entry widget
entry = tk.Entry(root, width=12, border=0, bg="#e8e1e1", font=('Helvetica', 20, "bold"))
entry.focus_set()
entry.place(x=519, y=355)

root.mainloop()