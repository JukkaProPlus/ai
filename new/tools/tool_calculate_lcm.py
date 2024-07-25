def calculate_lcm(a: int, b: int) -> str:
    """
    计算两个数的最小公倍数。

    参数:
    a (int): 第一个整数。
    b (int): 第二个整数。

    返回:
    str: 描述两个数最小公倍数的字符串。
    """
    def gcd(x, y):
        while y:
            x, y = y, x % y
        return x

    lcm = abs(a * b) // gcd(a, b)
    return f'{a}和{b}的最小公倍数是{lcm}'

from langchain.tools import StructuredTool
document_tool_calculate_lcm = StructuredTool.from_function(
    func=calculate_lcm,
    name='CalculateLCM',
    description='计算两个数的最小公倍数'
)