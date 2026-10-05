import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


DATABASE_NAME = "todo.db"


class DatabaseManager:
    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.connection.row_factory = sqlite3.Row
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            priority TEXT NOT NULL,
            category TEXT,
            status TEXT NOT NULL DEFAULT 'Pending',
            created_at TEXT NOT NULL
        )
        """
        self.connection.execute(query)
        self.connection.commit()

    def add_task(self, title, description, due_date, priority, category):
        query = """
        INSERT INTO tasks
        (title, description, due_date, priority, category, status, created_at)
        VALUES (?, ?, ?, ?, ?, 'Pending', ?)
        """

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.connection.execute(
            query,
            (
                title,
                description,
                due_date,
                priority,
                category,
                created_at
            )
        )
        self.connection.commit()

    def get_all_tasks(self):
        query = """
        SELECT *
        FROM tasks
        ORDER BY
            CASE priority
                WHEN 'High' THEN 1
                WHEN 'Medium' THEN 2
                WHEN 'Low' THEN 3
            END,
            id DESC
        """
        return self.connection.execute(query).fetchall()

    def search_tasks(self, keyword):
        query = """
        SELECT *
        FROM tasks
        WHERE title LIKE ?
           OR description LIKE ?
           OR category LIKE ?
        ORDER BY id DESC
        """

        search_value = f"%{keyword}%"

        return self.connection.execute(
            query,
            (search_value, search_value, search_value)
        ).fetchall()

    def get_task(self, task_id):
        query = "SELECT * FROM tasks WHERE id = ?"
        return self.connection.execute(query, (task_id,)).fetchone()

    def update_task(
        self,
        task_id,
        title,
        description,
        due_date,
        priority,
        category
    ):
        query = """
        UPDATE tasks
        SET title = ?,
            description = ?,
            due_date = ?,
            priority = ?,
            category = ?
        WHERE id = ?
        """

        self.connection.execute(
            query,
            (
                title,
                description,
                due_date,
                priority,
                category,
                task_id
            )
        )
        self.connection.commit()

    def update_status(self, task_id, status):
        query = "UPDATE tasks SET status = ? WHERE id = ?"
        self.connection.execute(query, (status, task_id))
        self.connection.commit()

    def delete_task(self, task_id):
        query = "DELETE FROM tasks WHERE id = ?"
        self.connection.execute(query, (task_id,))
        self.connection.commit()

    def get_statistics(self):
        query = """
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN status = 'Pending' THEN 1 ELSE 0 END) AS pending,
            SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed
        FROM tasks
        """

        result = self.connection.execute(query).fetchone()

        return {
            "total": result["total"] or 0,
            "pending": result["pending"] or 0,
            "completed": result["completed"] or 0
        }

    def close(self):
        self.connection.close()


class TodoApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Manager")
        self.root.geometry("1150x700")
        self.root.minsize(950, 600)

        self.database = DatabaseManager(DATABASE_NAME)
        self.selected_task_id = None

        self.setup_style()
        self.create_variables()
        self.create_layout()
        self.load_tasks()
        self.update_statistics()

        self.root.protocol("WM_DELETE_WINDOW", self.close_application)

    def setup_style(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Title.TLabel",
            font=("Arial", 24, "bold"),
            foreground="#1f2937"
        )

        style.configure(
            "Subtitle.TLabel",
            font=("Arial", 11),
            foreground="#6b7280"
        )

        style.configure(
            "Heading.TLabel",
            font=("Arial", 12, "bold"),
            foreground="#111827"
        )

        style.configure(
            "Main.TButton",
            font=("Arial", 10, "bold"),
            padding=7
        )

        style.configure(
            "Treeview",
            rowheight=32,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )

    def create_variables(self):
        self.title_variable = tk.StringVar()
        self.due_date_variable = tk.StringVar()
        self.priority_variable = tk.StringVar(value="Medium")
        self.category_variable = tk.StringVar()
        self.search_variable = tk.StringVar()

        self.total_variable = tk.StringVar(value="Total: 0")
        self.pending_variable = tk.StringVar(value="Pending: 0")
        self.completed_variable = tk.StringVar(value="Completed: 0")

    def create_layout(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill="both", expand=True)

        self.create_header(main_frame)
        self.create_statistics(main_frame)
        self.create_form(main_frame)
        self.create_search_bar(main_frame)
        self.create_task_table(main_frame)
        self.create_footer(main_frame)

    def create_header(self, parent):
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill="x", pady=(0, 15))

        title_label = ttk.Label(
            header_frame,
            text="TO-DO LIST MANAGER",
            style="Title.TLabel"
        )
        title_label.pack(anchor="w")

        subtitle_label = ttk.Label(
            header_frame,
            text="Create, organize, update, and track your daily tasks",
            style="Subtitle.TLabel"
        )
        subtitle_label.pack(anchor="w", pady=(4, 0))

    def create_statistics(self, parent):
        statistics_frame = ttk.Frame(parent)
        statistics_frame.pack(fill="x", pady=(0, 15))

        self.create_stat_card(
            statistics_frame,
            self.total_variable,
            "#2563eb"
        ).pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.create_stat_card(
            statistics_frame,
            self.pending_variable,
            "#d97706"
        ).pack(side="left", fill="x", expand=True, padx=8)

        self.create_stat_card(
            statistics_frame,
            self.completed_variable,
            "#16a34a"
        ).pack(side="left", fill="x", expand=True, padx=(8, 0))

    def create_stat_card(self, parent, variable, color):
        frame = tk.Frame(
            parent,
            bg=color,
            height=55,
            padx=15,
            pady=12
        )

        label = tk.Label(
            frame,
            textvariable=variable,
            bg=color,
            fg="white",
            font=("Arial", 12, "bold")
        )
        label.pack()

        return frame

    def create_form(self, parent):
        form_frame = ttk.LabelFrame(
            parent,
            text="Task Details",
            padding=15
        )
        form_frame.pack(fill="x", pady=(0, 15))

        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)

        ttk.Label(
            form_frame,
            text="Task Title *"
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.title_entry = ttk.Entry(
            form_frame,
            textvariable=self.title_variable
        )
        self.title_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            sticky="ew"
        )

        ttk.Label(
            form_frame,
            text="Due Date"
        ).grid(row=0, column=2, padx=5, pady=5, sticky="w")

        self.due_date_entry = ttk.Entry(
            form_frame,
            textvariable=self.due_date_variable
        )
        self.due_date_entry.grid(
            row=0,
            column=3,
            padx=5,
            pady=5,
            sticky="ew"
        )

        ttk.Label(
            form_frame,
            text="Priority"
        ).grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.priority_combo = ttk.Combobox(
            form_frame,
            textvariable=self.priority_variable,
            values=("High", "Medium", "Low"),
            state="readonly"
        )
        self.priority_combo.grid(
            row=1,
            column=1,
            padx=5,
            pady=5,
            sticky="ew"
        )

        ttk.Label(
            form_frame,
            text="Category"
        ).grid(row=1, column=2, padx=5, pady=5, sticky="w")

        self.category_entry = ttk.Entry(
            form_frame,
            textvariable=self.category_variable
        )
        self.category_entry.grid(
            row=1,
            column=3,
            padx=5,
            pady=5,
            sticky="ew"
        )

        ttk.Label(
            form_frame,
            text="Description"
        ).grid(row=2, column=0, padx=5, pady=5, sticky="nw")

        self.description_text = tk.Text(
            form_frame,
            height=3,
            font=("Arial", 10),
            wrap="word"
        )
        self.description_text.grid(
            row=2,
            column=1,
            columnspan=3,
            padx=5,
            pady=5,
            sticky="ew"
        )

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(
            row=3,
            column=0,
            columnspan=4,
            pady=(10, 0)
        )

        ttk.Button(
            button_frame,
            text="Add Task",
            style="Main.TButton",
            command=self.add_task
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Update Task",
            style="Main.TButton",
            command=self.update_task
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Clear Form",
            style="Main.TButton",
            command=self.clear_form
        ).pack(side="left", padx=5)

    def create_search_bar(self, parent):
        search_frame = ttk.Frame(parent)
        search_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(
            search_frame,
            text="Search:"
        ).pack(side="left", padx=(0, 8))

        search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_variable,
            width=35
        )
        search_entry.pack(side="left")

        search_entry.bind("<KeyRelease>", self.search_tasks)

        ttk.Button(
            search_frame,
            text="Show All",
            command=self.show_all_tasks
        ).pack(side="left", padx=8)

    def create_task_table(self, parent):
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill="both", expand=True)

        columns = (
            "id",
            "title",
            "description",
            "due_date",
            "priority",
            "category",
            "status"
        )

        self.task_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        headings = {
            "id": "ID",
            "title": "Title",
            "description": "Description",
            "due_date": "Due Date",
            "priority": "Priority",
            "category": "Category",
            "status": "Status"
        }

        widths = {
            "id": 45,
            "title": 180,
            "description": 260,
            "due_date": 100,
            "priority": 90,
            "category": 110,
            "status": 100
        }

        for column in columns:
            self.task_table.heading(
                column,
                text=headings[column]
            )
            self.task_table.column(
                column,
                width=widths[column],
                anchor="center"
            )

        vertical_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.task_table.yview
        )

        horizontal_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.task_table.xview
        )

        self.task_table.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        self.task_table.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        vertical_scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        horizontal_scrollbar.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self.task_table.bind(
            "<<TreeviewSelect>>",
            self.select_task
        )

        self.task_table.tag_configure(
            "completed",
            foreground="#16a34a"
        )

        self.task_table.tag_configure(
            "high",
            foreground="#dc2626"
        )

    def create_footer(self, parent):
        footer_frame = ttk.Frame(parent)
        footer_frame.pack(fill="x", pady=(12, 0))

        ttk.Button(
            footer_frame,
            text="Mark Completed",
            style="Main.TButton",
            command=self.mark_completed
        ).pack(side="left", padx=5)

        ttk.Button(
            footer_frame,
            text="Mark Pending",
            style="Main.TButton",
            command=self.mark_pending
        ).pack(side="left", padx=5)

        ttk.Button(
            footer_frame,
            text="Delete Task",
            style="Main.TButton",
            command=self.delete_task
        ).pack(side="left", padx=5)

        ttk.Button(
            footer_frame,
            text="Exit",
            style="Main.TButton",
            command=self.close_application
        ).pack(side="right", padx=5)

    def validate_form(self):
        title = self.title_variable.get().strip()
        due_date = self.due_date_variable.get().strip()

        if not title:
            messagebox.showwarning(
                "Validation Error",
                "Task title is required."
            )
            self.title_entry.focus()
            return False

        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning(
                    "Validation Error",
                    "Due date must use YYYY-MM-DD format."
                )
                self.due_date_entry.focus()
                return False

        return True

    def get_form_data(self):
        title = self.title_variable.get().strip()
        description = self.description_text.get(
            "1.0",
            tk.END
        ).strip()
        due_date = self.due_date_variable.get().strip()
        priority = self.priority_variable.get()
        category = self.category_variable.get().strip()

        return title, description, due_date, priority, category

    def add_task(self):
        if not self.validate_form():
            return

        task_data = self.get_form_data()

        self.database.add_task(*task_data)

        messagebox.showinfo(
            "Success",
            "Task added successfully."
        )

        self.clear_form()
        self.load_tasks()
        self.update_statistics()

    def update_task(self):
        if self.selected_task_id is None:
            messagebox.showwarning(
                "Selection Required",
                "Select a task before updating."
            )
            return

        if not self.validate_form():
            return

        task_data = self.get_form_data()

        self.database.update_task(
            self.selected_task_id,
            *task_data
        )

        messagebox.showinfo(
            "Success",
            "Task updated successfully."
        )

        self.clear_form()
        self.load_tasks()
        self.update_statistics()

    def delete_task(self):
        task_id = self.get_selected_task_id()

        if task_id is None:
            messagebox.showwarning(
                "Selection Required",
                "Select a task before deleting."
            )
            return

        confirmation = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this task?"
        )

        if confirmation:
            self.database.delete_task(task_id)
            self.clear_form()
            self.load_tasks()
            self.update_statistics()

    def mark_completed(self):
        self.change_task_status("Completed")

    def mark_pending(self):
        self.change_task_status("Pending")

    def change_task_status(self, status):
        task_id = self.get_selected_task_id()

        if task_id is None:
            messagebox.showwarning(
                "Selection Required",
                "Select a task first."
            )
            return

        self.database.update_status(task_id, status)
        self.load_tasks()
        self.update_statistics()

    def get_selected_task_id(self):
        selected_items = self.task_table.selection()

        if not selected_items:
            return None

        selected_item = selected_items[0]
        values = self.task_table.item(selected_item, "values")

        return int(values[0])

    def select_task(self, event=None):
        selected_items = self.task_table.selection()

        if not selected_items:
            return

        selected_item = selected_items[0]
        values = self.task_table.item(selected_item, "values")

        self.selected_task_id = int(values[0])

        task = self.database.get_task(self.selected_task_id)

        if task:
            self.title_variable.set(task["title"])
            self.due_date_variable.set(task["due_date"] or "")
            self.priority_variable.set(task["priority"])
            self.category_variable.set(task["category"] or "")

            self.description_text.delete("1.0", tk.END)
            self.description_text.insert(
                "1.0",
                task["description"] or ""
            )

    def load_tasks(self, tasks=None):
        for item in self.task_table.get_children():
            self.task_table.delete(item)

        if tasks is None:
            tasks = self.database.get_all_tasks()

        for task in tasks:
            tag = ""

            if task["status"] == "Completed":
                tag = "completed"
            elif task["priority"] == "High":
                tag = "high"

            self.task_table.insert(
                "",
                tk.END,
                values=(
                    task["id"],
                    task["title"],
                    task["description"] or "",
                    task["due_date"] or "",
                    task["priority"],
                    task["category"] or "",
                    task["status"]
                ),
                tags=(tag,)
            )

    def search_tasks(self, event=None):
        keyword = self.search_variable.get().strip()

        if keyword:
            tasks = self.database.search_tasks(keyword)
            self.load_tasks(tasks)
        else:
            self.load_tasks()

    def show_all_tasks(self):
        self.search_variable.set("")
        self.load_tasks()

    def update_statistics(self):
        statistics = self.database.get_statistics()

        self.total_variable.set(
            f"Total: {statistics['total']}"
        )

        self.pending_variable.set(
            f"Pending: {statistics['pending']}"
        )

        self.completed_variable.set(
            f"Completed: {statistics['completed']}"
        )

    def clear_form(self):
        self.selected_task_id = None

        self.title_variable.set("")
        self.due_date_variable.set("")
        self.priority_variable.set("Medium")
        self.category_variable.set("")

        self.description_text.delete("1.0", tk.END)

        for item in self.task_table.selection():
            self.task_table.selection_remove(item)

        self.title_entry.focus()

    def close_application(self):
        self.database.close()
        self.root.destroy()


def main():
    root = tk.Tk()
    application = TodoApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()