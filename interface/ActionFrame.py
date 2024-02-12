import tkinter as tk
from tkinter import ttk, scrolledtext
from interface.ListFrame import ListDisplayFrame

class MainFunctionEditor(tk.Frame):
    def __init__(self, parent, functions, **kwargs):
        super().__init__(parent, **kwargs)
        self.functions = functions

        # Création du ListDisplayFrame pour la liste des fonctions
        self.list_frame = ListDisplayFrame(self, functions, title="Fonctions", on_select=self.on_function_select)
        self.list_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False)

        # Création du FunctionEditor pour l'édition des fonctions
        self.editor_frame = FunctionEditor(self, on_submit=self.add_function)
        self.editor_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def on_function_select(self, function):
        # Mettre à jour l'éditeur avec les détails de la fonction sélectionnée
        self.editor_frame.function_name.delete(0, tk.END)
        self.editor_frame.function_name.insert(0, getattr(function, 'name', ''))
        self.editor_frame.function_description.delete(0, tk.END)
        self.editor_frame.function_description.insert(0, getattr(function, 'description', ''))

    def add_function(self, name, description):
        # Créer une nouvelle instance de Function et l'ajouter à la liste
        new_function = Function(name, description)
        self.list_frame.add_object(new_function)

# Exemple de liste de fonctions (ici, simplement représentées par des objets)
class Function:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description

class ParameterFrame(tk.Frame):
    def __init__(self, parent, remove_callback, **kwargs):
        super().__init__(parent, **kwargs)
        self.remove_callback = remove_callback

        # Label et champ pour le nom du paramètre
        ttk.Label(self, text="Nom :").grid(row=0, column=0, sticky="w", padx=2, pady=2)
        self.param_name = ttk.Entry(self)
        self.param_name.grid(row=0, column=1, sticky="ew", padx=2, pady=2)
        self.grid_columnconfigure(1, weight=1)

        # Label et combobox pour le type du paramètre
        ttk.Label(self, text="Type :").grid(row=0, column=2, sticky="w", padx=2, pady=2)
        self.param_type = ttk.Combobox(self, values=["string", "number", "boolean"], width=10)  # Réduction de la largeur
        self.param_type.grid(row=0, column=3, sticky="ew", padx=2, pady=2)
        self.param_type.set("string")

        # Checkbutton pour indiquer si le paramètre est requis
        self.param_required = ttk.Checkbutton(self, text="Requis?")
        self.param_required.grid(row=0, column=4, sticky="w", padx=2, pady=2)

        # Bouton pour supprimer le paramètre
        self.remove_button = ttk.Button(self, text="Supprimer", command=self.remove_self)
        self.remove_button.grid(row=0, column=5, padx=2, pady=2)

    def remove_self(self):
        self.remove_callback(self)
        self.destroy()

class FunctionEditor(tk.Frame):
    def __init__(self, parent, on_submit=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.parameters_frames = []
        self.on_submit = on_submit
        self.is_edit_mode = False

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)  # Assure que la zone de texte du code Python s'étende

        top_frame = tk.Frame(self)
        top_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        top_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(top_frame, text="Nom de la fonction :").grid(row=0, column=0, sticky="w")
        self.function_name = ttk.Entry(top_frame)
        self.function_name.grid(row=0, column=1, sticky="ew")

        ttk.Label(top_frame, text="Description de la fonction :").grid(row=1, column=0, sticky="nw")
        self.function_description = tk.Text(top_frame, height=5)
        self.function_description.grid(row=1, column=1, sticky="ew")

        self.params_frame = tk.Frame(self)
        self.params_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.params_frame.grid_columnconfigure(0, weight=1)

        self.add_param_button = ttk.Button(self, text="Ajouter Paramètre", command=self.add_parameter)
        self.add_param_button.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

        ttk.Label(self, text="Code Python :").grid(row=3, column=0, sticky="nw", padx=5)
        self.code_area = scrolledtext.ScrolledText(self)
        self.code_area.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)

        self.submit_button = ttk.Button(self, text="Créer", command=self.submit)
        self.submit_button.grid(row=5, column=0, sticky="ew", padx=5, pady=10)

    def add_parameter(self):
        param_frame = ParameterFrame(self.params_frame, self.remove_parameter)
        param_frame.grid(row=len(self.parameters_frames), column=0, sticky="ew", padx=5, pady=2)
        self.parameters_frames.append(param_frame)
        self.params_frame.grid_rowconfigure(len(self.parameters_frames), weight=1)

    def remove_parameter(self, frame):
        if frame in self.parameters_frames:
            self.parameters_frames.remove(frame)
            frame.destroy()
            # Réorganiser les frames restantes
            for i, param_frame in enumerate(self.parameters_frames):
                param_frame.grid(row=i, column=0, sticky="ew")

    def submit(self):
        # Récupérer les données des champs d'entrée
        name = self.function_name.get()
        description = self.function_description.get("1.0", tk.END).strip()
        
        # Appeler le callback de soumission si défini
        if self.on_submit:
            self.on_submit(name, description)

    def set_mode(self, is_edit):
        self.is_edit_mode = is_edit
        self.submit_button.config(text="Modifier" if self.is_edit_mode else "Créer")
