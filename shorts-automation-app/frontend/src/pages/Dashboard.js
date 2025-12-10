import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { channelsAPI, videosAPI } from '../services/api';
import './Dashboard.css';

function Dashboard() {
  const [channels, setChannels] = useState([]);
  const [recentVideos, setRecentVideos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalChannels: 0,
    totalVideos: 0,
    totalViews: 0,
  });

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);

      // 채널 목록 조회
      const channelsRes = await channelsAPI.list();
      setChannels(channelsRes.data);

      // 최근 비디오 조회
      const videosRes = await videosAPI.list({ limit: 10 });
      setRecentVideos(videosRes.data);

      // 통계 계산
      const totalChannels = channelsRes.data.length;
      const totalVideos = channelsRes.data.reduce((sum, ch) => sum + ch.total_videos, 0);
      const totalViews = channelsRes.data.reduce((sum, ch) => sum + ch.total_views, 0);

      setStats({ totalChannels, totalVideos, totalViews });
    } catch (error) {
      console.error('대시보드 로드 실패:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">로딩 중...</div>;
  }

  return (
    <div className="dashboard">
      <h1>대시보드</h1>

      <div className="stats-container">
        <div className="stat-card">
          <h3>총 채널 수</h3>
          <div className="stat-value">{stats.totalChannels}</div>
        </div>
        <div className="stat-card">
          <h3>총 비디오 수</h3>
          <div className="stat-value">{stats.totalVideos}</div>
        </div>
        <div className="stat-card">
          <h3>총 조회수</h3>
          <div className="stat-value">{stats.totalViews.toLocaleString()}</div>
        </div>
      </div>

      <div className="dashboard-grid">
        <div className="dashboard-section">
          <h2>채널 목록</h2>
          {channels.length === 0 ? (
            <div className="empty-state">
              <p>등록된 채널이 없습니다.</p>
              <Link to="/channels" className="btn btn-primary">
                첫 채널 만들기
              </Link>
            </div>
          ) : (
            <div className="channel-list">
              {channels.map((channel) => (
                <Link
                  key={channel.id}
                  to={`/channels/${channel.id}`}
                  className="channel-card"
                >
                  <h3>{channel.name}</h3>
                  <p className="channel-topic">{channel.topic}</p>
                  <div className="channel-stats">
                    <span>📹 {channel.total_videos}개</span>
                    <span>👁️ {channel.total_views.toLocaleString()}</span>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>

        <div className="dashboard-section">
          <h2>최근 비디오</h2>
          {recentVideos.length === 0 ? (
            <p className="empty-message">생성된 비디오가 없습니다.</p>
          ) : (
            <div className="video-list">
              {recentVideos.map((video) => (
                <div key={video.id} className="video-item">
                  <div className="video-info">
                    <h4>{video.title}</h4>
                    <span className={`status status-${video.status}`}>
                      {video.status}
                    </span>
                  </div>
                  <div className="video-meta">
                    <span>{new Date(video.created_at).toLocaleDateString()}</span>
                    {video.youtube_video_id && (
                      <a
                        href={`https://www.youtube.com/watch?v=${video.youtube_video_id}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="youtube-link"
                      >
                        YouTube에서 보기
                      </a>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
