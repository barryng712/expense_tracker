# Expense Tracker

A comprehensive expense tracking application to manage your finances efficiently. This CLI-based tool allows users to add, update, delete, and view their expenses, as well as set and manage budgets for different months.

## Features

1. Add expenses with description, amount, and month
2. Update existing expenses
3. Delete expenses
4. View all expenses
5. Get a summary of expenses (total or by month)
6. Set and manage monthly budgets
7. Receive warnings when expenses exceed the monthly budget

## Project Structure

The project consists of the following main components:

1. `cli.py`: The main command-line interface script
2. `expenses.json`: JSON file to store expense data
3. `budget.json`: JSON file to store budget data
4. `tests.py`: A test script to verify the functionality of the expense tracker

## Usage

The application can be run from the command line with various actions and parameters:

```
python cli.py <action> [--description <description>] [--amount <amount>] [--month <month>]
```

### Actions

1. `add`: Add a new expense

```
python cli.py add --description "Groceries" --amount 50.25 --month 5
```

2. `update`: Update an existing expense

```
python cli.py update --id 1 --description "Updated groceries" --amount 60.00 --month 5  
```

3. `delete`: Delete an existing expense

```
python cli.py delete --id 1
``` 

4. `view`: View all expenses

```
python cli.py view
```

5. `summary`: Get a summary of expenses (total or by month)

```
python cli.py summary
```

6. `budget`: Set or manage monthly budgets

```
python cli.py budget --month 5 --amount 100
``` 

## Testing

To run the tests, use the following command:

```
python tests.py
``` 

src https://roadmap.sh/projects/expense-tracker