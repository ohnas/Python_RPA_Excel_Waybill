from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox

from single_check import single_table_check
from single_insert import single_table_isert


def check_list():
    new_items_list = single_table_check()
    if len(new_items_list) == 0:
        msgbox.showinfo("알림", "새로운 항목이 없습니다.")
    else:
        for item in new_items_list:
            list_file.insert(END, item)


def move_button():
    selection_item = list_file.curselection()
    selection_item_list = list(list_file.get(selection_item[0]))
    label_product_name.insert(0, selection_item_list[0])
    label_quantity_name.insert(0, selection_item_list[1])
    list_file.delete(selection_item)


def save_button():
    selection_product = label_product_name.get()
    selection_quantity = int(label_quantity_name.get())
    selection_type = combobox_type.get()
    selection_price = int(combobox_price.get())
    selection_item = []
    selection_item.append(selection_product)
    selection_item.append(selection_quantity)
    selection_item.append(selection_type)
    selection_item.append(selection_price)
    selection_items = tuple(selection_item)
    single_table_isert(selection_items)


window = Tk()
window.title("Tkinte_Test")
window.geometry("1080x640")
window.resizable(True, True)

select_frame = Frame(window)
select_frame.pack(fill="x")

############ check_list btn ################
check_file_button = Button(
    select_frame,
    overrelief="solid",
    text="스마트스토어 단품 체크",
    width=20,
    height=2,
    padx=2,
    pady=2,
    command=check_list,
)
check_file_button.pack(side="left")
############################################
############ list box #####################
list_frame = LabelFrame(window, text="단품 항목", padx=5, pady=5)
list_frame.pack(fill="both")

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

list_file = Listbox(
    list_frame, selectmode="extended", height=7, yscrollcommand=scrollbar.set
)
list_file.pack(side="left", fill="both", expand=True)
scrollbar.config(command=list_file.yview)

move_btn = Button(
    list_frame,
    overrelief="solid",
    text="선택",
    width=5,
    height=2,
    padx=2,
    pady=2,
    command=move_button,
)
move_btn.pack(side="bottom")
############################################
############ select_option #################
frame_option = LabelFrame(window, text="선택항목")
frame_option.pack(padx=5, pady=5, fill="both")

save_btn = Button(
    frame_option,
    overrelief="solid",
    text="저장",
    width=10,
    height=2,
    padx=2,
    pady=2,
    command=save_button,
)
save_btn.pack(side="right")

label_product = Label(frame_option, text="품목명 :")
label_product.pack(side="left", padx=5, pady=5)
label_product_name = Entry(frame_option, width=60)
label_product_name.pack(side="left", padx=5, pady=5)

label_quantity = Label(frame_option, text="수량 :")
label_quantity.pack(side="left", padx=5, pady=5)
label_quantity_name = Entry(frame_option, width=5)
label_quantity_name.pack(side="left", padx=5, pady=5)

label_type = Label(frame_option, text="박스타입 :")
label_type.pack(side="left", padx=5, pady=5)
option_type = ["극소", "소", "중", "대", "이형"]
combobox_type = ttk.Combobox(frame_option, state="readonly", values=option_type)
combobox_type.pack(side="left", padx=5, pady=5)

label_price = Label(frame_option, text="기본운임 :")
label_price.pack(side="left", padx=5, pady=5)
option_price = [2050, 2050, 2050, 2050, 2050]
combobox_price = ttk.Combobox(frame_option, state="readonly", values=option_price)
combobox_price.pack(side="left", padx=5, pady=5)
############################################
window.mainloop()
