import tkinter as tk
from interface.Abstract import ClickableObject
from interface.Block import ClassBlock, FunctionBlock, ParameterBlock, Node, Link
import inspect
import json

# Exemple d'utilisation avec une classe de démonstration
class Agent:
    def at_start(prompt : str = "", personality : str = ""):
        pass

    def update_story(new_story : str):
        pass

    def get_story():
        pass

def class_to_dict(cls, to_json = False):
    class_data = {
        "name": cls.__name__,
        "functions": []
    }

    # Obtenir toutes les méthodes de la classe qui ne commencent pas par '__'
    methods = [m for m in inspect.getmembers(cls, inspect.isfunction) if not m[0].startswith('__')]
    for name, method in methods:
        output_signature = inspect.signature(method).return_annotation

        method_data = {
            "name": name,
            "parameters": [],
            "return_type": str(output_signature.__name__) if output_signature != inspect.Signature.empty and output_signature is not None else "None"
        }

        # Obtenir les paramètres pour chaque méthode
        params = inspect.signature(method).parameters
        for param_name, param in params.items():
            param_data = {
                "name": param_name,
                "type": param.annotation.__name__ if param.annotation != inspect.Parameter.empty and param.annotation is not None else "None",
                "is_input": True,  # Vous pouvez ajuster cette logique selon vos besoins
                "value": param.default if param.default != inspect.Parameter.empty else None
            }
            method_data["parameters"].append(param_data)

        class_data["functions"].append(method_data)

    if to_json:
        return json.dumps(class_data, indent=4)
    else :
        return class_data

def create_agent(canvas):
    object_data = class_to_dict(Agent)
    print(object_data)
    create_class_instance(canvas, object_data)

def create_class_instance(canvas, object_data):

    # Créer l'instance de ClassBlock pour l'agent
    class_block = ClassBlock(canvas, 100, 100, object_data['name'], 30, "green", children=[
        FunctionBlock(
            canvas, 
            150, 
            150, 
            function['name'], 
            24, 
            children=[
                ParameterBlock(canvas, 200, 200, param['name'], 18, IsInput=param['is_input'], IsUserInput=param['value']!=None)
                for param in function['parameters']
            ] + [
                ParameterBlock(canvas, 200, 200, "output", 18, IsInput=False, IsUserInput=False)
            ]
        )
        for function in object_data['functions']
    ])

    # Ajouter le ClassBlock au canvas
    canvas.add_object(class_block)  # Assurez-vous que cette méthode existe et est correcte


class AddButton(ClickableObject):
    def __init__(self, canvas, posX, posY, color, size = 70, radius=10, cross_color = "white", border_color="black", cross_size = 0.7, border_width=5, z_index=10):
        super().__init__(canvas, posX, posY, size, size, color, radius, border_color, border_width, z_index)
        self.cross_color = cross_color
        self.cross_size = cross_size

    def draw(self):
        super().draw()
        # Dessine une croix en forme de plus (+)
        arm_length = min(self.sizeX, self.sizeY) * self.cross_size / 2  # Longueur de chaque bras de la croix
        center_x = self.posX + self.sizeX / 2
        center_y = self.posY + self.sizeY / 2

        # Dessiner les bras horizontaux de la croix
        self.canvas.create_line(center_x - arm_length, center_y, center_x + arm_length, center_y, fill=self.cross_color, width=self.border_width)

        # Dessiner les bras verticaux de la croix
        self.canvas.create_line(center_x, center_y - arm_length, center_x, center_y + arm_length, fill=self.cross_color, width=self.border_width)

    def on_click(self):
        super().on_click()
        create_agent(self.canvas)

class PlayButton(ClickableObject):
    def __init__(self, canvas, posX, posY, color="green", size=70, radius=10, triangle_color="white", border_color="black", border_width=5, z_index=10):
        super().__init__(canvas, posX, posY, size, size, color, radius, border_color, border_width, z_index)
        self.triangle_color = triangle_color

    def draw(self):
        super().draw()
        # Calculer les points pour le triangle
        center_x = self.posX + self.sizeX / 2
        center_y = self.posY + self.sizeY / 2
        triangle_size = min(self.sizeX, self.sizeY) * 0.6  # Taille du triangle basée sur la taille du bouton

        # Points du triangle (pointe vers la droite)
        points = [
            (center_x - triangle_size / 2, center_y - triangle_size / 2),  # Point haut gauche
            (center_x - triangle_size / 2, center_y + triangle_size / 2),  # Point bas gauche
            (center_x + triangle_size / 2, center_y)  # Pointe du triangle
        ]

        # Dessiner le triangle
        self.canvas.create_polygon(points, fill=self.triangle_color, outline=self.triangle_color)

    def on_click(self):
        super().on_click()
        # Ici, vous pouvez ajouter la logique à exécuter lorsque le bouton est cliqué, comme démarrer une action

class MainCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.config(bg="white")  # Définit la couleur de fond du canvas
        self.BlocksList = []
        self.LinkList = []
        self.add_button = AddButton(self, 10, 90, color="grey")
        self.play_button = PlayButton(self, 10, 10)
        self.is_button1_down = False
        self.current_target = None
        self.last_mouse_pos = (0,0)

        self.refresh()
        self.add_object(self.add_button)
        self.add_object(self.play_button)
        self.bind("<Button-1>", self.on_button1_down)
        self.bind("<Button-3>", self.on_button3_down)
        self.bind("<B1-Motion>", self.on_drag_move)
        self.bind("<ButtonRelease-1>", self.on_button1_up)

    def delete_object(self, obj):
        self.BlocksList.remove(obj)
        self.refresh()

    def on_button1_down(self, event):
        self.is_button1_down = True
        # print("button down", self.is_button1_down)
        self.current_target = self.check_click(event.x, event.y)

        self.last_mouse_pos = (event.x, event.y)

    def on_button3_down(self, event):
        self.current_target = self.check_click(event.x, event.y, "right")

    def on_drag_move(self, event):
        # Calculer le déplacement depuis la dernière position de la souris
        deltaX = event.x - self.last_mouse_pos[0]
        deltaY = event.y - self.last_mouse_pos[1]
        self.last_mouse_pos = (event.x, event.y)  # Mise à jour de la dernière position de la souris

        # Aucun objet cible actuellement sélectionné
        if self.current_target is None:
            if not self.BlocksList:  # Vérifier si BlocksList est None ou vide
                return
            # Déplacer tous les blocs non statiques
            for block in self.BlocksList:
                if not block.IsStatic:
                    targetX, targetY = block.getPosition()
                    block.move(targetX + deltaX, targetY + deltaY)

        else:
            # Vérifier si le curseur est toujours dans le canvas
            if not self.IsInCanvas(event.x, event.y):
                return

            # Traitement spécifique si la cible actuelle est un Node et non une entrée
            if isinstance(self.current_target, Node) and not self.current_target.IsInput:
                self.refresh()  # Rafraîchir l'affichage pour nettoyer la ligne précédente si nécessaire
                # Calculer la position de départ de la ligne à partir du Node
                X = self.current_target.posX + self.current_target.sizeX / 2
                Y = self.current_target.posY + self.current_target.sizeY / 2
                # Dessiner une ligne temporaire entre le Node et la position actuelle de la souris
                self.create_line(X, Y, event.x, event.y, fill="black", width=self.current_target.sizeY // 2, arrow=tk.LAST, tags="arrow_line")

                # Vérifier si la souris est sur un autre Node qui pourrait être connecté
                second_node = self.check_click(event.x, event.y)
                if isinstance(second_node, Node) and self.current_target != second_node and second_node.IsInput:
                    # Créer un nouveau lien si un second Node valide est trouvé
                    new_link = Link(self, self.current_target, second_node, width=self.current_target.sizeY // 2)
                    self.add_object(new_link)  # Ajouter le nouveau lien au canvas
                    print(self.BlocksList)
                    self.current_target = None  # Réinitialiser la cible actuelle

            else:
                # Déplacer la cible actuelle si elle n'est pas statique
                if not self.current_target.IsStatic:
                    targetX, targetY = self.current_target.getPosition()
                    self.current_target.move(targetX + deltaX, targetY + deltaY)
                    self.refresh()  # Rafraîchir l'affichage après le déplacement

    def on_button1_up(self, event):
        self.is_button1_down = False
        # print("button down", self.is_button1_down)
        self.refresh()

    def IsInCanvas(self, mouse_x, mouse_y):
        self.width = self.winfo_width()
        self.height = self.winfo_height()

        IsIn = 0 <= mouse_x <= self.width and 0 <= mouse_y <= self.height
        # print(IsIn, mouse_x, self.width, mouse_y, self.height)
        return IsIn

    def add_object(self, obj):
        # Ajoute l'objet à la liste
        self.BlocksList.append(obj)
        # Dessine l'objet
        self.refresh()

    def refresh(self):
        self.delete("all")  # Efface tous les dessins sur le canvas avant de redessiner

        if self.BlocksList is None or len(self.BlocksList) == 0:
            return

        # Utilisez sorted() pour obtenir une nouvelle liste triée sans modifier l'originale
        for block in sorted(self.BlocksList, key=lambda x: x.z_index):
            if isinstance(block, Link):
                print(block)
            block.draw()

    def check_click(self, x, y, clic_type = "left"):

        if (self.BlocksList == None or len(self.BlocksList) == 0):
            return

        # Liste des objets cliqués
        clicked_objects = [block for block in self.BlocksList if block.is_inside(x, y)]

        # Trié les éléments par leur z_index
        clicked_objects = sorted(clicked_objects, key=lambda x: x.z_index)

        # Activer le clic (ou gérer l'événement de clic) pour l'objet le plus en haut
        IsActive = False
        i = len(clicked_objects)
        target = None
        while i > 0 and not IsActive:
            i -= 1
            try:
                target = clicked_objects[i]
                if clic_type == "left":
                    target.on_click()
                elif clic_type == "right":
                    target.on_click_right()
                IsActive = True
            except Exception as e:
                print(f"Erreur lors de l'appel de on_click: {e}")
                


        return target

# Création de la fenêtre principale et ajout du canvas
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Canvas Principal")
    root.geometry("400x300")

    canvas = MainCanvas(root)
    canvas.pack(fill="both", expand=True)  # Fait en sorte que le canvas remplisse la fenêtre parent

    root.mainloop()
