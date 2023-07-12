import tkinter as tk
import time
import random


def start_screen():
    label_text.set("Welcome to the Speed Typing Test!")


def display_text():
    global target_text
    target_text = load_text()
    text_widget.config(state=tk.NORMAL)
    text_widget.delete("1.0", tk.END)
    text_widget.insert(tk.END, target_text)
    text_widget.config(state=tk.DISABLED)
    wpm_label.config(text="WPM: 0")
    start_button.config(state=tk.DISABLED)
    root.bind('<Key>', check_input)
    root.focus_set()
    global current_text, start_time
    current_text = ""
    start_time = time.time()


def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()


def update_wpm():
    elapsed_time = max(time.time() - start_time, 1)
    wpm = round((len(current_text) / (elapsed_time / 60)) / 5)
    wpm_label.config(text=f"WPM: {wpm}")


def check_input(event):
    global current_text, target_text
    key = event.char

    if key == '\x1b':  # Escape key
        root.quit()
    elif key == '\x08':  # Backspace key
        if len(current_text) > 0:
            current_text = current_text[:-1]
    elif len(current_text) < len(target_text):
        if key == target_text[len(current_text)]:
            current_text += key

    update_wpm()
    display_current_text()

    if current_text == target_text:
        root.unbind('<Key>')
        completion_label.config(
            text="Perfect! You typed the phrase correctly.")
        start_button.config(text="Play Again", state=tk.NORMAL)


def display_current_text():
    text_widget.config(state=tk.NORMAL)
    text_widget.delete("1.0", tk.END)
    for i, char in enumerate(target_text):
        if i < len(current_text):
            if char == current_text[i]:
                text_widget.insert(tk.END, char, "correct")
                text_widget.tag_config("correct", foreground="green")
            else:
                text_widget.insert(tk.END, char, "incorrect")
                text_widget.tag_config("incorrect", foreground="red")
        else:
            text_widget.insert(tk.END, char, "incorrect")
            text_widget.tag_config("incorrect", foreground="red")
    text_widget.config(state=tk.DISABLED)


def play_again():
    completion_label.config(text="")
    completion_label.config(fg="black")
    start_button.config(text="Start", state=tk.DISABLED)
    display_text()


root = tk.Tk()
root.title("Speed Typing Test")

label_text = tk.StringVar()
start_screen_label = tk.Label(
    root, textvariable=label_text, font=("Helvetica", 20, "bold"))
start_screen_label.pack(pady=20)

text_widget = tk.Text(root, font=("Courier", 20), width=40, height=10)
text_widget.pack()

wpm_label = tk.Label(root, font=("Courier", 12))
wpm_label.pack()

completion_label = tk.Label(root, font=("Helvetica", 14, "bold"))
completion_label.pack()

start_button = tk.Button(
    root, text="Start", command=display_text, font=("Helvetica", 14, "bold"))
start_button.pack(pady=20)

current_text = ""
target_text = ""
start_time = 0

start_screen()

root.mainloop()
