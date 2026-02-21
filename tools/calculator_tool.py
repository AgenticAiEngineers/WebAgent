class CalculatorTool:

    def run(self, query: str):
        try:
            result = eval(query)
            return str(result)
        except:
            return "Invalid math expression."
