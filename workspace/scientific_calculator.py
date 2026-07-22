import math

def show_menu():
    print("\n--- Scientific Calculator ---")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")
    print("5. Power (^)")
    print("6. Square Root (sqrt)")
    print("7. Sine (sin) - Degrees")
    print("8. Cosine (cos) - Degrees")
    print("9. Tangent (tan) - Degrees")
    print("10. Logarithm (log10)")
    print("11. Natural Logarithm (ln)")
    print("12. Factorial (!)")
    print("0. Exit")
    print("-----------------------------")

def main():
    while True:
        show_menu()
        choice = input("Select an option (0-12): ")

        if choice == '0':
            print("Exiting calculator. Goodbye!")
            break

        try:
            if choice in ['1', '2', '3', '4', '5']:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
                
                if choice == '1':
                    print(f"Result: {num1 + num2}")
                elif choice == '2':
                    print(f"Result: {num1 - num2}")
                elif choice == '3':
                    print(f"Result: {num1 * num2}")
                elif choice == '4':
                    if num2 == 0:
                        print("Error: Division by zero.")
                    else:
                        print(f"Result: {num1 / num2}")
                elif choice == '5':
                    print(f"Result: {math.pow(num1, num2)}")

            elif choice in ['6', '7', '8', '9']:
                num = float(input("Enter number: "))
                if choice == '6':
                    print(f"Result: {math.sqrt(num)}")
                elif choice == '7':
                    print(f"Result: {math.sin(math.radians(num))}")
                elif choice == '8':
                    print(f"Result: {math.cos(math.radians(num))}")
                elif choice == '9':
                    print(f"Result: {math.tan(math.radians(num))}")

            elif choice in ['10', '11']:
                num = float(input("Enter number: "))
                if choice == '10':
                    if num <= 0:
                        print("Error: Logarithm of non-positive number.")
                    else:
                        print(f"Result: {math.log10(num)}")
                elif choice == '11':
                    if num <= 0:
                        print("Error: Logarithm of non-positive number.")
                    else:
                        print(f"Result: {math.log(num)}")

            elif choice == '12':
                num = int(input("Enter integer: "))
                if num < 0:
                    print("Error: Factorial of negative number.")
                else:
                    print(f"Result: {math.factorial(num)}")
            else:
                print("Invalid choice. Please try again.")

        except ValueError as e:
            print(f"Input Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
