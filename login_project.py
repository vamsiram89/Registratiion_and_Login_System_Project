import re
import os

DATA_FILE = "login_data.txt"


# ------------------ UTILITY FUNCTIONS ------------------

def file_exists():
    return os.path.exists(DATA_FILE)


def load_users():
    users = {}
    if file_exists():
        with open(DATA_FILE, "r") as file:
            for line in file:
                username, password = line.strip().split(":")
                users[username] = password
    return users


def save_user(username, password):
    with open(DATA_FILE, "a") as file:
        file.write(f"{username}:{password}\n")


def update_password(username, new_password):
    users = load_users()
    users[username] = new_password

    with open(DATA_FILE, "w") as file:
        for user, pwd in users.items():
            file.write(f"{user}:{pwd}\n")


# ------------------------------------------------------- VALIDATION FUNCTIONS --------------------------------------------------

def validate_username(username):

    """
    Rules:
    - Must contain '@'
    - Must contain at least one '.' after '@'
    - No special characters or digits at the beginning
    - No '.' immediately after '@'
    """

    pattern = r"^[a-zA-Z][a-zA-Z0-9._]*@[a-zA-Z]+\.[a-zA-Z.]+$"

    if not re.match(pattern, username):
        return False

    if "@." in username:
        return False

    return True


def validate_password(password):

    """
    Rules:
    - Length: 6 to 16
    - At least 1 uppercase
    - At least 1 lowercase
    - At least 1 digit
    - At least 1 special character
    """

    if len(password) < 6 or len(password) > 16:
        return False

    if not re.search(r"[A-Z]", password):
        return False

    if not re.search(r"[a-z]", password):
        return False

    if not re.search(r"\d", password):
        return False

    if not re.search(r"[!@#$%^&*()_+=\-]", password):
        return False

    return True


# --------------------------------------------------------- REGISTRATION --------------------------------------------------

def register():
    users = load_users()

    while True:
        username = input("Enter username (email): ")
        if not validate_username(username):
            print("❌ Invalid username format.")
            continue

        if username in users:
            print("❌ Username in the system already exists.")
            continue

        break

    while True:
        password = input("Enter password: ")
        if not validate_password(password):
            print("❌ Password does not meet  security requirements.")
            continue
        break

    save_user(username, password)
    print("✅ Registration successful!")


# ------------------------------------------------------------- LOGIN --------------------------------------------------------

def login():
    users = load_users()

    username = input("Enter username: ")
    password = input("Enter password: ")

    if username in users and users[username] == password:
        print("✅ Login is successful, Access granted.")
    else:
        print("❌ Invalid credentials.")
        login_options()


def login_options():
    print("\n1. Register")
    print("2. Forgot Password")
    choice = input("Choose an option (1/2): ")

    if choice == "1":
        register()
    elif choice == "2":
        forgot_password()
    else:
        print("❌ Invalid choice.")


# --------------------------------------------------------------- FORGOT PASSWORD ---------------------------------------------

def forgot_password():
    users = load_users()
    username = input("Enter your registered username: ")

    if username not in users:
        print("❌ Username not found. Please register.")
        return

    print("1. View Password")
    print("2. Reset Password")
    choice = input("Choose an option (1/2): ")

    if choice == "1":
        print(f"🔑 Your password is: {users[username]}")
    elif choice == "2":
        while True:
            new_password = input("Enter new password: ")
            if validate_password(new_password):
                update_password(username, new_password)
                print("✅ Password updated successfully.")
                break
            else:
                print("❌ Password does not meet requirements.")
    else:
        print("❌ Invalid choice.")


# --------------------------------------------------------------- MAIN MENU ---------------------------------------------------

def main():
    while True:
        print("\n--- Authentication System ---")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            print("👋 Exiting application.")
            break
        else:
            print("❌ Invalid choice.")


if __name__ == "__main__":
    main()
