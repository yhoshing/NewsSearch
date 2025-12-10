import React, { useState } from 'react';
import './ChannelForm.css';

function ChannelForm({ onSubmit, onCancel, initialData = {} }) {
  const [formData, setFormData] = useState({
    name: initialData.name || '',
    topic: initialData.topic || '',
    description: initialData.description || '',
    target_audience: initialData.target_audience || '',
    content_style: initialData.content_style || '',
    keywords: initialData.keywords?.join(', ') || '',
    schedule_hours: initialData.schedule_hours || 6,
    auto_upload: initialData.auto_upload || false,
    video_duration: initialData.video_duration || 60,
    privacy_status: initialData.privacy_status || 'private',
    creatomate_template_id: initialData.creatomate_template_id || '',
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!formData.name || !formData.topic) {
      setError('채널 이름과 주제는 필수입니다.');
      return;
    }

    try {
      setLoading(true);

      // keywords를 배열로 변환
      const submitData = {
        ...formData,
        keywords: formData.keywords
          ? formData.keywords.split(',').map((k) => k.trim())
          : [],
      };

      await onSubmit(submitData);
    } catch (error) {
      setError(error.response?.data?.detail || '채널 생성에 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="channel-form" onSubmit={handleSubmit}>
      {error && <div className="error-message">{error}</div>}

      <div className="form-group">
        <label htmlFor="name">채널 이름 *</label>
        <input
          type="text"
          id="name"
          name="name"
          value={formData.name}
          onChange={handleChange}
          placeholder="예: AI 뉴스 채널"
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="topic">채널 주제 *</label>
        <textarea
          id="topic"
          name="topic"
          value={formData.topic}
          onChange={handleChange}
          placeholder="예: 인공지능과 기술 관련 최신 뉴스를 재미있게 전달"
          rows="3"
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="description">채널 설명</label>
        <textarea
          id="description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          placeholder="채널에 대한 자세한 설명"
          rows="3"
        />
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="target_audience">타겟 청중</label>
          <input
            type="text"
            id="target_audience"
            name="target_audience"
            value={formData.target_audience}
            onChange={handleChange}
            placeholder="예: 20-30대 IT 종사자"
          />
        </div>

        <div className="form-group">
          <label htmlFor="content_style">콘텐츠 스타일</label>
          <input
            type="text"
            id="content_style"
            name="content_style"
            value={formData.content_style}
            onChange={handleChange}
            placeholder="예: 유머러스하고 친근한"
          />
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="keywords">키워드 (쉼표로 구분)</label>
        <input
          type="text"
          id="keywords"
          name="keywords"
          value={formData.keywords}
          onChange={handleChange}
          placeholder="예: AI, 기술, 뉴스"
        />
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="schedule_hours">실행 주기 (시간)</label>
          <input
            type="number"
            id="schedule_hours"
            name="schedule_hours"
            value={formData.schedule_hours}
            onChange={handleChange}
            min="1"
            max="168"
          />
        </div>

        <div className="form-group">
          <label htmlFor="video_duration">영상 길이 (초)</label>
          <input
            type="number"
            id="video_duration"
            name="video_duration"
            value={formData.video_duration}
            onChange={handleChange}
            min="15"
            max="300"
          />
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="privacy_status">YouTube 공개 상태</label>
          <select
            id="privacy_status"
            name="privacy_status"
            value={formData.privacy_status}
            onChange={handleChange}
          >
            <option value="private">비공개</option>
            <option value="unlisted">일부 공개</option>
            <option value="public">전체 공개</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="creatomate_template_id">Creatomate 템플릿 ID</label>
          <input
            type="text"
            id="creatomate_template_id"
            name="creatomate_template_id"
            value={formData.creatomate_template_id}
            onChange={handleChange}
            placeholder="템플릿 ID"
          />
        </div>
      </div>

      <div className="form-group checkbox-group">
        <label>
          <input
            type="checkbox"
            name="auto_upload"
            checked={formData.auto_upload}
            onChange={handleChange}
          />
          <span>자동으로 YouTube에 업로드</span>
        </label>
      </div>

      <div className="form-actions">
        <button type="button" className="btn btn-secondary" onClick={onCancel}>
          취소
        </button>
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? '처리 중...' : '저장'}
        </button>
      </div>
    </form>
  );
}

export default ChannelForm;
