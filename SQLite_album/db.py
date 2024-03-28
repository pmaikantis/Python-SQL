from contextlib import closing
import sqlite3
from objects import Genre, Artist, Album

conn = None

def connect():
    global conn
    if not conn:
        DB_FILE = "albums.sqlite"  
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row

def close():
    if conn:
        conn.close()

def make_genre(row):
    return Genre(row["genreID"], row["name"])

def make_artist(row):
    return Artist(row["artistID"], row["artist_name"])

def add_artist(artist_name):
    sql = "INSERT INTO Artist (artist_name) VALUES (?)"
    with closing(conn.cursor()) as c:
        
        c.execute(sql, (artist_name,))
        conn.commit()

def get_artist_by_name(artist_name):
    query = "SELECT artistID, artist_name FROM Artist WHERE artist_name = ?"
    with closing(conn.cursor()) as c:
        c.execute(query, (artist_name,))
        row = c.fetchone()
        if row:
            return make_artist(row)
        else:
            return None

def make_album(row):
    return Album(
        row["albumID"],  
        row["title"],
        row["artist_name"],
        row["year"],
        row["length"],
        row["tracks"],
    )

def get_genres():
    query = "SELECT genreID, name FROM Genre"
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

    return [make_genre(row) for row in results]

def get_genre(genre_id):
    query = "SELECT genreID, name FROM Genre WHERE genreID = ?"
    with closing(conn.cursor()) as c:
        c.execute(query, (genre_id,))
        row = c.fetchone()
        if row:
            return make_genre(row)
        else:
            return None

def get_artists():
    query = "SELECT artistID, artist_name FROM Artist"
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

    return [make_artist(row) for row in results]

def get_artist(artist_id):
    query = "SELECT artistID, artist_name FROM Artist WHERE artistID = ?"
    with closing(conn.cursor()) as c:
        c.execute(query, (artist_id,))
        row = c.fetchone()
        if row:
            return make_artist(row)
        else:
            return None

def get_albums_by_genre(genre_id):
    query = """
    SELECT Album.albumID, Album.title, Album.artistID, Album.year,
           Album.length, Album.tracks, Album.genreID, Artist.artist_name
    FROM Album
    JOIN Artist ON Album.artistID = Artist.artistID
    WHERE Album.genreID = ?
    """
    with closing(conn.cursor()) as c:
        c.execute(query, (genre_id,))
        results = c.fetchall()

    return [make_album(row) for row in results]

def get_albums_by_year(year):
    query = """
    SELECT Album.albumID, Album.title, Album.artistID, Album.year,
           Album.length, Album.tracks, Album.genreID, Artist.artist_name
    FROM Album
    JOIN Artist ON Album.artistID = Artist.artistID
    WHERE Album.year = ?
    """
    with closing(conn.cursor()) as c:
        c.execute(query, (year,))
        results = c.fetchall()

    return [make_album(row) for row in results]

def get_all_albums():
    query = """
    SELECT Album.albumID, Album.title, Album.artistID, Album.year,
           Album.length, Album.tracks, Album.genreID, Artist.artist_name
    FROM Album
    JOIN Artist ON Album.artistID = Artist.artistID
    """
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

    return [make_album(row) for row in results]

def add_album(album):
    sql = """
    INSERT INTO Album (title, artistID, year, length, tracks, genreID)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    with closing(conn.cursor()) as c:
        c.execute(
            sql,
            (
                album.title,
                album.artist_id,
                album.year,
                album.length,
                album.tracks,
                album.genre_id,
            ),
        )
        conn.commit()

def delete_album(album_id):
    sql = "DELETE FROM Album WHERE albumID = ?"
    with closing(conn.cursor()) as c:
        c.execute(sql, (album_id,))
        conn.commit()

def add_genre(genre):
    sql = "INSERT INTO Genre (name) VALUES (?)"
    with closing(conn.cursor()) as c:
        c.execute(sql, (genre.name,))
        conn.commit()

def remove_genre(genre_id):
    sql = "DELETE FROM Genre WHERE genreID = ?"
    with closing(conn.cursor()) as c:
        c.execute(sql, (genre_id,))
        conn.commit()
