def print_pascal_triangle(n: int) -> str:
    """
    打印杨辉三角的前n行。

    参数:
    n (int): 需要打印的杨辉三角的行数。

    返回:
    str: 杨辉三角的前n行，每行用逗号分隔。
    """
    triangle = []
    for i in range(n):
        row = [1] * (i + 1)
        for j in range(1, i):
            row[j] = triangle[i - 1][j - 1] + triangle[i - 1][j]
        triangle.append(row)
    result = '\n'.join([','.join(map(str, row)) for row in triangle])
    return result

from langchain.tools import StructuredTool

document_tool_print_pascal_triangle = StructuredTool.from_function(
    func=print_pascal_triangle,
    name='PrintPascalTriangle',
    description='打印杨辉三角的前n行，每行用逗号分隔'
)