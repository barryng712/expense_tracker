import subprocess
import os
import json
from datetime import datetime

TEMP_EXPENSES_FILE = "expenses.json"
TEMP_BUDGET_FILE = "budget.json"

def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    print(f"Command: {' '.join(command)}")
    print(f"Output: {result.stdout.strip()}")
    print(f"Error: {result.stderr.strip()}")
    print("-" * 50)
    return result

def cleanup():
    for file in [TEMP_EXPENSES_FILE, TEMP_BUDGET_FILE]:
        if os.path.exists(file):
            os.remove(file)

def test_expense_tracker():
    cleanup()

    # Test setting budget
    run_command(["python", "cli.py", "budget", "--month", "5", "--amount", "1000"])
    
    # Test adding expenses with month
    run_command(["python", "cli.py", "add", "--description", "Groceries", "--amount", "50.25", "--month", "5"])
    run_command(["python", "cli.py", "add", "--description", "Gas", "--amount", "30.00", "--month", "5"])

    # Test viewing expenses
    run_command(["python", "cli.py", "view"])

    # Test updating an expense
    run_command(["python", "cli.py", "update", "--id", "1", "--description", "Supermarket", "--amount", "55.50"])

    # Test deleting an expense
    run_command(["python", "cli.py", "delete", "--id", "2"])

    # Test summary
    run_command(["python", "cli.py", "summary"])

    # Test summary for a specific month
    run_command(["python", "cli.py", "summary", "--month", "5"])

    # Test adding expense that exceeds budget
    run_command(["python", "cli.py", "budget", "--month", "6", "--amount", "100"])
    run_command(["python", "cli.py", "add", "--description", "Expensive item", "--amount", "150", "--month", "6"])

    # Test invalid inputs
    run_command(["python", "cli.py", "add", "--description", "Invalid", "--amount", "-10", "--month", "5"])
    run_command(["python", "cli.py", "update", "--id", "999", "--description", "Non-existent", "--amount", "10"])
    run_command(["python", "cli.py", "budget", "--month", "13", "--amount", "1000"])
    run_command(["python", "cli.py", "budget", "--month", "5", "--amount", "-100"])
    run_command(["python", "cli.py", "add", "--description", "Invalid month", "--amount", "50", "--month", "13"])

    # Test adding expense without setting budget
    run_command(["python", "cli.py", "add", "--description", "No budget", "--amount", "75", "--month", "7"])

    # Verify final state of expenses and budget
    print("Final expenses:")
    with open(TEMP_EXPENSES_FILE, 'r') as f:
        print(json.dumps(json.load(f), indent=2))
    
    print("Final budget:")
    with open(TEMP_BUDGET_FILE, 'r') as f:
        print(json.dumps(json.load(f), indent=2))

    cleanup()

if __name__ == "__main__":
    test_expense_tracker()
