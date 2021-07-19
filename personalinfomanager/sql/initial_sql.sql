CREATE TABLE IF NOT EXISTS hashtag (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    date DATE,
    description TEXT,
    hashtag integer,
    FOREIGN KEY (hashtag) references hashtag(id) ON DELETE CASCADE
);