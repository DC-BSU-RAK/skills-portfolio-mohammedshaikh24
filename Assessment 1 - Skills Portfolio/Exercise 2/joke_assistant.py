import tkinter as tk
import random
import os
import sys

# --- custom styling ---
color_theme = {
    'background': '#002b36',  # dark cyan/solarized dark
    'foreground': '#fdf6e3',  # light text/solarized light
    'highlight': '#268bd2',   # blue accent
    'secondary': '#859900',  # green accent for actions
    'font_style': 'consolas',
    'font_size_title': 20,
    'font_size_joke': 16,
    'font_size_button': 12,
}

# --- main application class ---
class jokeassistantapp:
    # constructor sets up the app state and the main window
    def __init__(self, master, joke_file_content):
        self.master = master
        self.master.title("alexa tell me a joke")
        self.master.geometry("550x300")
        self.master.configure(bg=color_theme['background'])

        self.jokes = self.load_jokes(joke_file_content)
        self.current_joke_parts = (None, None)
        
        # main content frame
        self.main_frame = tk.Frame(master, bg=color_theme['background'])
        self.main_frame.pack(pady=20, padx=20, fill='both', expand=True)

        self.setup_ui()
        self.display_welcome()

    def load_jokes(self, content):
        """reads joke data and splits them into a list of (setup, punchline) tuples."""
        jokes_list = []
        for line in content.strip().split('\n'):
            if '?' in line:
                try:
                    # split the line exactly once at the first '?'
                    setup, punchline = line.split('?', 1)
                    # clean up and store
                    jokes_list.append((setup.strip(), punchline.strip()))
                except ValueError:
                    # handle lines without content after the separator
                    continue
        return jokes_list

    def setup_ui(self):
        """initializes the ui elements."""
        # joke setup label
        self.setup_label = tk.Label(self.main_frame, text="", bg=color_theme['background'], fg=color_theme['highlight'], font=(color_theme['font_style'], color_theme['font_size_joke'], 'bold'), wraplength=500, justify=tk.CENTER)
        self.setup_label.pack(pady=(20, 5), fill='x')

        # punchline label
        self.punchline_label = tk.Label(self.main_frame, text="", bg=color_theme['background'], fg=color_theme['foreground'], font=(color_theme['font_style'], color_theme['font_size_joke']), wraplength=500, justify=tk.CENTER)
        self.punchline_label.pack(pady=5, fill='x')

        # button frame for controls
        self.button_frame = tk.Frame(self.main_frame, bg=color_theme['background'])
        self.button_frame.pack(pady=(20, 10))

        # 1. tell joke button (initially main button)
        self.tell_joke_btn = tk.Button(self.button_frame, text="alexa, tell me a joke", command=self.tell_new_joke, bg=color_theme['secondary'], fg=color_theme['background'], font=(color_theme['font_style'], color_theme['font_size_button']), padx=10)
        self.tell_joke_btn.pack(side=tk.LEFT, padx=10)
        
        # 2. show punchline button
        self.punchline_btn = tk.Button(self.button_frame, text="show punchline", command=self.show_punchline, state=tk.DISABLED, bg=color_theme['highlight'], fg=color_theme['background'], font=(color_theme['font_style'], color_theme['font_size_button']), padx=10)
        self.punchline_btn.pack(side=tk.LEFT, padx=10)

        # 3. next joke button
        self.next_joke_btn = tk.Button(self.button_frame, text="next joke", command=self.tell_new_joke, state=tk.DISABLED, bg=color_theme['highlight'], fg=color_theme['background'], font=(color_theme['font_style'], color_theme['font_size_button']), padx=10)
        self.next_joke_btn.pack(side=tk.LEFT, padx=10)

        # 4. quit button
        self.quit_btn = tk.Button(self.button_frame, text="quit", command=self.master.destroy, bg=color_theme['secondary'], fg=color_theme['background'], font=(color_theme['font_style'], color_theme['font_size_button']), padx=10)
        self.quit_btn.pack(side=tk.LEFT, padx=10)

    def display_welcome(self):
        """shows initial welcome message."""
        self.setup_label.config(text="welcome to the joke assistant!")
        self.punchline_label.config(text="click 'alexa, tell me a joke' to begin.")
        self.punchline_btn.config(state=tk.DISABLED)
        self.next_joke_btn.config(state=tk.DISABLED)

    def tell_new_joke(self):
        """randomly selects and displays a new joke setup."""
        if not self.jokes:
            self.setup_label.config(text="sorry, i ran out of jokes! ensure randomJokes.txt is in the correct directory.")
            self.punchline_label.config(text="")
            self.punchline_btn.config(state=tk.DISABLED)
            self.next_joke_btn.config(state=tk.DISABLED)
            return

        # select random joke
        self.current_joke_parts = random.choice(self.jokes)
        setup, _ = self.current_joke_parts

        # display setup, hide punchline
        self.setup_label.config(text=setup + "?")
        self.punchline_label.config(text="")
        
        # enable/disable buttons
        self.tell_joke_btn.config(state=tk.DISABLED)
        self.punchline_btn.config(state=tk.NORMAL)
        self.next_joke_btn.config(state=tk.DISABLED)

    def show_punchline(self):
        """displays the punchline of the current joke."""
        _, punchline = self.current_joke_parts
        self.punchline_label.config(text=punchline)
        
        # enable/disable buttons
        self.punchline_btn.config(state=tk.DISABLED)
        self.tell_joke_btn.config(state=tk.NORMAL)
        self.next_joke_btn.config(state=tk.NORMAL)


# --- run application ---
if __name__ == '__main__':
    joke_file_name = "randomJokes.txt"
    joke_data = ""
    
    # safer pathing: look for the file relative to the script's own directory
    try:
        script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        file_path = os.path.join(script_dir, joke_file_name)
        
        with open(file_path, 'r') as f:
            joke_data = f.read()
            
    except filenotfounderror:
        print(f"error: '{joke_file_name}' not found. please ensure the file is in the script's directory.")
        # provide a fallback message for the app ui
        joke_data = "file not found?sorry, i can't find my joke book."
    except exception as e:
        print(f"an unexpected error occurred while reading the file: {e}")
        joke_data = "read error?something went wrong reading the file."

    root = tk.Tk()
    app = jokeassistantapp(root, joke_data)
    root.mainloop()