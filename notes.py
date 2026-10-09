import db

def add_note(title, content, user_id):
    sql = "INSERT INTO notes (title, content, user_id) VALUES (?, ?, ?)"
    db.execute(sql, [title, content, user_id])
    return db.last_insert_id()

def get_notes(user_id):
    sql = "SELECT id, title FROM notes WHERE user_id = ? ORDER By id DESC"
    return db.query(sql, [user_id])

def get_note(note_id):
    sql = "SELECT id, title, content, user_id FROM notes WHERE id = ?"
    result = db.query(sql, [note_id])
    return result[0] if result else None

def update_note(note_id, title, content):
    sql = "UPDATE notes SET title = ?, content = ? WHERE id = ?"
    db.execute(sql, [title, content, note_id])

def remove_note(note_id):
    sql = "DELETE FROM notes WHERE id = ?"
    db.execute(sql, [note_id])

def find_notes(query, user_id):
    #FLAW 3
    #sql = f"""SELECT id, title
    #          FROM notes
    #          WHERE user_id = ?
    #          AND (title LIKE '%{query}%' OR content LIKE '%{query}%')
    #          ORDER BY id DESC"""

    #return db.query(sql, [user_id])

    sql = """SELECT id, title
             FROM notes
            WHERE user_id = ?
             AND (title LIKE ? OR content LIKE ?)
             ORDER BY id DESC"""

    like = "%" + query + "%"
    return db.query(sql, [user_id, like, like])