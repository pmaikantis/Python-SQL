# objects.py

from dataclasses import dataclass

@dataclass
class Genre:
    id: int = 0
    name: str = ""

@dataclass
class Artist:
    id: int = 0
    artist_id: int = 0
    first_name: str = ""
    last_name: str = ""

@dataclass
@dataclass
class Album:
    id: int = 0
    title: str = ""
    artist_id: int = 0
    artist_name: str = ""
    year: int = 0
    length: str = ""
    tracks: int = 0
    genre_id: int = 0



