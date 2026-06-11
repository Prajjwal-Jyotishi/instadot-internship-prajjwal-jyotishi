from datetime import datetime
import os

name = input("Enter your name: ")
track = input("Enter active track: ")

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

message = (
    f"[{timestamp}] Welcome {name}. "
    f"You have been successfully onboarded to the {track} track.\n"
)

os.makedirs("logs", exist_ok=True)

with open("logs/onboarding.log", "a") as file:
    file.write(message)

print("System check completed successfully.")
print("Log written to logs/onboarding.log")