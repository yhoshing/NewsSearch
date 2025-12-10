import React, { useState, useEffect } from 'react';
import { ideasAPI } from '../services/api';

function Ideas() {
  const [ideas, setIdeas] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadIdeas();
  }, []);

  const loadIdeas = async () => {
    try {
      const response = await ideasAPI.list();
      setIdeas(response.data);
    } catch (error) {
      console.error('아이디어 로드 실패:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>로딩 중...</div>;

  return (
    <div className="ideas-page">
      <h1>아이디어 목록</h1>
      <div className="ideas-grid">
        {ideas.map((idea) => (
          <div key={idea.id} className="idea-card">
            <h3>{idea.title}</h3>
            <p>{idea.content}</p>
            <span className={`status-${idea.status}`}>{idea.status}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Ideas;
