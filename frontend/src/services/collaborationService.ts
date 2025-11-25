/**
 * Collaboration Service - Frontend-Backend Integration
 * 
 * Complete API integration for collaboration features:
 * - Study groups functionality
 * - Discussion forums  
 * - Peer code sharing
 * - Group challenges
 * - Mentorship system
 * 
 * Author: MiniMax Agent
 * Created: 2025-11-26
 */

import apiClient from './apiClient'

// Study Groups Types
export interface StudyGroup {
  id: string
  name: string
  description: string
  subject_area: string
  level: 'beginner' | 'intermediate' | 'advanced' | 'expert'
  max_members: number
  is_public: boolean
  requires_approval: boolean
  member_count: number
  is_member: boolean
  created_by: {
    id: number
    username: string
    first_name: string
    last_name: string
  }
  created_at: string
  updated_at: string
}

export interface StudyGroupMembership {
  id: string
  study_group: StudyGroup
  user: {
    id: number
    username: string
    first_name: string
    last_name: string
  }
  role: 'member' | 'moderator' | 'leader'
  joined_at: string
}

// Discussion Forum Types
export interface DiscussionTopic {
  id: string
  forum: string
  title: string
  content: string
  author: {
    id: number
    username: string
    first_name: string
    last_name: string
  }
  status: 'open' | 'closed' | 'pinned'
  is_pinned: boolean
  views_count: number
  posts_count: number
  created_at: string
  updated_at: string
}

export interface DiscussionPost {
  id: string
  topic: DiscussionTopic
  author: {
    id: number
    username: string
    first_name: string
    last_name: string
  }
  content: string
  parent_post?: DiscussionPost
  is_solution: boolean
  created_at: string
  updated_at: string
}

// Code Sharing Types
export interface PeerCodeShare {
  id: string
  title: string
  description: string
  code_content: string
  language: string
  file_name: string
  tags: string[]
  share_type: 'snippet' | 'project' | 'solution' | 'tutorial'
  is_public: boolean
  is_tutorial: boolean
  likes_count: number
  downloads_count: number
  views_count: number
  is_liked: boolean
  author: {
    id: number
    username: string
    first_name: string
    last_name: string
  }
  topic?: DiscussionTopic
  study_group?: StudyGroup
  created_at: string
  updated_at: string
}

// Group Challenge Types
export interface GroupChallenge {
  id: string
  title: string
  description: string
  challenge_type: 'coding' | 'problem_solving' | 'research' | 'presentation'
  difficulty_level: 'easy' | 'medium' | 'hard' | 'expert'
  problem_statement: string
  requirements: string[]
  test_cases: any[]
  solution_template: string
  start_date: string
  end_date: string
  estimated_duration: number
  status: 'draft' | 'active' | 'completed' | 'cancelled'
  max_participants: number
  allow_team_participation: boolean
  participant_count: number
  is_participating: boolean
  created_by: {
    id: number
    username: string
    first_name: string
    last_name: string
  }
  study_group: StudyGroup
  created_at: string
  updated_at: string
}

export interface ChallengeParticipation {
  id: string
  challenge: GroupChallenge
  participant: {
    id: number
    username: string
    first_name: string
    last_name: string
  }
  team_name: string
  team_members: string[]
  status: 'registered' | 'in_progress' | 'submitted' | 'completed' | 'abandoned'
  started_at?: string
  submitted_at?: string
  completed_at?: string
  submission_content: string
  code_files: any[]
  score?: number
  feedback: string
  created_at: string
  updated_at: string
}

// Mentorship Types
export interface MentorshipRelationship {
  id: string
  mentor: {
    id: number
    username: string
    first_name: string
    last_name: string
  }
  mentee: {
    id: number
    username: string
    first_name: string
    last_name: string
  }
  subject_areas: string[]
  goals: string
  status: 'pending' | 'active' | 'completed' | 'cancelled'
  meeting_frequency: string
  session_duration?: number
  started_at?: string
  ended_at?: string
  created_at: string
  updated_at: string
}

export interface MentorshipSession {
  id: string
  relationship: MentorshipRelationship
  title: string
  agenda: string
  notes: string
  action_items: string[]
  scheduled_start: string
  scheduled_end: string
  actual_start?: string
  actual_end?: string
  status: 'scheduled' | 'completed' | 'cancelled' | 'no_show'
  session_type: 'one_on_one' | 'group' | 'code_review' | 'project_discussion'
  mentor_feedback: string
  mentee_feedback: string
  rating?: number
  created_at: string
  updated_at: string
}

// Overview/Dashboard Types
export interface CollaborationOverview {
  total_study_groups: number
  active_discussions: number
  code_shares: number
  active_challenges: number
  active_mentorships: number
  my_study_groups: number
  my_posts: number
  my_code_shares: number
}

class CollaborationService {
  private baseURL = '/collaboration'

  // Study Groups API
  async getStudyGroups(params?: {
    search?: string
    subject_area?: string
    level?: string
    is_public?: boolean
    ordering?: string
  }): Promise<StudyGroup[]> {
    return apiClient.get(`${this.baseURL}/study-groups/`, { params }).then(res => res.data)
  }

  async getStudyGroup(id: string): Promise<StudyGroup> {
    return apiClient.get(`${this.baseURL}/study-groups/${id}/`).then(res => res.data)
  }

  async createStudyGroup(data: Partial<StudyGroup>): Promise<StudyGroup> {
    return apiClient.post(`${this.baseURL}/study-groups/`, data).then(res => res.data)
  }

  async updateStudyGroup(id: string, data: Partial<StudyGroup>): Promise<StudyGroup> {
    return apiClient.patch(`${this.baseURL}/study-groups/${id}/`, data).then(res => res.data)
  }

  async deleteStudyGroup(id: string): Promise<void> {
    return apiClient.delete(`${this.baseURL}/study-groups/${id}/`)
  }

  async joinStudyGroup(id: string): Promise<void> {
    return apiClient.post(`${this.baseURL}/study-groups/${id}/join/`)
  }

  async leaveStudyGroup(id: string): Promise<void> {
    return apiClient.post(`${this.baseURL}/study-groups/${id}/leave/`)
  }

  async getStudyGroupMembers(id: string): Promise<StudyGroupMembership[]> {
    return apiClient.get(`${this.baseURL}/study-groups/${id}/members/`).then(res => res.data)
  }

  // Discussion Forums API
  async getDiscussionTopics(params?: {
    search?: string
    status?: string
    forum?: string
    ordering?: string
  }): Promise<DiscussionTopic[]> {
    return apiClient.get(`${this.baseURL}/discussion-topics/`, { params }).then(res => res.data)
  }

  async getDiscussionTopic(id: string): Promise<DiscussionTopic> {
    return apiClient.get(`${this.baseURL}/discussion-topics/${id}/`).then(res => res.data)
  }

  async createDiscussionTopic(data: Partial<DiscussionTopic>): Promise<DiscussionTopic> {
    return apiClient.post(`${this.baseURL}/discussion-topics/`, data).then(res => res.data)
  }

  async updateDiscussionTopic(id: string, data: Partial<DiscussionTopic>): Promise<DiscussionTopic> {
    return apiClient.patch(`${this.baseURL}/discussion-topics/${id}/`, data).then(res => res.data)
  }

  async deleteDiscussionTopic(id: string): Promise<void> {
    return apiClient.delete(`${this.baseURL}/discussion-topics/${id}/`)
  }

  async pinTopic(id: string): Promise<void> {
    return apiClient.post(`${this.baseURL}/discussion-topics/${id}/pin/`)
  }

  // Discussion Posts API
  async getDiscussionPosts(topicId?: string): Promise<DiscussionPost[]> {
    const params = topicId ? { topic: topicId } : {}
    return apiClient.get(`${this.baseURL}/discussion-posts/`, { params }).then(res => res.data)
  }

  async createDiscussionPost(data: Partial<DiscussionPost>): Promise<DiscussionPost> {
    return apiClient.post(`${this.baseURL}/discussion-posts/`, data).then(res => res.data)
  }

  async updateDiscussionPost(id: string, data: Partial<DiscussionPost>): Promise<DiscussionPost> {
    return apiClient.patch(`${this.baseURL}/discussion-posts/${id}/`, data).then(res => res.data)
  }

  async deleteDiscussionPost(id: string): Promise<void> {
    return apiClient.delete(`${this.baseURL}/discussion-posts/${id}/`)
  }

  async markPostAsSolution(id: string): Promise<void> {
    return apiClient.post(`${this.baseURL}/discussion-posts/${id}/mark-solution/`)
  }

  // Code Sharing API
  async getCodeShares(params?: {
    search?: string
    language?: string
    share_type?: string
    is_public?: boolean
    ordering?: string
  }): Promise<PeerCodeShare[]> {
    return apiClient.get(`${this.baseURL}/code-shares/`, { params }).then(res => res.data)
  }

  async getCodeShare(id: string): Promise<PeerCodeShare> {
    return apiClient.get(`${this.baseURL}/code-shares/${id}/`).then(res => res.data)
  }

  async createCodeShare(data: Partial<PeerCodeShare>): Promise<PeerCodeShare> {
    return apiClient.post(`${this.baseURL}/code-shares/`, data).then(res => res.data)
  }

  async updateCodeShare(id: string, data: Partial<PeerCodeShare>): Promise<PeerCodeShare> {
    return apiClient.patch(`${this.baseURL}/code-shares/${id}/`, data).then(res => res.data)
  }

  async deleteCodeShare(id: string): Promise<void> {
    return apiClient.delete(`${this.baseURL}/code-shares/${id}/`)
  }

  async likeCodeShare(id: string): Promise<{ message: string, likes_count: number }> {
    return apiClient.post(`${this.baseURL}/code-shares/${id}/like/`).then(res => res.data)
  }

  async downloadCodeShare(id: string): Promise<{ downloads_count: number }> {
    return apiClient.post(`${this.baseURL}/code-shares/${id}/download/`).then(res => res.data)
  }

  // Group Challenges API
  async getGroupChallenges(params?: {
    search?: string
    challenge_type?: string
    difficulty_level?: string
    status?: string
    ordering?: string
  }): Promise<GroupChallenge[]> {
    return apiClient.get(`${this.baseURL}/challenges/`, { params }).then(res => res.data)
  }

  async getGroupChallenge(id: string): Promise<GroupChallenge> {
    return apiClient.get(`${this.baseURL}/challenges/${id}/`).then(res => res.data)
  }

  async createGroupChallenge(data: Partial<GroupChallenge>): Promise<GroupChallenge> {
    return apiClient.post(`${this.baseURL}/challenges/`, data).then(res => res.data)
  }

  async updateGroupChallenge(id: string, data: Partial<GroupChallenge>): Promise<GroupChallenge> {
    return apiClient.patch(`${this.baseURL}/challenges/${id}/`, data).then(res => res.data)
  }

  async deleteGroupChallenge(id: string): Promise<void> {
    return apiClient.delete(`${this.baseURL}/challenges/${id}/`)
  }

  async participateInChallenge(id: string): Promise<void> {
    return apiClient.post(`${this.baseURL}/challenges/${id}/participate/`)
  }

  async getChallengeParticipants(id: string): Promise<ChallengeParticipation[]> {
    return apiClient.get(`${this.baseURL}/challenges/${id}/participants/`).then(res => res.data)
  }

  // Challenge Participation API
  async getMyParticipations(): Promise<ChallengeParticipation[]> {
    return apiClient.get(`${this.baseURL}/participations/`).then(res => res.data)
  }

  async submitChallenge(id: string, data: {
    submission_content: string
    code_files: any[]
  }): Promise<void> {
    return apiClient.post(`${this.baseURL}/participations/${id}/submit/`, data)
  }

  // Mentorship API
  async getMentorshipRelationships(params?: {
    status?: string
  }): Promise<MentorshipRelationship[]> {
    return apiClient.get(`${this.baseURL}/mentorships/`, { params }).then(res => res.data)
  }

  async createMentorshipRelationship(data: Partial<MentorshipRelationship>): Promise<MentorshipRelationship> {
    return apiClient.post(`${this.baseURL}/mentorships/`, data).then(res => res.data)
  }

  async acceptMentorship(id: string): Promise<void> {
    return apiClient.post(`${this.baseURL}/mentorships/${id}/accept/`)
  }

  async completeMentorship(id: string): Promise<void> {
    return apiClient.post(`${this.baseURL}/mentorships/${id}/complete/`)
  }

  // Mentorship Sessions API
  async getMentorshipSessions(params?: {
    status?: string
    session_type?: string
    ordering?: string
  }): Promise<MentorshipSession[]> {
    return apiClient.get(`${this.baseURL}/sessions/`, { params }).then(res => res.data)
  }

  async createMentorshipSession(data: Partial<MentorshipSession>): Promise<MentorshipSession> {
    return apiClient.post(`${this.baseURL}/sessions/`, data).then(res => res.data)
  }

  async startMentorshipSession(id: string): Promise<void> {
    return apiClient.post(`${this.baseURL}/sessions/${id}/start/`)
  }

  async completeMentorshipSession(id: string, data: {
    notes?: string
    action_items?: string[]
  }): Promise<void> {
    return apiClient.post(`${this.baseURL}/sessions/${id}/complete/`, data)
  }

  // Overview/Dashboard API
  async getCollaborationOverview(): Promise<CollaborationOverview> {
    return apiClient.get(`${this.baseURL}/overview/overview/`).then(res => res.data)
  }

  // Utility methods
  async searchStudyGroups(query: string): Promise<StudyGroup[]> {
    return this.getStudyGroups({ search: query })
  }

  async searchCodeShares(query: string): Promise<PeerCodeShare[]> {
    return this.getCodeShares({ search: query })
  }

  async getPublicStudyGroups(): Promise<StudyGroup[]> {
    return this.getStudyGroups({ is_public: true })
  }

  async getMyStudyGroups(): Promise<StudyGroup[]> {
    const groups = await this.getStudyGroups()
    return groups.filter(group => group.is_member)
  }

  async getLanguageStats(): Promise<{ language: string, count: number }[]> {
    const codeShares = await this.getCodeShares()
    const stats: { [key: string]: number } = {}
    
    codeShares.forEach(share => {
      stats[share.language] = (stats[share.language] || 0) + 1
    })
    
    return Object.entries(stats).map(([language, count]) => ({
      language,
      count
    })).sort((a, b) => b.count - a.count)
  }
}

export const collaborationService = new CollaborationService()
export default collaborationService