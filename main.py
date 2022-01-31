from Monster.single_check import single_table_check

from tkinter import *
from turtle import right, width

from click import command


def check_list():
    new_items_list = single_table_check()
    if len(new_items_list) == 0:
        print("새로운 항목이 없습니다.")
    else:
        for item in new_items_list:
            list_file.insert(END, item)


window = Tk()
window.title("Tkinte_Test")
window.geometry("1080x640")
window.resizable(True, True)

select_frame = Frame(window)
select_frame.pack(fill="x")

check_file_button = Button(
    select_frame,
    overrelief="solid",
    text="파일체크",
    width=10,
    height=3,
    padx=5,
    pady=5,
    command=check_list,
)
check_file_button.pack(side="left")

list_frame = Frame(window, padx=5, pady=5)
list_frame.pack(fill="both")

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

list_file = Listbox(
    list_frame, selectmode="extended", height=10, yscrollcommand=scrollbar.set
)
list_file.pack(side="left", fill="both", expand=True)
scrollbar.config(command=list_file.yview)


window.mainloop()
