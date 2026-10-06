CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE, 
    password_hash TEXT
);

CREATE TABLE notes (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title TEXT, 
    content TEXT 
);
