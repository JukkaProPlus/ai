def calculate_vector_product(v1, v2):
    return v1[0]*v2[1] - v1[1]*v2[0]

def CalculateQuadrilateralArea(a, b, c, d):
    """
    计算给定四个顶点坐标（a, b, c, d）的四边形面积，并返回描述面积的字符串。

    参数:
    a, b, c, d (tuple): 四边形的顶点坐标，每个顶点坐标为二元组(X, Y)。

    返回:
    str: 描述四边形面积的字符串。
    """
    # 计算向量 ab 和 bc
    vector_ab = (b[0] - a[0], b[1] - a[1])
    vector_bc = (c[0] - b[0], c[1] - b[1])

    # 计算向量的叉乘，得到平行四边形的一半面积
    half_area = calculate_vector_product(vector_ab, vector_bc)

    # 计算整个四边形的面积
    area = abs(half_area) * 2

    return f'这个四边形的面积是{area}'

from langchain.tools import StructuredTool

document_tool_CalculateQuadrilateralArea = StructuredTool.from_function(
    func=CalculateQuadrilateralArea,
    name='CalculateQuadrilateralArea',
    description='计算给定四个顶点坐标的四边形面积'
)