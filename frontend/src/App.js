import React, { useState } from 'react';
import axios from 'axios';

function App() {
  // state hooks, manages values of genre, keywords, rec, and error
  const [genre, setGenre] = useState('');
  const [keywords, setKeywords] = useState('');
  const [recommendation, setRecommendation] = useState({});
  const [error, setError] = useState('');

  // event handling function
  // when 'get rec' button is clicked
  const handleRecommendation = async () => {
    try {
      const response = await axios.post('http://localhost:5000/recommend', {
        genre: genre,
        keywords: keywords,
      });
      setRecommendation(response.data);
      setError('');
    } catch (error) {
      setError('Error fetching recommendation');
      setRecommendation({});
    }
  };

  // UI 
  return (
    <div>
      <h1>My Book Recommender</h1>
      <div>
        <label>Enter a genre you are interested in reading: </label>
        <input
          type="text"
          value={genre}
          onChange={(e) => setGenre(e.target.value)}
        />
      </div>
      <div>
        <label>Enter keyword(s) that interest you (comma-separated): </label>
        <input
          type="text"
          value={keywords}
          onChange={(e) => setKeywords(e.target.value)}
        />
      </div>
      <div>
        <button onClick={handleRecommendation}>Get Recommendation</button>
      </div>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {recommendation.title && (
        <div>
          <p className="title">{recommendation.title}</p>
          <p>{recommendation.author}</p>
          <p>Page Count: {recommendation.pages}</p>
          <p>Subjects: </p>
          <p>{recommendation.subjects}</p>
          <p>Rating: {recommendation.rating} / 5</p>
        </div>
      )}
    </div>
  );
}

export default App;