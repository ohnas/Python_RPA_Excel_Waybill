import pandas as pd

row_df = pd.read_excel("read_sample.xlsx", engine="openpyxl")
select_df = row_df[
    ["상품주문번호", "수취인명", "옵션정보", "수량", "수취인연락처1", "수취인연락처2", "배송지", "배송메세지"]
]

select_df["내품명"] = ""
select_df["운임구분"] = "신용"
select_df["박스타입"] = "극소"
select_df["기본운임"] = 2050
select_df["보내는분성명"] = "몬스터moster"
select_df["보내는분주소(전체, 분할)"] = "인천 서구 가좌동 585-14 cj대한통운 인천가좌심곡대리점"
select_df["보내는분전화번호"] = "1522-8145"
select_df["보내는분기타연락처"] = ""

relocation_df = select_df[
    [
        "상품주문번호",
        "수취인명",
        "배송지",
        "수취인연락처1",
        "수취인연락처2",
        "옵션정보",
        "내품명",
        "수량",
        "배송메세지",
        "운임구분",
        "박스타입",
        "기본운임",
        "보내는분성명",
        "보내는분주소(전체, 분할)",
        "보내는분전화번호",
        "보내는분기타연락처",
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

# rename_df 에서 받는분섬명 , 받는분주소, 받는분전화번호를 기준으로 중복데이터 제거한 가공된 dataframe
drop_df = rename_df.drop_duplicates(
    keep=False, subset=["받는분성명", "받는분주소(전체,분할)", "받는분전화번호"]
)


# rename_df 에서 받는분섬명 , 받는분주소, 받는분전화번호를 기준으로 중복데이터만 골라낸 가공된 dataframe
duplicated_df = rename_df[
    rename_df.duplicated(keep=False, subset=["받는분성명", "받는분주소(전체,분할)", "받는분전화번호"])
]

# drop_df 와 duplicated_df 를 pd.concat 함수를 이용하여 병합하여, concat_df 로 만들어내기
concat_df = pd.concat([drop_df, duplicated_df])

concat_df.to_excel("test_sample.xlsx", index=False)
# duplicated_df.to_excel("test_sample1.xlsx", index=False)
