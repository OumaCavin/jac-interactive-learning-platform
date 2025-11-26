// JAC Learning Platform - TypeScript utilities by Cavin Otieno

/**
 * Collaboration Dashboard - Frontend Component
 * 
 * Main dashboard for collaboration features:
 * - Study groups overview
 * - Active discussions
 * - Code sharing
 * - Group challenges
 * - Mentorship system
 * 
 * Author: Cavin Otieno
 * Created: 2025-11-26
 */

import React, { useState, useEffect } from 'react'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '../ui/card'
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from '../ui/tabs'
import {
  Users,
  MessageSquare,
  Code,
  Trophy,
  GraduationCap,
  Plus,
  Search,
  Filter,
  Calendar,
  Star,
  Activity,
  TrendingUp,
} from 'lucide-react'
import Button from '../ui/button'
import Input from '../ui/input'
import Badge from '../ui/badge'
import Skeleton from '../ui/skeleton'
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from '../ui/alert-dialog'

import collaborationService, {
  CollaborationOverview,
  StudyGroup,
  DiscussionTopic,
  PeerCodeShare,
  GroupChallenge,
  MentorshipRelationship,
} from '../../services/collaborationService'

// Study Groups Component
const StudyGroupsSection: React.FC = () => {
  const [studyGroups, setStudyGroups] = useState<StudyGroup[]>([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')

  useEffect(() => {
    loadStudyGroups()
  }, [])

  const loadStudyGroups = async () => {
    try {
      setLoading(true)
      const groups = await collaborationService.getStudyGroups()
      setStudyGroups(groups)
    } catch (error) {
      console.error('Failed to load study groups:', error)
    } finally {
      setLoading(false)
    }
  }

  const filteredGroups = studyGroups.filter(group =>
    group.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    group.subject_area.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const handleJoinGroup = async (groupId: string) => {
    try {
      await collaborationService.joinStudyGroup(groupId)
      await loadStudyGroups() // Refresh the list
    } catch (error) {
      console.error('Failed to join study group:', error)
    }
  }

  if (loading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-20 w-full" />
        <Skeleton className="h-20 w-full" />
        <Skeleton className="h-20 w-full" />
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">Study Groups</h3>
        <Button size="sm">
          <Plus className="h-4 w-4 mr-2" />
          Create Group
        </Button>
      </div>

      <div className="flex items-center space-x-2">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
          <Input
            placeholder="Search study groups..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10"
          />
        </div>
        <Button variant="outline" size="sm">
          <Filter className="h-4 w-4 mr-2" />
          Filter
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {filteredGroups.map((group) => (
          <Card key={group.id} className="hover:shadow-md transition-shadow">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <CardTitle className="text-base">{group.name}</CardTitle>
                <Badge variant={group.is_member ? "default" : "secondary"}>
                  {group.is_member ? "Joined" : "Public"}
                </Badge>
              </div>
              <CardDescription className="text-sm">
                {group.subject_area} • {group.level}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between text-sm text-gray-600 mb-3">
                <span className="flex items-center">
                  <Users className="h-4 w-4 mr-1" />
                  {group.member_count}/{group.max_members} members
                </span>
                <span>{group.level}</span>
              </div>
              <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                {group.description}
              </p>
              <div className="flex items-center justify-between">
                <span className="text-xs text-gray-500">
                  Created by {group.created_by.username}
                </span>
                {group.is_member ? (
                  <Button variant="outline" size="sm">
                    View Group
                  </Button>
                ) : (
                  <Button 
                    size="sm"
                    onClick={() => handleJoinGroup(group.id)}
                  >
                    Join Group
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}

// Discussion Forums Component
const DiscussionForumsSection: React.FC = () => {
  const [topics, setTopics] = useState<DiscussionTopic[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadTopics()
  }, [])

  const loadTopics = async () => {
    try {
      setLoading(true)
      const data = await collaborationService.getDiscussionTopics()
      setTopics(data)
    } catch (error) {
      console.error('Failed to load discussion topics:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-16 w-full" />
        <Skeleton className="h-16 w-full" />
        <Skeleton className="h-16 w-full" />
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">Active Discussions</h3>
        <Button size="sm">
          <Plus className="h-4 w-4 mr-2" />
          New Topic
        </Button>
      </div>

      <div className="space-y-3">
        {topics.map((topic) => (
          <Card key={topic.id} className="hover:shadow-sm transition-shadow cursor-pointer">
            <CardContent className="p-4">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    {topic.is_pinned && (
                      <Star className="h-4 w-4 text-yellow-500" />
                    )}
                    <h4 className="font-medium">{topic.title}</h4>
                    <Badge variant={topic.status === 'open' ? 'default' : 'secondary'}>
                      {topic.status}
                    </Badge>
                  </div>
                  <p className="text-sm text-gray-600 line-clamp-2 mb-2">
                    {topic.content}
                  </p>
                  <div className="flex items-center text-xs text-gray-500 space-x-4">
                    <span>by {topic.author.username}</span>
                    <span>{topic.posts_count} replies</span>
                    <span>{topic.views_count} views</span>
                    <span>{new Date(topic.created_at).toLocaleDateString()}</span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}

// Code Sharing Component
const CodeSharingSection: React.FC = () => {
  const [codeShares, setCodeShares] = useState<PeerCodeShare[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadCodeShares()
  }, [])

  const loadCodeShares = async () => {
    try {
      setLoading(true)
      const data = await collaborationService.getCodeShares()
      setCodeShares(data)
    } catch (error) {
      console.error('Failed to load code shares:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleLike = async (id: string) => {
    try {
      await collaborationService.likeCodeShare(id)
      await loadCodeShares()
    } catch (error) {
      console.error('Failed to like code share:', error)
    }
  }

  if (loading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-16 w-full" />
        <Skeleton className="h-16 w-full" />
        <Skeleton className="h-16 w-full" />
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">Code Sharing</h3>
        <Button size="sm">
          <Plus className="h-4 w-4 mr-2" />
          Share Code
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {codeShares.map((share) => (
          <Card key={share.id} className="hover:shadow-md transition-shadow">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <CardTitle className="text-base">{share.title}</CardTitle>
                <div className="flex items-center space-x-2">
                  <Badge variant="outline">{share.language}</Badge>
                  <Badge variant={share.share_type === 'tutorial' ? 'default' : 'secondary'}>
                    {share.share_type}
                  </Badge>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                {share.description}
              </p>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4 text-sm text-gray-500">
                  <span className="flex items-center">
                    <Star className="h-4 w-4 mr-1" />
                    {share.likes_count}
                  </span>
                  <span className="flex items-center">
                    <Activity className="h-4 w-4 mr-1" />
                    {share.downloads_count}
                  </span>
                  <span>{share.views_count} views</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleLike(share.id)}
                  >
                    <Star className={`h-4 w-4 mr-1 ${share.is_liked ? 'fill-current text-yellow-500' : ''}`} />
                    Like
                  </Button>
                  <Button variant="outline" size="sm">
                    View Code
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}

// Group Challenges Component
const GroupChallengesSection: React.FC = () => {
  const [challenges, setChallenges] = useState<GroupChallenge[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadChallenges()
  }, [])

  const loadChallenges = async () => {
    try {
      setLoading(true)
      const data = await collaborationService.getGroupChallenges()
      setChallenges(data)
    } catch (error) {
      console.error('Failed to load group challenges:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleParticipate = async (id: string) => {
    try {
      await collaborationService.participateInChallenge(id)
      await loadChallenges()
    } catch (error) {
      console.error('Failed to participate in challenge:', error)
    }
  }

  if (loading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-20 w-full" />
        <Skeleton className="h-20 w-full" />
        <Skeleton className="h-20 w-full" />
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">Group Challenges</h3>
        <Button size="sm">
          <Plus className="h-4 w-4 mr-2" />
          Create Challenge
        </Button>
      </div>

      <div className="space-y-4">
        {challenges.map((challenge) => (
          <Card key={challenge.id} className="hover:shadow-md transition-shadow">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-lg">{challenge.title}</CardTitle>
                  <CardDescription>
                    {challenge.challenge_type} • {challenge.difficulty_level}
                  </CardDescription>
                </div>
                <div className="flex items-center space-x-2">
                  <Badge variant={challenge.status === 'active' ? 'default' : 'secondary'}>
                    {challenge.status}
                  </Badge>
                  <Badge variant="outline">
                    {challenge.participant_count} participants
                  </Badge>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600 mb-4 line-clamp-3">
                {challenge.description}
              </p>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4 text-sm text-gray-500">
                  <span className="flex items-center">
                    <Calendar className="h-4 w-4 mr-1" />
                    Ends {new Date(challenge.end_date).toLocaleDateString()}
                  </span>
                  <span>{challenge.estimated_duration}h estimated</span>
                </div>
                <div className="flex items-center space-x-2">
                  {challenge.is_participating ? (
                    <Button variant="outline" size="sm">
                      View Submission
                    </Button>
                  ) : (
                    <Button 
                      size="sm"
                      onClick={() => handleParticipate(challenge.id)}
                    >
                      Participate
                    </Button>
                  )}
                  <Button variant="outline" size="sm">
                    View Details
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}

// Mentorship Component
const MentorshipSection: React.FC = () => {
  const [mentorships, setMentorships] = useState<MentorshipRelationship[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadMentorships()
  }, [])

  const loadMentorships = async () => {
    try {
      setLoading(true)
      const data = await collaborationService.getMentorshipRelationships()
      setMentorships(data)
    } catch (error) {
      console.error('Failed to load mentorship relationships:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleAccept = async (id: string) => {
    try {
      await collaborationService.acceptMentorship(id)
      await loadMentorships()
    } catch (error) {
      console.error('Failed to accept mentorship:', error)
    }
  }

  if (loading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-16 w-full" />
        <Skeleton className="h-16 w-full" />
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">Mentorship</h3>
        <Button size="sm">
          <Plus className="h-4 w-4 mr-2" />
          Find Mentor
        </Button>
      </div>

      <div className="space-y-3">
        {mentorships.map((mentorship) => (
          <Card key={mentorship.id} className="hover:shadow-sm transition-shadow">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="flex items-center space-x-2 mb-2">
                    <GraduationCap className="h-4 w-4 text-blue-500" />
                    <span className="font-medium">
                      {mentorship.mentor.username} → {mentorship.mentee.username}
                    </span>
                    <Badge variant={mentorship.status === 'active' ? 'default' : 'secondary'}>
                      {mentorship.status}
                    </Badge>
                  </div>
                  <p className="text-sm text-gray-600 mb-2">
                    {mentorship.goals}
                  </p>
                  <div className="flex items-center space-x-4 text-xs text-gray-500">
                    <span>Areas: {mentorship.subject_areas.join(', ')}</span>
                    <span>{mentorship.meeting_frequency}</span>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  {mentorship.status === 'pending' && (
                    <Button size="sm" onClick={() => handleAccept(mentorship.id)}>
                      Accept
                    </Button>
                  )}
                  <Button variant="outline" size="sm">
                    View Sessions
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}

// Statistics Overview Component
const StatsOverview: React.FC<{ overview: CollaborationOverview }> = ({ overview }) => {
  const stats = [
    {
      title: 'Study Groups',
      value: overview.total_study_groups,
      icon: Users,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
    },
    {
      title: 'Active Discussions',
      value: overview.active_discussions,
      icon: MessageSquare,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
    },
    {
      title: 'Code Shares',
      value: overview.code_shares,
      icon: Code,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100',
    },
    {
      title: 'Active Challenges',
      value: overview.active_challenges,
      icon: Trophy,
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-100',
    },
    {
      title: 'Active Mentorships',
      value: overview.active_mentorships,
      icon: GraduationCap,
      color: 'text-indigo-600',
      bgColor: 'bg-indigo-100',
    },
  ]

  return (
    <div className="grid gap-4 md:grid-cols-3 lg:grid-cols-5 mb-6">
      {stats.map((stat) => {
        const Icon = stat.icon
        return (
          <Card key={stat.title}>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                  <p className="text-2xl font-bold">{stat.value}</p>
                </div>
                <div className={`p-3 rounded-full ${stat.bgColor}`}>
                  <Icon className={`h-6 w-6 ${stat.color}`} />
                </div>
              </div>
            </CardContent>
          </Card>
        )
      })}
    </div>
  )
}

// Main Collaboration Dashboard Component
const CollaborationDashboard: React.FC = () => {
  const [overview, setOverview] = useState<CollaborationOverview | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadOverview()
  }, [])

  const loadOverview = async () => {
    try {
      setLoading(true)
      const data = await collaborationService.getCollaborationOverview()
      setOverview(data)
    } catch (error) {
      console.error('Failed to load collaboration overview:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading || !overview) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold">Collaboration</h1>
        </div>
        <div className="grid gap-4 md:grid-cols-3 lg:grid-cols-5">
          {[...Array(5)].map((_, i) => (
            <Card key={i}>
              <CardContent className="p-6">
                <Skeleton className="h-20 w-full" />
              </CardContent>
            </Card>
          ))}
        </div>
        <Skeleton className="h-96 w-full" />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Collaboration</h1>
          <p className="text-gray-600">Connect, learn, and grow together</p>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="outline">
            <TrendingUp className="h-4 w-4 mr-2" />
            View Analytics
          </Button>
        </div>
      </div>

      <StatsOverview overview={overview} />

      <Tabs defaultValue="study-groups" className="w-full">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="study-groups">Study Groups</TabsTrigger>
          <TabsTrigger value="discussions">Discussions</TabsTrigger>
          <TabsTrigger value="code-sharing">Code Sharing</TabsTrigger>
          <TabsTrigger value="challenges">Challenges</TabsTrigger>
          <TabsTrigger value="mentorship">Mentorship</TabsTrigger>
        </TabsList>

        <TabsContent value="study-groups">
          <StudyGroupsSection />
        </TabsContent>

        <TabsContent value="discussions">
          <DiscussionForumsSection />
        </TabsContent>

        <TabsContent value="code-sharing">
          <CodeSharingSection />
        </TabsContent>

        <TabsContent value="challenges">
          <GroupChallengesSection />
        </TabsContent>

        <TabsContent value="mentorship">
          <MentorshipSection />
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default CollaborationDashboard