import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { channelsAPI, workflowAPI, ideasAPI, videosAPI } from '../services/api';
import './ChannelDetail.css';

function ChannelDetail() {
  const { id } = useParams();
  const [channel, setChannel] = useState(null);
  const [ideas, setIdeas] = useState([]);
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [workflowStatus, setWorkflowStatus] = useState(null);

  useEffect(() => {
    loadChannelData();
  }, [id]);

  const loadChannelData = async () => {
    try {
      setLoading(true);
      const [channelRes, ideasRes, videosRes, statusRes] = await Promise.all([
        channelsAPI.get(id),
        ideasAPI.list({ channel_id: id }),
        videosAPI.list({ channel_id: id }),
        workflowAPI.getStatus(id),
      ]);

      setChannel(channelRes.data);
      setIdeas(ideasRes.data);
      setVideos(videosRes.data);
      setWorkflowStatus(statusRes.data);
    } catch (error) {
      console.error('채널 데이터 로드 실패:', error);
      alert('채널 정보를 불러오는데 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const handleStartWorkflow = async (mode, numIdeas) => {
    try {
      await workflowAPI.start({
        channel_id: parseInt(id),
        mode: mode,
        num_ideas: numIdeas,
      });
      alert('워크플로우가 시작되었습니다!');
      loadChannelData();
    } catch (error) {
      console.error('워크플로우 시작 실패:', error);
      alert('워크플로우 시작에 실패했습니다.');
    }
  };

  if (loading) {
    return <div className="loading">로딩 중...</div>;
  }

  if (!channel) {
    return <div className="error">채널을 찾을 수 없습니다.</div>;
  }

  return (
    <div className="channel-detail">
      <div className="channel-header">
        <h1>{channel.name}</h1>
        <div className="workflow-controls">
          <button
            className="btn btn-primary"
            onClick={() => handleStartWorkflow('generate', 3)}
          >
            🚀 워크플로우 실행 (신규 아이디어)
          </button>
          <button
            className="btn btn-secondary"
            onClick={() => handleStartWorkflow('reuse', 3)}
          >
            🔄 워크플로우 실행 (기존 아이디어)
          </button>
        </div>
      </div>

      <div className="channel-info">
        <div className="info-section">
          <h3>채널 정보</h3>
          <div><strong>주제:</strong> {channel.topic}</div>
          {channel.target_audience && (
            <div><strong>타겟:</strong> {channel.target_audience}</div>
          )}
          {channel.content_style && (
            <div><strong>스타일:</strong> {channel.content_style}</div>
          )}
        </div>

        <div className="info-section">
          <h3>설정</h3>
          <div>⏰ {channel.schedule_hours}시간마다 실행</div>
          <div>📺 영상 길이: {channel.video_duration}초</div>
          <div>🔒 공개 상태: {channel.privacy_status}</div>
          {channel.auto_upload && <div>✅ 자동 업로드 활성화</div>}
        </div>
      </div>

      {workflowStatus && workflowStatus.status === 'running' && (
        <div className="workflow-status">
          <h3>워크플로우 진행 중</h3>
          <div>현재 단계: {workflowStatus.current_step}</div>
          <div>진행률: {workflowStatus.progress}%</div>
        </div>
      )}

      <div className="content-sections">
        <div className="section">
          <h2>아이디어 ({ideas.length})</h2>
          {ideas.length === 0 ? (
            <p>생성된 아이디어가 없습니다.</p>
          ) : (
            <div className="ideas-list">
              {ideas.map((idea) => (
                <div key={idea.id} className="idea-card">
                  <h4>{idea.title}</h4>
                  <p>{idea.content}</p>
                  <span className={`status status-${idea.status}`}>
                    {idea.status}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="section">
          <h2>비디오 ({videos.length})</h2>
          {videos.length === 0 ? (
            <p>생성된 비디오가 없습니다.</p>
          ) : (
            <div className="videos-list">
              {videos.map((video) => (
                <div key={video.id} className="video-card">
                  <h4>{video.title}</h4>
                  <div className="video-meta">
                    <span className={`status status-${video.status}`}>
                      {video.status}
                    </span>
                    <span>{new Date(video.created_at).toLocaleString()}</span>
                  </div>
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
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default ChannelDetail;
