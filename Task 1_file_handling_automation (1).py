"""
Task 1: Python File Handling & Automation
-------------------------------------------
Goal: Demonstrate file handling (txt/csv), automation of file operations
(rename, move, delete), and proper exception handling using try-except.

Author: (your name)
"""

import os
import csv
import shutil

# ----------------------------------------------------------------------
# 1. SETUP: Create a working folder structure so the script is self-contained
# ----------------------------------------------------------------------
BASE_DIR = "demo_files"          # main working folder
ARCHIVE_DIR = os.path.join(BASE_DIR, "archive")  # folder we'll move files into

# Create directories if they don't already exist.
# os.makedirs with exist_ok=True avoids raising an error if the folder exists.
try:
    os.makedirs(BASE_DIR, exist_ok=True)
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    print(f"Directories ready: '{BASE_DIR}' and '{ARCHIVE_DIR}'")
except OSError as e:
    print(f"Error creating directories: {e}")


# ----------------------------------------------------------------------
# 2. WRITE & READ A TEXT FILE
# ----------------------------------------------------------------------
def write_text_file(filepath, lines):
    """Write a list of strings to a text file, one per line."""
    try:
        with open(filepath, "w") as f:   # 'w' mode creates/overwrites the file
            for line in lines:
                f.write(line + "\n")
        print(f"Text file written: {filepath}")
    except IOError as e:
        print(f"Error writing text file: {e}")


def read_text_file(filepath):
    """Read and print the contents of a text file line by line."""
    try:
        with open(filepath, "r") as f:
            print(f"\n--- Contents of {filepath} ---")
            for line in f:
                print(line.strip())
    except FileNotFoundError:
        print(f"Error: '{filepath}' does not exist.")
    except IOError as e:
        print(f"Error reading text file: {e}")


# ----------------------------------------------------------------------
# 3. WRITE & READ A CSV FILE
# ----------------------------------------------------------------------
def write_csv_file(filepath, header, rows):
    """Write tabular data to a CSV file using the csv module."""
    try:
        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)   # column headers
            writer.writerows(rows)    # actual data rows
        print(f"CSV file written: {filepath}")
    except IOError as e:
        print(f"Error writing CSV file: {e}")


def read_csv_file(filepath):
    """Read and print CSV file contents row by row."""
    try:
        with open(filepath, "r", newline="") as f:
            reader = csv.reader(f)
            print(f"\n--- Contents of {filepath} ---")
            for row in reader:
                print(row)
    except FileNotFoundError:
        print(f"Error: '{filepath}' does not exist.")
    except IOError as e:
        print(f"Error reading CSV file: {e}")


# ----------------------------------------------------------------------
# 4. AUTOMATE FILE OPERATIONS: RENAME, MOVE, DELETE
# ----------------------------------------------------------------------
def rename_file(old_path, new_path):
    """Rename (or move+rename) a file safely."""
    try:
        os.rename(old_path, new_path)
        print(f"Renamed '{old_path}' -> '{new_path}'")
    except FileNotFoundError:
        print(f"Error: source file '{old_path}' not found.")
    except FileExistsError:
        print(f"Error: target file '{new_path}' already exists.")
    except OSError as e:
        print(f"Error renaming file: {e}")


def move_file(src_path, dest_folder):
    """Move a file into another folder, using shutil for cross-platform safety."""
    try:
        shutil.move(src_path, dest_folder)
        print(f"Moved '{src_path}' -> '{dest_folder}'")
    except FileNotFoundError:
        print(f"Error: '{src_path}' not found.")
    except shutil.Error as e:
        print(f"Error moving file: {e}")


def delete_file(filepath):
    """Delete a file if it exists; handle the case where it doesn't."""
    try:
        os.remove(filepath)
        print(f"Deleted '{filepath}'")
    except FileNotFoundError:
        print(f"Error: '{filepath}' does not exist, nothing to delete.")
    except OSError as e:
        print(f"Error deleting file: {e}")


# ----------------------------------------------------------------------
# 5. MAIN DEMO: run all operations in sequence so it can be screenshotted
# ----------------------------------------------------------------------
if __name__ == "__main__":
    txt_path = os.path.join(BASE_DIR, "notes.txt")
    csv_path = os.path.join(BASE_DIR, "data.csv")
    renamed_txt_path = os.path.join(BASE_DIR, "notes_renamed.txt")

    # --- Text file demo ---
    write_text_file(txt_path, ["Hello, this is line 1.", "Automation demo line 2."])
    read_text_file(txt_path)

    # --- CSV file demo ---
    write_csv_file(
        csv_path,
        header=["Name", "Score"],
        rows=[["Alice", 92], ["Bob", 85], ["Charlie", 78]],
    )
    read_csv_file(csv_path)

    # --- File automation demo ---
    rename_file(txt_path, renamed_txt_path)      # rename notes.txt
    move_file(csv_path, ARCHIVE_DIR)             # move data.csv into archive/
    delete_file(renamed_txt_path)                # delete the renamed txt file

    # --- Demonstrate error handling on a non-existent file ---
    delete_file(os.path.join(BASE_DIR, "does_not_exist.txt"))

    print("\nAll file handling & automation operations completed.")
