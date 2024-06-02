# Previous code deleted the whole file,
# not just information inside.
# Code was rewritten so that it opens the 'highscore.txt',
# file in write and deletes the info then closes the file.

import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from ttkbootstrap import Style
from data import data
import json
import os

class HighscoreManager():
    def __init__(self, filename='highscore.txt'):
        self.filename = filename
        self.highscore = self.load_highscore()

    def load_highscore(self):
        highscore = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    highscore.append(json.loads(line.strip()))
        return highscore

    def save_highscore(self):
        with open(self.filename, 'w') as file:
            for entry in self.highscore:
                file.write(json.dumps(entry) + '\n')

    def add_highscore(self, name, score):
        self.highscore.append({'name': name, 'score': score})
        self.highscore = sorted(self.highscore,
                                key=lambda x: x['score'], reverse=True)
        self.save_highscore()

    def get_highscore(self, limit=10):
        return self.highscore[:limit]

    def delete_highscore(self):
        self.highscore = []
        with open(self.filename, 'w') as file:
            pass  # Open the file in write mode and immediately close it to clear its contents
        messagebox.showinfo("Highscores Deleted", "All highscores have been deleted.")


highscore_manager = HighscoreManager()

# Initializing the quiz
def initialize_quiz():
    response = messagebox.askyesno("Quiz Start\n",
                                   "This is a test which will test your knowledge on Te Reo Maori\n"
                                   "As you go on, the questions will become harder\n"
                                   "Will you continue?")
    if response:
        print("Goodluck!")
        show_question()
    else:
        root.destroy()


# Display Questions
def show_question():
    question = data[current_question]
    question_lbl.config(text=question["question"])

    # Display different questions
    choices = question["choices"]
    for i in range(4):
        choice_button[i].config(text=choices[i], state="normal")

    feedback.config(text="")
    next_button.config(state="disabled")


# Check answer
def check(choice):
    question = data[current_question]
    selected_choice = choice_button[choice].cget("text")

    if selected_choice == question["answer"]:
        global score
        score += 1
        score_lbl.config(text="Score: {}/{}".format(score, len(data)))
        feedback.config(text="Correct!", foreground="green")
    else:
        feedback.config(text="Incorrect!\n"
                             "The correct answer is:\n"
                             + question["answer"], foreground="red")

    for button in choice_button:
        button.config(state="disabled")
    next_button.config(state="normal")


# Next question function
def next_question():
    global current_question
    current_question += 1

    if current_question < len(data):
        show_question()
    else:
        name = simpledialog.askstring("Quiz Completed",
                                      "Quiz Completed! Your final score is: {}/{}\n"
                                      "Enter your name: ".format(score, len(data)))
        if name:
            highscore_manager.add_highscore(name, score)
        root.destroy()


# Function to delete highscore
def delete_highscore():
    highscore_manager.delete_highscore()


# Create display
root = tk.Tk()
root.title("Te Reo Maori Quiz")
root.geometry("600x500")
style = Style(theme="darkly")

# Font
style.configure("label", font=("Times New Roman", 25))
style.configure("button", font=("Times New Roman", 20))

# Question Label
question_lbl = ttk.Label(
    root,
    anchor="center",
    wraplength=500,
    padding=10
)
question_lbl.pack(pady=10)

# Choice Button
choice_button = []
for i in range(4):
    button = ttk.Button(
        root,
        command=lambda: check(i)
    )
    button.pack(pady=5)
    choice_button.append(button)

# Feedback
feedback = ttk.Label(
    root,
    anchor="center",
    justify="center",
    padding=10
)
feedback.pack(pady=10)

score = 0

# Final Score
score_lbl = ttk.Label(
    root,
    text="Score: 0/{}".format(len(data)),
    anchor="center",
    padding=10
)
score_lbl.pack(pady=10)

# Ensuring button is only pressed in certain times
next_button = ttk.Button(
    root,
    text="Next",
    command=next_question,
    state="disabled"
)
next_button.pack(pady=10)

# Add a button to delete highscores
delete_button = ttk.Button(
    root,
    text="Delete Highscores",
    command=delete_highscore
)
delete_button.pack(pady=10)

current_question = 0

initialize_quiz()

root.mainloop()
