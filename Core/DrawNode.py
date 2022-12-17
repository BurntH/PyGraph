import Structure.Vec2 as Vec2
import dearpygui.dearpygui as dpg

node_radius = 25

def draw_node(pos: Vec2, window: str, tag, scale: float, fill_color: tuple =(255,255,255,255), create: bool=False):
    pos_array = pos.to_precision_array(8)
    # print("pos_array", pos_array)
    # print("tag", tag)
    # print("create", create)
    if not create:
        dpg.configure_item(tag, center=pos_array)
    else:
        dpg.draw_circle(pos_array, node_radius * scale, tag=tag, parent= window, fill=fill_color)

