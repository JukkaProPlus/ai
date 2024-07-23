def calculate_triangle_area_by_vertices(a, b, c):
    """
    计算由顶点坐标 a, b, c 确定的三角形面积。

    :param a: 第一个顶点坐标 (Xa, Ya)
    :param b: 第二个顶点坐标 (Xb, Yb)
    :param c: 第三个顶点坐标 (Xc, Yc)
    :return: 描述三角形面积的字符串
    """
    # 提取坐标值
    Xa, Ya = a
    Xb, Yb = b
    Xc, Yc = c

    # 计算向量AB和AC
    vector_AB = (Xb - Xa, Yb - Ya)
    vector_AC = (Xc - Xa, Yc - Ya)

    # 计算叉乘的z分量（即外积的模）
    cross_product_z = vector_AB[0] * vector_AC[1] - vector_AB[1] * vector_AC[0]

    # 计算面积
    area = abs(cross_product_z) / 2

    return f"这个三角形的面积是{area}"

# 将工具注册为StructuredTool
from langchain.tools import StructuredTool

document_tool_calculate_triangle_area_by_vertices = StructuredTool.from_function(
    func=calculate_triangle_area_by_vertices,
    name="CalculateTriangleAreaByVertices",
    description="根据三角形顶点坐标计算三角形的面积。输入为三个顶点坐标，输出为描述三角形面积的字符串。"
)