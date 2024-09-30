import json
import sys
from datetime import datetime
import argparse
import os

EXPENSES_FILE = "expenses.json"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
BUDGET_FILE = "budget.json"

def load_expenses():
    if not os.path.exists(EXPENSES_FILE):
        return []
    try:
        with open(EXPENSES_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}")
        return []

def save_expenses(expenses):
    try:    
        with open(EXPENSES_FILE, 'w') as f:
            json.dump(expenses, f, indent=2)
    except IOError as e:
        print(f"Error: {e}")

def load_budget():
    if not os.path.exists(BUDGET_FILE):
        return {}
    try:
        with open(BUDGET_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: {e}")
        return {}

def save_budget(budget):
    try:
        with open(BUDGET_FILE, 'w') as f:
            json.dump(budget, f, indent=2)
    except IOError as e:
        print(f"Error: {e}")

def set_budget(month, amount):
    budget = load_budget()
    if month < 1 or month > 12:
        print("Invalid month. Please enter a month between 1 and 12.")
        return
    if amount < 0 or amount is None:
        print("Invalid amount. Please enter a positive number.")
        return
    budget[str(month)] = amount
    save_budget(budget)
    print(f"Budget for month {month} set to ${amount:.2f}")

def get_budget(month):
    budget = load_budget()
    if month < 1 or month > 12:
        print("Invalid month. Please enter a month between 1 and 12.")
        return None
    return budget.get(str(month), 0)  # Convert month to string for dictionary lookup

def get_new_id(expenses):
    return max((expense['id'] for expense in expenses), default = 0) + 1

def add(description, amount, month):
    if not description or amount is None or amount < 0 or month is None or month < 1 or month > 12:
        print("Missing description or invalid amount or invalid month.")
        return
    
    expenses = load_expenses()
    new_expense = {
        "id": get_new_id(expenses),
        "description": description,
        "date": datetime.now().isoformat(),
        "amount": amount,
        "month": month
    }
    expenses.append(new_expense)
    budget = get_budget(month)
    if budget is None:
        print("Budget not set for this month. Please set the budget first.")
        return
    total_expenses = sum(expense['amount'] for expense in expenses if expense['month'] == month)
    if total_expenses > budget:
        print(f"Warning: Total expenses (${total_expenses:.2f}) exceed the budget for the month (${budget:.2f})")
    save_expenses(expenses)
    print(f"Expense added successfully (ID: {new_expense['id']})")

def update(id, description, amount):
    if id is None or not description or amount is None or amount < 0:
        print("Missing parameters or invalid parameters.")
        return
    expenses = load_expenses()
    for expense in expenses:
        if expense['id'] == id:
            expense['description'] = description
            expense['amount'] = amount
            expense['date'] = datetime.now().isoformat()
            save_expenses(expenses)
            print(f"Updated expense ID {id} successfully")
            return
    print(f"Expense with ID {id} not found")

def delete(id):
    expenses = load_expenses()
    original_length = len(expenses)
    expenses = [expense for expense in expenses if expense['id'] != id]
    if len(expenses) < original_length:
        save_expenses(expenses)
        print(f"Deleted expense ID {id} successfully")
    else:
        print(f"Expense with ID {id} not found")

def view():
    expenses = load_expenses()
    if not expenses:
        print("No expenses found")
        return
    print(f"{'ID':^4} {'Date':^19} {'Description':^20} {'Amount':^10}")
    print("-"*55)

    for expense in expenses:
        date = datetime.fromisoformat(expense['date']).strftime(DATE_FORMAT)
        print(f"{expense['id']:^4} {date:^19} {expense['description']:^20} {expense['amount']:^10.2f}")

def summary(month=None):
    expenses = load_expenses()
    
    if month is not None:
        try:
            month = int(month)
            if month < 1 or month > 12:
                raise ValueError
        except ValueError:
            print("Invalid month. Please enter a month between 1 and 12.")
            return
        filtered_expenses = [expense for expense in expenses if datetime.fromisoformat(expense['date']).month == month]
        total_expense = sum(expense['amount'] for expense in filtered_expenses)
        print(f"Total expenses in month {month} is: ${total_expense:.2f}")
    else:
        total_expense = sum(expense['amount'] for expense in expenses)
        print(f"Total expenses is: ${total_expense:.2f}")


def main():
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    parser.add_argument("action", type=str, choices = ['add', 'update', 'delete', 'view', 'summary', 'budget'], help="Action")
    parser.add_argument("--description", type=str, help="Expense Description")
    parser.add_argument("--amount", type=float, help="expense amount")
    parser.add_argument("--id", type=int, help="expenseid")
    parser.add_argument("--month", type=int, help="track expense in specific month")
    args = parser.parse_args()
    try:
        if args.action == "add":
            add(args.description, args.amount, args.month)
        elif args.action == "update":
            update(args.id, args.description, args.amount)
        elif args.action == "delete":
            delete(args.id)
        elif args.action == "view":
            view()
        elif args.action == "summary":
            summary(args.month)
        elif args.action == "budget":
            if args.month is None or args.amount is None:
                print("Both --month and --amount are required for setting a budget.")
            else:
                set_budget(args.month, args.amount)
        else:
            parser.print_help()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()