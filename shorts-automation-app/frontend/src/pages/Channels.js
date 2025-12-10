import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { channelsAPI } from '../services/api';
import ChannelForm from '../components/ChannelForm';
import './Channels.css';

function Channels() {
  const [channels, setChannels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    loadChannels();
  }, []);

  const loadChannels = async () => {
    try {
      setLoading(true);
      const response = await channelsAPI.list();
      setChannels(response.data);
    } catch (error) {
      console.error('채널 로드 실패:', error);
      alert('채널 목록을 불러오는데 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateChannel = async (channelData) => {
    try {
      await channelsAPI.create(channelData);
      setShowForm(false);
      loadChannels();
    } catch (error) {
      console.error('채널 생성 실패:', error);
      throw error;
    }
  };

  const handleDeleteChannel = async (id) => {
    if (!window.confirm('정말 이 채널을 삭제하시겠습니까?')) {
      return;
    }

    try {
      await channelsAPI.delete(id);
      loadChannels();
    } catch (error) {
      console.error('채널 삭제 실패:', error);
      alert('채널 삭제에 실패했습니다.');
    }
  };

  if (loading) {
    return <div className="loading">로딩 중...</div>;
  }

  return (
    <div className="channels-page">
      <div className="page-header">
        <h1>채널 관리</h1>
        <button
          className="btn btn-primary"
          onClick={() => setShowForm(true)}
        >
          + 새 채널 만들기
        </button>
      </div>

      {showForm && (
        <div className="modal-overlay" onClick={() => setShowForm(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h2>새 채널 만들기</h2>
            <ChannelForm
              onSubmit={handleCreateChannel}
              onCancel={() => setShowForm(false)}
            />
          </div>
        </div>
      )}

      {channels.length === 0 ? (
        <div className="empty-state">
          <h2>등록된 채널이 없습니다</h2>
          <p>첫 번째 채널을 만들어보세요!</p>
          <button
            className="btn btn-primary"
            onClick={() => setShowForm(true)}
          >
            첫 채널 만들기
          </button>
        </div>
      ) : (
        <div className="channels-grid">
          {channels.map((channel) => (
            <div key={channel.id} className="channel-card">
              <div className="channel-header">
                <h3>{channel.name}</h3>
                <button
                  className="btn-delete"
                  onClick={() => handleDeleteChannel(channel.id)}
                  title="삭제"
                >
                  ×
                </button>
              </div>

              <div className="channel-body">
                <div className="channel-topic">
                  <strong>주제:</strong> {channel.topic}
                </div>

                {channel.description && (
                  <p className="channel-description">{channel.description}</p>
                )}

                <div className="channel-meta">
                  {channel.target_audience && (
                    <div><strong>타겟:</strong> {channel.target_audience}</div>
                  )}
                  {channel.content_style && (
                    <div><strong>스타일:</strong> {channel.content_style}</div>
                  )}
                </div>

                <div className="channel-stats">
                  <div className="stat">
                    <span className="stat-label">총 비디오</span>
                    <span className="stat-value">{channel.total_videos}</span>
                  </div>
                  <div className="stat">
                    <span className="stat-label">총 조회수</span>
                    <span className="stat-value">
                      {channel.total_views.toLocaleString()}
                    </span>
                  </div>
                </div>

                <div className="channel-settings">
                  <small>
                    ⏰ {channel.schedule_hours}시간마다 실행
                    {channel.auto_upload && ' | 🔄 자동 업로드'}
                  </small>
                </div>
              </div>

              <div className="channel-footer">
                <Link
                  to={`/channels/${channel.id}`}
                  className="btn btn-secondary"
                >
                  상세 보기
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Channels;
