def calculate_square_difference(a: int, b: int) -> str:
    """Calculate the square difference between two numbers a and b."""
    square_diff = (a ** 2) - (b ** 2)
    return f'{a}和{b}的平方差是{square_diff}'

from langchain.tools import StructuredTool

calculate_square_difference_tool = StructuredTool.from_function(
    func=calculate_square_difference,
    name='CalculateSquareDifference',
    description='This tool calculates the square difference between two input numbers.'
)