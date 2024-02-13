from collections.abc import Callable
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from interface.Notebook import CustomNotebookFrame

PADDING = 5

class OngletSelector:
    def __init__(self, frame, noms_onglets: list):
        self.frame = frame
        self.noms_onglets = noms_onglets
        self.frames = {}  # Dictionnaire pour stocker les frames par nom

        self.notebook = ttk.Notebook(frame)

        for nom_onglet in self.noms_onglets:
            frame = ttk.Frame(self.notebook)
            self.frames[nom_onglet] = frame
            self.notebook.add(frame, text=nom_onglet)

        self.notebook.pack(fill='both', expand='yes')

    def get(self, nom_onglet):
        return self.frames.get(nom_onglet)
    
class MenuBar(tk.Menu):
    def __init__(self, master, new_file_command: Callable[[], None], open_file_command: Callable[[], None]):
        super().__init__(master)
        self.new_file_command = new_file_command
        self.open_file_command = open_file_command


        # Créer le menu Fichier et ses options
        filemenu = tk.Menu(self, tearoff=0)
        filemenu.add_command(label="Nouveau Fichier", command=self.new_file_command)
        filemenu.add_command(label="Ouvrir un Fichier", command=self.open_file_command)

        # Ajouter le menu Fichier à la barre de menu
        self.add_cascade(label="Fichier", menu=filemenu)

class NewProjectPopup(tk.Toplevel):
    def __init__(self, master, OnCreate: Callable[[str, str], None]):
        super().__init__(master)
        self.OnCreate = OnCreate

        self.save_directory = None

        self.master = master
        self.title("New Project")

        # Label Name
        self.name = tk.Label(self, text="Project Name:")
        self.name.pack(pady=PADDING)

        # Champ de saisie pour le nom du projet
        self.project_name_entry = tk.Entry(self)
        self.project_name_entry.pack(pady=PADDING)

        # Label Name
        self.path = tk.Label(self, text="Directory path:")
        self.path.pack(pady=PADDING)

        # Bouton pour choisir le chemin de sauvegarde
        self.Path_But = tk.Button(self, text="Choose Directory", command=self.choose_directory)
        self.Path_But.pack(pady=PADDING)

        # Bouton pour créer le nouveau projet
        self.create = tk.Button(self, text="Create Project", command=self.create_project)
        self.create.pack(pady=PADDING)

    def choose_directory(self):
        # Ouvre une boîte de dialogue pour sélectionner le dossier de sauvegarde
        self.save_directory = filedialog.askdirectory()
        if self.save_directory == "":
            self.Path_But.config(text="Choose Directory")
        else:
            self.Path_But.config(text=self.save_directory)
        print("Save directory:", self.save_directory)

    def create_project(self):
        # Créer le projet avec le nom et le chemin de sauvegarde sélectionnés
        project_name = self.project_name_entry.get()
        if project_name == '' or project_name is None:
            messagebox.showwarning("Warning", "Project name entry is empty")
        elif self.save_directory == '' or self.save_directory is None:
            messagebox.showwarning("Warning", "Directory path entry is empty")
        else:
            print("Project name:", project_name)
            print("Save directory:", self.save_directory)
            # Affiche une erreur si le dossier n'a pas pu être créé
            if os.path.exists(self.save_directory):
                # Afficher une popup avec un message de warning
                messagebox.showwarning("Warning", "Folder already exists !")
            else:
                self.OnCreate(self.save_directory, project_name)  # Appelle le callback avec le chemin du projet
                self.destroy()

class MainWin(tk.Tk):
    def __init__(self, kernel):
        super().__init__()

        self.kernel = kernel

        self.title("Graph GPT")
        self.geometry("800x800")

        # la fenêtre principale est elle affichée
        self.main_hidden = True

        # Créer la barre de menu
        menubar = MenuBar(self, self.new_file, self.open_file)

        # Associer la barre de menu à la fenêtre principale
        self.config(menu=menubar)

        # Création du label pour afficher le chemain du projet
        self.path_label = ttk.Label(self, text=self.kernel.get_data(), anchor="w", justify="left")        
        
        # Create main frame
        self.mainframe = CustomNotebookFrame(self)
        self.show_main()
        
    def show_main(self):
        if self.kernel.get_data() != '' and self.kernel.get_data() != None:
            self.path_label.config(text = self.kernel.get_data())
            if self.main_hidden :
                self.path_label.pack(fill=tk.X, padx=PADDING, pady=PADDING)
                self.mainframe.pack(fill=tk.BOTH, expand = True)
                self.main_hidden = False
        
    def new_file(self):
        def on_create_callback(path, name):
            print(f"Callback: New project created at {path}")
            self.kernel.new_project(path, name)

        popup = NewProjectPopup(self, on_create_callback)
        self.wait_window(popup)
        self.show_main()

    def open_file(self):
        directory = filedialog.askdirectory()
        if directory != '' and directory != None:
            print(f"Ouverture du fichier : {directory}")
            self.kernel.save_data(directory)
            self.show_main()

    def run(self):
        self.mainloop()

def main():
    win = MainWin()
    win.run()

if __name__ == "__main__":
    main()
