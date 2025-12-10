import React, { useState, useEffect } from 'react';
import { videosAPI } from '../services/api';

function Videos() {
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadVideos();
  }, []);

  const loadVideos = async () => {
    try {
      const response = await videosAPI.list();
      setVideos(response.data);
    } catch (error) {
      console.error('비디오 로드 실패:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>로딩 중...</div>;

  return (
    <div className="videos-page">
      <h1>비디오 목록</h1>
      <div className="videos-grid">
        {videos.map((video) => (
          <div key={video.id} className="video-card">
            <h3>{video.title}</h3>
            <span className={`status-${video.status}`}>{video.status}</span>
            {video.youtube_video_id && (
              <a
                href={`https://www.youtube.com/watch?v=${video.youtube_video_id}`}
                target="_blank"
                rel="noopener noreferrer"
              >
                YouTube에서 보기
              </a>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Videos;
