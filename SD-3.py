import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Import ttk for themed widgets
import pymongo

class ContactManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Management System")
        
        # MongoDB connection
        self.client = pymongo.MongoClient("mongodb://localhost:27017")
        self.db = self.client["contact_management"]
        self.collection = self.db["contacts"]
        
        # Configure background color
        self.root.configure(bg="#ffff99")  # Light yellow
        
        # Labels and Entry fields for adding new contacts
        self.label_name = tk.Label(root, text="Name:", bg="#ffff99", font=("Arial", 12))
        self.label_name.grid(row=0, column=0, padx=10, pady=10)
        self.entry_name = tk.Entry(root)
        self.entry_name.grid(row=0, column=1, padx=10, pady=10)
        
        self.label_phone = tk.Label(root, text="Phone:", bg="#ffff99", font=("Arial", 12))
        self.label_phone.grid(row=1, column=0, padx=10, pady=10)
        self.entry_phone = tk.Entry(root)
        self.entry_phone.grid(row=1, column=1, padx=10, pady=10)
        
        self.label_email = tk.Label(root, text="Email:", bg="#ffff99", font=("Arial", 12))
        self.label_email.grid(row=2, column=0, padx=10, pady=10)
        self.entry_email = tk.Entry(root)
        self.entry_email.grid(row=2, column=1, padx=10, pady=10)
        
        # Buttons for add, view, edit, delete contacts
        self.add_button = tk.Button(root, text="Add Contact", command=self.add_contact, bg="#ffa500", fg="#ffff99", font=("Arial", 12, "bold"))
        self.add_button.grid(row=3, column=0, padx=10, pady=10)
        
        self.view_button = tk.Button(root, text="View Contacts", command=self.view_contacts_table, bg="#ffa500", fg="#ffff99", font=("Arial", 12, "bold"))
        self.view_button.grid(row=3, column=1, padx=10, pady=10)
        
        self.edit_button = tk.Button(root, text="Edit Contact", command=self.edit_contact, bg="#ffa500", fg="#ffff99", font=("Arial", 12, "bold"))
        self.edit_button.grid(row=4, column=0, padx=10, pady=10)
        
        self.delete_button = tk.Button(root, text="Delete Contact", command=self.delete_contact, bg="#ffa500", fg="#ffff99", font=("Arial", 12, "bold"))
        self.delete_button.grid(row=4, column=1, padx=10, pady=10)
        
        # Result label for status messages
        self.result_label = tk.Label(root, text="", bg="#ffff99", font=("Arial", 16, "bold"), fg="red")
        self.result_label.grid(row=5, columnspan=2, padx=10, pady=10)
    
    def add_contact(self):
        name = self.entry_name.get()
        phone = self.entry_phone.get()
        email = self.entry_email.get()
        
        if name == "" or phone == "" or email == "":
            messagebox.showwarning("Incomplete Information", "Please enter Name, Phone, and Email.")
            return
        
        contact_data = {"Name": name, "Phone": phone, "Email": email}
        # Insert contact into MongoDB collection
        self.collection.insert_one(contact_data)
        
        self.clear_entries()
        self.result_label.config(text=f"Contact '{name}' added successfully.")
    
    def view_contacts_table(self):
        contacts_list = list(self.collection.find())
        if not contacts_list:
            self.result_label.config(text="No contacts to display.")
        else:
            # Create a new window for displaying contacts in a table
            self.view_window = tk.Toplevel(self.root)
            self.view_window.title("Contacts")
            self.view_window.configure(bg="#ffff99")
            
            # Create a treeview to display contacts
            columns = ("Name", "Phone", "Email")
            self.tree = ttk.Treeview(self.view_window, columns=columns, show="headings")
            self.tree.grid(row=0, column=0, padx=10, pady=10)
            
            for col in columns:
                self.tree.heading(col, text=col)
            
            for contact in contacts_list:
                self.tree.insert("", "end", values=(contact["Name"], contact["Phone"], contact["Email"]))
    
    def edit_contact(self):
        name = self.entry_name.get()
        phone = self.entry_phone.get()
        email = self.entry_email.get()
        
        if name == "" or phone == "" or email == "":
            messagebox.showwarning("Incomplete Information", "Please enter Name, Phone, and Email.")
            return
        
        contact_data = {"Name": name, "Phone": phone, "Email": email}
        # Update contact in MongoDB collection
        self.collection.update_one({"Name": name}, {"$set": contact_data})
        
        self.clear_entries()
        self.result_label.config(text=f"Contact '{name}' updated successfully.")
    
    def delete_contact(self):
        name = self.entry_name.get()
        
        if name == "":
            messagebox.showwarning("Incomplete Information", "Please enter Name to delete.")
            return
        
        result = self.collection.delete_one({"Name": name})
        if result.deleted_count == 0:
            self.result_label.config(text=f"No contact found with name '{name}'.", fg="red")
        else:
            self.clear_entries()
            self.result_label.config(text=f"Contact '{name}' deleted successfully.")
    
    def clear_entries(self):
        self.entry_name.delete(0, tk.END)
        self.entry_phone.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManagementApp(root)
    root.mainloop()
