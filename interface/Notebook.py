import tkinter as tk
from tkinter import ttk
from interface.Fonction.ActionFrame import MainFunctionEditor
from interface.Agent.CreateAgent import MainAgentEditor
from interface.Messages.MessagesFrame import MainMessagesFrame
from interface.BlocksCanvas.GraphFrame import MainCanvas


class CustomNotebookFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Create the notebook
        notebook = ttk.Notebook(self)

        # Create the frames for each tab
        tab_function = MainFunctionEditor(notebook, [])
        tab_agent = MainAgentEditor(notebook, [])
        tab_messages = MainMessagesFrame(notebook, [], [])
        tab_custom_graph = MainCanvas(notebook)

        # Add tabs to the notebook with a label
        notebook.add(tab_function, text='Action')
        notebook.add(tab_agent, text='Agent')
        notebook.add(tab_messages, text='Messages')
        notebook.add(tab_custom_graph, text='Custom Graph')

        # Pack the notebook into the CustomNotebookFrame
        notebook.pack(expand=True, fill='both')