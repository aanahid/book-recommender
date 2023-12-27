import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [genre, setGenre] = useState('');
  const [keywords, setKeywords] = useState('');
  const [recommendation, setRecommendation] = useState({});
  const [error, setError] = useState('');

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

  return (
    <div>
      <h1>Book Recommender</h1>
      <div>
        <label>Genre:</label>
        <input
          type="text"
          value={genre}
          onChange={(e) => setGenre(e.target.value)}
        />
      </div>
      <div>
        <label>Keywords:</label>
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
          <h2>Recommendation:</h2>
          <p>Title: {recommendation.title}</p>
          <p>Author: {recommendation.author}</p>
          <p>Pages: {recommendation.pages}</p>
          <p>Subjects: {recommendation.subjects}</p>
          <p>Rating: {recommendation.rating}</p>
        </div>
      )}
    </div>
  );
}

export default App;