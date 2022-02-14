import pandas as pd


def waybill_save(openfilename, savefilename):
    # waybill excel file 가져와서 Dataframe 으로 만들기
    waybill_df = pd.read_excel(f"{openfilename}", engine="openpyxl")
    # 원본 excel file 가져와서 Datafrawme 으로 만들기
    row_df = pd.read_excel(f"{savefilename}", engine="openpyxl")

    # waybil_df 에서 원하는 column 만 가져오기
    select_waybill_df = waybill_df[["운송장번호", "받는분", "받는분 전화번호", "받는분주소"]]
    # row_df 에서 원하는 column 만 가져오기
    select_row_df = row_df[["주문번호", "송장번호", "수취인명", "수취인연락처1", "배송지"]]
    # select_row_df 에서 "주문번호"로 index 설정
    set_index_row_df = select_row_df.set_index("주문번호", drop=False)

    # select_waybill_df를 dict 으로 만들고 전화번호에 빠져 있는 앞 0을 추가하고 하이픈(-)을 추가해주기
    waybill_list = []
    for row in select_waybill_df.to_dict("records"):
        phone_row = str(row["받는분 전화번호"])
        if len(phone_row) == 11:
            zero_add_phone_row = phone_row.zfill(
                12
            )  # python 내장 method인 zfill를 이용해서 전화번호마다 앞에다가 "0" 을 넣어주기
            hyphen_add_phone_row = (
                zero_add_phone_row[0:4]
                + "-"
                + zero_add_phone_row[4:8]
                + "-"
                + zero_add_phone_row[8:12]
            )
            row["받는분 전화번호"] = hyphen_add_phone_row
            waybill_list.append(row)
        elif len(phone_row) == 7:
            zero_add_phone_row = phone_row.zfill(8)
            hyphen_add_phone_row = (
                zero_add_phone_row[0:2]
                + "-"
                + zero_add_phone_row[2:5]
                + "-"
                + zero_add_phone_row[5:8]
            )
            row["받는분 전화번호"] = hyphen_add_phone_row
            waybill_list.append(row)
        elif len(phone_row) == 8:
            zero_add_phone_row = phone_row.zfill(9)
            hyphen_add_phone_row = (
                zero_add_phone_row[0:3]
                + "-"
                + zero_add_phone_row[3:6]
                + "-"
                + zero_add_phone_row[6:9]
            )
            row["받는분 전화번호"] = hyphen_add_phone_row
            waybill_list.append(row)
        else:
            zero_add_phone_row = phone_row.zfill(11)
            hyphen_add_phone_row = (
                zero_add_phone_row[0:3]
                + "-"
                + zero_add_phone_row[3:7]
                + "-"
                + zero_add_phone_row[7:11]
            )
            row["받는분 전화번호"] = hyphen_add_phone_row
            waybill_list.append(row)

    for row in set_index_row_df.to_dict("records"):
        for item in waybill_list:
            if (
                row["수취인명"] == item["받는분"]
                and row["수취인연락처1"] == item["받는분 전화번호"]
                and row["배송지"] == item["받는분주소"]
            ):
                set_index_row_df.loc[row["주문번호"], "송장번호"] = item["운송장번호"]
            else:
                continue
    # 송장번호만 따로 df 로 만들기
    waybill_number = set_index_row_df.reset_index(drop=True)[["송장번호"]]

    # append 모드를 사용하기 위해서 excelwriter 사용하기 "overlay" 와 "sheet_name" 확인하고, "startcol"을 이용해서 원하는 위치에 기존 파일에 append 하기
    with pd.ExcelWriter(
        f"{savefilename}", mode="a", engine="openpyxl", if_sheet_exists="overlay"
    ) as writer:
        waybill_number.to_excel(writer, sheet_name="발주발송관리", startcol=6, index=False)
