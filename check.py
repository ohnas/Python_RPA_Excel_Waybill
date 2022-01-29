import pymysql
import pandas as pd
import DB_auth


def single_table_check():
    conn = pymysql.connect(
        db=DB_auth.info["db"],
        host=DB_auth.info["host"],
        user=DB_auth.info["user"],
        password=DB_auth.info["password"],
        port=DB_auth.info["port"],
        charset=DB_auth.info["charset"],
    )

    db_cursor = conn.cursor(pymysql.cursors.DictCursor)
    single_sql = "SELECT * FROM single_table"
    db_cursor.execute(single_sql)
    single_table_rows = db_cursor.fetchall()

    db_single_df = pd.DataFrame(single_table_rows)
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

    # set_index_df 에서 받는분섬명 , 받는분주소, 받는분전화번호를 기준으로 중복데이터 제거한 가공된 dataframe 을 dict type 으로 변환
    drop_duplicated_df = set_index_df.drop_duplicates(
        keep=False, subset=["받는분성명", "받는분주소(전체,분할)", "받는분전화번호"]
    ).to_dict("records")

    # dict 에서 for 문을 통해 1개씩 값을 꺼내 db_single_df에 값이 존재하는지 확인하고 값이 empty 이면 tuple type 으로 list 저장
    new_items = []
    for df_row in drop_duplicated_df:
        check_db_single_df = db_single_df[
            db_single_df["품목명"].isin([df_row["품목명"]])
            & db_single_df["내품수량"].isin([df_row["내품수량"]])
        ]
        if check_db_single_df.empty == True:
            item = (df_row["품목명"], df_row["내품수량"])
            new_items.append(item)
        else:
            continue

    # new_items 리스트에서 중복값이 있다면 new_items_list에 중복값 제거하고 새로 list 생성
    new_items_list = []
    for item in new_items:
        if item not in new_items_list:
            new_items_list.append(item)

    # new_items_list 에서 값을 하나씩 가져와서 db_single_table 의 max id 값보다 1씩 증가시켜서 db insert 시키기
    for item in new_items_list:
        db_cursor = conn.cursor(pymysql.cursors.DictCursor)
        get_maxid_single_sql = (
            "SELECT MAX(id) FROM single_table"  # singel table에서 가장 큰 id 값 조회
        )
        db_cursor.execute(get_maxid_single_sql)
        single_table_maxid = db_cursor.fetchone()
        db_cursor.close()
        index_value = single_table_maxid["MAX(id)"] + 1  # 가장 큰 id 값보다 1 증가한  id로 만들기
        post_item = (index_value, item[0], item[1])
        db_insert_cursor = conn.cursor()
        insert_single_sql = (
            "INSERT INTO single_table(id, 품목명, 내품수량) VALUES (%s, %s , %s) "
        )
        db_insert_cursor.execute(insert_single_sql, post_item)
        db_insert_cursor.close()
        conn.commit()

    # db 접속 끊기
    conn.close()
    return
