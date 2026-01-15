
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import requests
import threading
import sqlite3
import pygame  # Import pygame for audio playback
import os

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Function to toggle password visibility
def toggle_password():
    if entry_password.cget('show') == '':
        entry_password.config(show='*')
    else:
        entry_password.config(show='')

def toggle_reg_password():
    if entry_reg_password.cget('show') == '':
        entry_reg_password.config(show='*')
    else:
        entry_reg_password.config(show='')

# Function to show the password requirements
def show_password_requirements(event):
    lbl_password_requirements.config(text="Password must contain 8 characters with at least one number and one special character.")

# Function to play audio automatically
def play_audio(file_path):
    try:
        # Load the audio file
        pygame.mixer.music.load(file_path)
        # Play the audio file
        pygame.mixer.music.play()
    except pygame.error as e:
        messagebox.showerror("Error", f"Unable to play the audio file: {str(e)}")

# Function to replay audio
def replay_audio():
    file_path = entry_file_path.get()
    if file_path:
        play_audio(file_path)
    else:
        messagebox.showwarning("No file", "Please select a file first to replay.")

# File selection for API and audio play
def select_file():
    file_path = filedialog.askopenfilename(
        title="Select an audio file", 
        filetypes=(("WAV files", ".wav"), ("All files", ".*"))
    )
    if file_path:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, file_path)

        # Automatically play the selected audio file
        play_audio(file_path)


# API processing
def process_file():
    file_path = entry_file_path.get()
    if not file_path:
        messagebox.showwarning(
            "No file selected",
            "Please select an audio file to process."
        )
        return

    progress_bar.start()
    btn_process.config(state=tk.DISABLED)

    threading.Thread(
        target=run_api,
        args=(file_path,),
        daemon=True
    ).start()


def run_api(file_path):
    url = "https://api.openai.com/v1/audio/transcriptions"

    API_KEY = os.getenv("OPENAI_API_KEY")
    if not API_KEY:
        messagebox.showerror(
            "API Key Missing",
            "OPENAI_API_KEY environment variable is not set"
        )
        progress_bar.stop()
        btn_process.config(state=tk.NORMAL)
        return

    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    try:
        with open(file_path, 'rb') as audio_file:
            files = {
                "file": audio_file,
                "model": (None, "whisper-1")
            }

            response = requests.post(url, headers=headers, files=files)
            result = response.json()
            show_result(result)

    except Exception as e:
        show_result({"error": str(e)})

    finally:
        progress_bar.stop()
        btn_process.config(state=tk.NORMAL)


# Display API result
def show_result(result):
    if 'error' in result:
        output_text = f"Error: {result['error']}"
    else:
        output_text = f"Transcription: {result.get('text', 'No transcription available')}"

    lbl_result.config(text=output_text)  # Update the result label in the main frame

# Function to show a frame
def show_frame(frame):
    frame.tkraise()

# Connect to the SQLite database
conn = sqlite3.connect('usersdata.db')
c = conn.cursor()

# Create a table for user registration
c.execute('''
    CREATE TABLE IF NOT EXISTS usersdata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

# Function to register a new user
def register_user():
    username = entry_reg_username.get()
    password = entry_reg_password.get()

    # Password validation logic
    if (len(password) < 8 or 
        not any(char.isdigit() for char in password) or 
        not any(not char.isalnum() for char in password)):
        messagebox.showwarning(
            "Invalid Password", 
            "Password must be at least 8 characters long, contain at least one number, and one special character."
        )
        return

    try:
        c.execute('INSERT INTO usersdata (username, password) VALUES (?, ?)', (username, password))
        conn.commit()

        messagebox.showinfo("Registration Successful", "User registered successfully!")
        entry_reg_username.delete(0, tk.END)
        entry_reg_password.delete(0, tk.END)
        show_frame(frame_login)
    except sqlite3.IntegrityError:
        messagebox.showwarning("Registration Failed", "Username already exists. Please choose a different one.")

# Function to log in the user
def login_user():
    username = entry_username.get()
    password = entry_password.get()

    c.execute('SELECT * FROM usersdata WHERE username = ? AND password = ?', (username, password))
    user = c.fetchone()

    if user:
        messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
        show_frame(frame_main)
    else:
        messagebox.showwarning("Login Failed", "Invalid username or password.")

# Main window setup
root = tk.Tk()
root.title("Speech-to-Text Application")
root.state('zoomed')

# Load the background images
login_bg_image_path = "LOGIN PG.jpg"  # The path where the login/register image is located
main_bg_image_path = "bg img stc.jpg"  # The path where the speech-to-text image is located

login_bg_image = Image.open(login_bg_image_path)
login_bg_photo = ImageTk.PhotoImage(login_bg_image)

main_bg_image = Image.open(main_bg_image_path)
main_bg_photo = ImageTk.PhotoImage(main_bg_image)

# Resize the background image to fill the entire frame for the main (speech-to-text) window
main_bg_image_resized = main_bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.Resampling.LANCZOS)
main_bg_photo_resized = ImageTk.PhotoImage(main_bg_image_resized)

# Set the root window to center everything
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Frames
frame_login = tk.Frame(root)
frame_register = tk.Frame(root)
frame_main = tk.Frame(root)

for frame in (frame_login, frame_register, frame_main):
    frame.grid(row=0, column=0, sticky='nsew')

# Center the contents of each frame
def center_frame_content(parent_frame, inner_frame):
    inner_frame.grid(row=0, column=0, padx=10, pady=10)
    parent_frame.grid_rowconfigure(0, weight=1)
    parent_frame.grid_columnconfigure(0, weight=1)

# Helper function to add the background image to a frame
def set_background(frame, image):
    background_label = tk.Label(frame, image=image)
    background_label.place(relwidth=1, relheight=1)  # Make it cover the entire frame
    return background_label

# Add background to login, register, and main frames
login_bg_label = set_background(frame_login, login_bg_photo)
register_bg_label = set_background(frame_register, login_bg_photo)

# Add resized background to the main frame
main_bg_label = set_background(frame_main, main_bg_photo_resized)

# Login Frame
frame_login_inner = tk.Frame(frame_login, bg="dark blue",  relief=tk.GROOVE, bd=5)
center_frame_content(frame_login, frame_login_inner)

tk.Label(frame_login_inner, text="Login", font=('Castellar', 18, 'bold'), bg="darkslate blue").pack(pady=20)
tk.Label(frame_login_inner, text="Username", font=('Eras Demi ITC', 12), bg="Cornflower Blue").pack(pady=5)

entry_username = tk.Entry(frame_login_inner, font=('Eras Demi ITC', 12)) 
entry_username.pack(pady=5, anchor='center')

tk.Label(frame_login_inner, text="Password", font=('Eras Demi ITC', 12), bg="Cornflower Blue").pack(pady=5)

password_frame = tk.Frame(frame_login_inner)
password_frame.pack(pady=5, anchor='center')

entry_password = tk.Entry(password_frame, show='*', font=('Arial', 12))
entry_password.pack(side=tk.LEFT, fill=tk.X, expand=True)

btn_toggle_password = tk.Button(password_frame, text='👁️', font=('Arial', 10), command=toggle_password, relief=tk.FLAT)
btn_toggle_password.pack(side=tk.LEFT, padx=5)

btn_login = tk.Button(frame_login_inner, text="Login", command=login_user, font=('castellar', 12, 'bold'), bg="green", fg="white")
btn_login.pack(pady=20)

btn_register = tk.Button(frame_login_inner, text="New user? Register Now", command=lambda: show_frame(frame_register), font=('Eras Demi ITC', 10, 'bold'))
btn_register.pack(pady=10)

# Register Frame
frame_register_inner = tk.Frame(frame_register, bg="Navy Blue",  relief=tk.GROOVE, bd=5)
center_frame_content(frame_register, frame_register_inner)

tk.Label(frame_register_inner, text="Register", font=('Castellar', 18, 'bold'), bg="SteelBlue1").pack(pady=20)
tk.Label(frame_register_inner, text="Username", font=('Eras Demi ITC', 12), bg="SteelBlue1").pack(pady=5)

entry_reg_username = tk.Entry(frame_register_inner, font=('Eras Demi ITC', 12))
entry_reg_username.pack(pady=5, anchor='center')

tk.Label(frame_register_inner, text="Password", font=('Eras Demi ITC', 12), bg="SteelBlue1").pack(pady=5)

password_frame_reg = tk.Frame(frame_register_inner)
password_frame_reg.pack(pady=5, anchor='center')

entry_reg_password = tk.Entry(password_frame_reg, show='*', font=('Arial', 12))
entry_reg_password.pack(side=tk.LEFT, fill=tk.X, expand=True)

btn_toggle_reg_password = tk.Button(password_frame_reg, text='👁️', font=('Arial', 10), command=toggle_reg_password, relief=tk.FLAT)
btn_toggle_reg_password.pack(side=tk.LEFT, padx=5)

entry_reg_password.bind('<FocusIn>', show_password_requirements)

lbl_password_requirements = tk.Label(frame_register_inner, text="", font=('Arial', 10), bg="SteelBlue1", fg="red")
lbl_password_requirements.pack()

btn_register_now = tk.Button(frame_register_inner, text="Register", command=register_user, font=('castellar', 12, 'bold'), bg="green", fg="white")
btn_register_now.pack(pady=20)

btn_back_to_login = tk.Button(frame_register_inner, text="Back to Login", command=lambda: show_frame(frame_login), font=('Eras Demi ITC', 10, 'bold'))
btn_back_to_login.pack(pady=10)

# Main Frame (Speech to Text)
frame_main_inner = tk.Frame(frame_main, bg="light gray", relief=tk.GROOVE, bd=5)
center_frame_content(frame_main, frame_main_inner)

tk.Label(frame_main_inner, text="Speech-to-Text Converter", font=('Castellar', 18, 'bold'), bg="gray").pack(pady=10)

frame_file = tk.Frame(frame_main_inner)
frame_file.pack(pady=10)

entry_file_path = tk.Entry(frame_file, width=40, font=('Eras Demi ITC', 12))
entry_file_path.pack(side=tk.LEFT, padx=5)

btn_browse = tk.Button(frame_file, text="Browse", command=select_file, font=('Eras Demi ITC', 12, 'bold'))
btn_browse.pack(side=tk.LEFT, padx=5)

btn_process = tk.Button(frame_main_inner, text="Convert", command=process_file, font=('castellar', 12, 'bold'), bg="green", fg="white")
btn_process.pack(pady=20)

progress_bar = ttk.Progressbar(frame_main_inner, mode='indeterminate')
progress_bar.pack(pady=10)

btn_replay_audio = tk.Button(frame_main_inner, text="Replay Audio", command=replay_audio, font=('Eras Demi ITC', 12, 'bold'), bg="blue", fg="white")
btn_replay_audio.pack(pady=10)

lbl_result = tk.Label(frame_main_inner, text="", font=('Arial', 12), wraplength=400)
lbl_result.pack(pady=10, padx=20)

btn_back_to_login_main = tk.Button(frame_main_inner, text="Logout", command=lambda: show_frame(frame_login), font=('Eras Demi ITC', 10, 'bold'))
btn_back_to_login_main.pack(pady=10)

# Initially show the login frame
show_frame(frame_login)

# Start the application
root.mainloop()





