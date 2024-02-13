# Click object

import tkinter as tk

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, outline="black", fill="", width=0):
    """Draws a rounded rectangle on a Tkinter canvas using loops to minimize code repetition.

    Args:
        canvas: The Tkinter canvas where the drawing will occur.
        x1, y1: The coordinates of the top-left corner of the rectangle.
        x2, y2: The coordinates of the bottom-right corner of the rectangle.
        radius: The radius of the rounded corners.
        outline: The color used for the outline of the rounded rectangle.
        fill: The fill color for the rectangle and the arcs.
        width: The width of the outline.
    """

    # Draw the inner rectangles for fill
    canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2 + 1, fill=fill, width=0)
    canvas.create_rectangle(x1, y1 + radius, x2 + 1, y2 - radius, fill=fill, width=0)

    # Corner arcs and connecting lines data
    arcs = [
        (x1, y1, x1 + 2*radius, y1 + 2*radius, 90),  # Top-left
        (x2 - 2*radius, y1, x2, y1 + 2*radius, 0),   # Top-right
        (x1, y2 - 2*radius, x1 + 2*radius, y2, 180), # Bottom-left
        (x2 - 2*radius, y2 - 2*radius, x2, y2, 270)  # Bottom-right
    ]

    lines = [
        (x1 + radius, y1, x2 - radius, y1),  # Top
        (x1 + radius, y2, x2 - radius, y2),  # Bottom
        (x1, y1 + radius, x1, y2 - radius),  # Left
        (x2, y1 + radius, x2, y2 - radius)   # Right
    ]

    # Draw the arcs
    for x1_arc, y1_arc, x2_arc, y2_arc, start in arcs:
        canvas.create_arc(x1_arc, y1_arc, x2_arc, y2_arc, start=start, extent=90, style='pieslice', fill=fill, outline=fill, width=0)
        if width > 0:
            canvas.create_arc(x1_arc, y1_arc, x2_arc, y2_arc, start=start, extent=90, style='arc', outline=outline, width=width)

    # Draw the connecting lines if outline width is greater than 0
    if width > 0:
        for x1_line, y1_line, x2_line, y2_line in lines:
            canvas.create_line(x1_line, y1_line, x2_line, y2_line, fill=outline, width=width)


class ClickableObject:
    def __init__(self, canvas, posX, posY, sizeX, sizeY, color, radius = 0, border_color="black", border_width=0, z_index = 0, IsStatic = True):
        self.canvas = canvas
        self.posX = posX
        self.posY = posY
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.radius = radius
        self.color = color
        self.border_color = border_color
        self.border_width = border_width
        self.z_index = z_index
        self.type = ("square", "ovale")[self.radius >= min(self.sizeX, self.sizeY) / 2]
        self.shape = None
        self.IsStatic = IsStatic

    def draw(self):
        if self.type == "ovale":
            # Dessine un ovale
            self.shape = self.canvas.create_oval(self.posX, self.posY, self.posX + self.sizeX, self.posY + self.sizeY, fill=self.color, outline=self.border_color, width=self.border_width)
        elif self.type == "square":

            # Dessine un rectangle avec des coins arrondis
            if(self.radius > 0):
                self.shape = create_rounded_rectangle(self.canvas, self.posX, self.posY, self.posX + self.sizeX, self.posY + self.sizeY, radius=self.radius, fill=self.color, width=self.border_width)
            else:
                self.shape = self.canvas.create_rectangle(self.posX, self.posY, self.posX + self.sizeX, self.posY + self.sizeY, fill=self.color, outline=self.border_color, width=self.border_width)

    def is_inside(self, x, y):
        # Vérifie si le point (x, y) est à l'intérieur de l'objet
        if self.type == "ovale":
            # Calcule le centre de l'ovale
            center_x = self.posX + self.sizeX / 2
            center_y = self.posY + self.sizeY / 2
            # Le "rayon" dans les directions x et y correspond à la moitié de la taille de l'ovale
            radius1 = self.sizeX / 2
            radius2 = self.sizeY / 2
            return self.is_inside_ovale(x, y, center_x, center_y, radius1, radius2)
        elif self.type == "square":
            return (self.posX <= x <= self.posX + self.sizeX) and (self.posY <= y <= self.posY + self.sizeY)

    
    def is_inside_ovale(self, x, y, center_x, center_y, radius1, radius2):
        # Calcule la normalisation des coordonnées du point par rapport au centre de l'ovale
        dx = (x - center_x) / radius1
        dy = (y - center_y) / radius2

        # Applique l'équation de l'ellipse
        return dx**2 + dy**2 <= 1
    
    def move(self, newX, newY):
        if not self.IsStatic:
            self.posX, self.posY = newX, newY

    def setSize(self, newSizeX, newSizeY):
        self.sizeX, self.sizeY = newSizeX, newSizeY

    def getSize(self):
        return self.sizeX, self.sizeY
    
    def setPosition(self, newX, newY):
        self.posX, self.posY = newX, newY

    def getPosition(self):
        return self.posX, self.posY

    def on_click(self):
            print(f"{self.type} at ({self.posX}, {self.posY}) was clicked")

    def on_click_right(self):
        print(f"{self.type} at ({self.posX}, {self.posY}) was right clicked")
