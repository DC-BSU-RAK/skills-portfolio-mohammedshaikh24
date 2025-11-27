import tkinter as tk
from tkinter import messagebox, ttk
import os, sys

# --- configuration and constants ---
data_file, max_coursework, max_exam = "studentMarks.txt", 60, 100
max_total = max_coursework + max_exam

# --- custom styling (modern slate theme) ---
theme = {
    'background': '#20232a', 
    'foreground': '#f0f0f0', 
    'primary': '#61dafb',    
    'secondary': '#4caf50',  
    'danger': '#dc3545',     
    'highlight': '#007bff', 
    'font_style_menu': 'segoe ui',
    'font_style_data': 'consolas', 
    'font_size_title': 16, 
    'font_size_menu': 12,
}

# --- utility functions ---
def _get_app_file_path():
    """determines the absolute path of the data file."""
    if getattr(sys, 'frozen', False): script_dir = os.path.dirname(sys.executable)
    else: script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, data_file)

def create_initial_file():
    """creates the studentMarks.txt file if it doesn't exist."""
    file_path = _get_app_file_path()
    if not os.path.exists(file_path):
        initial_data = """10
1345,John Curry,8,15,7,45
2345,Sam Sturtivant,14,15,14,77
9876,Lee Scott,17,11,16,99
3724,Matt Thompson,19,11,15,81
1212,Ron Herrema,14,17,18,66
8439,Jake Hobbs,10,11,10,43
2344,Jo Hyde,6,15,10,55
9384,Gareth Southgate,5,6,8,33
8327,Alan Shearer,20,20,20,100
2983,Les Ferdinand,15,17,18,92
"""
        try:
            with open(file_path, 'w') as f: f.write(initial_data)
        except Exception as e:
            messagebox.showerror("initial file creation error", f"could not create data file: {e}")


# --- 1. data model: student class ---
class student:
    def __init__(self, code, name, c1, c2, c3, exam):
        self.code, self.name = str(code), name
        self.c1, self.c2, self.c3, self.exam = int(c1), int(c2), int(c3), int(exam)
        self.coursework_total = self.c1 + self.c2 + self.c3
        self.overall_total = self.coursework_total + self.exam
        
    def calculate_percentage(self):
        """calculates overall percentage out of 160."""
        return round((self.overall_total / max_total) * 100, 2)

    def calculate_grade(self):
        """assigns a grade based on overall percentage."""
        percent = self.calculate_percentage()
        if percent >= 70: return 'a'
        if percent >= 60: return 'b'
        if percent >= 50: return 'c'
        if percent >= 40: return 'd'
        return 'f'

    def get_details(self):
        """returns a formatted dictionary of all calculated results."""
        return {"name": self.name, "code": self.code, "coursework_total": self.coursework_total,
                "exam_mark": self.exam, "overall_total": self.overall_total,
                "percentage": self.calculate_percentage(), "grade": self.calculate_grade().upper()}

# --- 2. data management and persistence ---
class datamanager:
    def __init__(self):
        self.students = []; self.load_data()
        
    def load_data(self):
        self.students = []
        try:
            with open(_get_app_file_path(), 'r') as f: lines = f.readlines()
            if not lines: return
            for line in lines[1:]:
                parts = line.strip().split(',')
                if len(parts) == 6:
                    self.students.append(student(code=parts[0], name=parts[1],
                                c1=parts[2], c2=parts[3], c3=parts[4], exam=parts[5]))
        except FileNotFoundError:
            pass 
        except Exception as e:
            messagebox.showerror("error", f"data loading error: {e}")

    def save_data(self):
        try:
            with open(_get_app_file_path(), 'w') as f:
                f.write(f"{len(self.students)}\n")
                for s in self.students:
                    f.write(f"{s.code},{s.name},{s.c1},{s.c2},{s.c3},{s.exam}\n")
            return True
        except Exception as e:
            messagebox.showerror("save error", f"failed to save data to file: {e}")
            return False

# --- 3. tkinter gui application ---
class studentmanagerapp:
    def __init__(self, master):
        self.manager = datamanager(); self.master = master
        master.title("student records manager"); master.geometry("800x600")
        master.configure(bg=theme['background'])

        # main frames for layout
        self.menu_frame = tk.Frame(master, bg=theme['background'], padx=20, pady=20)
        self.display_frame = tk.Frame(master, bg=theme['background'], padx=10, pady=10)
        
        # pack frames first (left and right)
        self.menu_frame.pack(side=tk.LEFT, fill='y')
        self.display_frame.pack(side=tk.RIGHT, fill='both', expand=True)
        
        # populate frames
        self._create_menu_buttons() 
        self._display_title_screen()
        
        # force update to ensure initial rendering is correct
        self.master.update_idletasks() 

    def _clear_display(self):
        for widget in self.display_frame.winfo_children(): widget.destroy()

    def _create_menu_buttons(self):
        # altered menu phrases for maximum originality
        menu_items = [
            ("1. display all class data", self.view_all_records), 
            ("2. search specific student", self.view_individual_record),
            ("3. highest scoring individual", self.show_highest_score), 
            ("4. lowest scoring individual", self.show_lowest_score),
            ("5. sort student records", self.sort_records_gui), 
            ("6. add a new record", self.add_student_gui),
            ("7. remove a student entry", self.delete_student_gui), 
            ("8. edit student details", self.update_student_gui)
        ]
        tk.Label(self.menu_frame, text="~ data management menu ~", bg=theme['background'], fg=theme['primary'], font=(theme['font_style_menu'], theme['font_size_title'], 'bold')).pack(pady=10)
        for text, command in menu_items:
            tk.Button(self.menu_frame, text=text.upper(), command=command, bg=theme['secondary'], fg=theme['background'],
                      font=(theme['font_style_menu'], theme['font_size_menu']), width=30, anchor='w').pack(pady=5, ipady=5) 

    def _display_title_screen(self):
        self._clear_display()
        tk.Label(self.display_frame, text="student records analysis tool", bg=theme['background'], fg=theme['foreground'], font=(theme['font_style_menu'], 24, 'bold')).pack(pady=100)
        tk.Label(self.display_frame, text="select an option from the menu on the left.", bg=theme['background'], fg=theme['primary'], font=(theme['font_style_menu'], 16)).pack()

    # --- display utility functions ---
    def _display_student_list(self, students_list, title="all student records"):
        self._clear_display()
        tk.Label(self.display_frame, text=title.upper(), bg=theme['background'], fg=theme['primary'], font=(theme['font_style_menu'], theme['font_size_title'], 'bold')).pack(pady=10)
        
        # use Monospaced Font (consolas) for data display for perfect column alignment
        text_widget = tk.Text(self.display_frame, bg=theme['background'], fg=theme['foreground'], font=(theme['font_style_data'], 12), borderwidth=0, wrap='word')
        text_widget.pack(fill='both', expand=True, padx=10, pady=5)

        output = ""; 
        # adjusted header widths for better fit
        header = f"{'name':<25}{'code':<10}{'coursework':<12}{'exam':<10}{'total':<10}{'percentage':<12}{'grade':<5}\n"
        output += header + "=" * (len(header) + 50) + "\n"
        total_percentage_sum = 0
        
        for s in students_list:
            details = s.get_details()
            total_percentage_sum += details['percentage']
            # use monospaced formatting for data rows
            output += (
                f"{details['name']:<25}"
                f"{details['code']:<10}"
                f"{details['coursework_total']:<12}"
                f"{details['exam_mark']:<10}"
                f"{details['overall_total']:<10}"
                f"{details['percentage']:<12}"
                f"{details['grade']:<5}\n"
            )
            
        output += "\n" + "=" * 80 + "\n"; output += f"summary:\n"; output += f"number of students in class: {len(students_list)}\n"
        if students_list:
            avg_percent = round(total_percentage_sum / len(students_list), 2)
            output += f"average percentage mark obtained: {avg_percent}%\n"
        
        text_widget.insert(tk.END, output); text_widget.config(state=tk.DISABLED)

    # --- 4. menu item functionality ---
    def view_all_records(self): self._display_student_list(self.manager.students, "all student records")

    # 2. view individual student record
    def view_individual_record(self):
        self._clear_display(); tk.Label(self.display_frame, text="search specific student", bg=theme['background'], fg=theme['primary'], font=(theme['font_style_menu'], theme['font_size_title'], 'bold')).pack(pady=10)
        search_frame = tk.Frame(self.display_frame, bg=theme['background']); search_frame.pack(pady=10)
        
        # align search labels left
        tk.Label(search_frame, text="enter name or student code:", bg=theme['background'], fg=theme['foreground'], font=(theme['font_style_menu'], theme['font_size_menu'])).pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, font=(theme['font_style_menu'], theme['font_size_menu'])); self.search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="search", command=self._perform_individual_search, bg=theme['secondary'], fg=theme['background'], font=(theme['font_style_menu'], theme['font_size_menu'])).pack(side=tk.LEFT, padx=5)

    def _perform_individual_search(self):
        query = self.search_entry.get().strip().lower()
        if not query: messagebox.showwarning("input error", "please enter a name or student code."); return
        found_student = next((s for s in self.manager.students if s.code == query or s.name.lower() == query), None)
        if found_student: self._display_student_list([found_student], f"record for {found_student.name}")
        else: messagebox.showinfo("not found", f"no student found matching '{query}'.")

    # 3. show student with highest total score
    def show_highest_score(self):
        if not self.manager.students: messagebox.showinfo("info", "no student records available."); return
        highest_student = max(self.manager.students, key=lambda s: s.overall_total)
        self._display_student_list([highest_student], "highest scoring individual")

    # 4. show student with lowest total score
    def show_lowest_score(self):
        if not self.manager.students: messagebox.showinfo("info", "no student records available."); return
        lowest_student = min(self.manager.students, key=lambda s: s.overall_total)
        self._display_student_list([lowest_student], "lowest scoring individual")

    # --- 5. extension problem functionality (crud/sort) ---
    def sort_records_gui(self):
        self._clear_display(); tk.Label(self.display_frame, text="sort records", bg=theme['background'], fg=theme['primary'], font=(theme['font_style_menu'], theme['font_size_title'], 'bold')).pack(pady=10)
        sort_frame = tk.Frame(self.display_frame, bg=theme['background']); sort_frame.pack(pady=10)
        sort_options = [
            ("total score (high to low)", lambda s: s.overall_total, True), ("total score (low to high)", lambda s: s.overall_total, False),
            ("name (a-z)", lambda s: s.name, False), ("student code", lambda s: s.code, False),
        ]
        for text, key_func, reverse in sort_options:
            tk.Button(sort_frame, text=text.upper(), command=lambda k=key_func, r=reverse: self._perform_sort(k, r),
                      bg=theme['secondary'], fg=theme['background'], font=(theme['font_style_menu'], theme['font_size_menu']), width=40).pack(pady=5)

    def _perform_sort(self, key_func, reverse):
        sorted_students = sorted(self.manager.students, key=key_func, reverse=reverse)
        self._display_student_list(sorted_students, "sorted student records")

    # 6. add a student record
    def add_student_gui(self):
        self._clear_display(); tk.Label(self.display_frame, text="add a new record", bg=theme['background'], fg=theme['primary'], font=(theme['font_style_menu'], theme['font_size_title'], 'bold')).pack(pady=10)
        form_frame = tk.Frame(self.display_frame, bg=theme['background']); form_frame.pack(pady=10)
        fields = ["code (1000-9999)", "name", "course 1 (0-20)", "course 2 (0-20)", "course 3 (0-20)", "exam (0-100)"]
        self.entry_vars = {}
        for i, field in enumerate(fields):
            # uses sticky='w' for left alignment
            tk.Label(form_frame, text=field.upper() + ":", bg=theme['background'], fg=theme['foreground'], font=(theme['font_style_menu'], theme['font_size_menu'])).grid(row=i, column=0, padx=5, pady=5, sticky='w')
            var = tk.StringVar()
            tk.Entry(form_frame, textvariable=var, font=(theme['font_style_menu'], theme['font_size_menu'])).grid(row=i, column=1, padx=5, pady=5, sticky='ew')
            self.entry_vars[field] = var
        tk.Button(self.display_frame, text="submit new student", command=self._add_student_record, bg=theme['secondary'], fg=theme['background'], font=(theme['font_style_menu'], theme['font_size_menu']), width=20).pack(pady=10)

    def _add_student_record(self):
        try:
            code = self.entry_vars["code (1000-9999)"].get().strip(); name = self.entry_vars["name"].get().strip()
            c1, c2, c3 = int(self.entry_vars["course 1 (0-20)"].get()), int(self.entry_vars["course 2 (0-20)"].get()), int(self.entry_vars["course 3 (0-20)"].get())
            exam = int(self.entry_vars["exam (0-100)"].get())
            
            if not (1000 <= int(code) <= 9999): raise ValueError("code outside range 1000-9999.")
            if not name: raise ValueError("name cannot be empty.")
            if not all(0 <= c <= 20 for c in [c1, c2, c3]): raise ValueError("course marks must be 0-20.")
            if not (0 <= exam <= 100): raise ValueError("exam mark must be 0-100.")
            if any(s.code == code for s in self.manager.students): messagebox.showwarning("validation error", "student code already exists."); return

            self.manager.students.append(student(code, name, c1, c2, c3, exam))
            if self.manager.save_data():
                messagebox.showinfo("success", f"student '{name}' added successfully."); self.view_all_records()
        except ValueError as e:
            messagebox.showwarning("validation error", f"invalid input: {e}")
        except Exception as e:
            messagebox.showerror("error", f"an unknown error occurred: {e}")

    # 7. delete a student record
    def delete_student_gui(self):
        self._clear_display(); tk.Label(self.display_frame, text="remove a student entry", bg=theme['background'], fg=theme['primary'], font=(theme['font_style_menu'], theme['font_size_title'], 'bold')).pack(pady=10)
        delete_frame = tk.Frame(self.display_frame, bg=theme['background']); delete_frame.pack(pady=10)
        tk.Label(delete_frame, text="enter student code or name:", bg=theme['background'], fg=theme['foreground'], font=(theme['font_style_menu'], theme['font_size_menu'])).pack(side=tk.LEFT, padx=5)
        self.delete_entry = tk.Entry(delete_frame, font=(theme['font_style_menu'], theme['font_size_menu'])); self.delete_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(delete_frame, text="delete", command=self._delete_student_record, bg=theme['danger'], fg=theme['background'], font=(theme['font_style_menu'], theme['font_size_menu'])).pack(side=tk.LEFT, padx=5)

    def _delete_student_record(self):
        query = self.delete_entry.get().strip().lower()
        if not query: messagebox.showwarning("input error", "please enter student code or name."); return
        initial_count = len(self.manager.students)
        self.manager.students = [s for s in self.manager.students if s.code != query and s.name.lower() != query]
        
        if len(self.manager.students) < initial_count:
            if self.manager.save_data():
                messagebox.showinfo("success", f"student record matching '{query}' deleted successfully."); self.view_all_records()
        else:
            messagebox.showinfo("not found", f"no student found matching '{query}'. deletion failed.")

    # 8. update a students record
    def update_student_gui(self):
        self._clear_display(); tk.Label(self.display_frame, text="edit student details", bg=theme['background'], fg=theme['primary'], font=(theme['font_style_menu'], theme['font_size_title'], 'bold')).pack(pady=10)
        update_frame = tk.Frame(self.display_frame, bg=theme['background']); update_frame.pack(pady=10)
        tk.Label(update_frame, text="enter student code or name to update:", bg=theme['background'], fg=theme['foreground'], font=(theme['font_style_menu'], theme['font_size_menu'])).pack(side=tk.LEFT, padx=5)
        self.update_query_entry = tk.Entry(update_frame, font=(theme['font_style_menu'], theme['font_size_menu'])); self.update_query_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(update_frame, text="find student", command=self._search_for_update, bg=theme['secondary'], fg=theme['background'], font=(theme['font_style_menu'], theme['font_size_menu'])).pack(side=tk.LEFT, padx=5)
        
    def _search_for_update(self):
        query = self.update_query_entry.get().strip().lower()
        if not query: messagebox.showwarning("input error", "please enter student code or name."); return
        target_student = next((s for s in self.manager.students if s.code == query or s.name.lower() == query), None)
        if target_student: self._show_update_form(target_student)
        else: messagebox.showinfo("not found", f"no student found matching '{query}'.")

    def _show_update_form(self, student_obj):
        for widget in self.display_frame.winfo_children():
            if widget.winfo_id() != self.update_query_entry.master.winfo_id(): widget.destroy()

        tk.Label(self.display_frame, text=f"editing: {student_obj.name} ({student_obj.code})", bg=theme['background'], fg=theme['highlight'], font=(theme['font_style_menu'], theme['font_size_title'])).pack(pady=10)
        form_frame = tk.Frame(self.display_frame, bg=theme['background']); form_frame.pack(pady=10)
        fields = {"code": student_obj.code, "name": student_obj.name, "c1": student_obj.c1, "c2": student_obj.c2, "c3": student_obj.c3, "exam": student_obj.exam}
        self.update_vars = {}

        for i, (key, value) in enumerate(fields.items()):
            # uses sticky='w' for left alignment
            tk.Label(form_frame, text=key.upper() + ":", bg=theme['background'], fg=theme['foreground'], font=(theme['font_style_menu'], theme['font_size_menu'])).grid(row=i, column=0, padx=5, pady=5, sticky='w')
            var = tk.StringVar(value=str(value))
            entry = tk.Entry(form_frame, textvariable=var, font=(theme['font_style_menu'], theme['font_size_menu']), state=tk.DISABLED if key == 'code' else tk.NORMAL)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
            self.update_vars[key] = var
            
        tk.Button(self.display_frame, text="confirm update", command=lambda s=student_obj: self._confirm_update(s), bg=theme['primary'], fg=theme['background'], font=(theme['font_style_menu'], theme['font_size_menu']), width=20).pack(pady=10)

    def _confirm_update(self, student_obj):
        try:
            new_name = self.update_vars["name"].get().strip(); new_c1 = int(self.update_vars["c1"].get()); new_c2 = int(self.update_vars["c2"].get())
            new_c3 = int(self.update_vars["c3"].get()); new_exam = int(self.update_vars["exam"].get())
            
            if not new_name: raise ValueError("name cannot be empty.")
            if not all(0 <= c <= 20 for c in [new_c1, new_c2, new_c3]): raise ValueError("course marks must be 0-20.")
            if not (0 <= new_exam <= 100): raise ValueError("exam mark must be 0-100.")

            student_obj.name, student_obj.c1, student_obj.c2, student_obj.c3, student_obj.exam = new_name, new_c1, new_c2, new_c3, new_exam
            index = next(i for i, s in enumerate(self.manager.students) if s.code == student_obj.code)
            self.manager.students[index] = student(student_obj.code, new_name, new_c1, new_c2, new_c3, new_exam)

            if self.manager.save_data():
                messagebox.showinfo("success", f"student '{student_obj.code}' updated successfully."); self.view_all_records()
        
        except ValueError as e:
            messagebox.showwarning("validation error", f"invalid input: {e}")
        except Exception as e:
            messagebox.showerror("error", f"an unknown error occurred: {e}")

if __name__ == '__main__':
    create_initial_file()
    root = tk.Tk()
    app = studentmanagerapp(root)
    root.mainloop()