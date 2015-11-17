from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine

def get_user_by_email(google_email):
    user_table, conn = initialize_db_connection("User")
    sel = user_table.select().where(user_table.c.email==google_email)
    result = conn.execute(sel)
    conn.close()
    return result.fetchone()
    
def get_user_by_uid(uid):
    user_table, conn = initialize_db_connection("User")
    sel = user_table.select().where(user_table.c.uid==uid)
    result = conn.execute(sel)
    conn.close()
    return result.fetchone()

def insert_user(nickname, email):
    user_table, conn = initialize_db_connection("User")
    ins = user_table.insert().values(nickname=nickname, email=email)
    result = conn.execute(ins)  
    conn.close()
    return result.inserted_primary_key
    
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
    upd = comment_table.update().where(comment_table.c.cid==cid).values(text=description)
    conn.execute(upd)
    conn.close()
    
def update_user(uid, nickname):
    user_table, conn = initialize_db_connection("User")
    upd = user_table.update().where(user_table.c.uid==uid).values(nickname=nickname)
    conn.execute(upd)
    conn.close()

def delete_post(pid):
    post_table, conn = initialize_db_connection("Post")
    del_post = post_table.delete().where(post_table.c.pid==pid)
    conn.execute(del_post)
    conn.close()
    
    comment_table, conn = initialize_db_connection("Comment")
    del_comments = comment_table.delete().where(comment_table.c.post_pid==pid)
    conn.execute(del_comments)
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
    result = reversed(conn.execute(sel).fetchall() )
    conn.close()
    return result

def select_n_post_offset(n, offset):
    post_table, conn = initialize_db_connection("Post")
    sel = post_table.select().order_by(post_table.c.time)
    result = list(reversed(conn.execute(sel).fetchall() ))
    conn.close()
    if n > len(result):
        offset, n = 0, len(result)
    elif n+offset > len(result):
        offset = len(result)-n
    elif offset < 0:
        offset = 0
    return result[offset:offset+n]

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
        reformat['uname'] = 'Anonymous'
        user = get_user_by_uid(comment[comment_table.c.uid])
        if user:
            reformat['uname'] = get_user_by_uid(comment[comment_table.c.uid])['nickname']
        reformat['parent_cid'] = comment[comment_table.c.parent_cid]
        reformat['post_pid'] = comment[comment_table.c.post_pid]
        reformat['children'] = []
        comments.append(reformat)
    base = []
    change = 1
    for comment in comments:
        if comment['parent_cid'] is None or comment['parent_cid'] == 0:
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
    return result
    
def get_comments_by_email(email):
    engine = create_engine("mysql+pymysql://root:4tspicturhost@localhost/pictur")
    conn = engine.connect()
    meta = MetaData()
    meta.bind = engine
    result = engine.execute("SELECT likes, text, time FROM Comment, User WHERE User.uid = Comment.uid AND User.email = %s", email)
    return result
    
    
def get_posts_commented_by_email(email):
    engine = create_engine("mysql+pymysql://root:4tspicturhost@localhost/pictur")
    conn = engine.connect()
    meta = MetaData()
    meta.bind = engine
    result = engine.execute("SELECT Post.pid, Post.title, Post.likes FROM Post, Comment, User WHERE Comment.uid = User.uid AND Comment.post_pid = Post.pid AND User.email = %s GROUP BY Post.pid", email)
    return result
    

def initialize_db_connection(table_name):
    engine = create_engine("mysql+pymysql://root:4tspicturhost@localhost/pictur")
    conn = engine.connect()
    meta = MetaData()
    meta.bind = engine
    table = Table(table_name, meta, autoload=True, autoload_with=engine)
    return table, conn