from os import dup, rename
import pymysql
import pandas as pd
import numpy as np
import DB_auth as DB_auth


def multi_table_check():
    # db 접속정보를 DB_auth.py에서 불러와서 입력해놓기
    conn = pymysql.connect(
        db=DB_auth.info["db"],
        host=DB_auth.info["host"],
        user=DB_auth.info["user"],
        password=DB_auth.info["password"],
        port=DB_auth.info["port"],
        charset=DB_auth.info["charset"],
    )

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

    # set_index_df 에서 받는분섬명 , 받는분주소, 받는분전화번호를 기준으로 중복데이터만 골라낸 가공된 dataframe
    duplicated_df = set_index_df[
        set_index_df.duplicated(keep=False, subset=["받는분성명", "받는분주소(전체,분할)", "받는분전화번호"])
    ]

    # duplicated_df 에서 중복값중 첫번째값만 남기기(이유는 index 값을 하나만 얻기 위해서 index 값이 2개면 중복으로 불러오기 때문에)
    duplicated_df_first = duplicated_df.drop_duplicates(
        keep="first", subset=["받는분성명", "받는분주소(전체,분할)", "받는분전화번호"]
    )

    # multi db 데이터와 duplicated_df 데이터를 db 에 등록된 데이터가 있는지 비교하기
    df_get_index_list = []
    for df_row in duplicated_df_first.to_dict("records"):
        new_df = duplicated_df.loc[df_row["고객주문번호"], :]
        reset_index_df = new_df.reset_index(drop=True)[["품목명", "내품수량"]]
        for db_row in db_multi_drop_duplicates_df.to_dict("records"):
            db_new_df = db_multi_set_index_df.loc[db_row["id"], :]
            db_reset_index_df = db_new_df.reset_index(drop=True)[["품목명", "내품수량"]]
            isin_df = db_reset_index_df.isin(
                reset_index_df
            )  # isin 메소드를 사용하여 같은 value가 존재하는지 확인
            result_isin_df = isin_df.all(
                axis=None
            )  # all 메소드를 사용하여 같은 value가 ture 인지 false 인지 확인 all 메소드는 모든 value가 true 여야 true 반환, 하나라도 false 면 false 반환
            if result_isin_df == True:
                df_get_index = list(
                    new_df.index
                )  # 존재하는 데이터를 찾았다면 존재하는 df 의 index 값을 리스트로 반환
                df_get_index_list.append(
                    df_get_index
                )  # 찾은 index 값을 df_get_index_list 에 append
            else:
                continue

    # 존재하는 데이터의 index 값으로 duplicated_df 에서 drop 시키기
    for row in df_get_index_list:
        duplicated_df = duplicated_df.drop(row)

    duplicated_df_drop_df_first = duplicated_df.drop_duplicates(
        keep="first", subset=["고객주문번호"]
    )

    # db에 존재하지 않는 새로운 df를 db에 새롭게 저장
    for df_row in duplicated_df_drop_df_first.to_dict("records"):
        db_cursor = conn.cursor(pymysql.cursors.DictCursor)
        get_maxid_multi_sql = (
            "SELECT MAX(id) FROM multi_table"  # multi table에서 가장 큰 id 값 조회
        )
        db_cursor.execute(get_maxid_multi_sql)
        multi_table_maxid = db_cursor.fetchone()
        db_cursor.close()
        index_value = multi_table_maxid["MAX(id)"] + 1  # 가장 큰 id 값보다 1 증가한  id로 만들기
        new_df = duplicated_df.loc[df_row["고객주문번호"], :]
        new_df["고객주문번호"] = index_value  # 기존 인덱스 값을 가장 큰 id +1 값으로 변경
        reset_index_df = new_df.reset_index(drop=True)[["고객주문번호", "품목명", "내품수량"]]
        result = reset_index_df.to_dict("records")
        new_items_list = []
        for r in result:
            order_number = np.int64(
                r["고객주문번호"]
            )  # np.int64를 하는 이유는 mysql 이 numpy.int64 type을 받아들이지 못함
            product_name = r["품목명"]
            quantity = np.int64(r["내품수량"])
            item = (
                order_number.item(),
                product_name,
                quantity.item(),
            )  # np.int64 후 item 메소드를 이용하여 python int type으로 변경
            new_items_list.append(item)
        new_items_tuple = tuple(new_items_list)
        db_insert_cursor = conn.cursor()
        insert_multi_sql = "insert into multi_table(id, 품목명, 내품수량) values (%s, %s, %s)"
        db_insert_cursor.executemany(insert_multi_sql, new_items_tuple)
        db_insert_cursor.close()
        conn.commit()

    # db 접속 끊기
    conn.close()
    return
