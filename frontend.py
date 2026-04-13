import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests

API_BASE_URL = "http://127.0.0.1:5000"


class BloggingAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blogging App")
        self.root.geometry("900x700")

        self.token = None
        self.current_user = None

        self.build_layout()

    def build_layout(self):
        title_label = tk.Label(
            self.root,
            text="Blogging App",
            font=("Arial", 20, "bold")
        )
        title_label.pack(pady=10)

        self.status_label = tk.Label(
            self.root,
            text="Not logged in",
            font=("Arial", 11),
            fg="blue"
        )
        self.status_label.pack(pady=5)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Register", width=15, command=self.show_register_form).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Login", width=15, command=self.show_login_form).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Create Post", width=15, command=self.show_create_post_form).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(button_frame, text="List Posts", width=15, command=self.show_posts).grid(row=0, column=3, padx=5, pady=5)
        tk.Button(button_frame, text="List Categories", width=15, command=self.show_categories).grid(row=0, column=4, padx=5, pady=5)

        self.form_frame = tk.Frame(self.root)
        self.form_frame.pack(pady=10, fill="x")

        self.output_area = scrolledtext.ScrolledText(self.root, width=100, height=25)
        self.output_area.pack(padx=10, pady=10, fill="both", expand=True)

        self.write_output(f"GUI started. Backend URL: {API_BASE_URL}")

    def clear_form(self):
        for widget in self.form_frame.winfo_children():
            widget.destroy()

    def write_output(self, message):
        self.output_area.delete("1.0", tk.END)
        self.output_area.insert(tk.END, message)

    def api_request(self, method, endpoint, data=None, use_auth=False):
        url = f"{API_BASE_URL}{endpoint}"
        headers = {}

        if use_auth and self.token:
            headers["Authorization"] = self.token

        try:
            response = requests.request(method, url, json=data, headers=headers, timeout=5)
            return response
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Connection Error", f"Could not connect to backend:\n{e}")
            return None

    def show_register_form(self):
        self.clear_form()

        tk.Label(self.form_frame, text="First Name").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        first_name_entry = tk.Entry(self.form_frame, width=30)
        first_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.form_frame, text="Last Name").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        last_name_entry = tk.Entry(self.form_frame, width=30)
        last_name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.form_frame, text="Password").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        password_entry = tk.Entry(self.form_frame, width=30, show="*")
        password_entry.grid(row=2, column=1, padx=5, pady=5)

        is_admin_var = tk.BooleanVar()
        tk.Checkbutton(self.form_frame, text="Register as admin", variable=is_admin_var).grid(
            row=3, column=1, padx=5, pady=5, sticky="w"
        )

        def submit_register():
            payload = {
                "first_name": first_name_entry.get().strip(),
                "last_name": last_name_entry.get().strip(),
                "password": password_entry.get().strip(),
                "is_admin": is_admin_var.get()
            }

            response = self.api_request("POST", "/register", data=payload)

            if response is None:
                return

            try:
                result = response.json()
            except ValueError:
                self.write_output("Invalid JSON response from backend.")
                return

            if response.status_code == 201:
                user = result.get("user", {})
                self.write_output(
                    "Registration successful\n\n"
                    f"ID: {user.get('id')}\n"
                    f"First Name: {user.get('first_name')}\n"
                    f"Last Name: {user.get('last_name')}\n"
                    f"Email: {user.get('email')}\n"
                    f"Admin: {user.get('is_admin')}"
                )
                messagebox.showinfo("Success", "User registered successfully.")
            else:
                self.write_output(str(result))
                messagebox.showerror("Registration Failed", result.get("error", "Unknown error"))

        tk.Button(self.form_frame, text="Submit Registration", command=submit_register).grid(
            row=4, column=1, padx=5, pady=10, sticky="w"
        )

        self.write_output("Register form loaded.")

    def show_login_form(self):
        self.clear_form()

        tk.Label(self.form_frame, text="Email").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        email_entry = tk.Entry(self.form_frame, width=30)
        email_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.form_frame, text="Password").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        password_entry = tk.Entry(self.form_frame, width=30, show="*")
        password_entry.grid(row=1, column=1, padx=5, pady=5)

        def submit_login():
            payload = {
                "email": email_entry.get().strip(),
                "password": password_entry.get().strip()
            }

            response = self.api_request("POST", "/login", data=payload)

            if response is None:
                return

            try:
                result = response.json()
            except ValueError:
                self.write_output("Invalid JSON response from backend.")
                return

            if response.status_code == 200:
                self.token = result.get("token")
                self.current_user = result.get("user", {})

                user_email = self.current_user.get("email", "unknown")
                is_admin = self.current_user.get("is_admin", False)

                self.status_label.config(
                    text=f"Logged in as {user_email} | Admin: {is_admin}",
                    fg="green"
                )

                self.write_output(
                    "Login successful\n\n"
                    f"Token: {self.token}\n"
                    f"ID: {self.current_user.get('id')}\n"
                    f"First Name: {self.current_user.get('first_name')}\n"
                    f"Last Name: {self.current_user.get('last_name')}\n"
                    f"Email: {self.current_user.get('email')}\n"
                    f"Admin: {self.current_user.get('is_admin')}"
                )
                messagebox.showinfo("Success", "Login successful.")
            else:
                self.write_output(str(result))
                messagebox.showerror("Login Failed", result.get("error", "Unknown error"))

        tk.Button(self.form_frame, text="Submit Login", command=submit_login).grid(
            row=2, column=1, padx=5, pady=10, sticky="w"
        )

        self.write_output("Login form loaded.")

    def show_create_post_form(self):
        self.clear_form()

        if not self.token:
            self.write_output("You must log in before creating a post.")
            messagebox.showwarning("Not Logged In", "Please log in first.")
            return

        tk.Label(self.form_frame, text="Title").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        title_entry = tk.Entry(self.form_frame, width=50)
        title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.form_frame, text="Content").grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        content_text = tk.Text(self.form_frame, width=50, height=10)
        content_text.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.form_frame, text="Category ID").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        category_id_entry = tk.Entry(self.form_frame, width=20)
        category_id_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        def submit_post():
            category_id_raw = category_id_entry.get().strip()

            try:
                category_id = int(category_id_raw)
            except ValueError:
                messagebox.showerror("Invalid Input", "Category ID must be a number.")
                return

            payload = {
                "title": title_entry.get().strip(),
                "content": content_text.get("1.0", tk.END).strip(),
                "category_id": category_id
            }

            response = self.api_request("POST", "/posts", data=payload, use_auth=True)

            if response is None:
                return

            try:
                result = response.json()
            except ValueError:
                self.write_output("Invalid JSON response from backend.")
                return

            if response.status_code == 201:
                post = result.get("post", {})
                self.write_output(
                    "Post created successfully\n\n"
                    f"ID: {post.get('id')}\n"
                    f"Title: {post.get('title')}\n"
                    f"Content: {post.get('content')}\n"
                    f"User ID: {post.get('user_id')}\n"
                    f"Category ID: {post.get('category_id')}\n"
                    f"Created At: {post.get('created_at')}"
                )
                messagebox.showinfo("Success", "Post created successfully.")
            else:
                self.write_output(str(result))
                messagebox.showerror("Create Post Failed", result.get("error", "Unknown error"))

        tk.Button(self.form_frame, text="Submit Post", command=submit_post).grid(
            row=3, column=1, padx=5, pady=10, sticky="w"
        )

        self.write_output("Create Post form loaded.")


    def show_posts(self):
        self.clear_form()

        response = self.api_request("GET", "/posts")

        if response is None:
            return

        try:
            result = response.json()
        except ValueError:
            self.write_output("Invalid JSON response from backend.")
            return

        if response.status_code == 200:
            if not result:
                self.write_output("No posts found.")
                return

            lines = ["Posts\n"]
            for post in result:
                author = post.get("author", {})
                category = post.get("category", {})

                lines.append(
                    f"Post ID: {post.get('id')}\n"
                    f"Title: {post.get('title')}\n"
                    f"Content: {post.get('content')}\n"
                    f"Created At: {post.get('created_at')}\n"
                    f"Author: {author.get('first_name')} {author.get('last_name')} ({author.get('email')})\n"
                    f"Category: {category.get('name')}\n"
                    f"{'-' * 60}"
                )

            self.write_output("\n".join(lines))
        else:
            self.write_output(str(result))
            messagebox.showerror("Error", "Failed to load posts.")

    def show_categories(self):
        self.clear_form()

        response = self.api_request("GET", "/categories")

        if response is None:
            return

        try:
            result = response.json()
        except ValueError:
            self.write_output("Invalid JSON response from backend.")
            return

        if response.status_code == 200:
            if not result:
                self.write_output("No categories found.")
                return

            lines = ["Categories\n"]
            for category in result:
                lines.append(f"ID: {category.get('id')} | Name: {category.get('name')}")

            self.write_output("\n".join(lines))
        else:
            self.write_output(str(result))
            messagebox.showerror("Error", "Failed to load categories.")


if __name__ == "__main__":
    root = tk.Tk()
    app = BloggingAppGUI(root)
    root.mainloop()
