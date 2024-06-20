import tkinter as tk
from tkinter import messagebox
import pyautogui
import time
import requests
import io
import threading

# Function to get the color at a specific position on the screen
def get_color_at_position(x, y):
    try:
        screenshot = pyautogui.screenshot()
        color = screenshot.getpixel((x, y))
        return color
    except Exception as e:
        print("Error:", e)
        return None

# Function to send a webhook message with an attached image
def send_webhook_message_with_image(webhook_url, image_bytes):
    files = {'file': ('screenshot.png', image_bytes, 'image/png')}
    requests.post(webhook_url, files=files)

# Main function to be run in a separate thread
def main_loop(webhook_url, pos_a, pos_b, pos_c):
    while True:
        try:
            color_a = get_color_at_position(*pos_a)
            color_b = get_color_at_position(*pos_b)
            color_c = get_color_at_position(*pos_c)

            print("Color at position A:", color_a)
            print("Color at position B:", color_b)
            print("Color at position C:", color_c)

            if color_a == (0, 0, 0) and color_b != (0, 0, 0) and (color_c == (0, 0, 0) or color_c == (1, 0, 1)):
                print("Rare Found!")
                time.sleep(2)
                screenshot = pyautogui.screenshot()
                img_byte_array = io.BytesIO()
                screenshot.save(img_byte_array, format='PNG')
                img_byte_array.seek(0)
                send_webhook_message_with_image(webhook_url, img_byte_array)
                time.sleep(14)
            else:
                print("Not Rare")
        except Exception as e:
            print("Error:", e)
        
        time.sleep(0.1)

# Function to start the main loop in a separate thread
def start_script():
    try:
        webhook_url = webhook_entry.get()
        if not webhook_url:
            messagebox.showerror("Error", "Please enter a valid webhook URL.")
            return

        pos_a = (int(position_a_x_entry.get()), int(position_a_y_entry.get()))
        pos_b = (int(position_b_x_entry.get()), int(position_b_y_entry.get()))
        pos_c = (int(position_c_x_entry.get()), int(position_c_y_entry.get()))

        thread = threading.Thread(target=main_loop, args=(webhook_url, pos_a, pos_b, pos_c), daemon=True)
        thread.start()
        start_button.config(state=tk.DISABLED)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid coordinates.")

# Function to display the current mouse position
def show_mouse_position():
    time.sleep(2)
    x, y = pyautogui.position()
    messagebox.showinfo("Mouse Position", f"Current mouse position: ({x}, {y})")

# Setting up the GUI
root = tk.Tk()
root.title("Unknown RNG Log")

frame = tk.Frame(root)
frame.pack(pady=20)

# Webhook URL Entry
webhook_label = tk.Label(frame, text="Enter Discord Webhook URL:",width=50)
webhook_label.pack(pady=5)

webhook_entry = tk.Entry(frame, width=50)
webhook_entry.pack(pady=5)

# Position A Entry
position_a_label = tk.Label(frame, text="Enter Position A (x, y) Corner 1:")
position_a_label.pack(pady=5)

position_a_frame = tk.Frame(frame)
position_a_frame.pack(pady=5)

position_a_x_entry = tk.Entry(position_a_frame, width=10)
position_a_x_entry.pack(side=tk.LEFT)
position_a_y_entry = tk.Entry(position_a_frame, width=10)
position_a_y_entry.pack(side=tk.LEFT)

# Position B Entry
position_b_label = tk.Label(frame, text="Enter Position B (x, y) Star Position:")
position_b_label.pack(pady=5)

position_b_frame = tk.Frame(frame)
position_b_frame.pack(pady=5)

position_b_x_entry = tk.Entry(position_b_frame, width=10)
position_b_x_entry.pack(side=tk.LEFT)
position_b_y_entry = tk.Entry(position_b_frame, width=10)
position_b_y_entry.pack(side=tk.LEFT)

# Position C Entry
position_c_label = tk.Label(frame, text="Enter Position C (x, y) Corner 2:")
position_c_label.pack(pady=5)

position_c_frame = tk.Frame(frame)
position_c_frame.pack(pady=5)

position_c_x_entry = tk.Entry(position_c_frame, width=10)
position_c_x_entry.pack(side=tk.LEFT)
position_c_y_entry = tk.Entry(position_c_frame, width=10)
position_c_y_entry.pack(side=tk.LEFT)

# Start Button
start_button = tk.Button(frame, text="Start Script", command=start_script)
start_button.pack(pady=20)

# Mouse Position Button
mouse_position_button = tk.Button(frame, text="Show Mouse Position (After 2 Seconds)", command=show_mouse_position)
mouse_position_button.pack(pady=10)

root.mainloop()
