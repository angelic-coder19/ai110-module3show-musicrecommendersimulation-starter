"""
Tests for the procedural recommender implementation.
Covers: score_song, recommend_songs, load_songs
"""
import pytest
from pathlib import Path
import sys

# Ensure the project root is on sys.path so the `src` package can be imported
# when running this test file directly (e.g. `python tests\test_recommender.py`).
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.recommender import score_song, recommend_songs, load_songs


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def pop_song():
    return {
        "id": 1, "title": "Sunrise City", "artist": "Neon Echo",
        "genre": "pop", "mood": "happy",
        "energy": 0.82, "valence": 0.84, "acousticness": 0.18,
        "tempo_bpm": 118, "danceability": 0.79,
    }

@pytest.fixture
def lofi_song():
    return {
        "id": 2, "title": "Midnight Coding", "artist": "LoRoom",
        "genre": "lofi", "mood": "chill",
        "energy": 0.42, "valence": 0.56, "acousticness": 0.71,
        "tempo_bpm": 78, "danceability": 0.62,
    }

@pytest.fixture
def pop_prefs():
    """User preferences that strongly favour pop_song."""
    return {
        "genre": "pop", "mood": "happy",
        "energy": 0.82, "likes_acoustic": False, "valence": 0.84,
    }

@pytest.fixture
def two_songs(pop_song, lofi_song):
    return [pop_song, lofi_song]

@pytest.fixture
def csv_path():
    return Path(__file__).resolve().parents[1] / "data" / "songs.csv"


# ── score_song: return type ───────────────────────────────────────────────────

def test_score_song_score_is_float(pop_prefs, pop_song):
    score, _ = score_song(pop_prefs, pop_song)
    assert isinstance(score, float)

def test_score_song_reasons_is_list_of_strings(pop_prefs, pop_song):
    _, reasons = score_song(pop_prefs, pop_song)
    assert isinstance(reasons, list)
    assert all(isinstance(r, str) for r in reasons)


# ── score_song: score range ───────────────────────────────────────────────────

def test_score_song_is_never_negative(pop_prefs, pop_song):
    score, _ = score_song(pop_prefs, pop_song)
    assert score >= 0.0

def test_score_song_never_exceeds_one(pop_prefs, pop_song):
    score, _ = score_song(pop_prefs, pop_song)
    assert score <= 1.0

def test_score_song_near_perfect_match_approaches_one(pop_prefs, pop_song):
    score, _ = score_song(pop_prefs, pop_song)
    assert score >= 0.95


# ── score_song: mood feature ──────────────────────────────────────────────────

def test_mood_match_adds_point_35(pop_song):
    prefs_match    = {"mood": "happy", "energy": 0.5, "valence": 0.5}
    prefs_mismatch = {"mood": "chill", "energy": 0.5, "valence": 0.5}
    score_match,    _ = score_song(prefs_match,    pop_song)
    score_mismatch, _ = score_song(prefs_mismatch, pop_song)
    assert score_match - score_mismatch == pytest.approx(0.35, abs=1e-6)

def test_mood_match_appears_in_reasons(pop_prefs, pop_song):
    _, reasons = score_song(pop_prefs, pop_song)
    assert any("mood match" in r for r in reasons)

def test_mood_mismatch_absent_from_reasons(lofi_song):
    prefs = {"mood": "happy", "energy": 0.5, "valence": 0.5}
    _, reasons = score_song(prefs, lofi_song)
    assert not any("mood match" in r for r in reasons)


# ── score_song: genre feature ─────────────────────────────────────────────────

def test_genre_match_adds_point_20(pop_song):
    prefs_match    = {"genre": "pop",  "energy": 0.5, "valence": 0.5}
    prefs_mismatch = {"genre": "lofi", "energy": 0.5, "valence": 0.5}
    score_match,    _ = score_song(prefs_match,    pop_song)
    score_mismatch, _ = score_song(prefs_mismatch, pop_song)
    assert score_match - score_mismatch == pytest.approx(0.20, abs=1e-6)

def test_genre_match_appears_in_reasons(pop_prefs, pop_song):
    _, reasons = score_song(pop_prefs, pop_song)
    assert any("genre match" in r for r in reasons)

def test_genre_mismatch_absent_from_reasons(lofi_song):
    prefs = {"genre": "pop", "energy": 0.5, "valence": 0.5}
    _, reasons = score_song(prefs, lofi_song)
    assert not any("genre match" in r for r in reasons)


# ── score_song: energy proximity ──────────────────────────────────────────────

def test_energy_always_contributes_a_reason(pop_prefs, pop_song):
    _, reasons = score_song(pop_prefs, pop_song)
    assert any("energy" in r for r in reasons)

def test_closer_energy_scores_higher(pop_song):
    prefs_near = {"energy": 0.82, "valence": 0.5}  # matches pop_song energy exactly
    prefs_far  = {"energy": 0.10, "valence": 0.5}
    score_near, _ = score_song(prefs_near, pop_song)
    score_far,  _ = score_song(prefs_far,  pop_song)
    assert score_near > score_far

def test_perfect_energy_match_contributes_point_25():
    # Use energy=0.0 vs energy=1.0 to get maximum possible distance (diff = 0.25)
    song = {"genre": "", "mood": "", "energy": 0.0, "valence": 0.5, "acousticness": 0.5}
    prefs_exact = {"energy": 0.0, "valence": 0.5}   # distance = 0 → contribution = 0.25
    prefs_worst = {"energy": 1.0, "valence": 0.5}   # distance = 1 → contribution = 0.00
    score_exact, _ = score_song(prefs_exact, song)
    score_worst, _ = score_song(prefs_worst, song)
    assert score_exact - score_worst == pytest.approx(0.25, abs=1e-6)


# ── score_song: acousticness direction ───────────────────────────────────────

def test_acoustic_always_contributes_a_reason(pop_prefs, pop_song):
    _, reasons = score_song(pop_prefs, pop_song)
    assert any("acoustic" in r for r in reasons)

def test_likes_acoustic_rewards_high_acousticness():
    song = {"genre": "", "mood": "", "energy": 0.5, "valence": 0.5, "acousticness": 1.0}
    score_likes,    _ = score_song({"energy": 0.5, "valence": 0.5, "likes_acoustic": True},  song)
    score_dislikes, _ = score_song({"energy": 0.5, "valence": 0.5, "likes_acoustic": False}, song)
    assert score_likes > score_dislikes

def test_dislikes_acoustic_rewards_low_acousticness():
    song = {"genre": "", "mood": "", "energy": 0.5, "valence": 0.5, "acousticness": 0.0}
    score_dislikes, _ = score_song({"energy": 0.5, "valence": 0.5, "likes_acoustic": False}, song)
    score_likes,    _ = score_song({"energy": 0.5, "valence": 0.5, "likes_acoustic": True},  song)
    assert score_dislikes > score_likes


# ── score_song: valence proximity ─────────────────────────────────────────────

def test_valence_always_contributes_a_reason(pop_prefs, pop_song):
    _, reasons = score_song(pop_prefs, pop_song)
    assert any("valence" in r for r in reasons)

def test_closer_valence_scores_higher(pop_song):
    prefs_near = {"energy": 0.5, "valence": 0.84}  # matches pop_song valence exactly
    prefs_far  = {"energy": 0.5, "valence": 0.10}
    score_near, _ = score_song(prefs_near, pop_song)
    score_far,  _ = score_song(prefs_far,  pop_song)
    assert score_near > score_far


# ── recommend_songs: result shape ─────────────────────────────────────────────

def test_recommend_returns_k_results(pop_prefs, two_songs):
    results = recommend_songs(pop_prefs, two_songs, k=1)
    assert len(results) == 1

def test_recommend_returns_all_when_k_equals_catalog_size(pop_prefs, two_songs):
    results = recommend_songs(pop_prefs, two_songs, k=2)
    assert len(results) == 2

def test_recommend_each_item_is_song_score_explanation(pop_prefs, two_songs):
    for song, score, explanation in recommend_songs(pop_prefs, two_songs, k=2):
        assert isinstance(song, dict)
        assert isinstance(score, float)
        assert isinstance(explanation, str)


# ── recommend_songs: ranking ──────────────────────────────────────────────────

def test_recommend_scores_are_descending(pop_prefs, two_songs):
    scores = [score for _, score, _ in recommend_songs(pop_prefs, two_songs, k=2)]
    assert scores == sorted(scores, reverse=True)

def test_recommend_best_match_is_first(pop_prefs, two_songs, pop_song):
    top_song, _, _ = recommend_songs(pop_prefs, two_songs, k=2)[0]
    assert top_song["title"] == pop_song["title"]

def test_recommend_explanation_is_nonempty(pop_prefs, two_songs):
    _, _, explanation = recommend_songs(pop_prefs, two_songs, k=1)[0]
    assert explanation.strip() != ""


# ── recommend_songs: edge cases ───────────────────────────────────────────────

def test_recommend_k_larger_than_catalog_returns_all(pop_prefs, two_songs):
    results = recommend_songs(pop_prefs, two_songs, k=100)
    assert len(results) == len(two_songs)

def test_recommend_k_zero_returns_empty(pop_prefs, two_songs):
    results = recommend_songs(pop_prefs, two_songs, k=0)
    assert results == []


# ── load_songs: data integrity ────────────────────────────────────────────────

def test_load_songs_returns_list(csv_path):
    songs = load_songs(str(csv_path))
    assert isinstance(songs, list)

def test_load_songs_correct_count(csv_path):
    songs = load_songs(str(csv_path))
    assert len(songs) == 20

def test_load_songs_each_item_is_dict(csv_path):
    songs = load_songs(str(csv_path))
    assert all(isinstance(s, dict) for s in songs)

def test_load_songs_energy_fields_are_floats(csv_path):
    songs = load_songs(str(csv_path))
    assert all(isinstance(s["energy"], float) for s in songs)

def test_load_songs_id_fields_are_ints(csv_path):
    songs = load_songs(str(csv_path))
    assert all(isinstance(s["id"], int) for s in songs if s.get("id") is not None)

def test_load_songs_first_title_is_known(csv_path):
    songs = load_songs(str(csv_path))
    assert songs[0]["title"] == "Sunrise City"


# ── load_songs: error handling ────────────────────────────────────────────────

def test_load_songs_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_songs("nonexistent.csv")
