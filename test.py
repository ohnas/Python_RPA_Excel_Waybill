from os import dup, rename
import time
import pymysql
import pandas as pd
import DB_auth

start = time.time()


def save_file():
    # db 접속정보를 DB_auth.py에서 불러와서 입력해놓기
    conn = pymysql.connect(
        db=DB_auth.info["db"],
        host=DB_auth.info["host"],
        user=DB_auth.info["user"],
        password=DB_auth.info["password"],
        port=DB_auth.info["port"],
        charset=DB_auth.info["charset"],
    )

    # db 에서 single table 에서 data 불러오기
    db_cursor = conn.cursor(pymysql.cursors.DictCursor)
    single_sql = "SELECT * FROM single_table"
    db_cursor.execute(single_sql)
    single_table_rows = db_cursor.fetchall()

    db_single_df = pd.DataFrame(single_table_rows)
    db_cursor.close()

    # db 에서 multi table 에서 data 불러오기
    db_cursor = conn.cursor(pymysql.cursors.DictCursor)
    multi_sql = "select * from multi_table"
    db_cursor.execute(multi_sql)
    multi_table_rows = db_cursor.fetchall()

    db_multi_df = pd.DataFrame(multi_table_rows)
    db_multi_set_index_df = db_multi_df.set_index("id")
    db_multi_drop_duplicates_df = db_multi_df.drop_duplicates(
        keep="first", subset=["id"]
    )

    db_cursor.close()

    # 원본 excel file 가져와서 Dataframe 으로 만들기
    row_df = pd.read_excel("read_sample.xlsx", engine="openpyxl")

    # row_df 에서 원하는 column 만 가져오기
    select_df = row_df[
        ["주문번호", "수취인명", "옵션정보", "수량", "수취인연락처1", "수취인연락처2", "배송지", "배송메세지"]
    ]

    # select_df 에서 column 위치조정
    relocation_df = select_df[
        [
            "주문번호",
            "수취인명",
            "배송지",
            "수취인연락처1",
            "수취인연락처2",
            "옵션정보",
            "수량",
            "배송메세지",
        ]
    ]

    # relocation_df 에서 column 이름 rename 하기
    rename_df = relocation_df.rename(
        columns={
            "주문번호": "고객주문번호",
            "수취인명": "받는분성명",
            "배송지": "받는분주소(전체,분할)",
            "수취인연락처1": "받는분전화번호",
            "수취인연락처2": "받는분기타연락처",
            "옵션정보": "품목명",
            "수량": "내품수량",
        }
    )

    # rename_df 에서 인덱스를 고객주문번호으로 재설정하기
    set_index_df = rename_df.set_index("고객주문번호", drop=False)

    # set_index_df 에서 받는분섬명 , 받는분주소, 받는분전화번호를 기준으로 중복데이터 제거한 가공된 dataframe
    drop_duplicated_df = set_index_df.drop_duplicates(
        keep=False, subset=["받는분성명", "받는분주소(전체,분할)", "받는분전화번호"]
    )

    # single db 와 비교해서 데이터 값 넣기
    for df_row in drop_duplicated_df.to_dict("records"):
        for db_row in db_single_df.to_dict("records"):
            if df_row["품목명"] == db_row["품목명"] and df_row["내품수량"] == db_row["내품수량"]:
                drop_duplicated_df.at[df_row["고객주문번호"], "운임구분"] = db_row["운임구분"]
                drop_duplicated_df.at[df_row["고객주문번호"], "박스타입"] = db_row["박스타입"]
                drop_duplicated_df.at[df_row["고객주문번호"], "기본운임"] = db_row["기본운임"]
                drop_duplicated_df.at[df_row["고객주문번호"], "보내는분성명"] = db_row["보내는분성명"]
                drop_duplicated_df.at[df_row["고객주문번호"], "보내는분주소(전체, 분할)"] = db_row[
                    "보내는분주소(전체, 분할)"
                ]
                drop_duplicated_df.at[df_row["고객주문번호"], "보내는분전화번호"] = db_row["보내는분전화번호"]
                drop_duplicated_df.at[df_row["고객주문번호"], "보내는분기타연락처"] = db_row[
                    "보내는분기타연락처"
                ]
            else:
                continue

    # set_index_df 에서 받는분섬명 , 받는분주소, 받는분전화번호를 기준으로 중복데이터만 골라낸 가공된 dataframe
    duplicated_df = set_index_df[
        set_index_df.duplicated(keep=False, subset=["받는분성명", "받는분주소(전체,분할)", "받는분전화번호"])
    ]

    # duplicated_df 에서 중복값중 첫번째값만 남기기(이유는 index 값을 하나만 얻기 위해서 index 값이 2개면 중복으로 불러오기 때문에)
    duplicated_df_first = duplicated_df.drop_duplicates(
        keep="first", subset=["받는분성명", "받는분주소(전체,분할)", "받는분전화번호"]
    )

    # multi db 와 비교해서 데이터 값 넣기
    for df_row in duplicated_df_first.to_dict("records"):
        new_df = duplicated_df.loc[df_row["고객주문번호"], :]
        reset_index_df = new_df.reset_index(drop=True)[["품목명", "내품수량"]]
        for db_row in db_multi_drop_duplicates_df.to_dict("records"):
            db_new_df = db_multi_set_index_df.loc[db_row["id"], :]
            db_reset_index_df = db_new_df.reset_index(drop=True)[["품목명", "내품수량"]]
            if reset_index_df.equals(db_reset_index_df) == True:
                duplicated_df.at[df_row["고객주문번호"], "운임구분"] = db_row["운임구분"]
                duplicated_df.at[df_row["고객주문번호"], "박스타입"] = db_row["박스타입"]
                duplicated_df.at[df_row["고객주문번호"], "기본운임"] = db_row["기본운임"]
                duplicated_df.at[df_row["고객주문번호"], "보내는분성명"] = db_row["보내는분성명"]
                duplicated_df.at[df_row["고객주문번호"], "보내는분주소(전체, 분할)"] = db_row[
                    "보내는분주소(전체, 분할)"
                ]
                duplicated_df.at[df_row["고객주문번호"], "보내는분전화번호"] = db_row["보내는분전화번호"]
                duplicated_df.at[df_row["고객주문번호"], "보내는분기타연락처"] = db_row["보내는분기타연락처"]
            else:
                continue

    # drop_duplicated_df 와 duplicated_df 를 pd.concat 함수를 이용하여 병합하여, concat_df 로 만들어내기
    concat_df = pd.concat([drop_duplicated_df, duplicated_df])
    # db 접속 끊기
    conn.close()
    # concat_df를 엑셀파일로 만들어내기
    return concat_df.to_excel("test_sample.xlsx", index=False)


print(time.time() - start)
