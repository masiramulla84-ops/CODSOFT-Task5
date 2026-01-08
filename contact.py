import customtkinter as ctk
from tkinter import messagebox
import json
import os

# --- Configuration ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")


class ModernContactApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("Contact Manager Pro")
        self.geometry("900x600")

        # Grid Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- COLORS ---
        self.sidebar_color = "#1a1a2e"
        self.main_bg_color = "#16213e"
        self.accent_color = "#e94560"
        self.text_color = "#ffffff"

        # --- DATA SETUP ---
        self.data_file = "contacts.json"
        self.contacts = []
        self.current_contact_index = None

        # Load data from file immediately
        self.load_from_file()

        self.create_sidebar()
        self.create_main_area()
        self.populate_directory()

    def create_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=self.sidebar_color)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(2, weight=1)

        # Logo
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="📇 MyContacts", font=("Segoe UI", 24, "bold"),
                                       text_color=self.accent_color)
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 10), sticky="w")

        # Search
        self.search_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="🔍 Search...", height=35,
                                         corner_radius=20, fg_color="#2b2d42", border_width=0)
        self.search_entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.search_entry.bind("<KeyRelease>", self.filter_directory)

        # Directory List
        self.contact_list_frame = ctk.CTkScrollableFrame(self.sidebar_frame, fg_color="transparent",
                                                         label_text="Your Directory", label_text_color="#aaaaaa")
        self.contact_list_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

    def create_main_area(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=self.main_bg_color)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Header
        self.header_label = ctk.CTkLabel(self.main_frame, text="Contact Details", font=("Segoe UI", 24, "bold"))
        self.header_label.grid(row=0, column=0, padx=40, pady=(40, 20), sticky="w")

        # Form Card
        self.form_card = ctk.CTkFrame(self.main_frame, fg_color="#0f3460", corner_radius=15, border_width=1,
                                      border_color="#333")
        self.form_card.grid(row=1, column=0, padx=40, sticky="nsew")
        self.form_card.grid_columnconfigure(0, weight=1)

        # Helpers for Inputs
        def create_input(parent, row, label, placeholder):
            ctk.CTkLabel(parent, text=label, text_color="#a2a8d3").grid(row=row, column=0, padx=20, pady=(15, 5),
                                                                        sticky="w")
            entry = ctk.CTkEntry(parent, placeholder_text=placeholder, height=40, corner_radius=8, fg_color="#1a1a2e",
                                 border_width=0)
            entry.grid(row=row + 1, column=0, padx=20, pady=(0, 5), sticky="ew")
            return entry

        self.name_entry = create_input(self.form_card, 0, "FULL NAME", "Ex: John Doe")
        self.phone_entry = create_input(self.form_card, 2, "PHONE NUMBER", "Ex: +1 234 567 890")
        self.email_entry = create_input(self.form_card, 4, "EMAIL ADDRESS", "Ex: john@example.com")
        self.addr_entry = create_input(self.form_card, 6, "HOME ADDRESS", "Ex: 123 Maple St, NY")

        # Buttons
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.grid(row=2, column=0, padx=40, pady=30, sticky="ew")

        # Save Button
        self.save_btn = ctk.CTkButton(self.button_frame, text="💾 Save / Update", font=("Roboto", 14, "bold"),
                                      fg_color=self.accent_color, hover_color="#c0354c", height=45, corner_radius=8,
                                      command=self.save_contact)
        self.save_btn.pack(side="right", padx=10)

        # Clear Button
        self.clear_btn = ctk.CTkButton(self.button_frame, text="Clear Form", fg_color="transparent", border_width=1,
                                       border_color="#666", text_color="#ccc", hover_color="#333", height=45,
                                       corner_radius=8, command=self.clear_form)
        self.clear_btn.pack(side="right", padx=10)

        # Delete Button
        self.delete_btn = ctk.CTkButton(self.button_frame, text="🗑️ Delete", fg_color="#2b2b2b", text_color="#ff5555",
                                        hover_color="#441111", height=45, corner_radius=8, command=self.delete_contact)
        self.delete_btn.pack(side="left", padx=10)

    # --- FUNCTIONALITY ---

    def load_from_file(self):
        # Checks if file exists, if so, loads data
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.contacts = json.load(f)
            except:
                self.contacts = []  # If file is corrupt, start fresh

    def save_to_file(self):
        # Saves current list to JSON file
        with open(self.data_file, 'w') as f:
            json.dump(self.contacts, f, indent=4)

    def populate_directory(self, search_query=""):
        for widget in self.contact_list_frame.winfo_children():
            widget.destroy()

        for index, contact in enumerate(self.contacts):
            if search_query.lower() in contact['name'].lower():
                btn = ctk.CTkButton(
                    self.contact_list_frame,
                    text=contact['name'],  # DISPLAYS NAME
                    fg_color="transparent",
                    text_color="#ccc",
                    anchor="w",
                    hover_color=self.accent_color,
                    height=30,
                    command=lambda i=index: self.load_contact(i)
                )
                btn.pack(fill="x", pady=2)

    def filter_directory(self, event):
        query = self.search_entry.get()
        self.populate_directory(query)

    def load_contact(self, index):
        self.current_contact_index = index
        data = self.contacts[index]

        self.clear_form(keep_index=True)
        self.name_entry.insert(0, data['name'])
        self.phone_entry.insert(0, data['phone'])
        self.email_entry.insert(0, data['email'])
        self.addr_entry.insert(0, data['address'])

    def save_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.addr_entry.get()

        if not name:
            messagebox.showwarning("Input Error", "Name is required!")
            return

        new_data = {"name": name, "phone": phone, "email": email, "address": address}

        if self.current_contact_index is not None:
            self.contacts[self.current_contact_index] = new_data
            messagebox.showinfo("Success", f"Updated {name}")
        else:
            self.contacts.append(new_data)
            messagebox.showinfo("Success", f"Added {name}")

        self.save_to_file()  # <--- Saves to computer
        self.populate_directory()
        self.clear_form()

    def delete_contact(self):
        if self.current_contact_index is not None:
            name = self.contacts[self.current_contact_index]['name']
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {name}?")
            if confirm:
                del self.contacts[self.current_contact_index]
                self.save_to_file()  # <--- Updates file on computer
                self.populate_directory()
                self.clear_form()
        else:
            messagebox.showwarning("Selection Error", "Please select a contact to delete first.")

    def clear_form(self, keep_index=False):
        self.name_entry.delete(0, "end")
        self.phone_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.addr_entry.delete(0, "end")

        if not keep_index:
            self.current_contact_index = None


if __name__ == "__main__":
    app = ModernContactApp()
    app.mainloop()