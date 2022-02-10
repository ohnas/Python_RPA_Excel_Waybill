import pymysql

from DB_auth import db_info

# gui 에서 받아온 list 을 인자로 사용하는 insert 함수
def multi_table_isert(selection_items):
    info = db_info()
    conn = pymysql.connect(
        db=info["db"],
        host=info["host"],
        user=info["user"],
        password=info["password"],
        port=info["port"],
        charset=info["charset"],
    )
    db_cursor = conn.cursor(pymysql.cursors.DictCursor)
    get_maxid_multi_sql = (
        "SELECT MAX(id) FROM multi_table"  # multi table에서 가장 큰 id 값 조회
    )
    db_cursor.execute(get_maxid_multi_sql)
    multi_table_maxid = db_cursor.fetchone()
    db_cursor.close()
    index_value = multi_table_maxid["MAX(id)"] + 1  # 가장 큰 id 값보다 1 증가한  id로 만들기
    post_items = []
    for item in selection_items:
        post_item = (
            index_value,
            item[0],
            item[1],
            item[2],
            item[3],
        )
        post_items.append(post_item)
    post_items_tuple = tuple(post_items)
    db_insert_cursor = conn.cursor()
    insert_multi_sql = "insert into multi_table(id, 품목명, 내품수량, 박스타입, 기본운임) VALUES (%s, %s , %s, %s, %s)"
    db_insert_cursor.executemany(insert_multi_sql, post_items_tuple)
    db_insert_cursor.close()
    conn.commit()
    # db 접속 끊기
    return conn.close()


""" duplicated_df_drop_df_first = duplicated_df.drop_duplicates(
    keep="first", subset=["고객주문번호"]
)

# db에 존재하지 않는 새로운 df를 db에 새롭게 저장
for df_row in duplicated_df_drop_df_first.to_dict("records"):
    db_cursor = conn.cursor(pymysql.cursors.DictCursor)



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
    new_items_tuple = tuple(new_items_list) """
