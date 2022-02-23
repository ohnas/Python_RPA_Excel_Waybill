from tkinter import *
from tkinter import filedialog
from tkinter import ttk as ttk
from tkinter import messagebox as msg

from smartstore_single_check import single_table_check
from smartstore_single_insert import single_table_isert
from smartstore_multi_check import multi_table_check
from smartstore_multi_insert import multi_table_isert
from smartstore_sample_save import sample_save
from smartstore_waybill_save import waybill_save
from todayhome_GUI import Todayhome


class Smartstore:
    def open_window(self):
        self.window = Tk()
        self.window.title("스마트 스토어")
        self.window.geometry("1440x900")
        self.window.resizable(True, True)

        ############ file_add ################
        self.file_frame = LabelFrame(self.window, text="스마트 스토어", padx=5, pady=5)
        self.file_frame.pack(padx=10, pady=10, fill="x")

        self.file_add_button = Button(
            self.file_frame,
            relief="raised",
            overrelief="solid",
            text="원본 파일 선택",
            width=20,
            height=2,
            padx=2,
            pady=2,
            command=smartstore_app.excel_file_add,
        )
        self.file_add_button.pack(side="left")

        self.file_label = Label(self.file_frame, text="선택된 파일명 :")
        self.file_label.pack(side="left", padx=5, pady=5)
        self.file_label_name = Entry(self.file_frame, width=60)
        self.file_label_name.pack(side="left", padx=5, pady=5)
        ###################################################
        ############ single_check_list btn ################
        self.single_frame = LabelFrame(self.window, text="단품 항목", padx=5, pady=5)
        self.single_frame.pack(padx=10, pady=10, fill="x")

        self.single_check_button = Button(
            self.single_frame,
            relief="raised",
            overrelief="solid",
            text="단품 체크",
            width=50,
            height=2,
            pady=2,
            command=smartstore_app.is_single_new_item_check,
        )
        self.single_check_button.pack()
        ##################################################
        ############ single_list box #####################
        self.single_list_frame = LabelFrame(
            self.single_frame, text="신규 단품 항목", padx=5, pady=5
        )
        self.single_list_frame.pack(fill="both")

        self.single_scrollbar = Scrollbar(self.single_list_frame)
        self.single_scrollbar.pack(side="right", fill="y")

        self.single_list = Listbox(
            self.single_list_frame,
            selectmode="extended",
            height=5,
            yscrollcommand=self.single_scrollbar.set,
        )
        self.single_list.pack(side="left", fill="both", expand=True)
        self.single_scrollbar.config(command=self.single_list.yview)
        ############ single_move button #####################
        self.single_move_btn = Button(
            self.single_list_frame,
            relief="raised",
            overrelief="solid",
            text="선택",
            width=5,
            height=2,
            padx=2,
            pady=2,
            command=smartstore_app.single_move_button,
        )
        self.single_move_btn.pack(side="bottom")
        ###################################################
        ############ single_select_option_save #################
        self.single_option = LabelFrame(self.single_frame, text="선택항목")
        self.single_option.pack(padx=5, pady=5, fill="both")

        self.single_save_btn = Button(
            self.single_option,
            relief="raised",
            overrelief="solid",
            text="저장",
            width=10,
            height=2,
            padx=2,
            pady=2,
            command=smartstore_app.single_save_button,
        )
        self.single_save_btn.pack(side="right")

        self.single_label_product = Label(self.single_option, text="품목명 :")
        self.single_label_product.pack(side="left", padx=5, pady=5)
        self.single_label_product_name = Entry(self.single_option, width=60)
        self.single_label_product_name.pack(side="left", padx=5, pady=5)

        self.single_label_quantity = Label(self.single_option, text="수량 :")
        self.single_label_quantity.pack(side="left", padx=5, pady=5)
        self.single_label_quantity_name = Entry(self.single_option, width=5)
        self.single_label_quantity_name.pack(side="left", padx=5, pady=5)

        self.single_label_type = Label(self.single_option, text="박스타입 :")
        self.single_label_type.pack(side="left", padx=5, pady=5)
        self.single_option_type = ["선택", "극소", "소", "중", "대", "이형"]
        self.single_combobox_type = ttk.Combobox(
            self.single_option, state="readonly", values=self.single_option_type
        )
        self.single_combobox_type.current(0)
        self.single_combobox_type.pack(side="left", padx=5, pady=5)

        self.single_label_price = Label(self.single_option, text="기본운임 :")
        self.single_label_price.pack(side="left", padx=5, pady=5)
        self.single_option_price = ["선택", 2050, 2450, 2900, 4300, 4700, 11000, 15000]
        self.single_combobox_price = ttk.Combobox(
            self.single_option, state="readonly", values=self.single_option_price
        )
        self.single_combobox_price.current(0)
        self.single_combobox_price.pack(side="left", padx=5, pady=5)
        #####################################################################################
        ############ multi_check_list btn ################
        self.multi_frame = LabelFrame(self.window, text="합포 항목", padx=5, pady=5)
        self.multi_frame.pack(padx=10, pady=10, fill="x")

        self.multi_check_button = Button(
            self.multi_frame,
            relief="raised",
            overrelief="solid",
            text="합포 체크",
            width=50,
            height=2,
            pady=2,
            command=smartstore_app.is_multi_new_item_check,
        )
        self.multi_check_button.pack()
        ############################################
        ############ multi_list box #####################
        self.multi_list_frame = LabelFrame(
            self.multi_frame, text="신규 합포 항목", padx=5, pady=5
        )
        self.multi_list_frame.pack(fill="both")

        self.multi_scrollbar = Scrollbar(self.multi_list_frame)
        self.multi_scrollbar.pack(side="right", fill="y")

        self.multi_list = Listbox(
            self.multi_list_frame,
            selectmode="extended",
            height=10,
            yscrollcommand=self.multi_scrollbar.set,
        )
        self.multi_list.pack(side="left", fill="both", expand=True)
        self.multi_scrollbar.config(command=self.multi_list.yview)
        #####################################################
        ############ multi_move button #####################
        self.multi_move_btn = Button(
            self.multi_list_frame,
            relief="raised",
            overrelief="solid",
            text="선택",
            width=5,
            height=2,
            padx=2,
            pady=2,
            command=smartstore_app.multi_move_button,
        )
        self.multi_move_btn.pack(side="bottom")
        ###################################################
        ############ multi_select_option_save #################
        self.multi_option = LabelFrame(self.multi_frame, text="선택항목")
        self.multi_option.pack(padx=5, pady=5, fill="both")

        self.multi_save_btn = Button(
            self.multi_option,
            relief="raised",
            overrelief="solid",
            text="저장",
            width=10,
            height=2,
            padx=2,
            pady=2,
            command=smartstore_app.multi_save_button,
        )
        self.multi_save_btn.pack(side="right")

        self.multi_label_product = Label(self.multi_option, text="품목명 :")
        self.multi_label_product.pack(side="left", padx=5, pady=5)
        self.multi_label_product_name = Listbox(self.multi_option, height=5, width=60)
        self.multi_label_product_name.pack(side="left", padx=5, pady=5)

        self.multi_label_quantity = Label(self.multi_option, text="수량 :")
        self.multi_label_quantity.pack(side="left", padx=5, pady=5)
        self.multi_label_quantity_name = Listbox(self.multi_option, height=5, width=5)
        self.multi_label_quantity_name.pack(side="left", padx=5, pady=5)

        self.multi_label_type = Label(self.multi_option, text="박스타입 :")
        self.multi_label_type.pack(side="left", padx=5, pady=5)
        self.multi_option_type = ["선택", "극소", "소", "중", "대", "이형"]
        self.multi_combobox_type = ttk.Combobox(
            self.multi_option, state="readonly", values=self.multi_option_type
        )
        self.multi_combobox_type.current(0)
        self.multi_combobox_type.pack(side="left", padx=5, pady=5)

        self.multi_label_price = Label(self.multi_option, text="기본운임 :")
        self.multi_label_price.pack(side="left", padx=5, pady=5)
        self.multi_option_price = ["선택", 2050, 2450, 2900, 4300, 4700, 11000, 15000]
        self.multi_combobox_price = ttk.Combobox(
            self.multi_option, state="readonly", values=self.multi_option_price
        )
        self.multi_combobox_price.current(0)
        self.multi_combobox_price.pack(side="left", padx=5, pady=5)
        #####################################################################################
        ############ other_file_frame and window_transform ################
        self.other_file_frame = LabelFrame(self.window, text="파일 및 창전환", padx=5, pady=5)
        self.other_file_frame.pack(padx=10, pady=10, fill="x")

        self.sample_frame = LabelFrame(
            self.other_file_frame, text="샘플 파일", padx=5, pady=5
        )
        self.sample_frame.grid(padx=10, pady=10, row=0, column=0)

        self.save_sampel_file_button = Button(
            self.sample_frame,
            relief="raised",
            overrelief="solid",
            text="CJ대한통운 샘플 파일 생성",
            width=25,
            height=2,
            padx=2,
            pady=2,
            command=smartstore_app.sample_file_save,
        )
        self.save_sampel_file_button.pack(side="left")

        self.waybill_frame = LabelFrame(
            self.other_file_frame, text="운송장 파일", padx=5, pady=5
        )
        self.waybill_frame.grid(padx=10, pady=10, row=0, column=1)

        self.select_waybill_file_button = Button(
            self.waybill_frame,
            relief="raised",
            overrelief="solid",
            text="운송장 파일 선택",
            width=25,
            height=2,
            padx=2,
            pady=2,
            command=smartstore_app.waybill_file_add,
        )
        self.select_waybill_file_button.pack(side="left")

        self.waybill_label = Label(self.waybill_frame, text="선택된 파일명 :")
        self.waybill_label.pack(side="left", padx=5, pady=5)
        self.waybill_label_name = Entry(self.waybill_frame, width=60)
        self.waybill_label_name.pack(side="left", padx=5, pady=5)

        self.save_waybill_file_button = Button(
            self.waybill_frame,
            relief="raised",
            overrelief="solid",
            text="운송장 파일 저장",
            width=25,
            height=2,
            padx=2,
            pady=2,
            command=smartstore_app.waybill_file_save,
        )
        self.save_waybill_file_button.pack(side="right")

        self.transform_frame = LabelFrame(
            self.other_file_frame, text="창 전환", padx=5, pady=5
        )
        self.transform_frame.grid(padx=10, pady=10, row=0, column=2)

        self.transform_label = Label(self.transform_frame, text="이동 :")
        self.transform_label.pack(side="left", padx=5, pady=5)
        self.transform_option = ["선택", "오늘의 집", "펀샵", "리빙픽", "1300k", "티몬"]
        self.transform_combobox = ttk.Combobox(
            self.transform_frame, state="readonly", values=self.transform_option
        )
        self.transform_combobox.current(0)
        self.transform_combobox.pack(side="left", padx=5, pady=5)

        self.transform_button = Button(
            self.transform_frame,
            relief="raised",
            overrelief="solid",
            text="전환",
            width=10,
            height=2,
            padx=2,
            pady=2,
            command=smartstore_app.window_transform,
        )
        self.transform_button.pack(side="right")
        #####################################################################################
        self.window.mainloop()

    def excel_file_add(self):
        filename = filedialog.askopenfilename(
            title="스마트스토어 파일을 선택하세요",
            filetypes=(("EXCEL 파일", "*.xlsx"), ("모든파일", "*.*")),
            initialdir="C:\\Users\\오나성\\Desktop\\Python_RPA_Excel_Waybill",
        )
        self.file_label_name.insert(0, filename)

    def is_single_new_item_check(self):
        filename = self.file_label_name.get()
        new_items_list = single_table_check(
            filename
        )  # single_table_check 함수에서 return 값 받아옴
        # 받아온 리스트에 항목이 없으면 메시지 띄우기 항목이 있으면 리스트 박스에 표시하기
        if len(new_items_list) == 0:
            msg.showinfo("알림", "새로운 항목이 없습니다.")
        else:
            for item in new_items_list:
                self.single_list.insert(END, item)

    def single_move_button(self):
        selection_item = (
            self.single_list.curselection()
        )  # 리스트 박스에서 선택한 아이템 선택 method는 curselection
        selection_item_list = list(
            self.single_list.get(selection_item[0])
        )  # 선택한 항목의 값으 get() 하고 list로 변환
        self.single_label_product_name.insert(
            0, selection_item_list[0]
        )  # 리스트에서 품목명은 품목명 Entry 로 보내기
        self.single_label_quantity_name.insert(
            0, selection_item_list[1]
        )  # 리스트에서 수량은 수량 Entry 로 보내기
        self.single_list.delete(selection_item)  # 보내기가 완료되었다면 선택했었던 항목은 지워버리기

    def single_save_button(self):
        selection_product = (
            self.single_label_product_name.get()
        )  # 보낸 품목명의 값을 가져오기 get()
        selection_quantity = int(
            self.single_label_quantity_name.get()
        )  # 보낸 수량의 값을 가져오기 get()
        selection_type = self.single_combobox_type.get()  # combobox에서 고른 값 가져오기 get()
        selection_price = int(
            self.single_combobox_price.get()
        )  # combobox에서 고른 값 가져오기 get()
        selection_item = []
        selection_item.append(selection_product)  # get 한 값들 빈 리스트에 append
        selection_item.append(selection_quantity)  # get 한 값들 빈 리스트에 append
        selection_item.append(selection_type)  # get 한 값들 빈 리스트에 append
        selection_item.append(selection_price)  # get 한 값들 빈 리스트에 append
        selection_items = tuple(
            selection_item
        )  # 리스트 값들 전부 tuple로 변환(데이터 베이스로 insert 하기 위해서)
        single_table_isert(
            selection_items
        )  # 변환시킨 tuple을 single_table_insert 함수의 인자로 보내기
        self.single_label_product_name.delete(0, END)  # 표시되어 있는 품목명 delete
        self.single_label_quantity_name.delete(0, END)  # 표시되어 있는 수량 delete
        self.single_combobox_type.current(0)  # 표시되어 있는 combobox 항목 초기화
        self.single_combobox_price.current(0)  # 표시되어 있는 combobox 항목 초기화

    def is_multi_new_item_check(self):
        filename = self.file_label_name.get()
        new_items_list = multi_table_check(
            filename
        )  # single_table_check 함수에서 return 값 받아옴
        # 받아온 리스트에 항목이 없으면 메시지 띄우기 항목이 있으면 리스트 박스에 표시하기
        if len(new_items_list) == 0:
            msg.showinfo("알림", "새로운 항목이 없습니다.")
        else:
            for item in new_items_list:
                self.multi_list.insert(END, item)

    def multi_move_button(self):
        selection_item = (
            self.multi_list.curselection()
        )  # 리스트 박스에서 선택한 아이템 선택 method는 curselection
        selection_item_list = []
        # 선택한 아이템의 값을 get 해서 list 로 만들기
        for item in selection_item:
            get_item = self.multi_list.get(item)
            selection_item_list.append(get_item)
        # list로 만든 아이템들을 listbox 로 insert
        for item in selection_item_list:
            self.multi_label_product_name.insert(END, item[2])
            self.multi_label_quantity_name.insert(END, item[3])
        self.multi_list.delete(selection_item[0], selection_item[-1])

    def multi_save_button(self):
        selection_product = list(
            self.multi_label_product_name.get(0, END)
        )  # 보낸 품목명의 값을 가져오기 get() 해서 list
        selection_quantity = list(
            self.multi_label_quantity_name.get(0, END)
        )  # 보낸 수량의 값을 가져오기 get() 해서 list
        selection_type = self.multi_combobox_type.get()  # combobox에서 고른 값 가져오기 get()
        selection_price = int(
            self.multi_combobox_price.get()
        )  # combobox에서 고른 값 가져오기 get()
        selection_items = []
        # 각각의 독립적인 list 들을 하나의 list 작업 하기
        while len(selection_product) != 0 and len(selection_quantity) != 0:
            selection_item = []
            selection_item.append(selection_product[0])
            selection_item.append(selection_quantity[0])
            selection_item.append(selection_type)
            selection_item.append(selection_price)
            selection_items.append(selection_item)
            del selection_product[0]
            del selection_quantity[0]
        multi_table_isert(
            selection_items
        )  # list로 만든 값들을 multi_table_insert 함수의 인자로 보내기
        self.multi_label_product_name.delete(0, END)  # 표시되어 있는 품목명 delete
        self.multi_label_quantity_name.delete(0, END)  # 표시되어 있는 수량 delete
        self.multi_combobox_type.current(0)  # 표시되어 있는 combobox 항목 초기화
        self.multi_combobox_price.current(0)  # 표시되어 있는 combobox 항목 초기화

    def sample_file_save(self):
        # 최초의 가져온 원본 excel file 가져오기
        openfilename = self.file_label_name.get()
        # 샘플 파일을 저장할 경로 설정
        savefilename = filedialog.asksaveasfilename(
            title="CJ대한통운 샘플 파일을 저장하세요",
            filetypes=(("EXCEL 파일", "*.xlsx"), ("모든파일", "*.*")),
            initialdir="C:\\Users\\오나성\Desktop\\Python_RPA_Excel_Waybill",
        )
        # sample_save 의 인자로 2개의 변수 보내주기
        sample_save(openfilename, savefilename)

    def waybill_file_add(self):
        # 운송장 파일을 가져오기
        filename = filedialog.askopenfilename(
            title="운송장 파일을 선택하세요",
            filetypes=(("EXCEL 파일", "*.xlsx"), ("모든파일", "*.*")),
            initialdir="C:\\Users\\오나성\Desktop",
        )
        self.waybill_label_name.insert(0, filename)

    def waybill_file_save(self):
        # 가져온 운송장 파일을 변수로 저장
        openfilename = self.waybill_label_name.get()
        # 원본파일을 변수로 저장
        savefilename = self.file_label_name.get()
        # waybill_save 의 인자로 2개의 변수 보내주기
        waybill_save(openfilename, savefilename)

    def window_transform(self):
        selection_platform = self.transform_combobox.get()
        if selection_platform == "오늘의 집":
            self.window.destroy()
            today_app = Todayhome()
            today_app.open_window()


if __name__ == "__main__":
    smartstore_app = Smartstore()
    smartstore_app.open_window()
