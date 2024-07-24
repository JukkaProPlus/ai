import math
def calculate_sphere_volume(radius):
    """
    计算球体的体积。

    参数:
    radius (float): 球体的半径。

    返回:
    str: 描述球体体积的字符串。
    """
    volume = (4/3) * math.pi * (radius**3)
    return f"这个球的体积是{volume}"

from langchain.tools import StructuredTool

document_tool_calculate_sphere_volume = StructuredTool.from_function(
    func=calculate_sphere_volume,
    name="CalculateSphereVolume",
    description="计算给定半径的球体体积。"
)