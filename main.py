import dearpygui.dearpygui as dpg
import networkx as nx
import Editor.Editor as Editor
import algorithms as alg
dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()

################# GUI #################

# def change_text(sender, app_data):
#     print("sender", sender)
#     print("app_data", app_data)
#     # if not panning_mode:
#         # dpg.set_value("text_item", f"Mouse Button: {app_data[0]}, Down Time: {app_data[1]} seconds")

# with dpg.handler_registry():
#     dpg.add_mouse_drag_handler(callback=change_text)

# with dpg.window(width=500, height=300):
#     dpg.add_text("Press any mouse button", tag="text_item")

## GUI::Main ##
with dpg.window(label="Primary", tag="primary", width = 1000, height=600):
    with dpg.group(horizontal=True, width=dpg.get_item_width("primary")/4*3):
        with dpg.tab_bar(label = "Graph View Bar", tag = "view_bar"):
            with dpg.tab(label = "Main View", tag = "main_view"):
                    with dpg.drawlist(label = "Main", tag = "main", width = 800, height = 800):
                        pass
        with dpg.group(horizontal=False):
            ## GUI::Info ##
            with dpg.group():
                with dpg.tab_bar(label = "Info Tab Bar", tag = "info_bar"):
                    with dpg.tab(label = "Info", tag = "info"):
                        dpg.add_text(default_value="This is info text.")
            ## GUI::Constants / Control ##
            with dpg.group():
                with dpg.tab_bar(label = "Control Tab Bar", tag = "control_bar"):
                    with dpg.tab(label = "Control", tag = "control"):
                        # dpg.add_text(default_value="This is info text.")
                        pass
            ## GUI::Terminal ##
            with dpg.group():
                with dpg.tab_bar(label = "Terminal Tab Bar", tag = "terminal_bar"):
                    with dpg.tab(label = "Terminal", tag = "terminal"):
                        # dpg.add_text(default_value="This is info text.")
                        pass

################# Editor Register #################
# RenderGraph.init_render_graph(G)
editor_registor = []

# main_ed = Editor.Editor(window = "main", graph = G)
# G = nx.Graph()
# G.add_edge(1, 2) # default edge data=1
# G.add_edge(2, 3, weight=0.9) # specify edge data


main_ed = Editor.Editor(window = "main")
# main_ed.graph.add_node(1)
# main_ed.graph.add_node(2)
# main_ed.graph.add_node(3)
main_ed.add_node(1, pos=[0, 0], color = (0,0,255,255))
main_ed.add_node(2, pos=[700, 400], color = (0,255,255,255))
main_ed.add_node(3, pos=[300, 500], color = (0,255,0,255))
main_ed.add_node(4, pos=[30, 500], color = (255,255,0,255))
main_ed.add_node(5, pos=[300, 50], color = (255,0,0,255))
# write a piece of code that generates colors?

main_ed.add_edge(3,5)
main_ed.add_edge(2,5)
main_ed.add_edge(4,5)
main_ed.add_edge(3,2) 
main_ed.add_edge(1,4)

main_ed.set_camera(0.5, [-100, -100])


### test algoritms ###

#alg.hl_shortest_path(main_ed,3,4)
print(alg.eccentricity(main_ed, 2))
#alg.hl_eccentricity(main_ed, 2)
alg.hl_periphery(main_ed)
editor_registor.append(main_ed)




################# Main Loop #################

dpg.show_viewport()
dpg.set_primary_window("primary", True)
mode = None
while dpg.is_dearpygui_running():
    for ed in editor_registor:
        ed.update_window()
        
    
    if mode == "pan":
        pass 
    
    dpg.render_dearpygui_frame()

dpg.destroy_context()


#################



