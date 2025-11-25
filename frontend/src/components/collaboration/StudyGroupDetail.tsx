/**
 * Study Group Detail Component
 * 
 * Detailed view for a specific study group with:
 * - Group information
 * - Member management
 * - Discussion forum
 * - Code sharing
 * - Group challenges
 * 
 * Author: Cavin Otieno
 * Created: 2025-11-26
 */

import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
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
  Settings,
  UserPlus,
  UserMinus,
  Crown,
  Shield,
  Calendar,
  Activity,
  Star,
  ArrowLeft,
} from 'lucide-react'
import Button from '../ui/button'
import Badge from '../ui/badge'
import { Avatar, AvatarFallback } from '../ui/avatar'
import Skeleton from '../ui/skeleton'

import collaborationService, {
  StudyGroup,
  StudyGroupMembership,
  DiscussionTopic,
  PeerCodeShare,
  GroupChallenge,
} from '../../services/collaborationService'

// Members List Component
const MembersList: React.FC<{ group: StudyGroup, memberships: StudyGroupMembership[] }> = ({ group, memberships }) => {
  const getRoleIcon = (role: string) => {
    switch (role) {
      case 'leader':
        return <Crown className="h-4 w-4 text-yellow-500" />
      case 'moderator':
        return <Shield className="h-4 w-4 text-blue-500" />
      default:
        return <Users className="h-4 w-4 text-gray-500" />
    }
  }

  const getRoleBadgeVariant = (role: string) => {
    switch (role) {
      case 'leader':
        return 'default'
      case 'moderator':
        return 'secondary'
      default:
        return 'outline'
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">Members ({memberships.length}/{group.max_members})</h3>
      </div>
      
      <div className="grid gap-3">
        {memberships.map((membership) => (
          <div key={membership.id} className="flex items-center justify-between p-3 border rounded-lg">
            <div className="flex items-center space-x-3">
              <Avatar>
                <AvatarFallback>
                  {membership.user.first_name?.[0]}{membership.user.last_name?.[0] || membership.user.username[0]}
                </AvatarFallback>
              </Avatar>
              <div>
                <div className="flex items-center space-x-2">
                  <span className="font-medium">
                    {membership.user.first_name} {membership.user.last_name}
                  </span>
                  {membership.user.username && (
                    <span className="text-sm text-gray-500">@{membership.user.username}</span>
                  )}
                </div>
                <div className="flex items-center space-x-2 mt-1">
                  {getRoleIcon(membership.role)}
                  <Badge variant={getRoleBadgeVariant(membership.role)}>
                    {membership.role}
                  </Badge>
                </div>
              </div>
            </div>
            <div className="text-sm text-gray-500">
              Joined {new Date(membership.joined_at).toLocaleDateString()}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

// Group Discussion Component
const GroupDiscussions: React.FC<{ groupId: string }> = ({ groupId }) => {
  const [topics, setTopics] = useState<DiscussionTopic[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadTopics()
  }, [groupId])

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
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">Discussions</h3>
        <Button size="sm">
          <MessageSquare className="h-4 w-4 mr-2" />
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

// Group Code Sharing Component
const GroupCodeSharing: React.FC<{ groupId: string }> = ({ groupId }) => {
  const [codeShares, setCodeShares] = useState<PeerCodeShare[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadCodeShares()
  }, [groupId])

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
        <h3 className="text-lg font-semibold">Shared Code</h3>
        <Button size="sm">
          <Code className="h-4 w-4 mr-2" />
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
                </div>
                <Button variant="outline" size="sm">
                  View Code
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}

// Group Challenges Component
const GroupChallenges: React.FC<{ groupId: string }> = ({ groupId }) => {
  const [challenges, setChallenges] = useState<GroupChallenge[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadChallenges()
  }, [groupId])

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

  if (loading) {
    return (
      <div className="space-y-4">
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
          <Trophy className="h-4 w-4 mr-2" />
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
                    <Button size="sm">
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

// Main Study Group Detail Component
const StudyGroupDetail: React.FC = () => {
  const { groupId } = useParams<{ groupId: string }>()
  const navigate = useNavigate()
  const [group, setGroup] = useState<StudyGroup | null>(null)
  const [memberships, setMemberships] = useState<StudyGroupMembership[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (groupId) {
      loadGroupData()
    }
  }, [groupId])

  const loadGroupData = async () => {
    try {
      setLoading(true)
      const [groupData, membersData] = await Promise.all([
        collaborationService.getStudyGroup(groupId!),
        collaborationService.getStudyGroupMembers(groupId!),
      ])
      setGroup(groupData)
      setMemberships(membersData)
    } catch (error) {
      console.error('Failed to load study group:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleLeaveGroup = async () => {
    if (!groupId) return
    
    try {
      await collaborationService.leaveStudyGroup(groupId)
      navigate('/collaboration')
    } catch (error) {
      console.error('Failed to leave study group:', error)
    }
  }

  if (loading || !group) {
    return (
      <div className="space-y-6">
        <div className="flex items-center space-x-4">
          <Skeleton className="h-10 w-10 rounded-full" />
          <Skeleton className="h-8 w-64" />
        </div>
        <Skeleton className="h-96 w-full" />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Button
            variant="outline"
            size="sm"
            onClick={() => navigate('/collaboration')}
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back
          </Button>
          <div>
            <h1 className="text-3xl font-bold">{group.name}</h1>
            <p className="text-gray-600">
              {group.subject_area} • {group.level} • {group.member_count}/{group.max_members} members
            </p>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          {group.is_member ? (
            <Button variant="outline" onClick={handleLeaveGroup}>
              <UserMinus className="h-4 w-4 mr-2" />
              Leave Group
            </Button>
          ) : (
            <Button>
              <UserPlus className="h-4 w-4 mr-2" />
              Join Group
            </Button>
          )}
          <Button variant="outline">
            <Settings className="h-4 w-4 mr-2" />
            Settings
          </Button>
        </div>
      </div>

      {/* Group Info */}
      <Card>
        <CardHeader>
          <CardTitle>About this Group</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-700 mb-4">{group.description}</p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <p className="text-sm font-medium text-gray-600">Subject Area</p>
              <p className="text-lg">{group.subject_area}</p>
            </div>
            <div>
              <p className="text-sm font-medium text-gray-600">Level</p>
              <p className="text-lg capitalize">{group.level}</p>
            </div>
            <div>
              <p className="text-sm font-medium text-gray-600">Privacy</p>
              <p className="text-lg">{group.is_public ? 'Public' : 'Private'}</p>
            </div>
            <div>
              <p className="text-sm font-medium text-gray-600">Created</p>
              <p className="text-lg">{new Date(group.created_at).toLocaleDateString()}</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Tabs */}
      <Tabs defaultValue="discussions" className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="discussions">Discussions</TabsTrigger>
          <TabsTrigger value="code-sharing">Code Sharing</TabsTrigger>
          <TabsTrigger value="challenges">Challenges</TabsTrigger>
          <TabsTrigger value="members">Members</TabsTrigger>
        </TabsList>

        <TabsContent value="discussions">
          <GroupDiscussions groupId={group.id} />
        </TabsContent>

        <TabsContent value="code-sharing">
          <GroupCodeSharing groupId={group.id} />
        </TabsContent>

        <TabsContent value="challenges">
          <GroupChallenges groupId={group.id} />
        </TabsContent>

        <TabsContent value="members">
          <MembersList group={group} memberships={memberships} />
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default StudyGroupDetail