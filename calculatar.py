"""
CodSoft Python Programming Internship - Task 2: Calculator
Accepts unlimited integers from the user (type 'done' to stop),
applies the chosen operation left to right and displays the result.
"""

from functools import reduce


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError
    if a % b == 0:          # exact division -> keep as integer
        return a // b
    return a / b


def modulus(a, b):
    if b == 0:
        raise ZeroDivisionError
    return a % b


OPERATIONS = {
    "1": ("+", add, "Addition"),
    "2": ("-", subtract, "Subtraction"),
    "3": ("*", multiply, "Multiplication"),
    "4": ("/", divide, "Division"),
    "5": ("%", modulus, "Modulus"),
}


def get_integers():
    """Read any number of integers until the user types 'done'."""
    numbers = []
    print("\nEnter integers one by one. Type 'done' when finished.")
    while True:
        value = input(f"  Number {len(numbers) + 1}: ").strip()

        if value.lower() == "done":
            if len(numbers) < 2:
                print("  Please enter at least 2 numbers.")
                continue
            return numbers

        try:
            numbers.append(int(value))
        except ValueError:
            print("  Invalid input. Please enter a whole number (integer).")


def show_menu():
    print("\nSelect an operation:")
    for key, (symbol, _, name) in OPERATIONS.items():
        print(f"  {key}. {name:<15} ({symbol})")


def main():
    print("=" * 40)
    print("   CALCULATOR - UNLIMITED INTEGERS")
    print("=" * 40)

    while True:
        numbers = get_integers()

        show_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice not in OPERATIONS:
            print("\nInvalid choice! Please select a number from 1 to 5.")
        else:
            symbol, func, _ = OPERATIONS[choice]
            try:
                result = reduce(func, numbers)
                expression = f" {symbol} ".join(str(n) for n in numbers)
                print(f"\nResult: {expression} = {result}")
            except ZeroDivisionError:
                print("\nError: Division by zero is not allowed.")
            except OverflowError:
                print("\nError: Result is too large to display as a decimal.")

        again = input("\nDo you want to perform another calculation? (y/n): ").strip().lower()
        if again != "y":
            print("\nThank you for using the calculator. Goodbye!")
            break


if __name__ == "__main__":
    main()