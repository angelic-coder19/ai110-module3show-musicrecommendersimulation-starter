"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from pathlib import Path

try:
    from .recommender import load_songs, recommend_songs
except Exception:
    from recommender import load_songs, recommend_songs


def main() -> None:
    # Resolve the songs path relative to the project root so this works
    # when running from the project root or from the `src` directory.
    project_root = Path(__file__).resolve().parent.parent
    songs_path = project_root / "data" / "songs.csv"
    songs = load_songs(str(songs_path))

    # Taste profile: late-night study session
    # Someone who wants calm, acoustic-leaning music to focus with
    user_prefs = {
        "genre":          "lofi",    # preferred genre
        "mood":           "focused", # preferred mood
        "energy":         0.42,      # target energy level (calm but not silent)
        "likes_acoustic": True,      # prefers organic/acoustic texture over produced sound
        "valence":        0.58,      # moderately positive — not too bright, not melancholic
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
