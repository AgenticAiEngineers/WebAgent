from tools.calculator_tool import CalculatorTool

calc = CalculatorTool()

while True:
    q = input("Enter math: ")
    print("Result:", calc.run(q))
