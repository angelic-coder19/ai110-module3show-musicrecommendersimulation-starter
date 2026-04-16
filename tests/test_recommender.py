from pathlib import Path

from src.recommender import Song, UserProfile, Recommender, load_songs

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_load_songs_from_relative_data_path():
    # Ensure load_songs can read the project's data/songs.csv using a relative path
    songs = load_songs("data/songs.csv")
    assert isinstance(songs, list)
    assert len(songs) > 0
    first = songs[0]
    assert isinstance(first, dict)
    # Verify we parsed a known title from the CSV
    assert first.get('title') == "Sunrise City"


def test_load_songs_from_absolute_path_and_types():
    # Build an absolute path to the data file based on this test file location
    csv_path = Path(__file__).resolve().parents[1] / "data" / "songs.csv"
    songs = load_songs(str(csv_path))
    assert len(songs) == 10
    # Verify numeric fields were converted correctly
    ids = [s['id'] for s in songs if s.get('id') is not None]
    assert all(isinstance(i, int) for i in ids)
    assert all(isinstance(s.get('energy'), float) for s in songs)


def test_load_songs_missing_file_raises():
    import pytest

    with pytest.raises(FileNotFoundError):
        load_songs("this_file_does_not_exist.csv")
