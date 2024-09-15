import tkinter as tk
from tkinter import messagebox, ttk
import requests
import html

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Quiz Application")

        self.setup_ui()
        self.score = 0
        self.question_index = 0
        self.questions = []

    def setup_ui(self):
        # Topic Entry
        topic_frame = tk.Frame(self.root)
        topic_frame.pack(pady=10)
        topic_label = tk.Label(topic_frame, text="Enter Topic (e.g., General Knowledge, Science):")
        topic_label.pack(side=tk.LEFT)
        self.topic_entry = tk.Entry(topic_frame, width=30)
        self.topic_entry.pack(side=tk.LEFT)

        # Difficulty Selection
        difficulty_frame = tk.Frame(self.root)
        difficulty_frame.pack(pady=10)
        difficulty_label = tk.Label(difficulty_frame, text="Select Difficulty:")
        difficulty_label.pack(side=tk.LEFT)
        self.difficulty = tk.StringVar(value="easy")
        self.easy_rb = ttk.Radiobutton(difficulty_frame, text="Easy", variable=self.difficulty, value="easy")
        self.easy_rb.pack(side=tk.LEFT)
        self.moderate_rb = ttk.Radiobutton(difficulty_frame, text="Moderate", variable=self.difficulty, value="medium")
        self.moderate_rb.pack(side=tk.LEFT)
        self.difficult_rb = ttk.Radiobutton(difficulty_frame, text="Difficult", variable=self.difficulty, value="hard")
        self.difficult_rb.pack(side=tk.LEFT)

        # Start Button
        self.start_button = ttk.Button(self.root, text="Start Quiz", command=self.start_quiz)
        self.start_button.pack(pady=10)

        # Question Label
        self.question_label = tk.Label(self.root, text="", wraplength=400, justify=tk.LEFT)
        self.question_label.pack(pady=10)

        # Options Frame
        self.options_frame = tk.Frame(self.root)
        self.options_frame.pack(pady=10)

    def start_quiz(self):
        topic = self.topic_entry.get().lower()
        difficulty = self.difficulty.get()

        if topic:
            self.fetch_questions(topic, difficulty)
        else:
            messagebox.showwarning("Input Error", "Please enter a topic.")

    def fetch_questions(self, topic, difficulty):
        # Predefined categories (can be expanded)
        categories = {
            "general knowledge": 9,
            "science": 17,
            "math": 19,
            "history": 23
            # Add more categories as needed
        }

        if topic not in categories:
            messagebox.showwarning("Input Error", "Invalid topic. Please enter a valid topic (e.g., General Knowledge, Science).")
            return

        category_id = categories[topic]
        url = f"https://opentdb.com/api.php?amount=10&category={category_id}&difficulty={difficulty}&type=multiple"
        response = requests.get(url)
        data = response.json()

        if data['response_code'] == 0:
            self.questions = data['results']
            self.display_question()
        else:
            messagebox.showerror("Error", "Failed to fetch questions. Please try again.")

    def display_question(self):
        if self.question_index < len(self.questions):
            question_data = self.questions[self.question_index]
            self.question_label.config(text=html.unescape(question_data['question']))

            for widget in self.options_frame.winfo_children():
                widget.destroy()

            correct_answer = question_data['correct_answer']
            options = question_data['incorrect_answers'] + [correct_answer]
            options = sorted(options)

            def check_answer(selected_option):
                if selected_option == correct_answer:
                    self.score += 1
                self.question_index += 1
                self.display_question()

            for option in options:
                button = ttk.Button(self.options_frame, text=html.unescape(option), command=lambda opt=option: check_answer(opt))
                button.pack(anchor="w")
        else:
            self.show_result()

    def show_result(self):
        self.question_label.config(text=f"Your Score: {self.score}/{len(self.questions)}")
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        suggestion = self.get_suggestion()

        messagebox.showinfo("Quiz Completed", f"Your Score: {self.score}/{len(self.questions)}\n{suggestion}")
        self.reset_quiz()

    def get_suggestion(self):
        if self.score > 7:
            return "Excellent!"
        elif self.score > 4:
            return "Good job! Keep practicing."
        else:
            return "You need more practice."

    def reset_quiz(self):
        self.score = 0
        self.question_index = 0
        self.questions = []
        self.topic_entry.delete(0, tk.END)
        self.question_label.config(text="")
        self.start_button.config(text="Start Quiz", command=self.start_quiz)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
