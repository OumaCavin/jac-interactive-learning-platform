/**
 * React Components for Adaptive Learning System
 * Demonstrates frontend integration with backend adaptive learning APIs
 */

import React, { useState, useEffect } from 'react';
import { Card, Button, Progress, Alert, Badge, Tabs, Table, Statistic } from 'antd';
import { 
  BrainOutlined, 
  TrophyOutlined, 
  ClockCircleOutlined, 
  BarChartOutlined,
  CheckCircleOutlined,
  ExclamationCircleOutlined
} from '@ant-design/icons';

// ===== ADAPTIVE CHALLENGE COMPONENT =====

export const AdaptiveChallengeGenerator = () => {
  const [loading, setLoading] = useState(false);
  const [challenge, setChallenge] = useState(null);
  const [userProfile, setUserProfile] = useState(null);
  const [error, setError] = useState(null);

  const generateChallenge = async (challengeType = null, specificTopic = null) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/adaptive-challenges/generate/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          challenge_type: challengeType,
          specific_topic: specificTopic
        })
      });

      const data = await response.json();
      
      if (data.success) {
        setChallenge(data.challenge);
        setUserProfile(data.personalization);
      } else {
        setError(data.error || 'Failed to generate challenge');
      }
    } catch (err) {
      setError('Network error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card 
      title={
        <span>
          <BrainOutlined /> Adaptive Challenge Generator
        </span>
      }
      extra={
        <Button 
          type="primary" 
          loading={loading}
          onClick={() => generateChallenge()}
        >
          Generate New Challenge
        </Button>
      }
    >
      {error && <Alert type="error" message={error} style={{ marginBottom: 16 }} />}
      
      {userProfile && (
        <Card size="small" style={{ marginBottom: 16 }}>
          <h4>Your Current Profile</h4>
          <div style={{ display: 'flex', gap: 20, flexWrap: 'wrap' }}>
            <div>
              <strong>Difficulty Level:</strong> 
              <Badge status="processing" text={userProfile.difficulty_level} />
            </div>
            <div>
              <strong>Recent Accuracy:</strong> 
              <Progress 
                percent={Math.round(userProfile.recent_accuracy * 100)} 
                size="small" 
                style={{ width: 100 }}
              />
            </div>
            <div>
              <strong>Success Streak:</strong> 
              <Badge count={userProfile.success_streak} style={{ backgroundColor: '#52c41a' }} />
            </div>
          </div>
        </Card>
      )}

      {challenge && <ChallengeDisplay challenge={challenge} />}
    </Card>
  );
};

// ===== CHALLENGE DISPLAY COMPONENT =====

const ChallengeDisplay = ({ challenge }) => {
  const [responses, setResponses] = useState({});
  const [feedback, setFeedback] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);

  const handleResponseChange = (questionId, value) => {
    setResponses(prev => ({ ...prev, [questionId]: value }));
  };

  const submitChallenge = async () => {
    setSubmitting(true);
    
    try {
      const response = await fetch(`/api/adaptive-challenges/${challenge.id}/submit/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          responses,
          feedback
        })
      });

      const data = await response.json();
      
      if (data.success) {
        setResult(data);
      } else {
        console.error('Submission failed:', data.error);
      }
    } catch (err) {
      console.error('Network error:', err);
    } finally {
      setSubmitting(false);
    }
  };

  const renderChallengeContent = (content) => {
    const questions = content.questions || [];
    
    return (
      <div>
        <h3>{challenge.title}</h3>
        <p>{challenge.description}</p>
        
        <div style={{ backgroundColor: '#f5f5f5', padding: 16, marginBottom: 16 }}>
          <div><strong>Challenge Type:</strong> {challenge.challenge_type}</div>
          <div><strong>Difficulty:</strong> {challenge.difficulty_level}</div>
          <div><strong>Estimated Time:</strong> {challenge.estimated_time} minutes</div>
          <div><strong>Target Skills:</strong> {Object.keys(challenge.skill_dimensions).join(', ')}</div>
        </div>

        {questions.map((question, index) => (
          <Card key={index} size="small" style={{ marginBottom: 12 }}>
            <div><strong>Question {index + 1}:</strong></div>
            <p>{question.question}</p>
            
            {question.type === 'multiple_choice' && (
              <div>
                {question.options.map((option, optIndex) => (
                  <div key={optIndex} style={{ marginBottom: 8 }}>
                    <label>
                      <input
                        type="radio"
                        name={`question_${index}`}
                        value={optIndex}
                        onChange={(e) => handleResponseChange(`question_${index}`, parseInt(e.target.value))}
                        style={{ marginRight: 8 }}
                      />
                      {option}
                    </label>
                  </div>
                ))}
              </div>
            )}
            
            {question.type === 'coding' && (
              <textarea
                placeholder="Write your code here..."
                value={responses[`question_${index}`] || ''}
                onChange={(e) => handleResponseChange(`question_${index}`, e.target.value)}
                style={{ width: '100%', height: 120, fontFamily: 'monospace' }}
              />
            )}
          </Card>
        ))}

        <div style={{ marginTop: 16 }}>
          <label>
            <strong>Additional Feedback (Optional):</strong>
            <textarea
              placeholder="How did you find this challenge? Any suggestions?"
              value={feedback}
              onChange={(e) => setFeedback(e.target.value)}
              style={{ width: '100%', height: 80, marginTop: 8 }}
            />
          </label>
        </div>

        <Button 
          type="primary" 
          onClick={submitChallenge}
          loading={submitting}
          style={{ marginTop: 16 }}
        >
          Submit Challenge
        </Button>
      </div>
    );
  };

  if (result) {
    return (
      <Card title="Challenge Results" size="small">
        <div style={{ textAlign: 'center', marginBottom: 16 }}>
          <Statistic 
            title="Your Score" 
            value={Math.round(result.score * 100)} 
            suffix="%"
            valueStyle={{ color: result.score >= 0.7 ? '#3f8600' : '#cf1322' }}
          />
        </div>
        
        <div style={{ backgroundColor: '#f6ffed', padding: 16, border: '1px solid #b7eb8f', borderRadius: 6 }}>
          <h4>
            <CheckCircleOutlined style={{ color: '#52c41a', marginRight: 8 }} />
            AI Feedback
          </h4>
          <p>{result.feedback}</p>
        </div>

        {result.next_steps && result.next_steps.length > 0 && (
          <div style={{ marginTop: 16 }}>
            <h4>Next Steps:</h4>
            <ul>
              {result.next_steps.map((step, index) => (
                <li key={index}>{step}</li>
              ))}
            </ul>
          </div>
        )}

        {result.difficulty_adjustment && result.difficulty_adjustment.adjusted && (
          <Alert
            type="success"
            message={`Difficulty Adjusted: ${result.difficulty_adjustment.new_difficulty}`}
            description={result.difficulty_adjustment.message}
            style={{ marginTop: 16 }}
          />
        )}
      </Card>
    );
  }

  return (
    <Card title="Challenge Content" size="small">
      {renderChallengeContent(challenge.content)}
    </Card>
  );
};

// ===== PERFORMANCE ANALYTICS COMPONENT =====

export const PerformanceAnalytics = () => {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(false);
  const [timeRange, setTimeRange] = useState(30);

  const fetchAnalytics = async () => {
    setLoading(true);
    try {
      const response = await fetch(`/api/performance/analytics/?days=${timeRange}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      const data = await response.json();
      setAnalytics(data);
    } catch (err) {
      console.error('Failed to fetch analytics:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalytics();
  }, [timeRange]);

  if (!analytics) {
    return <Card loading={loading} />;
  }

  const metrics = analytics.difficulty_metrics;
  const patterns = analytics.learning_patterns;

  return (
    <div>
      <Card 
        title={
          <span>
            <BarChartOutlined /> Performance Analytics
          </span>
        }
        extra={
          <select 
            value={timeRange} 
            onChange={(e) => setTimeRange(parseInt(e.target.value))}
          >
            <option value={7}>Last 7 days</option>
            <option value={30}>Last 30 days</option>
            <option value={90}>Last 90 days</option>
          </select>
        }
      >
        <Tabs defaultActiveKey="metrics">
          <Tabs.TabPane tab="Key Metrics" key="metrics">
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 16 }}>
              <Card size="small">
                <Statistic 
                  title="Success Rate" 
                  value={Math.round(metrics.challenge_success_rate * 100)}
                  suffix="%"
                  prefix={<TrophyOutlined />}
                />
              </Card>
              <Card size="small">
                <Statistic 
                  title="Average Score" 
                  value={Math.round(metrics.average_challenge_score * 100)}
                  suffix="%"
                  prefix={<BarChartOutlined />}
                />
              </Card>
              <Card size="small">
                <Statistic 
                  title="Learning Velocity" 
                  value={metrics.learning_velocity.toFixed(1)}
                  suffix="activities/day"
                  prefix={<ClockCircleOutlined />}
                />
              </Card>
              <Card size="small">
                <Statistic 
                  title="Engagement Score" 
                  value={Math.round(metrics.engagement_level * 100)}
                  suffix="%"
                  prefix={<BrainOutlined />}
                />
              </Card>
            </div>
          </Tabs.TabPane>

          <Tabs.TabPane tab="Learning Patterns" key="patterns">
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
              <Card size="small" title="Performance Trend">
                <Badge 
                  status={
                    metrics.performance_trend === 'improving' ? 'success' :
                    metrics.performance_trend === 'declining' ? 'error' : 'processing'
                  } 
                  text={metrics.performance_trend}
                />
                <div style={{ marginTop: 8 }}>
                  <Progress 
                    percent={metrics.performance_consistency * 100} 
                    format={() => 'Consistency'}
                  />
                </div>
              </Card>

              <Card size="small" title="Skill Dimensions">
                {Object.entries(patterns.skill_levels || {}).map(([skill, level]) => (
                  <div key={skill} style={{ marginBottom: 8 }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <span>{skill.replace('_', ' ').toUpperCase()}</span>
                      <span>{level}/10</span>
                    </div>
                    <Progress percent={level * 10} size="small" />
                  </div>
                ))}
              </Card>
            </div>
          </Tabs.TabPane>

          <Tabs.TabPane tab="Recommendations" key="recommendations">
            {analytics.recommendations.recommendations.map((rec, index) => (
              <Alert
                key={index}
                type={
                  rec.priority === 'high' ? 'warning' :
                  rec.priority === 'medium' ? 'info' : 'success'
                }
                message={rec.type.replace('_', ' ').toUpperCase()}
                description={rec.reason}
                style={{ marginBottom: 8 }}
              />
            ))}

            {analytics.recommendations.proposed_adjustments.map((adj, index) => (
              <Card key={index} size="small" style={{ marginTop: 16 }}>
                <div>
                  <strong>Proposed Adjustment:</strong> {adj.difficulty}
                  {adj.new_level && (
                    <Badge 
                      count={adj.new_level} 
                      style={{ marginLeft: 8, backgroundColor: '#52c41a' }} 
                    />
                  )}
                </div>
                <p style={{ marginTop: 8, marginBottom: 0 }}>{adj.rationale}</p>
              </Card>
            ))}
          </Tabs.TabPane>
        </Tabs>
      </Card>
    </div>
  );
};

// ===== SPACED REPETITION COMPONENT =====

export const SpacedRepetitionReview = () => {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(false);
  const [currentReview, setCurrentReview] = useState(null);
  const [qualityRating, setQualityRating] = useState(null);

  const fetchDueReviews = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/adaptive-challenges/due-reviews/', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      const data = await response.json();
      setReviews(data.reviews || []);
    } catch (err) {
      console.error('Failed to fetch reviews:', err);
    } finally {
      setLoading(false);
    }
  };

  const completeReview = async (sessionId, rating) => {
    try {
      const response = await fetch(`/api/spaced-repetition/${sessionId}/complete-review/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ quality_rating: rating })
      });

      const data = await response.json();
      
      if (data.success) {
        // Remove completed review from list
        setReviews(prev => prev.filter(review => review.session_id !== sessionId));
        setCurrentReview(null);
        setQualityRating(null);
        
        // Show success message
        console.log(`Next review scheduled for: ${data.next_review_date}`);
      }
    } catch (err) {
      console.error('Failed to complete review:', err);
    }
  };

  if (loading) {
    return <Card loading />;
  }

  if (currentReview) {
    return (
      <Card 
        title={`Review: ${currentReview.challenge.title}`}
        extra={
          <Button onClick={() => setCurrentReview(null)}>
            Back to List
          </Button>
        }
      >
        <div style={{ backgroundColor: '#f0f0f0', padding: 16, borderRadius: 6, marginBottom: 16 }}>
          <p><strong>Challenge Type:</strong> {currentReview.challenge.challenge_type}</p>
          <p><strong>Description:</strong> {currentReview.challenge.description}</p>
          <p><strong>Review Stage:</strong> {currentReview.review_stage}</p>
          <p><strong>Ease Factor:</strong> {currentReview.ease_factor.toFixed(2)}</p>
        </div>

        <div style={{ textAlign: 'center', marginBottom: 16 }}>
          <h4>How well did you remember this challenge?</h4>
          <div style={{ display: 'flex', justifyContent: 'center', gap: 8, marginTop: 8 }}>
            {[0, 1, 2, 3, 4, 5].map(rating => (
              <Button
                key={rating}
                type={qualityRating === rating ? 'primary' : 'default'}
                onClick={() => setQualityRating(rating)}
              >
                {rating}
              </Button>
            ))}
          </div>
        </div>

        {qualityRating !== null && (
          <Button 
            type="primary" 
            block
            onClick={() => completeReview(currentReview.session_id, qualityRating)}
          >
            Complete Review
          </Button>
        )}
      </Card>
    );
  }

  return (
    <Card 
      title={
        <span>
          <ClockCircleOutlined /> Spaced Repetition Reviews
        </span>
      }
      extra={
        <Button onClick={fetchDueReviews}>
          Refresh
        </Button>
      }
    >
      {reviews.length === 0 ? (
        <Alert 
          type="success" 
          message="No reviews due!" 
          description="You have completed all scheduled reviews. Great job!"
        />
      ) : (
        <Table
          dataSource={reviews}
          columns={[
            {
              title: 'Challenge',
              dataIndex: ['challenge', 'title'],
              key: 'title',
            },
            {
              title: 'Type',
              dataIndex: ['challenge', 'challenge_type'],
              key: 'type',
            },
            {
              title: 'Stage',
              dataIndex: 'review_stage',
              key: 'stage',
            },
            {
              title: 'Actions',
              key: 'actions',
              render: (_, record) => (
                <Button 
                  type="primary" 
                  size="small"
                  onClick={() => setCurrentReview(record)}
                >
                  Review Now
                </Button>
              ),
            },
          ]}
          pagination={false}
          rowKey="session_id"
        />
      )}
    </Card>
  );
};

// ===== USER LEARNING SUMMARY COMPONENT =====

export const UserLearningSummary = () => {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchSummary = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/difficulty-profile/summary/', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      const data = await response.json();
      setSummary(data);
    } catch (err) {
      console.error('Failed to fetch summary:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSummary();
  }, []);

  if (loading || !summary) {
    return <Card loading />;
  }

  const { difficulty_profile, recent_attempts, due_reviews, performance_summary } = summary;

  return (
    <Card title="Learning Summary">
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 16 }}>
        {/* User Profile */}
        <Card size="small" title="Current Profile">
          <div style={{ marginBottom: 8 }}>
            <strong>Difficulty Level:</strong> 
            <Badge status="processing" text={difficulty_profile.current_difficulty} />
          </div>
          
          <div style={{ marginBottom: 8 }}>
            <strong>Overall Skill Level:</strong>
            <Progress 
              percent={Math.round(difficulty_profile.overall_skill_level * 10)} 
              format={() => difficulty_profile.overall_skill_level.toFixed(1) + '/10'}
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8, marginTop: 16 }}>
            <div>
              <div><strong>JAC Knowledge:</strong></div>
              <Progress percent={difficulty_profile.jac_knowledge_level * 10} size="small" />
            </div>
            <div>
              <div><strong>Problem Solving:</strong></div>
              <Progress percent={difficulty_profile.problem_solving_level * 10} size="small" />
            </div>
            <div>
              <div><strong>Coding Skill:</strong></div>
              <Progress percent={difficulty_profile.coding_skill_level * 10} size="small" />
            </div>
          </div>
        </Card>

        {/* Performance Metrics */}
        <Card size="small" title="Recent Performance">
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
            <Statistic 
              title="Recent Accuracy" 
              value={Math.round(performance_summary.recent_accuracy * 100)}
              suffix="%"
              valueStyle={{ fontSize: 18 }}
            />
            <Statistic 
              title="Current Streak" 
              value={performance_summary.current_streak}
              suffix="correct"
              valueStyle={{ fontSize: 18 }}
            />
            <Statistic 
              title="Total Attempts" 
              value={performance_summary.total_attempts}
              valueStyle={{ fontSize: 18 }}
            />
          </div>
        </Card>

        {/* Due Reviews */}
        <Card size="small" title="Due Reviews">
          {due_reviews.length === 0 ? (
            <Alert 
              type="success" 
              message="All caught up!" 
              description="No reviews are currently due."
              showIcon={false}
            />
          ) : (
            <div>
              <Statistic 
                title="Reviews Due" 
                value={due_reviews.length}
                valueStyle={{ color: '#cf1322' }}
              />
              <Button 
                type="primary" 
                size="small" 
                style={{ marginTop: 8 }}
                href="#spaced-repetition"
              >
                Start Reviews
              </Button>
            </div>
          )}
        </Card>
      </div>

      {/* Recent Attempts */}
      {recent_attempts.length > 0 && (
        <Card size="small" title="Recent Challenge Attempts" style={{ marginTop: 16 }}>
          <Table
            dataSource={recent_attempts}
            columns={[
              {
                title: 'Challenge',
                dataIndex: ['challenge', 'title'],
                key: 'title',
              },
              {
                title: 'Type',
                dataIndex: ['challenge', 'challenge_type'],
                key: 'type',
              },
              {
                title: 'Score',
                dataIndex: 'score',
                key: 'score',
                render: (score) => (
                  <span>
                    {score !== null ? (
                      <span style={{ 
                        color: score >= 0.7 ? '#3f8600' : score >= 0.5 ? '#faad14' : '#cf1322' 
                      }}>
                        {Math.round(score * 100)}%
                      </span>
                    ) : (
                      '-'
                    )}
                  </span>
                ),
              },
              {
                title: 'Status',
                dataIndex: 'status',
                key: 'status',
                render: (status) => (
                  <Badge 
                    status={
                      status === 'completed' ? 'success' :
                      status === 'failed' ? 'error' : 'processing'
                    }
                    text={status}
                  />
                ),
              },
            ]}
            pagination={false}
            size="small"
            rowKey="id"
          />
        </Card>
      )}
    </Card>
  );
};

// ===== MAIN ADAPTIVE LEARNING DASHBOARD =====

export const AdaptiveLearningDashboard = () => {
  const [activeTab, setActiveTab] = useState('summary');

  return (
    <div style={{ padding: 24 }}>
      <h1>Adaptive Learning Dashboard</h1>
      
      <Tabs activeKey={activeTab} onChange={setActiveTab}>
        <Tabs.TabPane tab="Summary" key="summary">
          <UserLearningSummary />
        </Tabs.TabPane>
        
        <Tabs.TabPane tab="Generate Challenge" key="generator">
          <AdaptiveChallengeGenerator />
        </Tabs.TabPane>
        
        <Tabs.TabPane tab="Analytics" key="analytics">
          <PerformanceAnalytics />
        </Tabs.TabPane>
        
        <Tabs.TabPane tab="Spaced Repetition" key="spaced-repetition">
          <SpacedRepetitionReview />
        </Tabs.TabPane>
      </Tabs>
    </div>
  );
};

export default AdaptiveLearningDashboard;