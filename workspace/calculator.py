import math
import sys
from typing import Union

class Calculator:
    """A production-grade calculator class providing basic and advanced arithmetic."""

    def __init__(self):
        pass

    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Error: Division by zero is not allowed.")
        return a / b

    def power(self, base: float, exponent: float) -> float:
        return math.pow(base, exponent)

    def square_root(self, a: float) -> float:
        if a < 0:
            raise ValueError("Error: Cannot calculate the square root of a negative number.")
        return math.sqrt(a)

def main():
    calc = Calculator()
    print("--- Production Grade Calculator ---")
    print("Operations: add, subtract, multiply, divide, power, sqrt, exit")

    while True:
        try:
            user_input = input("\nEnter operation (or 'exit' to quit): ").lower().strip()
            
            if user_input == 'exit':
                print("Exiting calculator. Goodbye!")
                break

            # Get numbers from user
            num1_raw = input("Enter first number: ")
            num2_raw = input("Enter second number (if applicable): ")
            
            num1 = float(num1_raw)
            num2 = float(num2_raw) if num2_raw else 0.0

            if user_input == 'add':
                result = calc.add(num1, num2)
                print(f"Result: {num1} + {num2} = {result}")
            elif user_input == 'subtract':
                result = calc.subtract(num1, num2)
                print(f"Result: {num1} - {num2} = {result}")
            elif user_input == 'multiply':
                result = calc.multiply(num1, num2)
                print(f"Result: {num1} * {num2} = {result}")
            elif user_input == 'divide':
                result = calc.divide(num1, num2)
                print(f"Result: {num1} / {num2} = {result}")
            elif user_input == 'power':
                result = calc.power(num1, num2)
                print(f"Result: {num1} ^ {num2} = {result}")
            elif user_input == 'sqrt':
                result = calc.square_root(num1)
                print(f"Result: sqrt({num1}) = {result}")
            else:
                print("Invalid operation. Please try again.")

        except ValueError as e:
            print(e)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
