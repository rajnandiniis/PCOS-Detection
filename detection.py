import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import tkinter as tk
from tkinter import messagebox, font
from PIL import Image, ImageTk
import cv2

# Function to calculate BMI
def calculate_bmi(weight, height):
    return weight / (height ** 2)

# Function to classify BMI into categories
def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal"
    elif 25 <= bmi < 29.9:
        
        return "Overweight"
    elif 30 <= bmi < 34.9:
        return "Obesity Class 1"
    elif 35 <= bmi < 39.9:
        return "Obesity Class 2"
    else:
        return "Obesity Class 3"

# Function to analyze PCOS risk based on BMI and image analysis
def pcos_risk_analysis(bmi, acne_detected, hair_growth_detected):
    if bmi > 25 and acne_detected and hair_growth_detected:
        return "High"
    else:
        return "Low"

# Camera feed function
def open_camera():
    global cap
    cap = cv2.VideoCapture(0)
    update_frame()

# Function to update the frame in the GUI
def update_frame():
    global cap
    ret, frame = cap.read()
    if ret:
        # Resize frame for better performance
        frame = cv2.resize(frame, (320, 240))  # Resize to 320x240
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        img_label.imgtk = imgtk
        img_label.configure(image=imgtk)
    img_label.after(10, update_frame)  # Continuously update the frame

# Function to capture the image and process for acne and excessive hair growth
def capture_image():
    global cap
    if cap is not None:
        ret, frame = cap.read()
        if ret:
            # Save the captured image if needed
            cv2.imwrite("captured_face.jpg", frame)

            # Face detection
            face_detected = detect_face(frame)
            if face_detected:
                # Update the form with the detection results
                acne_detected = detect_acne(frame)
                hair_growth_detected = detect_hair_growth(frame)

                entry_acne.delete(0, tk.END)
                entry_acne.insert(0, "Yes" if acne_detected else "No")

                entry_hair_growth.delete(0, tk.END)
                entry_hair_growth.insert(0, "Yes" if hair_growth_detected else "No")
                
                messagebox.showinfo("Success", "Image captured successfully!")
            else:
                messagebox.showwarning("Face Detection", "No face detected in the image.")

# Function to detect faces in an image
def detect_face(image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)
    return len(faces) > 0  # Returns True if at least one face is detected

# Placeholder function to detect acne
def detect_acne(image):
    # Actual acne detection would involve image processing techniques
    return True  # Return True if acne is detected, for now use as dummy

# Placeholder function to detect excessive hair growth
def detect_hair_growth(image):
    # Actual hair growth detection would involve image processing techniques
    return True  # Return True if hair growth is detected, for now use as dummy

# Function to show the final result
def show_result():
    try:
        # Collect user input
        weight = float(entry_weight.get())
        height = float(entry_height.get())
        cycle_length = int(entry_cycle_length.get())
        sleep_hours = int(entry_sleep_hours.get())

        # Calculate BMI and classify it
        bmi = calculate_bmi(weight, height)
        bmi_cat = bmi_category(bmi)

        # Detect acne and excessive hair growth using camera capture
        acne_detected = entry_acne.get() == "Yes"
        hair_growth_detected = entry_hair_growth.get() == "Yes"

        # Analyze PCOS risk based on BMI and image analysis
        pcos_risk = pcos_risk_analysis(bmi, acne_detected, hair_growth_detected)

        # Display results
        label_bmi.config(text=f"BMI: {bmi:.2f} ({bmi_cat})")
        label_risk.config(text=f"PCOS Risk: {pcos_risk}")

    except ValueError:
        label_risk.config(text="Please enter valid numeric inputs.")

# Initialize the GUI window
root = tk.Tk()
root.title("PCOS Detection System")

# Set a smaller window size
root.geometry("400x500")  # Set window size to 400x500 pixels

# Custom fonts
label_font = font.Font(family="Helvetica", size=12)
button_font = font.Font(family="Helvetica", size=10, weight="bold")

# User inputs
tk.Label(root, text="Weight (kg):", font=label_font).pack(pady=5)
entry_weight = tk.Entry(root)
entry_weight.pack(pady=5)

tk.Label(root, text="Height (m):", font=label_font).pack(pady=5)
entry_height = tk.Entry(root)
entry_height.pack(pady=5)

tk.Label(root, text="Menstrual Cycle Length (days):", font=label_font).pack(pady=5)
entry_cycle_length = tk.Entry(root)
entry_cycle_length.pack(pady=5)

tk.Label(root, text="Average Sleep Hours:", font=label_font).pack(pady=5)
entry_sleep_hours = tk.Entry(root)
entry_sleep_hours.pack(pady=5)

tk.Label(root, text="Do you have acne? (Yes/No):", font=label_font).pack(pady=5)
entry_acne = tk.Entry(root)
entry_acne.pack(pady=5)

tk.Label(root, text="Do you have excessive hair growth? (Yes/No):", font=label_font).pack(pady=5)
entry_hair_growth = tk.Entry(root)
entry_hair_growth.pack(pady=5)

# Button to open the camera
button_camera = tk.Button(root, text="Open Camera", font=button_font, bg="#80c1ff", fg="white", command=open_camera)
button_camera.pack(pady=10)

# Label to show the camera feed
img_label = tk.Label(root)
img_label.pack(pady=5)

# Capture button
button_capture = tk.Button(root, text="Capture Image", font=button_font, bg="#80c1ff", fg="white", command=capture_image)
button_capture.pack(pady=5)

# Result labels
label_bmi = tk.Label(root, text="BMI:", font=label_font)
label_bmi.pack(pady=10)

label_risk = tk.Label(root, text="PCOS Risk:", font=label_font)
label_risk.pack(pady=10)

# Button to check the final PCOS risk
button_check = tk.Button(root, text="Check PCOS Risk", font=button_font, bg="#0059b3", fg="white", command=show_result)
button_check.pack(pady=10)

# Start the GUI loop
root.mainloop()

# Clean up the camera when the application is closed
if cap is not None:
    cap.release()
    cv2.destroyAllWindows()
