from .tool_read_file import document_tool_read_file
from .tool_write_file import document_tool_write_file
from .tool_list_dir import document_tool_list_dir
from .tool_fibonacci import document_tool_fibonacci
from .tool_create_directory import document_tool_create_directory
from .tool_square_difference import calculate_square_difference_tool
from .tool_calculate_triangle_area import document_tool_calculate_triangle_area
from .tool_CalculateParallelogramArea import document_tool_CalculateParallelogramArea
from .tool_calculate_triangle_area_by_vertices import document_tool_calculate_triangle_area_by_vertices
from .tool_calculate_sphere_volume import document_tool_calculate_sphere_volume
from .tool_CalculateQuadrilateralArea import document_tool_CalculateQuadrilateralArea

tools = [
    document_tool_read_file,
    document_tool_write_file,
    document_tool_list_dir,
    document_tool_fibonacci,
    document_tool_create_directory,
    calculate_square_difference_tool,
    document_tool_calculate_triangle_area,
    document_tool_CalculateParallelogramArea,
    document_tool_calculate_triangle_area_by_vertices,
    document_tool_calculate_sphere_volume,
    document_tool_CalculateQuadrilateralArea,
]