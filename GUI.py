from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox

from single_check import single_table_check
from single_insert import single_table_isert


def is_single_new_item_check():
    new_items_list = single_table_check()  # single_table_check 함수에서 return 값 받아옴
    # 받아온 리스트에 항목이 없으면 메시지 띄우기 항목이 있으면 리스트 박스에 표시하기
    if len(new_items_list) == 0:
        msgbox.showinfo("알림", "새로운 항목이 없습니다.")
    else:
        for item in new_items_list:
            list_file.insert(END, item)


def move_button():
    selection_item = (
        list_file.curselection()
    )  # 리스트 박스에서 선택한 아이템 선택 method는 curselection
    selection_item_list = list(
        list_file.get(selection_item[0])
    )  # 선택한 항목의 값으 get() 하고 list로 변환
    label_product_name.insert(0, selection_item_list[0])  # 리스트에서 품목명은 품목명 Entry 로 보내기
    label_quantity_name.insert(0, selection_item_list[1])  # 리스트에서 수량은 수량 Entry 로 보내기
    list_file.delete(selection_item)  # 보내기가 완료되었다면 선택했었던 항목은 지워버리기


def save_button():
    selection_product = label_product_name.get()  # 보낸 품목명의 값을 가져오기 get()
    selection_quantity = int(label_quantity_name.get())  # 보낸 수량의 값을 가져오기 get()
    selection_type = combobox_type.get()  # combobox에서 고른 값 가져오기 get()
    selection_price = int(combobox_price.get())  # combobox에서 고른 값 가져오기 get()
    selection_item = []
    selection_item.append(selection_product)  # get 한 값들 빈 리스트에 append
    selection_item.append(selection_quantity)  # get 한 값들 빈 리스트에 append
    selection_item.append(selection_type)  # get 한 값들 빈 리스트에 append
    selection_item.append(selection_price)  # get 한 값들 빈 리스트에 append
    selection_items = tuple(
        selection_item
    )  # 리스트 값들 전부 tuple로 변환(데이터 베이스로 insert 하기 위해서)
    single_table_isert(selection_items)  # 변환시킨 tuple을 single_table_insert 함수의 인자로 보내기
    label_product_name.delete(0, END)  # 표시되어 있는 품목명 delete
    label_quantity_name.delete(0, END)  # 표시되어 있는 수량 delete
    combobox_type.current(0)  # 표시되어 있는 combobox 항목 초기화
    combobox_price.current(0)  # 표시되어 있는 combobox 항목 초기화


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
    command=is_single_new_item_check,
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
option_type = ["선택", "극소", "소", "중", "대", "이형"]
combobox_type = ttk.Combobox(frame_option, state="readonly", values=option_type)
combobox_type.current(0)
combobox_type.pack(side="left", padx=5, pady=5)

label_price = Label(frame_option, text="기본운임 :")
label_price.pack(side="left", padx=5, pady=5)
option_price = ["선택", 2050, 2050, 2050, 2050, 2050]
combobox_price = ttk.Combobox(frame_option, state="readonly", values=option_price)
combobox_price.current(0)
combobox_price.pack(side="left", padx=5, pady=5)
############################################
window.mainloop()
