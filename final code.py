import datetime
import pywhatkit as kit
import customtkinter as ctk
from tkinter import messagebox
from tabulate import tabulate

# Function to get student data
def get_student_data():
    return [
        ("Manisha Borah", "g"),
        ("Rupali Jonak Mahanta", "g"), 
        ("Sakshi Satish Kohle", "g"),
        ("Abhinav Anubhab Khound", "b"), 
        ("Bibhuti Ranjan Borah", "b"), 
        ("Himanshu Gupta", "b"),
        ("Mohd. Farman Usta", "b"), 
        ("Prasujya Pritam Borah", "b"), 
        ("Vansh Behal", "b"),
        ("Anamika Das", "g"), 
        ("Aryan Raj Gupta", "b"), 
        ("Bhagyashree Saikia", "g"),
        ("Bhumika Roy", "g"), 
        ("Bhumika Sarma", "g"), 
        ("Bonani Bhuyan", "g"),
        ("Bedangraj Baruah", "b"), 
        ("Deepanita Chakraborty", "g"), 
        ("Geetashree Baruah", "g"),
        ("Hemphu Engti", "b"), 
        ("Himashree Nag", "g"), 
        ("Himesh Biswas", "b"),
        ("Himanku Rajkhown", "b"), 
        ("Manyataa Kashyap", "g"), 
        ("Mouchami Nath", "g"),
        ("Prakiti Bora", "g"), 
        ("Priyam Bora", "b"), 
        ("Priyanko Devchoudhary", "b"),
        ("Rituparna Deka", "g"), 
        ("Rupjyoti Borah", "b"), 
        ("Suprabhat Borah", "b"),
        ("Uday Debnath", "b"), 
        ("Kumari Lucky", "g"), 
        ("Tulika Singhal", "g"),
        ("Sumesh Kumar", "b"), 
        ("Debasish Borah", "b")
    ]

# Function to validate password
def get_password():
    valid_passwords = [12345, "12345"]
    password = ctk.CTkInputDialog(text="Enter the password:", title="Password").get_input()
    if password and int(password) in valid_passwords:
        return True
    else:
        messagebox.showerror("Error", "Invalid password.")
        return False

# Function to collect attendance using dropdown selection
def collect_attendance(students):
    attendance = {}
    present_count = 0
    absent_students = []

    # Create attendance window for input
    attendance_window = ctk.CTkToplevel()
    attendance_window.title("e-Attendance")
    attendance_window.geometry("450x600")

    # Create a scrollable frame for the attendance list
    scrollable_frame = ctk.CTkScrollableFrame(master=attendance_window, width=400, height=500, corner_radius=10)
    scrollable_frame.pack(pady=20, padx=10, fill="both", expand=True)

    # Create a dictionary to store the attendance status of each student
    status_options = {}

    # Loop through each student to create options for attendance
    for idx, (name, gender) in enumerate(students, start=1):
        g_b = "GIRL" if gender == "g" else "BOY"

        # Create a label for each student
        student_label = ctk.CTkLabel(scrollable_frame, text=f"{idx}. {name} ({g_b})", font=("Arial", 12))
        student_label.pack(pady=5)

        # Create an OptionMenu for present/absent
        options = ["Present", "Absent"]
        status_options[name] = ctk.StringVar(value="Present")
        attendance_menu = ctk.CTkOptionMenu(scrollable_frame, variable=status_options[name], values=options)
        attendance_menu.pack(pady=5)

    # Create a function to collect attendance status
    def submit_attendance():
        nonlocal present_count, absent_students

        # Loop through the status options and update attendance
        for idx, (name, gender) in enumerate(students, start=1):
            g_b = "GIRL" if gender == "g" else "BOY"
            status = status_options[name].get()

            if status == "Present":
                present_count += 1
                attendance[idx] = [name, "PRESENT", g_b]
            else:
                absent_students.append(name)
                attendance[idx] = [name, "ABSENT", g_b]

        attendance_window.destroy()  # Close the attendance window after submission

    # Create a submit button
    submit_button = ctk.CTkButton(attendance_window, text="Submit Attendance", command=submit_attendance)
    submit_button.pack(pady=10)

    attendance_window.mainloop()  # Run the attendance window

    return attendance, present_count, absent_students

# Function to save attendance to a file
def save_to_file(filename, attendance, present_count, total_students, absent_students):
    with open(filename, 'w') as f:
        current_time = datetime.datetime.now()
        f.write(f"Total number of students: {total_students}\n")
        f.write(f"At Date and Time from timestamp: {current_time}\n")
        
        # Attendance Table
        headers = ['NAME', 'STATUS', 'GENDER']
        table = [[data[0], data[1], data[2]] for data in attendance.values()]
        f.write(tabulate(table, headers, tablefmt='grid') + "\n")

        # Absent Students
        f.write("Students who are absent:\n")
        f.write("\n".join(absent_students) + "\n")
        
        f.write(f"Total number of students present: {present_count}\n")
        f.write(f"Total number of students absent: {total_students - present_count}\n")
        f.write(f"Total girls: {sum(1 for _, _, g in attendance.values() if g == 'GIRL')}\n")
        f.write(f"Total boys: {sum(1 for _, _, g in attendance.values() if g == 'BOY')}\n")

# Function to send WhatsApp message
def send_whatsapp_message(phone_number, message, hour, minute):
    kit.sendwhatmsg(phone_number, message, hour, minute)

# Main function to run the attendance system
def main():
    if get_password():
        filename = ctk.CTkInputDialog(text="Enter the filename to save (add .txt at the end):", title="Filename").get_input()
        if filename:
            students = get_student_data()
            attendance, present_count, absent_students = collect_attendance(students)
            total_students = len(students)

            # Save attendance data to file
            save_to_file(filename, attendance, present_count, total_students, absent_students)

            # Create message with attendance summary
            absent_list = "\n".join(absent_students)
            message = (f"Attendance Report Saved.\n"
                       f"Total Students: {total_students}\n"
                       f"Total Present: {present_count}\n"
                       f"Total Absent: {total_students - present_count}\n"
                       f"Absent Students:\n{absent_list}")

            # Specify the time to send the message
            now = datetime.datetime.now()
            send_hour = now.hour
            send_minute = now.minute + 2

            # Adjust minute and hour if minute exceeds 59
            if send_minute >= 60:
                send_minute -= 60
                send_hour += 1

            # Send WhatsApp message at the specified time
            send_whatsapp_message("+918399925675", message, send_hour, send_minute)
            messagebox.showinfo("Success", "Attendance recorded and WhatsApp message sent!")

# Set up the main customtkinter window
ctk.set_appearance_mode("Dark")  # Dark theme for a modern look
ctk.set_default_color_theme("green")  # Green theme for visual appeal

root = ctk.CTk()  # Use CTk instead of Tk
root.title("KV MISA Attendance System")
root.geometry("500x300")

# Create a frame for better layout
frame = ctk.CTkFrame(master=root, corner_radius=10)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Title Label
title_label = ctk.CTkLabel(master=frame, text="KV MISA Attendance System", font=("Arial", 24))
title_label.pack(pady=10)

# Add a separator line for design
separator = ctk.CTkLabel(master=frame, text="--------------------", font=("Arial", 14))
separator.pack()

# Instructions Label
instructions_label = ctk.CTkLabel(master=frame, text="Click the button below to start attendance:", font=("Arial", 14))
instructions_label.pack(pady=10)

# Start Attendance Button
start_button = ctk.CTkButton(master=frame, text="Start Attendance", command=main, corner_radius=8, width=200)
start_button.pack(pady=20)

# Footer Label
footer_label = ctk.CTkLabel(master=frame, text="Made by Farman & Himanshu", font=("Arial", 10))
footer_label.pack(side="bottom", pady=10)

# Run the application
root.mainloop()