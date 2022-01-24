import time
from tkinter import *
from turtle import right, width

start = time.time()

window = Tk()
window.title("Tkinte_Test")
window.geometry("1080x640")
window.resizable(True, True)

select_frame = Frame(window)
select_frame.pack(fill="x")

select_file_button = Button(
    select_frame,
    overrelief="solid",
    text="파일선택",
    width=10,
    height=3,
    padx=5,
    pady=5,
)
select_file_button.pack(side="left")

list_frame = Frame(window, padx=5, pady=5)
list_frame.pack(fill="both")

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

list_file = Listbox(
    list_frame, selectmode="extended", height=15, yscrollcommand=scrollbar.set
)
list_file.pack(side="left", fill="both", expand=True)
scrollbar.config(command=list_file.yview)


""" button = tkinter.Button(window, text="저장", command=save_file)
button.pack() """


print(time.time() - start)
window.mainloop()
