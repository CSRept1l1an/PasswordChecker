# Password Strength Checker

This Python script checks the strength of a password based on various criteria, including length, the presence of uppercase and lowercase letters, digits, and special characters. 
It also estimates the time it would take to crack the password using the zxcvbn library. 

## Usage

1. Ensure you have Python installed on your machine.

2. Install the required library:

    ```bash
    pip install zxcvbn
    ```

3. Run the script:

    ```bash
    python PasswordChecker.py
    ```

4. Enter a password when prompted.

5. The script will display the password strength, weaknesses, and the estimated time to crack.

#Acknowledgments
The zxcvbn library for password strength estimation.
Tkinter for providing the graphical user interface.
