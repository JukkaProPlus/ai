def calculate_triangle_area(base: float, height: float) -> str:
    """
    计算三角形的面积。

    参数:
    base (float): 三角形的底边长。
    height (float): 三角形的高。

    返回:
    str: 描述三角形面积的字符串，格式为'三角形的面积是c'，其中c为计算出的面积。
    """
    # 计算三角形面积
    area = 0.5 * base * height

    # 返回格式化的字符串结果
    return f"三角形的面积是{area}"

from langchain.tools import StructuredTool

document_tool_calculate_triangle_area = StructuredTool.from_function(
    func=calculate_triangle_area,
    name="CalculateTriangleArea",
    description="计算三角形的面积，输入是三角形的底边长和高，输出是描述三角形面积的字符串。"
)