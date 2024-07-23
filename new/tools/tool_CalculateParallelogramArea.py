def CalculateParallelogramArea(base: float, height: float) -> str:
    """
    计算平行四边形的面积，并返回描述面积的字符串。

    参数:
    base (float): 平行四边形的底边长度。
    height (float): 平行四边形的高。

    返回:
    str: 描述平行四边形面积的字符串。
    """
    area = base * height
    return f'这个底边为{base}, 高为{height}的平行四边形的面积是{area}'

from langchain.tools import StructuredTool

document_tool_CalculateParallelogramArea = StructuredTool.from_function(
    func=CalculateParallelogramArea,
    name='CalculateParallelogramArea',
    description='计算给定底边和高的平行四边形的面积'
)