import tkinter as tk
from tkinter import ttk, scrolledtext
from interface.Utility.ListFrame import ListDisplayFrame

class MainAgentEditor(tk.Frame):
    def __init__(self, parent, functions, **kwargs):
        super().__init__(parent, **kwargs)
        self.functions = functions

        # Création du ListDisplayFrame pour la liste des fonctions
        self.list_frame = ListDisplayFrame(self, functions, title="Agents", on_select=self.on_function_select)
        self.list_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False)

        # Création du AgentEditor pour l'édition des agents
        self.editor_frame = AgentEditor(self, on_submit=self.add_function)
        self.editor_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def add_function(self, name, description):
        # Créer une nouvelle instance d'agent et l'ajouter à la liste
        new_function = Agent(name, description)
        self.list_frame.add_object(new_function)

    def on_function_select(self, function):
        # Mettre à jour l'éditeur avec les détails de la fonction sélectionnée
        self.editor_frame.function_name.delete(0, tk.END)
        self.editor_frame.function_name.insert(0, getattr(function, 'name', ''))
        self.editor_frame.function_description.delete(0, tk.END)
        self.editor_frame.function_description.insert(0, getattr(function, 'description', ''))

class Agent:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description

class AgentEditor(tk.Frame):
    def __init__(self, parent, on_submit=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.on_submit = on_submit
        self.is_edit_mode = False

        # Nom de l'agent
        ttk.Label(self, text="Nom de l'agent :").grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.entree_nom = ttk.Entry(self)
        self.entree_nom.grid(column=1, row=0, sticky=tk.EW, padx=5, pady=5)

        # Description de l'agent
        ttk.Label(self, text="Description de l'agent :").grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
        self.entree_description = ttk.Entry(self)
        self.entree_description.grid(column=1, row=1, sticky=tk.EW, padx=5, pady=5)

        # Model
        ttk.Label(self, text="Model :").grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
        self.entree_model = ttk.Entry(self)
        self.entree_model.grid(column=1, row=2, sticky=tk.EW, padx=5, pady=5)

        # Best of
        ttk.Label(self, text="Best of :").grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)
        self.entree_best_of = ttk.Entry(self)
        self.entree_best_of.grid(column=1, row=4, sticky=tk.EW, padx=5, pady=5)

        # Temperature
        ttk.Label(self, text="Temperature :").grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)
        self.entree_temperature = ttk.Entry(self)
        self.entree_temperature.grid(column=1, row=5, sticky=tk.EW, padx=5, pady=5)

        # Max Tokens
        ttk.Label(self, text="Max Tokens :").grid(column=0, row=6, sticky=tk.W, padx=5, pady=5)
        self.entree_max_tokens = ttk.Entry(self)
        self.entree_max_tokens.grid(column=1, row=6, sticky=tk.EW, padx=5, pady=5)

        # frequency_penalty

        # logit_bias

        # logprobs

        # top_logprobs

        # n (nombre de version)

        # presence_penalty

        # response_format

        # seed

        # stop

        # stream

        # top_p

        # tools

        # tool_choice

        # user

        # function_call

        # functions

        # message

        # Bouton de création
        self.bouton_creer = ttk.Button(self, text="Créer l'Agent", command=self.creer_agent)
        self.bouton_creer.grid(column=1, row=7, sticky=tk.E, padx=5, pady=20)

    def creer_agent(self):
        # Récupération des valeurs des champs
        nom_agent = self.entree_nom.get()
        description_agent = self.entree_description.get()
        model = self.entree_model.get()
        best_of = self.entree_best_of.get()
        temperature = self.entree_temperature.get()
        max_tokens = self.entree_max_tokens.get()

        # Ici, ajoutez le code pour créer l'agent ChatGPT avec les informations saisies
        print(f"Création de l'agent: {nom_agent}\nDescription: {description_agent}\nModel: {model}\nPrompt: {prompt}\nBest of: {best_of}\nTemperature: {temperature}\nMax Tokens: {max_tokens}")

        # Réinitialiser les champs après création
        self.entree_nom.delete(0, tk.END)
        self.entree_description.delete(0, tk.END)
        self.entree_model.delete(0, tk.END)
        self.entree_best_of.delete(0, tk.END)
        self.entree_temperature.delete(0, tk.END)
        self.entree_max_tokens.delete(0, tk.END)

"""
https://platform.openai.com/docs/api-reference/completions/create#completions/object-system_fingerprint

model
string
Required

ID of the model to use. You can use the List models API to see all of your available models, or see our Model overview for descriptions of them.
prompt
string or array
Required

The prompt(s) to generate completions for, encoded as a string, array of strings, array of tokens, or array of token arrays.

Note that <|endoftext|> is the document separator that the model sees during training, so if a prompt is not specified the model will generate as if from the beginning of a new document.
best_of
integer or null
Optional
Defaults to 1

Generates best_of completions server-side and returns the "best" (the one with the highest log probability per token). Results cannot be streamed.

When used with n, best_of controls the number of candidate completions and n specifies how many to return – best_of must be greater than n.

Note: Because this parameter generates many completions, it can quickly consume your token quota. Use carefully and ensure that you have reasonable settings for max_tokens and stop.
echo
boolean or null
Optional
Defaults to false

Echo back the prompt in addition to the completion
frequency_penalty
number or null
Optional
Defaults to 0

Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.

See more information about frequency and presence penalties.
logit_bias
map
Optional
Defaults to null

Modify the likelihood of specified tokens appearing in the completion.

Accepts a JSON object that maps tokens (specified by their token ID in the GPT tokenizer) to an associated bias value from -100 to 100. You can use this tokenizer tool to convert text to token IDs. Mathematically, the bias is added to the logits generated by the model prior to sampling. The exact effect will vary per model, but values between -1 and 1 should decrease or increase likelihood of selection; values like -100 or 100 should result in a ban or exclusive selection of the relevant token.

As an example, you can pass {"50256": -100} to prevent the <|endoftext|> token from being generated.
logprobs
integer or null
Optional
Defaults to null

Include the log probabilities on the logprobs most likely output tokens, as well the chosen tokens. For example, if logprobs is 5, the API will return a list of the 5 most likely tokens. The API will always return the logprob of the sampled token, so there may be up to logprobs+1 elements in the response.

The maximum value for logprobs is 5.
max_tokens
integer or null
Optional
Defaults to 16

The maximum number of tokens that can be generated in the completion.

The token count of your prompt plus max_tokens cannot exceed the model's context length. Example Python code for counting tokens.
n
integer or null
Optional
Defaults to 1

How many completions to generate for each prompt.

Note: Because this parameter generates many completions, it can quickly consume your token quota. Use carefully and ensure that you have reasonable settings for max_tokens and stop.
presence_penalty
number or null
Optional
Defaults to 0

Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.

See more information about frequency and presence penalties.
seed
integer or null
Optional

If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result.

Determinism is not guaranteed, and you should refer to the system_fingerprint response parameter to monitor changes in the backend.
stop
string / array / null
Optional
Defaults to null

Up to 4 sequences where the API will stop generating further tokens. The returned text will not contain the stop sequence.
stream
boolean or null
Optional
Defaults to false

Whether to stream back partial progress. If set, tokens will be sent as data-only server-sent events as they become available, with the stream terminated by a data: [DONE] message. Example Python code.
suffix
string or null
Optional
Defaults to null

The suffix that comes after a completion of inserted text.
temperature
number or null
Optional
Defaults to 1

What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.

We generally recommend altering this or top_p but not both.
top_p
number or null
Optional
Defaults to 1

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or temperature but not both.
user
string
Optional

A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse. Learn more.

"""