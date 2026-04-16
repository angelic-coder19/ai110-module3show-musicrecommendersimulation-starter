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

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Returns a weighted score in [0.0, 1.0] and a list of human-readable reasons.

    Weights: mood 0.35 | energy 0.25 | genre 0.20 | acousticness 0.12 | valence 0.08
    """
    score = 0.0
    reasons: List[str] = []

    # Mood match (weight: 0.35) — highest weight, strongest intent signal
    if user_prefs.get("mood") and user_prefs.get("mood") == song.get("mood"):
        score += 0.35
        reasons.append("mood match (+0.35)")

    # Energy proximity (weight: 0.25) — how close the song's energy is to the target
    energy_contribution = (1.0 - abs(user_prefs.get("energy", 0.5) - song.get("energy", 0.5))) * 0.25
    score += energy_contribution
    reasons.append(f"energy proximity (+{energy_contribution:.2f})")

    # Genre match (weight: 0.20) — penalized less than mood due to sparse catalog
    if user_prefs.get("genre") and user_prefs.get("genre") == song.get("genre"):
        score += 0.20
        reasons.append("genre match (+0.20)")

    # Acoustic direction score (weight: 0.12) — direction flip based on boolean preference
    acousticness = song.get("acousticness", 0.5)
    acoustic_raw = acousticness if user_prefs.get("likes_acoustic", True) else (1.0 - acousticness)
    acoustic_contribution = acoustic_raw * 0.12
    score += acoustic_contribution
    reasons.append(f"acoustic fit (+{acoustic_contribution:.2f})")

    # Valence proximity (weight: 0.08) — emotional positiveness, kept low to avoid mood overlap
    valence_contribution = (1.0 - abs(user_prefs.get("valence", 0.5) - song.get("valence", 0.5))) * 0.08
    score += valence_contribution
    reasons.append(f"valence proximity (+{valence_contribution:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Ranks all songs using score_song as the judge and returns the top k.
    Required by src/main.py
    """
    scored = sorted(
        [(song, *score_song(user_prefs, song)) for song in songs],
        key=lambda item: item[1],
        reverse=True
    )
    return [(song, score, ", ".join(reasons)) for song, score, reasons in scored[:k]]
