import pymysql

from DB_auth import db_info

# gui 에서 받아온 list 을 인자로 사용하는 insert 함수
def multi_table_isert(selection_items):
    try:
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
        get_maxid_multi_sql = "SELECT MAX(id) FROM rudiments_samrtstore_multi_table"  # multi table에서 가장 큰 id 값 조회
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
        insert_multi_sql = "insert into rudiments_samrtstore_multi_table(id, 품목명, 내품수량, 박스타입, 기본운임) VALUES (%s, %s , %s, %s, %s)"
        db_insert_cursor.executemany(insert_multi_sql, post_items_tuple)
        db_insert_cursor.close()
        conn.commit()
        # db 접속 끊기
        conn.close()
    except:
        print("오류가 있습니다 . 확인해보세요")
        conn.close()
    return
