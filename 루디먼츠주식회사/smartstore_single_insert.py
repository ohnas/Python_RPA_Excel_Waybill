import pymysql

from DB_auth import db_info

# gui 에서 받아온 tuple 을 인자로 사용하는 insert 함수
def single_table_isert(selection_items):
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
        get_maxid_single_sql = "SELECT MAX(id) FROM rudiments_samrtstore_single_table"  # singel table에서 가장 큰 id 값 조회
        db_cursor.execute(get_maxid_single_sql)
        single_table_maxid = db_cursor.fetchone()
        db_cursor.close()
        if single_table_maxid["MAX(id)"] == None:
            index_value = 1  # single table에 아무 데이터가 없다면 초기 id 값을 1로 설정해주어야함 데이터가 없으면 max id = none 으로 나오기 때문에
        else:
            index_value = (
                single_table_maxid["MAX(id)"] + 1
            )  # 가장 큰 id 값보다 1 증가한  id로 만들기
        post_item = (
            index_value,
            selection_items[0],
            selection_items[1],
            selection_items[2],
            selection_items[3],
        )
        db_insert_cursor = conn.cursor()
        insert_single_sql = "INSERT INTO rudiments_samrtstore_single_table(id, 품목명, 내품수량, 박스타입, 기본운임) VALUES (%s, %s , %s, %s, %s) "
        db_insert_cursor.execute(insert_single_sql, post_item)
        db_insert_cursor.close()
        conn.commit()
        # db 접속 끊기
        conn.close()
    except:
        print("오류가 있습니다 . 확인해보세요")
        conn.close()
    return
