# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Beat Buddy 1.0
---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
  
  This model generates music recommendations based on a user's preferred genre, mood, and energy level. It suggests 3 to 5 songs from a small catalog that match those preferences.

- What assumptions does it make about the user  

    It assumes that the user's musical tastes can be captured by those three preferences and that they are looking for songs that closely match them.
    
    It also assumes that the user has exact knowledge of their preferences and that those preferences are static for the session.

- Is this for real users or classroom exploration  

    This model is for classroom exploration only, not for real users. It is a simplified simulation to help understand how recommenders work, rather than a production-ready system.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.) 
    The model uses the genre, energy level, mood, valence and acousticness of each song in the catalog of songs.

- What user preferences are considered  
    The model considers the user's preferred genre, mood (as a word like "Happy"), energy level (a number on a scale of 1 to 10), acousticness (as a choice yes or no) and valence (a number on a scale of 1 to 10).

- How does the model turn those into a score  
    The model calculates a score for each song based on how well it matches the user's preferences. It rewards songs that match the preferred genre, mood, energy level, acousticness and valence by adding points to the score. The songs with the highest scores are the ones that are recommended.

- What changes did you make from the starter logic  
    I changed the scoring logic to place more emphasis on mood rather than genre to add a hint of diversity to the recommendatiosn and allow the user to discover a new genre that they might like.

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
    The catalog contains 20 songs.

- What genres or moods are represented  
    genres: 
        pop
        lofi
        rock
        ambient
        jazz
        synthwave
        indie pop
        hip hop
        classical
        metal
        country
        reggae
        electronic
        folk
        rnb
        blues
        world
    
    moods:
        melancholic
        moody
        nostalgic
        playful
        relaxed
        romantic
        somber
        sultry
        uplifting
        chill
        intense
        happy 

- Did you add or remove data  
    I added 10 more songs
    Did not remove any data 

- Are there parts of musical taste missing in the dataset  
    Lyrics, Lexical density and language are not represented in the dataset
---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
    It gives reasonable results for users with clear preferences for genre, mood and energy level. For example, a user who prefers "Happy" mood, "Pop" genre and high energy level will get recommendations that closely match those preferences.

- Any patterns you think your scoring captures correctly  
    The scoring captures the idea that mood is a strong signal of musical taste, and that energy level can help differentiate between songs within the same genre. It also captures the idea that acousticness can be a desirable trait for some users and undesirable for others.

- Cases where the recommendations matched your intuition
    For a user who prefers "Relaxed" mood, "Jazz" genre and low energy level, the model recommended songs that are indeed relaxed jazz tracks with low energy, which felt right.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
