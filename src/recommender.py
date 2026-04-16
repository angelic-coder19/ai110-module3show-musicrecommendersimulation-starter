from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv
from pathlib import Path

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []

    print(f"Loading songs from {csv_path}...")
    path = Path(csv_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Songs CSV not found: {csv_path}")
    
        
    with path.open(newline='', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            # Normalize and convert types
            try:
                song = {
                    'id': int(row.get('id', '').strip()) if row.get('id') is not None and row.get('id').strip() != '' else None,
                    'title': row.get('title', '').strip(),
                    'artist': row.get('artist', '').strip(),
                    'genre': row.get('genre', '').strip(),
                    'mood': row.get('mood', '').strip(),
                    'energy': float(row.get('energy', 0.0)) if row.get('energy') not in (None, '') else 0.0,
                    'tempo_bpm': float(row.get('tempo_bpm', 0.0)) if row.get('tempo_bpm') not in (None, '') else 0.0,
                    'valence': float(row.get('valence', 0.0)) if row.get('valence') not in (None, '') else 0.0,
                    'danceability': float(row.get('danceability', 0.0)) if row.get('danceability') not in (None, '') else 0.0,
                    'acousticness': float(row.get('acousticness', 0.0)) if row.get('acousticness') not in (None, '') else 0.0,
                }
            except ValueError:
                # Skip rows with bad numeric values
                continue

            songs.append(song)

    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # TODO: Implement scoring and ranking logic
    # Expected return format: (song_dict, score, explanation)
    return []
