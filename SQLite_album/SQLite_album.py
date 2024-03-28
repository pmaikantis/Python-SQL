import db
from objects import Album, Genre
import re

def display_welcome():
    print("The Album List program")
    print()
    display_menu()

def display_menu():
    print("COMMAND MENU")
    print("genre - View albums by genre")
    print("year - View albums by year")
    print("artist - View artist by ID")
    print("list - List all albums")
    print("add - Add an album")
    print("add_genre - Add a new genre")
    print("remove_genre - Remove a genre")
    print("del - Delete an album")
    print("exit - Exit program")
    print()

def display_genres():
    print("GENRES")
    genres = db.get_genres()
    for genre in genres:
        print(f"{genre.id}. {genre.name}")
    print()

def display_albums(albums, genre_term):
    print(f"ALBUMS - {genre_term}\n")
    print(f"{'ID':<4}{'Title':<40}{'Artist':<27}"
          f"{'Year':<6}{'Length':<10}{'Tracks':<8}{'Genre':<15}")
    print("-" * 100)

    for album in albums:
        print(f"{album.id:<4}{album.title:<40}{album.artist_name:<27}"
              f"{album.year:<6}{album.length:<10}{album.tracks:<8}{album.genre_id:<15}")
    print()

def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid whole number. Please try again.\n")

def display_albums_by_genre():
    genre_id = get_int("Genre ID: ")
    genre = db.get_genre(genre_id)

    if genre is None:
        print("There is no genre with that ID.\n")
    else:
        print()
        albums = db.get_albums_by_genre(genre_id)
        display_albums(albums, genre.name.upper())

def display_albums_by_year():
    year = get_int("Year: ")
    print()
    albums = db.get_albums_by_year(year)
    display_albums(albums, str(year))

def display_artists_by_id():
    artist_id = get_int("Artist ID: ")
    artist = db.get_artist(artist_id)

    if artist is None:
        print("There is no artist with that ID.\n")
    else:
        print()
        print(f"ID: {artist.id}")
        print(f"Artist Name: {artist.artist_id}")
        print()

def list_all_albums():
    albums = db.get_all_albums()
    display_albums(albums, "All Albums")

def remove_genre_from_db():
    genre_id = get_int("Genre ID: ")
    if db.get_genre(genre_id) is not None:
        db.remove_genre(genre_id)
        print(f"Genre ID {genre_id} was removed from the database.\n")
    else:
        print("There is no genre with that ID.\n")

def get_time(prompt):
    while True:
        time_str = input(prompt)
        if re.match(r'^\d{2}:\d{2}$', time_str):
            return time_str
        else:
            print("Invalid time format. Please enter in 00:00 format.")

def add_album():
    title = input("Title: ")
    artist_name = input("Artist Name: ")

    
    artist = db.get_artist_by_name(artist_name)

    if artist is None:
        
        artist_id = db.add_artist(artist_name)
    else:
        artist_id = artist.id  

    year = get_int("Year: ")

    while True:
        length_input = get_time("Length (00:00): ")
        if length_input:
            length = length_input
            break
        else:
            print("Invalid time format. Please enter in 00:00 format.")

    tracks = get_int("Tracks: ")  

    genre_id = get_int("Genre ID: ") 

    album = Album(
        title=title,
        artist_id=artist_id,
        year=year,
        length=length,
        tracks=tracks, 
        genre_id=genre_id  
    )

    db.add_album(album)
    print(f"{title} was added to the database.\n")

def add_artist_album():
    try:
        artist_id = get_int("Artist ID: ")
        if db.get_artist(artist_id) is None:
            print("Artist ID not found. Please add the artist first.")
            return

        title = input("Title: ")
        year = get_int("Year: ")
        length = get_time("Length (00:00): ")
        tracks = get_int("Tracks: ")

        genre_id = None
        while genre_id is None:
            genre_id = get_int("Genre ID: ")
            if db.get_genre(genre_id) is None:
                print("Invalid genre ID. Please try again.")
                genre_id = None

        album = Album(
            title=title,
            artist_id=artist_id,
            year=year,
            length=length,
            tracks=tracks,
            genre_id=genre_id,
        )

        db.add_album(album)
        print(f"{title} by Artist ID {artist_id} was added to the database.\n")
    except ValueError:
        print("Invalid input. Please make sure to enter whole numbers for year, length, tracks, and genre ID.\n")
    
import db
from objects import Album, Genre, Artist

def add_artist_album():
    try:
        artist_id = get_int("Artist ID: ")
        if db.get_artist(artist_id) is None:
            print("Artist ID not found. Please add the artist first.")
            return

        title = input("Title: ")
        year = get_int("Year: ")
        length = get_int("Length (minutes): ")
        tracks = get_int("Tracks: ")

        genre_id = None
        while genre_id is None:
            genre_id = get_int("Genre ID: ")
            if db.get_genre(genre_id) is None:
                print("Invalid genre ID. Please try again.")
                genre_id = None

        album = Album(
            title=title,
            artist_id=artist_id,
            year=year,
            length=length,
            tracks=tracks,
            genre_id=genre_id,
        )

        db.add_album(album)
        print(f"{title} by Artist ID {artist_id} was added to the database.\n")
    except ValueError:
        print("Invalid input. Please make sure to enter whole numbers for year, length, tracks, and genre ID.\n")

def add_genre():
    genre_name = input("Genre Name: ")
    genre = Genre(name=genre_name)
    db.add_genre(genre)
    print(f"Genre '{genre_name}' was added to the database.\n")

def delete_album():
    album_id = get_int("Album ID: ")
    db.delete_album(album_id)
    print(f"Album ID {album_id} was deleted from the database.\n")

def main():
    db.connect()
    display_welcome()
    display_genres()

    while True:
        command = input("Command: ").lower()
        if command == "genre":
            display_albums_by_genre()
        elif command == "year":
            display_albums_by_year()
        elif command == "artist":
            display_artists_by_id()
        elif command == "list":
            list_all_albums()
        elif command == "add":
            add_album()
        elif command == "add_genre":
            add_genre()
        elif command == "remove_genre":
            remove_genre_from_db()
        elif command == "del":
            delete_album()
        elif command == "exit":
            break
        else:
            print("Not a valid command. Please try again.\n")
            display_menu()

    db.close()
    print("Bye!")

if __name__ == "__main__":
    main()
