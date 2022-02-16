from tkinter import *
from tkinter import filedialog
from tkinter import ttk as ttk
from tkinter import messagebox as msgbox

from smartstore_single_check import single_table_check
from smartstore_single_insert import single_table_isert
from smartstore_multi_check import multi_table_check
from smartstore_multi_insert import multi_table_isert
from smartstore_sample_save import sample_save
from smartstore_waybill_save import waybill_save


class Smartstore:
    def excel_file_path_change(self):
        # self.folder_selcted = filedialog.askdirectory()
        pass

    def excel_file_add(self):
        self.filename = filedialog.askopenfilename(
            title="스마트스토어 파일을 선택하세요",
            filetypes=(("EXCEL 파일", "*.xlsx"), ("모든파일", "*.*")),
            initialdir="C:\\Users\\오나성\\Desktop\\Python_RPA_Excel_Waybill",
        )
        file_label_name.insert(0, self.filename)

    def is_single_new_item_check(self):
        self.filename = file_label_name.get()
        new_items_list = single_table_check(
            self.filename
        )  # single_table_check 함수에서 return 값 받아옴
        # 받아온 리스트에 항목이 없으면 메시지 띄우기 항목이 있으면 리스트 박스에 표시하기
        if len(new_items_list) == 0:
            msgbox.showinfo("알림", "새로운 항목이 없습니다.")
        else:
            for item in new_items_list:
                single_list.insert(END, item)

    def single_move_button(self):
        self.selection_item = (
            single_list.curselection()
        )  # 리스트 박스에서 선택한 아이템 선택 method는 curselection
        selection_item_list = list(
            single_list.get(self.selection_item[0])
        )  # 선택한 항목의 값으 get() 하고 list로 변환
        single_label_product_name.insert(
            0, selection_item_list[0]
        )  # 리스트에서 품목명은 품목명 Entry 로 보내기
        single_label_quantity_name.insert(
            0, selection_item_list[1]
        )  # 리스트에서 수량은 수량 Entry 로 보내기
        single_list.delete(self.selection_item)  # 보내기가 완료되었다면 선택했었던 항목은 지워버리기

    def single_save_button(self):
        self.selection_product = (
            single_label_product_name.get()
        )  # 보낸 품목명의 값을 가져오기 get()
        self.selection_quantity = int(
            single_label_quantity_name.get()
        )  # 보낸 수량의 값을 가져오기 get()
        self.selection_type = single_combobox_type.get()  # combobox에서 고른 값 가져오기 get()
        self.selection_price = int(
            single_combobox_price.get()
        )  # combobox에서 고른 값 가져오기 get()
        selection_item = []
        selection_item.append(self.selection_product)  # get 한 값들 빈 리스트에 append
        selection_item.append(self.selection_quantity)  # get 한 값들 빈 리스트에 append
        selection_item.append(self.selection_type)  # get 한 값들 빈 리스트에 append
        selection_item.append(self.selection_price)  # get 한 값들 빈 리스트에 append
        selection_items = tuple(
            selection_item
        )  # 리스트 값들 전부 tuple로 변환(데이터 베이스로 insert 하기 위해서)
        single_table_isert(
            selection_items
        )  # 변환시킨 tuple을 single_table_insert 함수의 인자로 보내기
        single_label_product_name.delete(0, END)  # 표시되어 있는 품목명 delete
        single_label_quantity_name.delete(0, END)  # 표시되어 있는 수량 delete
        single_combobox_type.current(0)  # 표시되어 있는 combobox 항목 초기화
        single_combobox_price.current(0)  # 표시되어 있는 combobox 항목 초기화

    def is_multi_new_item_check(self):
        self.filename = file_label_name.get()
        new_items_list = multi_table_check(
            self.filename
        )  # single_table_check 함수에서 return 값 받아옴
        # 받아온 리스트에 항목이 없으면 메시지 띄우기 항목이 있으면 리스트 박스에 표시하기
        if len(new_items_list) == 0:
            msgbox.showinfo("알림", "새로운 항목이 없습니다.")
        else:
            for item in new_items_list:
                multi_list.insert(END, item)

    def multi_move_button(self):
        self.selection_item = (
            multi_list.curselection()
        )  # 리스트 박스에서 선택한 아이템 선택 method는 curselection
        selection_item_list = []
        # 선택한 아이템의 값을 get 해서 list 로 만들기
        for item in self.selection_item:
            get_item = multi_list.get(item)
            selection_item_list.append(get_item)
        # list로 만든 아이템들을 listbox 로 insert
        for item in selection_item_list:
            multi_label_product_name.insert(END, item[2])
            multi_label_quantity_name.insert(END, item[3])
        multi_list.delete(self.selection_item[0], self.selection_item[-1])

    def multi_save_button(self):
        self.selection_product = list(
            multi_label_product_name.get(0, END)
        )  # 보낸 품목명의 값을 가져오기 get() 해서 list
        self.selection_quantity = list(
            multi_label_quantity_name.get(0, END)
        )  # 보낸 수량의 값을 가져오기 get() 해서 list
        self.selection_type = multi_combobox_type.get()  # combobox에서 고른 값 가져오기 get()
        self.selection_price = int(
            multi_combobox_price.get()
        )  # combobox에서 고른 값 가져오기 get()
        selection_items = []
        # 각각의 독립적인 list 들을 하나의 list 작업 하기
        while len(self.selection_product) != 0 and len(self.selection_quantity) != 0:
            selection_item = []
            selection_item.append(self.selection_product[0])
            selection_item.append(self.selection_quantity[0])
            selection_item.append(self.selection_type)
            selection_item.append(self.selection_price)
            selection_items.append(selection_item)
            del self.selection_product[0]
            del self.selection_quantity[0]
        multi_table_isert(
            selection_items
        )  # list로 만든 값들을 multi_table_insert 함수의 인자로 보내기
        multi_label_product_name.delete(0, END)  # 표시되어 있는 품목명 delete
        multi_label_quantity_name.delete(0, END)  # 표시되어 있는 수량 delete
        multi_combobox_type.current(0)  # 표시되어 있는 combobox 항목 초기화
        multi_combobox_price.current(0)  # 표시되어 있는 combobox 항목 초기화

    def sample_file_save(self):
        self.openfilename = file_label_name.get()
        self.savefilename = filedialog.asksaveasfilename(
            title="CJ대한통운 샘플 파일을 저장하세요",
            filetypes=(("EXCEL 파일", "*.xlsx"), ("모든파일", "*.*")),
            initialdir="C:\\Users\\오나성\Desktop\\Python_RPA_Excel_Waybill",
        )
        sample_save(self.openfilename, self.savefilename)

    def waybill_file_add(self):
        self.filename = filedialog.askopenfilename(
            title="운송장 파일을 선택하세요",
            filetypes=(("EXCEL 파일", "*.xlsx"), ("모든파일", "*.*")),
            initialdir="C:\\Users\\오나성\Desktop",
        )
        waybill_label_name.insert(0, self.filename)

    def waybill_file_save(self):
        self.openfilename = waybill_label_name.get()
        self.savefilename = file_label_name.get()
        waybill_save(self.openfilename, self.savefilename)

    def window_transform(self):
        pass
        # self.window = window
        # self.window.destroy()
        # app = Todayhome()
        # app.open_window()


app = Smartstore()

window = Tk()
window.title("스마트 스토어")
window.geometry("1440x900")
window.resizable(True, True)

############ file_add ################
file_frame = LabelFrame(window, text="스마트 스토어", padx=5, pady=5)
file_frame.pack(padx=10, pady=10, fill="x")

file_add_button = Button(
    file_frame,
    relief="raised",
    overrelief="solid",
    text="원본 파일 선택",
    width=20,
    height=2,
    padx=2,
    pady=2,
    command=app.excel_file_add,
)
file_add_button.pack(side="left")

file_label = Label(file_frame, text="선택된 파일명 :")
file_label.pack(side="left", padx=5, pady=5)
file_label_name = Entry(file_frame, width=60)
file_label_name.pack(side="left", padx=5, pady=5)

""" file_path_label = Label(file_frame, text="현재 파일 경로 :")
file_path_label.pack(side="left", padx=5, pady=5)
file_path_default = StringVar(file_frame)
file_path_default.set("hello world")
file_path_label_name = Entry(file_frame, width=60, textvariable=file_path_default)
file_path_label_name.pack(side="left", padx=5, pady=5)

file_path_change_button = Button(
    file_frame,
    relief="raised",
    overrelief="solid",
    text="파일 선택 경로 변경",
    width=20,
    height=2,
    padx=2,
    pady=2,
    command=app.excel_file_path_change,
)
file_path_change_button.pack(side="left") """
###################################################
############ single_check_list btn ################
single_frame = LabelFrame(window, text="단품 항목", padx=5, pady=5)
single_frame.pack(padx=10, pady=10, fill="x")

single_check_button = Button(
    single_frame,
    relief="raised",
    overrelief="solid",
    text="단품 체크",
    width=50,
    height=2,
    pady=2,
    command=app.is_single_new_item_check,
)
single_check_button.pack()
##################################################
############ single_list box #####################
single_list_frame = LabelFrame(single_frame, text="신규 단품 항목", padx=5, pady=5)
single_list_frame.pack(fill="both")

single_scrollbar = Scrollbar(single_list_frame)
single_scrollbar.pack(side="right", fill="y")

single_list = Listbox(
    single_list_frame,
    selectmode="extended",
    height=5,
    yscrollcommand=single_scrollbar.set,
)
single_list.pack(side="left", fill="both", expand=True)
single_scrollbar.config(command=single_list.yview)
############ single_move button #####################
single_move_btn = Button(
    single_list_frame,
    relief="raised",
    overrelief="solid",
    text="선택",
    width=5,
    height=2,
    padx=2,
    pady=2,
    command=app.single_move_button,
)
single_move_btn.pack(side="bottom")
###################################################
############ single_select_option_save #################
single_option = LabelFrame(single_frame, text="선택항목")
single_option.pack(padx=5, pady=5, fill="both")

single_save_btn = Button(
    single_option,
    relief="raised",
    overrelief="solid",
    text="저장",
    width=10,
    height=2,
    padx=2,
    pady=2,
    command=app.single_save_button,
)
single_save_btn.pack(side="right")

single_label_product = Label(single_option, text="품목명 :")
single_label_product.pack(side="left", padx=5, pady=5)
single_label_product_name = Entry(single_option, width=60)
single_label_product_name.pack(side="left", padx=5, pady=5)

single_label_quantity = Label(single_option, text="수량 :")
single_label_quantity.pack(side="left", padx=5, pady=5)
single_label_quantity_name = Entry(single_option, width=5)
single_label_quantity_name.pack(side="left", padx=5, pady=5)

single_label_type = Label(single_option, text="박스타입 :")
single_label_type.pack(side="left", padx=5, pady=5)
single_option_type = ["선택", "극소", "소", "중", "대", "이형"]
single_combobox_type = ttk.Combobox(
    single_option, state="readonly", values=single_option_type
)
single_combobox_type.current(0)
single_combobox_type.pack(side="left", padx=5, pady=5)

single_label_price = Label(single_option, text="기본운임 :")
single_label_price.pack(side="left", padx=5, pady=5)
single_option_price = ["선택", 2050, 2450, 2900, 4300, 4700, 11000, 15000]
single_combobox_price = ttk.Combobox(
    single_option, state="readonly", values=single_option_price
)
single_combobox_price.current(0)
single_combobox_price.pack(side="left", padx=5, pady=5)
#####################################################################################
############ multi_check_list btn ################
multi_frame = LabelFrame(window, text="합포 항목", padx=5, pady=5)
multi_frame.pack(padx=10, pady=10, fill="x")

multi_check_button = Button(
    multi_frame,
    relief="raised",
    overrelief="solid",
    text="합포 체크",
    width=50,
    height=2,
    pady=2,
    command=app.is_multi_new_item_check,
)
multi_check_button.pack()
############################################
############ multi_list box #####################
multi_list_frame = LabelFrame(multi_frame, text="신규 합포 항목", padx=5, pady=5)
multi_list_frame.pack(fill="both")

multi_scrollbar = Scrollbar(multi_list_frame)
multi_scrollbar.pack(side="right", fill="y")

multi_list = Listbox(
    multi_list_frame,
    selectmode="extended",
    height=10,
    yscrollcommand=multi_scrollbar.set,
)
multi_list.pack(side="left", fill="both", expand=True)
multi_scrollbar.config(command=multi_list.yview)
#####################################################
############ multi_move button #####################
multi_move_btn = Button(
    multi_list_frame,
    relief="raised",
    overrelief="solid",
    text="선택",
    width=5,
    height=2,
    padx=2,
    pady=2,
    command=app.multi_move_button,
)
multi_move_btn.pack(side="bottom")
###################################################
############ multi_select_option_save #################
multi_option = LabelFrame(multi_frame, text="선택항목")
multi_option.pack(padx=5, pady=5, fill="both")

multi_save_btn = Button(
    multi_option,
    relief="raised",
    overrelief="solid",
    text="저장",
    width=10,
    height=2,
    padx=2,
    pady=2,
    command=app.multi_save_button,
)
multi_save_btn.pack(side="right")

multi_label_product = Label(multi_option, text="품목명 :")
multi_label_product.pack(side="left", padx=5, pady=5)
multi_label_product_name = Listbox(multi_option, height=5, width=60)
multi_label_product_name.pack(side="left", padx=5, pady=5)

multi_label_quantity = Label(multi_option, text="수량 :")
multi_label_quantity.pack(side="left", padx=5, pady=5)
multi_label_quantity_name = Listbox(multi_option, height=5, width=5)
multi_label_quantity_name.pack(side="left", padx=5, pady=5)

multi_label_type = Label(multi_option, text="박스타입 :")
multi_label_type.pack(side="left", padx=5, pady=5)
multi_option_type = ["선택", "극소", "소", "중", "대", "이형"]
multi_combobox_type = ttk.Combobox(
    multi_option, state="readonly", values=multi_option_type
)
multi_combobox_type.current(0)
multi_combobox_type.pack(side="left", padx=5, pady=5)

multi_label_price = Label(multi_option, text="기본운임 :")
multi_label_price.pack(side="left", padx=5, pady=5)
multi_option_price = ["선택", 2050, 2450, 2900, 4300, 4700, 11000, 15000]
multi_combobox_price = ttk.Combobox(
    multi_option, state="readonly", values=multi_option_price
)
multi_combobox_price.current(0)
multi_combobox_price.pack(side="left", padx=5, pady=5)
#####################################################################################
############ other_file_frame and window_transform ################
other_file_frame = LabelFrame(window, text="파일 및 창전환", padx=5, pady=5)
other_file_frame.pack(padx=10, pady=10, fill="x")

sample_frame = LabelFrame(other_file_frame, text="샘플 파일", padx=5, pady=5)
sample_frame.grid(padx=10, pady=10, row=0, column=0)

save_sampel_file_button = Button(
    sample_frame,
    relief="raised",
    overrelief="solid",
    text="CJ대한통운 샘플 파일 생성",
    width=25,
    height=2,
    padx=2,
    pady=2,
    command=app.sample_file_save,
)
save_sampel_file_button.pack(side="left")

waybill_frame = LabelFrame(other_file_frame, text="운송장 파일", padx=5, pady=5)
waybill_frame.grid(padx=10, pady=10, row=0, column=1)

select_waybill_file_button = Button(
    waybill_frame,
    relief="raised",
    overrelief="solid",
    text="운송장 파일 선택",
    width=25,
    height=2,
    padx=2,
    pady=2,
    command=app.waybill_file_add,
)
select_waybill_file_button.pack(side="left")

waybill_label = Label(waybill_frame, text="선택된 파일명 :")
waybill_label.pack(side="left", padx=5, pady=5)
waybill_label_name = Entry(waybill_frame, width=60)
waybill_label_name.pack(side="left", padx=5, pady=5)

save_waybill_file_button = Button(
    waybill_frame,
    relief="raised",
    overrelief="solid",
    text="운송장 파일 저장",
    width=25,
    height=2,
    padx=2,
    pady=2,
    command=app.waybill_file_save,
)
save_waybill_file_button.pack(side="right")

transform_frame = LabelFrame(other_file_frame, text="창 전환", padx=5, pady=5)
transform_frame.grid(padx=10, pady=10, row=0, column=2)

transform_label = Label(transform_frame, text="이동 :")
transform_label.pack(side="left", padx=5, pady=5)
transform_option = ["선택", "오늘의 집", "펀샵", "리빙픽", "1300k"]
transform_combobox = ttk.Combobox(
    transform_frame, state="readonly", values=transform_option
)
transform_combobox.current(0)
transform_combobox.pack(side="left", padx=5, pady=5)

transform_button = Button(
    transform_frame,
    relief="raised",
    overrelief="solid",
    text="전환",
    width=10,
    height=2,
    padx=2,
    pady=2,
    command=app.window_transform,
)
transform_button.pack(side="right")
#####################################################################################
window.mainloop()
