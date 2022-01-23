from test import save_file
import tkinter

window = tkinter.Tk()
window.title("Tkinte_Test")
window.geometry("640x400")
window.resizable(True, True)

label = tkinter.Label(window, text="hello world !!")
label.pack()

button = tkinter.Button(window, text="저장", command=save_file)
button.pack()

window.mainloop()
