from interface.BlocksCanvas.Abstract import ClickableObject
from tkinter.font import Font
import tkinter as tk
import math
from tkinter import simpledialog

class PopupEditor:
    def __init__(self, master, data):
        self.top = tk.Toplevel(master)
        self.top.title("Modifier les paramètres")
        self.data = data
        self.entries = {}

        for function in self.data['functions']:
            function_frame = tk.LabelFrame(self.top, text=function['name'], padx=5, pady=5)
            function_frame.pack(padx=10, pady=10, fill=tk.X, expand=True)

            for param in function['parameters']:
                param_frame = tk.Frame(function_frame)
                param_frame.pack(fill=tk.X, padx=5, pady=5)

                tk.Label(param_frame, text=param['name']).pack(side=tk.LEFT)
                if param['user_input'] and param['is_input'] :
                    entry = tk.Entry(param_frame)
                    entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)
                    self.entries[param['name']] = entry

        tk.Button(self.top, text="Enregistrer", command=self.save_data).pack(pady=20)

    def save_data(self):
        for function in self.data['functions']:
            for param in function['parameters']:
                param_name = param['name']
                param['value'] = self.entries.get(param_name, None)
        self.top.destroy()

def create_popup_from_json(master, data):
    popup = PopupEditor(master, data)
    master.wait_window(popup.top)  # Attendre que la fenêtre popup soit fermée
    return data  # Renvoyer les données mises à jour

class AbstractBlock(ClickableObject):
    def __init__(self, canvas, posX, posY, text, font_size, color, children=None, text_alignement = "center", radius=10, border_color="black", border_width=0, z_index=0, IsStatic=False):
        if children is None:
            children = []  # Utilisation d'une valeur par défaut mutable dans un argument de fonction est une mauvaise pratique
        self.text = text
        self.font_size = font_size
        self.font = Font(size=font_size)  # Assurez-vous que Font est correctement importé depuis tkinter.font
        self.radius = radius
        self.canvas = canvas
        self.children = children
        self.text_alignement = text_alignement
        sizeX, sizeY = self.calculate_text_dimensions(text)
        super().__init__(canvas, posX, posY, sizeX, sizeY, color, radius, border_color, border_width, z_index, IsStatic)

    def calculate_text_dimensions(self, text):
        self.text_width = self.font.measure(text)
        self.text_height = self.font.metrics("linespace")

        width = self.text_width + self.radius * 2
        height = self.text_height + self.radius * 3

        for child in self.children:
            sX, sY = child.getSize()
            height += sY
            width = max(width, sX + self.radius * 2)
        return width, height
    
    def get_children_node(self):
        nodes = []

        for child in self.children:
            try:
                nodes.extend(child.get_children_node())
            except:
                pass

        return nodes
    
    def draw(self):
        super().draw()
        if self.text_alignement == "center":
            centerX = self.posX + self.sizeX / 2
        else:
            centerX = self.posX + self.text_width / 2 + self.radius
        centerY = self.posY + self.radius + self.text_height / 2
        self.canvas.create_text(centerX, centerY, text=self.text, font=self.font, fill="white")

        currentY = centerY + self.text_height / 2 + self.radius
        for child in self.children:
            sX, sY = child.getSize()
            child.setSize(self.sizeX, sY)
            currentX = self.posX
            child.move(currentX, currentY)
            child.draw()
            currentY += sY

class DeleteButton(ClickableObject):
    def __init__(self, canvas, master, posX, posY, color="red", size = 70, radius=10, cross_color="white", border_color="black", cross_size=0.7, border_width=5, z_index=10):
        super().__init__(canvas, posX, posY, size, size, color, radius, border_color, border_width, z_index)
        self.cross_color = cross_color
        self.cross_size = cross_size
        self.master = master

    def draw(self):
        super().draw()
        # Calculer la longueur de la diagonale de la croix
        diagonal_length = min(self.sizeX, self.sizeY) * self.cross_size

        # Calculer les points de départ et de fin pour chaque diagonale de la croix
        start_x1 = self.posX + (self.sizeX - diagonal_length) / 2
        end_x1 = start_x1 + diagonal_length
        start_y1 = self.posY + (self.sizeY - diagonal_length) / 2
        end_y1 = start_y1 + diagonal_length

        start_x2 = self.posX + (self.sizeX + diagonal_length) / 2
        end_x2 = start_x2 - diagonal_length

        # Dessiner les diagonales de la croix
        self.canvas.create_line(start_x1, start_y1, end_x1, end_y1, fill=self.cross_color, width=self.border_width)
        self.canvas.create_line(start_x2, start_y1, end_x2, end_y1, fill=self.cross_color, width=self.border_width)

    def on_click(self):
        super().on_click()
        print("delete")

        self.canvas.delete_object(self.master)
        self.canvas.delete_object(self)
        nodes = self.master.get_children_node()
        for n in nodes :
            n.delete()
        
# Object class
class ClassBlock(AbstractBlock):
    def __init__(self, canvas, posX, posY, text, font_size, color, children=[], z_index=0):
        super().__init__(canvas, posX, posY, text, font_size, color, children, z_index = z_index, text_alignement = "right")
        self.setSize(self.sizeX + self.text_height + self.radius, self.sizeY)
        X = self.posX + self.sizeX - self.radius - self.text_height
        Y = self.posY + self.radius
        self.delete_button = DeleteButton(self.canvas, self, X, Y, size = self.text_height, radius=self.radius)
        self.canvas.add_object(self.delete_button)

    def draw(self):
        super().draw()
        X = self.posX + self.sizeX - self.radius - self.text_height
        Y = self.posY + self.radius
        self.delete_button.setPosition(X, Y)

    def get_info(self):
        res = []
        for child in self.children:
            if isinstance(child, FunctionBlock):
                res.append(child.get_info())

        return {"name": self.text, "functions" : res}

    def on_click_right(self):
        super().on_click_right()
        data = create_popup_from_json(self.canvas, self.get_info())
        print(data)

# Function class
class FunctionBlock(AbstractBlock):
    def __init__(self, canvas, posX, posY, text, font_size, children=[], z_index=0):
        super().__init__(canvas, posX, posY, text, font_size, color = "grey", children = children, z_index = z_index, radius=0)

    def get_info(self):
        res = []
        for child in self.children:
            if isinstance(child, ParameterBlock):
                res.append(child.get_info())

        return {"name": self.text, "parameters" : res}

class ConstBlock(FunctionBlock):
    def __init__(self, canvas, posX, posY, text, font_size, z_index=0):
        super().__init__(canvas, posX, posY, text, font_size, children = [], z_index = z_index, radius=2)
        self.value = None
        self.children = [ParameterBlock(posX, posY, text = str(self.value), font_size = font_size, IsInput = False, z_index = z_index)]

# Parameter class
class ParameterBlock(AbstractBlock):
    def __init__(self, canvas, posX, posY, text, font_size, IsInput, IsUserInput, z_index=0):
        super().__init__(canvas, posX, posY, text, font_size, color = "grey", z_index = z_index, radius=2)
        self.IsInput = IsInput
        self.IsUserInput = IsUserInput
        self.nodeRadius = self.text_height * 0.4
        nodeX = self.posX - self.nodeRadius if self.IsInput else self.posX + self.sizeX - self.nodeRadius
        nodeY = self.posY + self.text_height / 2 - self.nodeRadius / 2 
        self.node = Node(canvas, nodeX, nodeY, IsInput, radius = self.nodeRadius, z_index = z_index + 1)
        self.canvas.add_object(self.node)

    def draw(self):
        super().draw()
        r = self.nodeRadius/2
        nodeX = self.posX - self.nodeRadius if self.IsInput else self.posX + self.sizeX - self.nodeRadius
        nodeY = self.posY + self.text_height / 2 - self.nodeRadius / 2 
        self.node.setPosition(nodeX, nodeY)

    def get_info(self):
        return {"name": self.text, "is_input": self.IsInput, "user_input": self.IsUserInput}

    def get_children_node(self):
        return [self.node]

# Node
class Node(ClickableObject):
    def __init__(self, canvas, posX, posY, IsInput, radius=5, color = "black", z_index = 0):
        super().__init__(canvas, posX + radius, posY + radius, radius * 2, radius * 2, color, radius, border_width=0, z_index=z_index, IsStatic=True)
        self.IsInput = IsInput
        self.target_links = []

    def on_click(self):
        super().on_click()
        # self.canvas.target_node = self

    def delete(self):
        for link in self.target_links:
            link.delete()

        self.canvas.delete_object(self)

    def add_link(self, link):
        self.target_links.append(link)

    def remove_link(self, link):
        if link in self.target_links:
            self.target_links.remove(link)

class Link:
    def __init__(self, canvas, node_start, node_end, color="black", width=2, z_index = 1):
        self.canvas = canvas
        self.node_start = node_start
        self.node_end = node_end
        self.color = color
        self.width = width
        self.z_index = z_index
        self.IsStatic = True

        self.node_start.add_link(self)
        self.node_end.add_link(self)

    def get_coord(self):
        # Calculer la position de début et de fin
        x1, y1 = self.node_start.posX + self.node_start.radius, self.node_start.posY + self.node_start.radius
        x2, y2 = self.node_end.posX + self.node_end.radius, self.node_end.posY + self.node_end.radius

        return x1, y1, x2, y2

    def draw(self):
        # Calculer la position de début et de fin
        x1, y1, x2, y2 = self.get_coord()

        # Dessiner la ligne et la flèche
        self.draw_arrow(x1, y1, x2, y2)

        print("draw arrow", x1)

    def draw_arrow(self, x1, y1, x2, y2):
        # Dessiner une ligne avec une flèche à la fin
        self.canvas.create_line(x1, y1, x2, y2, fill=self.color, width=self.width, arrow=tk.LAST, tags="arrow_line")

    def on_click(self):
        self.delete()
        print("delete", self)

    def delete(self):
        self.node_start.remove_link(self)
        self.node_end.remove_link(self)
        self.canvas.delete_object(self)

    def is_inside(self, x, y):
        # Calculer la position de début et de fin
        x1, y1, x2, y2 = self.get_coord()
        return is_point_inside_thick_line_segment(x1, y1, x2, y2, x, y, self.width)


def is_point_inside_thick_line_segment(x1, y1, x2, y2, xm, ym, thickness):
    # Calculer la distance entre (x1, y1) et (x2, y2)
    line_length = math.hypot(x2 - x1, y2 - y1)
    
    # Calculer le vecteur directeur de la ligne
    if line_length == 0:
        return False

    dx = (x2 - x1) / line_length
    dy = (y2 - y1) / line_length
    
    # Calculer le vecteur perpendiculaire à la ligne
    perp_dx = -dy
    perp_dy = dx
    
    # Calculer la distance du point (xm, ym) à la ligne
    distance_to_line = abs(perp_dx * (xm - x1) + perp_dy * (ym - y1))
    
    # Vérifier si le point est à moins de la moitié de l'épaisseur de la ligne
    if distance_to_line <= thickness / 2:
        # Calculer les projections sur la ligne
        dot_product = dx * (xm - x1) + dy * (ym - y1)
        projection_x = x1 + dot_product * dx
        projection_y = y1 + dot_product * dy
        
        # Vérifier si la projection est entre les points (x1, y1) et (x2, y2)
        if min(x1, x2) <= projection_x <= max(x1, x2) and min(y1, y2) <= projection_y <= max(y1, y2):
            return True

    return False
