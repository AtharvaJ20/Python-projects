def add(a,b):
    return a+b

def subtract(a,b):
    return a-b

def multiply(a,b):
    return a*b

def divide(a,b):
    if b==0:
        return "Error : Cant divide by zero"
    return a/b

def power(a,b):
    return a**b

def modulus(a,b):
    return a%b 

operations = {
    '+' : add,
    '-' : subtract,
    '*' : multiply,
    '/' : divide,
    '**' : power,
    '%' : modulus
}

def user_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except:
            print("Please enter a valid number")

def calculate():
    print("\n ---Simple calculator---")

    a = user_input("Enter first number: ")
    b = user_input("Enter second number: ")

    print(f"\nOperators : {''.join(operations.keys())}")

    while True:
        operator = input("Choose an operator:").strip()

        if operator in operations:
            break
        
        print(f"Unknown operator {operator}. Try +,-,*,/.")
            
    
    result = operations[operator](a,b)
    output = f"\n{a} {operator} {b} = {result}"

    print(f"\n{output}")
    return output

def main():
    print("Welcome to Calculator")
    history = []

    while True:
        result = calculate()

        if result:
            history.append(result)

        again = input("\nTry again? (y/n) : ").strip().lower()

        if again!= 'y':
            if history:
                print("\n---History Session---")
                for i,entry in enumerate(history,start=1):
                    print(f"{i}.{entry}")
            print("Goodbye! See you again")
            break


main()


