from os import dup
import time
import pymysql
import pandas as pd
from pymysql.cursors import DictCursor
import DB_auth

start = time.time()

# db 접속정보를 DB_auth.py에서 불러와서 입력해놓기
conn = pymysql.connect(
    db=DB_auth.info["db"],
    host=DB_auth.info["host"],
    user=DB_auth.info["user"],
    password=DB_auth.info["password"],
    port=DB_auth.info["port"],
    charset=DB_auth.info["charset"],
)

row_df = pd.read_excel("read_sample.xlsx", engine="openpyxl")
select_df = row_df[
    ["상품주문번호", "수취인명", "옵션정보", "수량", "수취인연락처1", "수취인연락처2", "배송지", "배송메세지"]
]

relocation_df = select_df[
    [
        "상품주문번호",
        "수취인명",
        "배송지",
        "수취인연락처1",
        "수취인연락처2",
        "옵션정보",
        "수량",
        "배송메세지",
    ]
]
rename_df = relocation_df.rename(
    columns={
        "상품주문번호": "고객주문번호",
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
drop_df = set_index_df.drop_duplicates(
    keep=False, subset=["받는분성명", "받는분주소(전체,분할)", "받는분전화번호"]
)


# set_index_df 에서 받는분섬명 , 받는분주소, 받는분전화번호를 기준으로 중복데이터만 골라낸 가공된 dataframe
""" duplicated_df = set_index_df[
    rename_df.duplicated(keep=False, subset=["받는분성명", "받는분주소(전체,분할)", "받는분전화번호"])
] """

# db에 접속해서 활동하기 db에서 활동하는 cursor를 Dict cursor 로 설정
cur = conn.cursor(pymysql.cursors.DictCursor)
sql = "SELECT * FROM testtable"
cur.execute(sql)


while True:
    db_row = cur.fetchone()
    if db_row == None:
        break
    for df_row in drop_df.to_dict("records"):
        if df_row["품목명"] == db_row["품목명"] and df_row["내품수량"] == db_row["내품수량"]:
            drop_df.at[df_row["고객주문번호"], "운임구분"] = db_row["운임구분"]
            drop_df.at[df_row["고객주문번호"], "박스타입"] = db_row["박스타입"]
            drop_df.at[df_row["고객주문번호"], "기본운임"] = db_row["기본운임"]
            drop_df.at[df_row["고객주문번호"], "보내는분성명"] = db_row["보내는분성명"]
            drop_df.at[df_row["고객주문번호"], "보내는분주소(전체, 분할)"] = db_row["보내는분주소(전체, 분할)"]
            drop_df.at[df_row["고객주문번호"], "보내는분전화번호"] = db_row["보내는분전화번호"]
            drop_df.at[df_row["고객주문번호"], "보내는분기타연락처"] = db_row["보내는분기타연락처"]
        else:
            continue

conn.close()

drop_df.to_excel("test_sample.xlsx", index=False)
print(time.time() - start)

# drop_df 와 duplicated_df 를 pd.concat 함수를 이용하여 병합하여, concat_df 로 만들어내기
# concat_df = pd.concat([drop_df, duplicated_df])

# concat_df를 엑셀파일로 만들어내기
# concat_df.to_excel("test_sample.xlsx", index=False)
