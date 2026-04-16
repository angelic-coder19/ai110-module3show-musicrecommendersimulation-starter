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

"""
USER PREFERENCES
different tast profiles
"""
STUDY_FOCUS =  {
        "genre":          "lofi",    # preferred genre
        "mood":           "focused", # preferred mood
        "energy":         0.42,      # target energy level (calm but not silent)
        "likes_acoustic": True,      # prefers organic/acoustic texture over produced sound
        "valence":        0.58,      # moderately positive — not too bright, not melancholic
    }

HIGH_ENERGY_POP = {
        "genre":          "pop",    # preferred genre
        "mood":           "happy", # preferred mood
        "energy":         0.70,      # target energy level (calm but not silent)
        "likes_acoustic": False,      # prefers organic/acoustic texture over produced sound
        "valence":        0.22,      # moderately positive — not too bright, not melancholic
    }

DEEP_INTENSE_ROCK = {
        "genre":          "rock",    # preferred genre
        "mood":           "intense", # preferred mood
        "energy":         0.90,      # target energy level (calm but not silent)
        "likes_acoustic": False,      # prefers organic/acoustic texture over produced sound
        "valence":        0.46,      # moderately positive — not too bright, not melancholic
    }


def main() -> None:
    # Resolve the songs path relative to the project root so this works
    # when running from the project root or from the `src` directory.
    project_root = Path(__file__).resolve().parent.parent
    songs_path = project_root / "data" / "songs.csv"
    songs = load_songs(str(songs_path))

    user_prefs = STUDY_FOCUS 


    recommendations = recommend_songs(user_prefs, songs, k=5)

    # ── Header ────────────────────────────────────────────
    W = 54
    DIV = "-" * W
    acoustic_label = "Yes" if user_prefs["likes_acoustic"] else "No"

    print(f"\n{DIV}")
    print(f"  BEATS BUDDY 1.0")
    print(DIV)
    print()
    print("  Your Taste Profile")
    print(f"  {'Genre':<10}: {user_prefs['genre']:<14}  {'Acoustic':<10}: {acoustic_label}")
    print(f"  {'Mood':<10}: {user_prefs['mood']:<14}  {'Valence':<10}: {user_prefs['valence']}")
    print(f"  {'Energy':<10}: {user_prefs['energy']}")
    print()

    # ── Results ───────────────────────────────────────────
    print(DIV)
    print(f"  Top {len(recommendations)} Recommendations  ({len(songs)} songs scored)")
    print(DIV)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        bar = "#" * int(score * 20)
        print(f"\n  #{rank}  {song['title']}  -  {song['artist']}")
        print(f"       Score  : {score:.2f}  [{bar:<20}]")
        print(f"       Genre  : {song['genre']:<12}  Mood : {song['mood']}")
        print(f"       Why    :", end="")
        for i, reason in enumerate(explanation.split(", ")):
            prefix = " " if i == 0 else " " * 15
            print(f"{prefix}{reason}")

    print(f"\n{DIV}\n")


if __name__ == "__main__":
    main()
