import Structure.Vec2 as Vec2
import dearpygui.dearpygui as dpg

edge_thickness = 5

def draw_edge(pos1: Vec2, pos2: Vec2, window: str, tag, color: tuple, create: bool = False):
    pos1_array = pos1.to_precision_array(8)
    pos2_array = pos2.to_precision_array(8)
    
    # print("pos_array", pos_array)
    # print("tag", tag)
    # print("create", create)
    if not create:
        dpg.configure_item(tag, p1 = pos1_array, p2 = pos2_array)
    else:
        dpg.draw_line(pos1_array, pos2_array, tag=tag, parent= window, color= color, thickness= edge_thickness)