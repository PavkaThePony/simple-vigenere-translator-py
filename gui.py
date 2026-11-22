import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from cipher_impl import vigenere

# onbuttonclick funcs
def onEncode():
  handle_vigenere("encrypt")

def onDecode():
  handle_vigenere("decrypt")

def importText():
  filetypes = (("Text files", "*.txt"), ("All files", "*.*"))
  filename = fd.askopenfilename(title="choose a file", initialdir="~/", filetypes=filetypes)
  if not filename: return
  with open(filename, "r", encoding="utf-8") as file:
    contents = file.read()
  translation_box.delete("1.0", "end")
  translation_box.insert("1.0", contents)

def importKey():
  filetypes = (("Key text files", "*.key"), ("Text files", "*.txt"), ("All files", "*.*"))
  filename = fd.askopenfilename(title="choose a file", initialdir="~/", filetypes=filetypes)
  if not filename: return
  with open(filename, "r", encoding="utf-8") as file:
    contents = file.read()
  contents = contents.replace("\n", "").replace("\r", "").upper()
  key_entry_var.set(value=contents)

def exportFile():
  filename = fd.asksaveasfilename(title="export file", initialdir="~/", defaultextension=".txt")
  if not filename: return
  with open(filename, "w", encoding="utf-8") as file:
    file.write(output_box.get("1.0", "end-1c"))

root = tk.Tk()
root.title("Simple Vigenere Translator")
root.geometry("1200x600")
root.minsize(400, 300)
root.resizable(True, True)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, sticky="nsew")

translator_frame = ttk.Frame(notebook)
settings_frame   = ttk.Frame(notebook)
license_frame    = ttk.Frame(notebook)

notebook.add(translator_frame, text="Translator")
notebook.add(settings_frame, text="Settings")
notebook.add(license_frame, text="License")

#configure le frames
translator_frame.columnconfigure(0, weight=1)
translator_frame.columnconfigure(1, weight=0)
translator_frame.columnconfigure(2, weight=0)
translator_frame.rowconfigure(0,    weight=0)
translator_frame.rowconfigure(1,    weight=1)
translator_frame.rowconfigure(2,    weight=0)
translator_frame.rowconfigure(3,    weight=0)
translator_frame.rowconfigure(4,    weight=0)
translator_frame.rowconfigure(5,    weight=1)

# DO NOT USE settings_frame.rowconfigure() ! It messes the rows in settings
settings_frame.columnconfigure(0, weight=1)

license_frame.columnconfigure(0, weight=1)
license_frame.rowconfigure(0, weight=1)

# items inside of the translator_frame
text_label = ttk.Label(translator_frame, text="Your text")
text_label.grid(row=0, column=0, sticky="sw")

import_text_btn = ttk.Button(translator_frame, text="Import text", command=importText)
import_text_btn.grid(row=1, column=1, sticky="ne")

translation_box = tk.Text(translator_frame, font=("TkDefaultFont", 16), wrap="word")
translation_box.grid(row=1, column=0, sticky="new")

encode_btn = ttk.Button(translator_frame, text="Encode", command=onEncode)
encode_btn.grid(row=1, column=1, sticky="sew")

decode_btn = ttk.Button(translator_frame, text="Decode", command=onDecode)
decode_btn.grid(row=1, column=2, sticky="sew")

keyword_lable = ttk.Label(translator_frame, text="Key")
keyword_lable.grid(row=2, column=0, sticky="nw")

import_key_btn = ttk.Button(translator_frame, text="Import key", command=importKey)
import_key_btn.grid(row=3, column=1, sticky="w")

key_entry_var = tk.StringVar(value="")
keyword_line = ttk.Entry(translator_frame, font=("TkDefaultFont", 16), textvariable=key_entry_var)
keyword_line.grid(row=3, column=0, sticky="new")

output_label = ttk.Label(translator_frame, text="Output")
output_label.grid(row=4, column=0, sticky="sw")

output_box = tk.Text(translator_frame, font=("TkDefaultFont", 16), wrap="word")
output_box.grid(row=5, column=0, sticky="new")

export_btn = ttk.Button(translator_frame, text="Export", command=exportFile)
export_btn.grid(row=5, column=1, sticky="se")

# items inside of settings_frame
non_alphabetic_char_handling_labelframe = ttk.Labelframe(settings_frame, text="Non-Alphabetic Character Handling", padding=10)
non_alphabetic_char_handling_labelframe.grid(row=0, column=0, sticky="new")

nach_var = tk.StringVar(value="ignore")

ttk.Radiobutton(
    non_alphabetic_char_handling_labelframe, 
    text="Ignore (Leave any non-alphabetic characters as they are in the output and do not advance the key on them) (Default)",
    variable=nach_var,
    value="ignore",

    ).grid(row=0, column=0, sticky="w")
ttk.Radiobutton(
    non_alphabetic_char_handling_labelframe,
    text="Strip (Delete all non-alphabetics from the text)",
    variable=nach_var,
    value="strip",
    ).grid(row=1, column=0, sticky="w")

case_sensitivity_labelframe = ttk.Labelframe(settings_frame, text="Case Sensitivity", padding=10)
case_sensitivity_labelframe.grid(row=1, column=0, sticky="new")

cs_var = tk.StringVar(value="preserve")

ttk.Radiobutton(
    case_sensitivity_labelframe,
    text="Preserve (Keep same case in output as it was in input) (Default)",
    variable=cs_var,
    value="preserve",
    ).grid(row=0, column=0, sticky="w")
ttk.Radiobutton(
    case_sensitivity_labelframe,
    text="Force Uppercase (Make output all uppercase)",
    variable=cs_var,
    value="uppercase",
    ).grid(row=1, column=0, sticky="w")
ttk.Radiobutton(
    case_sensitivity_labelframe,
    text="Force Lowercase (Make output all lowercase)",
    variable=cs_var,
    value="lowercase",
    ).grid(row=2, column=0, sticky="w")

key_behaviour_labelframe = ttk.Labelframe(settings_frame, text="Key behaviour", padding=10)
key_behaviour_labelframe.grid(row=2, column=0, sticky="new")

kbeh_var = tk.StringVar(value="repeat")

ttk.Radiobutton(
    key_behaviour_labelframe,
    text="Repeat (Cycles the same key) (Default)",
    variable=kbeh_var,
    value="repeat",
    ).grid(row=0, column=0, sticky="w")

ttk.Radiobutton(
    key_behaviour_labelframe,
    text="Random (Ignore user's input to the key, generate the key with secrets module)\nThe key will have the length of the input string, making it impossible to decipher if you never reuse it\nNote: the generated key will be appended to output file at the end",
    variable=kbeh_var,
    value="random",
    ).grid(row=1, column=0, sticky="w")

language_labelframe = ttk.Labelframe(settings_frame, text="Target Language", padding=10)
language_labelframe.grid(row=3, column=0, sticky="new")

lang_var = tk.StringVar(value="en")

ttk.Radiobutton(
    language_labelframe,
    text="English",
    variable=lang_var,
    value="en"
    ).grid(row=0, column=0, sticky="w")

ttk.Radiobutton(
    language_labelframe,
    text="Russian",
    variable=lang_var,
    value="ru"
    ).grid(row=1, column=0, sticky="w")

# items inside license_frame
license_labelframe = ttk.LabelFrame(license_frame, text="License", padding=10)
license_labelframe.grid(row=0, column=0, sticky="nsew")

license_contents="""MIT License

Copyright (c) 2026 Pavka

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
license_label = ttk.Label(license_labelframe, text=license_contents)
license_label.grid(row=0, column=0, sticky="ew")

# functions to glue gui with logic

def handle_vigenere(action: str):
  lang = lang_var.get()
  kbeh = kbeh_var.get()
  nach = True if nach_var.get() == "strip" else False
  cs = cs_var.get()
  text = translation_box.get("1.0", "end-1c")

  if kbeh == "repeat":
    key = keyword_line.get()
  elif kbeh == "random" and action == "decrypt":
    key = keyword_line.get()
  else:
    key = "NONE"

  encrypted_str, actual_key = vigenere(text, key, action, lang, cs, nach, kbeh)

  if kbeh == "random" and action == "encrypt":
    encrypted_str = encrypted_str + "\n\n[KEY USED] " + actual_key

  print_to_output(encrypted_str)

def print_to_output(text_to_print: str):
  output_box.delete("1.0", "end")
  output_box.insert("1.0", text_to_print)

root.mainloop()

