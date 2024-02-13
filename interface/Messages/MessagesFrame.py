import tkinter as tk
from interface.Utility.ListFrame import ListDisplayFrame

class MessageFrame(tk.Frame):
    def __init__(self, parent, message):
        super().__init__(parent)
        self.message = message
        self.create_widgets()

    def create_widgets(self):
        message_label = tk.Label(self, text=self.message, wraplength=250, anchor="w", justify="left")
        message_label.pack(side="top", fill="both", expand=True)

class MainMessagesFrame(tk.Frame):
    def __init__(self, parent, conversation_list, prewritten_messages_list):
        super().__init__(parent)
        self.conversation_list = conversation_list
        self.prewritten_messages_list = prewritten_messages_list
        self.create_widgets()

    def create_widgets(self):
        # Zone de liste des conversations
        self.conversation_list_frame = ListDisplayFrame(self, self.conversation_list, title="Conversations", on_select=self.on_conversation_select)
        self.conversation_list_frame.pack(side="left", fill="y")

        # Zone principale de dialogue
        self.dialog_frame = DialogFrame(self)
        self.dialog_frame.pack(side="left", fill="both", expand=True)

        # Zone de liste des messages pré-écrits
        self.prewritten_messages_frame = ListDisplayFrame(self, self.prewritten_messages_list, title="Prewritten Messages", on_select=self.on_prewritten_message_select)
        self.prewritten_messages_frame.pack(side="left", fill="y")

    def on_conversation_select(self, conversation):
        # Logique pour gérer la sélection d'une conversation
        pass

    def on_prewritten_message_select(self, message):
        # Logique pour gérer la sélection d'un message pré-écrit
        # Par exemple, insérer le message pré-écrit dans la zone de saisie de DialogFrame
        self.dialog_frame.message_entry.delete(0, tk.END)
        self.dialog_frame.message_entry.insert(0, message)

class DialogFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.history_frame = tk.Frame(self)
        self.entry_frame = tk.Frame(self)
        self.create_widgets()
        self.layout_widgets()

    def create_widgets(self):
        # Configuration de la frame pour l'historique des messages
        self.scrollbar = tk.Scrollbar(self.history_frame)
        self.message_canvas = tk.Canvas(self.history_frame, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.message_canvas.yview)

        self.message_container = tk.Frame(self.message_canvas)
        self.message_canvas.create_window((0, 0), window=self.message_container, anchor="nw")

        # Mise à jour de la scrollregion du canvas automatiquement
        self.message_container.bind("<Configure>", lambda e: self.message_canvas.configure(scrollregion=self.message_canvas.bbox("all")))

        # Configuration de la frame pour la zone de saisie
        self.message_entry = tk.Entry(self.entry_frame)
        self.send_button = tk.Button(self.entry_frame, text="Send", command=self.send_message)

    def layout_widgets(self):
        self.history_frame.pack(side="top", fill="both", expand=True)
        self.entry_frame.pack(side="bottom", fill="x")
        self.scrollbar.pack(side="right", fill="y")
        self.message_canvas.pack(side="left", fill="both", expand=True)

        self.message_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        self.send_button.pack(side="right", padx=5, pady=5)

    def send_message(self):
        message_text = self.message_entry.get()
        if message_text:
            # Ajout du nouveau message dans l'historique
            new_message = MessageFrame(self.message_container, message_text)
            new_message.pack(side="top", fill="x", padx=5, pady=5)
            self.message_entry.delete(0, tk.END)  # Efface le contenu de la zone de saisie