from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine

def insert_post(tags, uid, description, title):
    post_table, conn = initialize_db_connection("Post")
    ins = post_table.insert().values(tags=tags, uid=uid, description=description, likes=0, title=title)
    result = conn.execute(ins)  
    conn.close()
    return result.inserted_primary_key

def insert_comment(pid, uid, description, pcid):
    comment_table, conn = initialize_db_connection("Comment")
    ins = comment_table.insert().values(likes=0, uid=uid, parent_cid=pcid, text=description, post_pid=pid)
    result = conn.execute(ins)
    conn.close()
    return result.inserted_primary_key

def update_comment(cid, description):
    comment_table, conn = initialize_db_connection("Comment")
    upd = comment_table.update().values(cid=cid, text=description)
    conn.execute(upd)
    conn.close()

def delete_comment(cid):
    comment_table, conn = initialize_db_connection("Comment")
    upd = comment_table.delete().values(cid=cid)
    conn.execute(upd)
    conn.close()

def select_post(pid):
    post_table, conn = initialize_db_connection("Post")
    sel = post_table.select().where(post_table.c.pid==pid)
    result = conn.execute(sel)
    conn.close()
    return result.fetchone()


def select_comments_for_post(pid):
    comment_table, conn = initialize_db_connection("Comment")
    sel = comment_table.select().values(post_pid=pid)
    result = conn.execute(sel)
    conn.close()
    return result

def initialize_db_connection(table_name):
    engine = create_engine("mysql+pymysql://root:4tspicturhost@localhost/pictur")
    conn = engine.connect()
    meta = MetaData()
    meta.bind = engine
    table = Table(table_name, meta, autoload=True, autoload_with=engine)
    return table, conn


