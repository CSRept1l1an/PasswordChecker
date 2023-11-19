import tkinter as tk
import re
import zxcvbn
import math


def time_to_crack(password):
    result = zxcvbn.zxcvbn(password)
    guesses_log10 = result['guesses_log10']

    # Constants (adjust as needed)
    guesses_per_second = 1000000000  # Number of password guesses per second

    # Calculate time to crack in seconds
    time_to_crack_seconds = math.pow(10, guesses_log10) / guesses_per_second

    # Convert time to crack to a more readable format
    time_to_crack_readable = format_time(time_to_crack_seconds)

    return time_to_crack_seconds, time_to_crack_readable


def format_time(seconds):
    # Convert seconds to days, hours, minutes, and seconds
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    return f"{int(days)} days, {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds"


def check_password_validation(password):
    # Add your password strength checking logic here
    length_criteria = len(password) >= 8
    uppercase_criteria = any(char.isupper() for char in password)
    lowercase_criteria = any(char.islower() for char in password)
    digit_criteria = any(char.isdigit() for char in password)
    special_char_criteria = re.search(r'[!@#$%^&*(),.?":{}|<>]', password) is not None

    # Check if all criteria are met
    if all([length_criteria, uppercase_criteria, lowercase_criteria, digit_criteria, special_char_criteria]):
        return "Valid", ""
    else:
        weaknesses = []
        if not length_criteria:
            weaknesses.append("Password should be at least 8 characters long.")
        if not uppercase_criteria:
            weaknesses.append("Password should contain at least one uppercase letter.")
        if not lowercase_criteria:
            weaknesses.append("Password should contain at least one lowercase letter.")
        if not digit_criteria:
            weaknesses.append("Password should contain at least one digit.")
        if not special_char_criteria:
            weaknesses.append("Password should contain at least one special character.")

        return "Invalid", weaknesses


class PasswordCheckerApp:
    def __init__(self, root):
        self.time_label = None
        self.check_button = None
        self.strength_label = None
        self.weaknesses_label = None
        self.password_entry = None
        self.password_label = None
        self.root = root
        self.root.title("Password Checker")
        self.root.geometry("500x400")
        self.create_password_page()

    def create_password_page(self):
        self.password_label = tk.Label(self.root, text="Enter Password:", font=("Helvetica", 14))
        self.password_label.pack(pady=10)

        self.password_entry = tk.Entry(self.root, font=("Helvetica", 12), show="")
        self.password_entry.pack(pady=10)

        self.strength_label = tk.Label(self.root, text="", font=("Helvetica", 12))
        self.strength_label.pack(pady=5)

        self.weaknesses_label = tk.Label(self.root, text="", font=("Helvetica", 12), fg="red", justify="left")
        self.weaknesses_label.pack(pady=5)

        self.time_label = tk.Label(self.root, text="", font=("Helvetica", 12), justify="left")
        self.time_label.pack(pady=5)

        self.check_button = tk.Button(self.root, text="Check Password", command=self.check_password,
                                      font=("Helvetica", 12))
        self.check_button.pack(pady=10)

    def check_password(self):
        password = self.password_entry.get()
        strength, weaknesses = check_password_validation(password)

        if strength == "Valid":
            time_seconds, time_readable = time_to_crack(password)

            if 0 <= time_seconds <= 60:  # between 1 second and 1 week
                strength_category = "Weak"
                color = "red"
            elif 60 < time_seconds <= 3600:  # between 1 minute and 1 hour
                strength_category = "Medium"
                color = "orange"
            elif 3600 < time_seconds <= 86400:  # between 1 hour and 1 day
                strength_category = "Medium (Stronger)"
                color = "green"
            else:  # more than 1 day
                strength_category = "Strong"
                color = "blue"

            self.weaknesses_label.config(text="")
            self.time_label.config(
                text=f"Estimated time to crack: \n{time_readable}\nPassword Strength: {strength_category}", fg=color)
        else:
            error_message = (f"Weak password. Weaknesses:\n• {'\n• '.join(weaknesses)}\nPlease enter a password that "
                             f"meets the requirements below.")
            self.weaknesses_label.config(text=error_message)
            self.time_label.config(text="")


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordCheckerApp(root)
    root.mainloop()
