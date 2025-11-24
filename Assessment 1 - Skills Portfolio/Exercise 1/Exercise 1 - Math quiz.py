# python program for a tkinter-based maths quiz
import tkinter as tk
from tkinter import messagebox
import random

# --- quiz configuration ---
total_questions = 10
score_per_first_try = 10
score_per_second_try = 5
quiz_difficulty_settings = {
    'easy': (1, 9),      # single digits
    'moderate': (10, 99),  # double digits
    'advanced': (1000, 9999) # four digits
}

# --- custom styling ---
color_theme = {
    'background': '#1f1f1f',
    'foreground': '#ffffff',
    'highlight': '#00ff7f',
    'secondary': '#ff4500',
    'wrong': '#dc143c',
    'correct': '#32cd32',
    'font_style': 'calibri',
    'font_size_large': 18,
    'font_size_medium': 14,
}

# --- main application class ---
class mathsquizapp:
    # constructor sets up the app state and the main window
    def __init__(self, master):
        self.master = master
        self.master.title("arithmetic speed challenge")
        self.master.geometry("500x400")
        self.master.configure(bg=color_theme['background'])

        # quiz state variables
        self.difficulty = None
        self.score = 0
        self.current_question = 0
        self.attempts = 0
        self.num1 = 0
        self.num2 = 0
        self.op = ''
        self.correct_answer = 0

        # ui widgets container
        self.main_frame = tk.Frame(master, bg=color_theme['background'])
        self.main_frame.pack(pady=20, padx=20, fill='both', expand=True)

        self.display_menu()

    # --- functional requirements (using specified function names) ---

    def display_menu(self):
        # clears any existing widgets
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # title label
        tk.Label(self.main_frame, text="~ choose your skill level ~", font=(color_theme['font_style'], color_theme['font_size_large'], 'bold'), bg=color_theme['background'], fg=color_theme['highlight']).pack(pady=20)

        # instruction label
        tk.Label(self.main_frame, text="choose your challenge:", font=(color_theme['font_style'], color_theme['font_size_medium']), bg=color_theme['background'], fg=color_theme['foreground']).pack(pady=10)

        # buttons for difficulty selection
        for i, (level, _) in enumerate(quiz_difficulty_settings.items()):
            button = tk.Button(self.main_frame, text=f"{i+1}. {level.capitalize()}",
                               command=lambda l=level: self.start_quiz(l),
                               bg=color_theme['highlight'], fg=color_theme['background'],
                               font=(color_theme['font_style'], color_theme['font_size_medium']))
            button.pack(pady=8, ipadx=10)

    def start_quiz(self, difficulty_level):
        """initializes quiz state and starts the first question."""
        self.difficulty = difficulty_level
        self.score = 0
        self.current_question = 0
        self.attempts = 0
        self.display_problem()

    def random_int(self, difficulty):
        """determines the values used in each question based on difficulty."""
        min_val, max_val = quiz_difficulty_settings[difficulty]
        # generates a random integer within the specified range
        return random.randint(min_val, max_val)

    def decide_operation(self):
        """randomly decides whether the problem is addition or subtraction."""
        return random.choice(['+', '-'])

    def display_problem(self):
        """displays the question to the user and accepts their answer."""
        # check if quiz is finished
        if self.current_question >= total_questions:
            return self.display_results()

        # clear frame for new question
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.current_question += 1
        self.attempts = 1 # reset attempts for new question

        # generate new problem values
        self.num1 = self.random_int(self.difficulty)
        self.num2 = self.random_int(self.difficulty)
        self.op = self.decide_operation()
        
        # calculate correct answer
        if self.op == '+':
            self.correct_answer = self.num1 + self.num2
        else:
            self.correct_answer = self.num1 - self.num2

        question_text = f"question {self.current_question} of {total_questions}:"
        problem_text = f"{self.num1} {self.op} {self.num2} ="

        # score display
        tk.Label(self.main_frame, text=f"current score: {self.score}", bg=color_theme['background'], fg=color_theme['secondary'], font=(color_theme['font_style'], color_theme['font_size_medium'])).pack(pady=5)
        
        # question label
        tk.Label(self.main_frame, text=question_text, bg=color_theme['background'], fg=color_theme['foreground'], font=(color_theme['font_style'], color_theme['font_size_medium'])).pack(pady=(15, 0))
        
        # problem label
        tk.Label(self.main_frame, text=problem_text, bg=color_theme['background'], fg=color_theme['highlight'], font=(color_theme['font_style'], color_theme['font_size_large'], 'bold')).pack(pady=10)
        
        # answer entry
        self.answer_entry = tk.Entry(self.main_frame, font=(color_theme['font_style'], color_theme['font_size_medium']), width=10, justify='center', bg=color_theme['foreground'], fg=color_theme['background'])
        self.answer_entry.pack(pady=10, ipady=5)

        # submit button
        tk.Button(self.main_frame, text="submit answer",
                  command=self.check_answer_and_proceed,
                  bg=color_theme['secondary'], fg=color_theme['background'],
                  font=(color_theme['font_style'], color_theme['font_size_medium'])).pack(pady=15, ipadx=10)

        # feedback label
        self.feedback_label = tk.Label(self.main_frame, text="", bg=color_theme['background'], fg=color_theme['foreground'], font=(color_theme['font_style'], color_theme['font_size_medium']))
        self.feedback_label.pack(pady=10)

    def is_correct(self, user_answer):
        """checks whether the user's answer was correct."""
        try:
            return int(user_answer) == self.correct_answer
        except ValueError:
            # handle non-numeric input gracefully
            return False

    def check_answer_and_proceed(self):
        """handles user input, scoring, and progression."""
        user_answer = self.answer_entry.get().strip()

        if self.is_correct(user_answer):
            points = score_per_first_try if self.attempts == 1 else score_per_second_try
            self.score += points
            
            # display success message
            self.feedback_label.config(text=f"correct! awarded {points} points.", fg=color_theme['correct'])
            
            # wait briefly and move to next problem
            self.master.after(1000, self.display_problem)

        else:
            if self.attempts == 1:
                # first incorrect attempt
                self.attempts += 1
                self.feedback_label.config(text="incorrect. try once more!", fg=color_theme['wrong'])
            else:
                # second incorrect attempt
                self.feedback_label.config(text=f"incorrect. the answer was {self.correct_answer}.", fg=color_theme['wrong'])
                
                # wait briefly and move to next problem
                self.master.after(1500, self.display_problem)

    def get_rank(self):
        """determines the user's rank based on their final score."""
        if self.score > 90:
            return "a+"
        elif self.score >= 80:
            return "a"
        elif self.score >= 70:
            return "b"
        elif self.score >= 60:
            return "c"
        else:
            return "d"

    def display_results(self):
        """outputs the user's final score and rank."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        max_score = total_questions * score_per_first_try
        rank = self.get_rank()

        tk.Label(self.main_frame, text="~ quiz finished ~", font=(color_theme['font_style'], color_theme['font_size_large'], 'bold'), bg=color_theme['background'], fg=color_theme['highlight']).pack(pady=20)

        tk.Label(self.main_frame, text=f"final score: {self.score} / {max_score}", bg=color_theme['background'], fg=color_theme['secondary'], font=(color_theme['font_style'], color_theme['font_size_medium'])).pack(pady=10)
        
        tk.Label(self.main_frame, text=f"your rank: {rank.upper()}", bg=color_theme['background'], fg=color_theme['foreground'], font=(color_theme['font_style'], color_theme['font_size_large'], 'bold')).pack(pady=10)
        
        # replay option
        tk.Label(self.main_frame, text="ready for another round?", bg=color_theme['background'], fg=color_theme['foreground'], font=(color_theme['font_style'], color_theme['font_size_medium'])).pack(pady=20)

        tk.Button(self.main_frame, text="new game",
                  command=self.display_menu,
                  bg=color_theme['highlight'], fg=color_theme['background'],
                  font=(color_theme['font_style'], color_theme['font_size_medium'])).pack(pady=10, ipadx=10)
        
        tk.Button(self.main_frame, text="close app",
                  command=self.master.destroy,
                  bg=color_theme['wrong'], fg=color_theme['background'],
                  font=(color_theme['font_style'], color_theme['font_size_medium'])).pack(pady=10, ipadx=10)

# --- run application ---
if __name__ == '__main__':
    root = tk.Tk()
    app = mathsquizapp(root)
    root.mainloop()