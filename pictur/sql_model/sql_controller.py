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

def select_n_post(n):
    post_table, conn = initialize_db_connection("Post")
    sel = post_table.select().order_by(post_table.c.time).limit(n)
    result = conn.execute(sel)
    conn.close()
    return result


def select_comments_for_post(pid):
    comment_table, conn = initialize_db_connection("Comment")
    sel = comment_table.select().where(comment_table.c.post_pid==pid)
    result = conn.execute(sel)
    conn.close()
    comments = []
    for comment in result:
        reformat = {}
        reformat['cid'] = comment[comment_table.c.cid]
        reformat['likes'] = comment[comment_table.c.likes]
        reformat['text'] = comment[comment_table.c.text]
        reformat['time'] = comment[comment_table.c.time]
        reformat['uid'] = comment[comment_table.c.uid]
        reformat['parent_cid'] = comment[comment_table.c.parent_cid]
        reformat['post_pid'] = comment[comment_table.c.post_pid]
        reformat['children'] = []
        comments.append(reformat)
    base = []
    change = 1
    for comment in comments:
        if comment['parent_cid'] is None:
            base.append(comment)
        else:
            for p_comment in comments:
                if p_comment['cid'] == comment['parent_cid']:
                    p_comment['children'].append(comment)
    return base

def tag_search(tag, n):
    post_table, conn = initialize_db_connection("Post")
    sel = post_table.select().where(post_table.c.tags.contains(tag)).limit(n)
    result = conn.execute(sel)
    ids = []
    for post in result:
        ids.append(post['pid'])
    return ids

def initialize_db_connection(table_name):
    engine = create_engine("mysql+pymysql://root:4tspicturhost@localhost/pictur")
    conn = engine.connect()
    meta = MetaData()
    meta.bind = engine
    table = Table(table_name, meta, autoload=True, autoload_with=engine)
    return table, conn