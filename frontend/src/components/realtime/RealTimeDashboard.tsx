/**
 * Real-time Dashboard Component
 * 
 * Provides live dashboard updates via WebSocket connections including
 * real-time metrics, activities, and alerts.
 * 
 * Author: MiniMax Agent
 * Created: 2025-11-26
 */

import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { 
  Activity, 
  TrendingUp, 
  TrendingDown, 
  AlertTriangle, 
  CheckCircle,
  RefreshCw,
  Wifi,
  WifiOff,
  Clock,
  Target
} from 'lucide-react';
import { useRealtimeDashboard, useRealtimeAlerts, useRealtimeMetrics } from '@/hooks/useWebSocket';

interface RealTimeDashboardProps {
  className?: string;
  autoRefresh?: boolean;
  refreshInterval?: number;
}

export const RealTimeDashboard: React.FC<RealTimeDashboardProps> = ({
  className = '',
  autoRefresh = true,
  refreshInterval = 30000 // 30 seconds
}) => {
  const [isRefreshing, setIsRefreshing] = useState(false);
  
  // Real-time data hooks
  const {
    dashboardData,
    recentActivities,
    metrics,
    connectionStatus: dashboardStatus,
    isConnected: dashboardConnected,
    refreshData
  } = useRealtimeDashboard();

  const {
    alerts,
    unreadCount,
    connectionStatus: alertsStatus,
    acknowledgeAlert
  } = useRealtimeAlerts();

  const {
    metrics: realtimeMetrics,
    historicalData,
    connectionStatus: metricsStatus,
    isConnected: metricsConnected
  } = useRealtimeMetrics();

  // Handle manual refresh
  const handleRefresh = async () => {
    setIsRefreshing(true);
    try {
      refreshData();
      // Wait a moment for data to update
      setTimeout(() => setIsRefreshing(false), 1000);
    } catch (error) {
      console.error('Refresh failed:', error);
      setIsRefreshing(false);
    }
  };

  // Auto-refresh functionality
  useEffect(() => {
    if (!autoRefresh) return;

    const interval = setInterval(() => {
      handleRefresh();
    }, refreshInterval);

    return () => clearInterval(interval);
  }, [autoRefresh, refreshInterval]);

  // Connection status indicators
  const getConnectionStatus = (status: string) => {
    switch (status) {
      case 'connected':
        return { icon: Wifi, color: 'text-green-500', text: 'Connected' };
      case 'connecting':
        return { icon: RefreshCw, color: 'text-yellow-500', text: 'Connecting' };
      case 'error':
        return { icon: WifiOff, color: 'text-red-500', text: 'Error' };
      default:
        return { icon: WifiOff, color: 'text-gray-500', text: 'Disconnected' };
    }
  };

  const dashboardConn = getConnectionStatus(dashboardStatus);
  const alertsConn = getConnectionStatus(alertsStatus);
  const metricsConn = getConnectionStatus(metricsStatus);

  // Helper functions
  const formatTime = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString();
  };

  const getPerformanceTrend = (current: number, previous: number) => {
    const change = current - previous;
    if (change > 0) {
      return { icon: TrendingUp, color: 'text-green-500', text: `+${change.toFixed(1)}%` };
    } else if (change < 0) {
      return { icon: TrendingDown, color: 'text-red-500', text: `${change.toFixed(1)}%` };
    } else {
      return { icon: Activity, color: 'text-gray-500', text: '0.0%' };
    }
  };

  const getAlertSeverity = (severity: string) => {
    switch (severity) {
      case 'high':
        return { variant: 'destructive' as const, icon: AlertTriangle };
      case 'medium':
        return { variant: 'secondary' as const, icon: AlertTriangle };
      case 'low':
        return { variant: 'outline' as const, icon: CheckCircle };
      default:
        return { variant: 'outline' as const, icon: CheckCircle };
    }
  };

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Connection Status Header */}
      <Card>
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <CardTitle className="text-lg font-semibold">Real-time Dashboard</CardTitle>
            <div className="flex items-center gap-4">
              <Button
                variant="outline"
                size="sm"
                onClick={handleRefresh}
                disabled={isRefreshing}
                className="gap-2"
              >
                <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
                Refresh
              </Button>
              
              <div className="flex items-center gap-3 text-sm">
                <div className="flex items-center gap-1">
                  <dashboardConn.icon className={`w-4 h-4 ${dashboardConn.color}`} />
                  <span className={dashboardConn.color}>Dashboard</span>
                </div>
                <div className="flex items-center gap-1">
                  <alertsConn.icon className={`w-4 h-4 ${alertsConn.color}`} />
                  <span className={alertsConn.color}>Alerts</span>
                  {unreadCount > 0 && (
                    <Badge variant="destructive" className="ml-1">
                      {unreadCount}
                    </Badge>
                  )}
                </div>
                <div className="flex items-center gap-1">
                  <metricsConn.icon className={`w-4 h-4 ${metricsConn.color}`} />
                  <span className={metricsConn.color}>Metrics</span>
                </div>
              </div>
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* Main Dashboard Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Progress Summary */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Target className="w-5 h-5" />
              Learning Progress
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {dashboardData ? (
              <>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">Overall Progress</p>
                    <div className="flex items-center gap-2">
                      <Progress value={dashboardData.progress_summary?.overall_progress || 0} className="flex-1" />
                      <span className="text-sm font-medium">
                        {dashboardData.progress_summary?.overall_progress?.toFixed(1) || 0}%
                      </span>
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">Current Level</p>
                    <Badge variant="outline">
                      {dashboardData.progress_summary?.current_level || 'Beginner'}
                    </Badge>
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-4 pt-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">
                      {dashboardData.progress_summary?.modules_completed || 0}
                    </div>
                    <p className="text-sm text-muted-foreground">Completed</p>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">
                      {dashboardData.progress_summary?.total_modules || 0}
                    </div>
                    <p className="text-sm text-muted-foreground">Total</p>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-orange-600">
                      {dashboardData.progress_summary?.streak_days || 0}
                    </div>
                    <p className="text-sm text-muted-foreground">Day Streak</p>
                  </div>
                </div>
              </>
            ) : (
              <div className="text-center py-8 text-muted-foreground">
                <Activity className="w-8 h-8 mx-auto mb-2 opacity-50" />
                <p>Loading progress data...</p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Real-time Metrics */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Activity className="w-5 h-5" />
              Live Metrics
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {metrics || realtimeMetrics ? (
              <>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-muted-foreground">Daily Activities</span>
                    <span className="font-medium">
                      {(metrics || realtimeMetrics)?.daily_activities || 0}
                    </span>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-muted-foreground">Average Score</span>
                    <div className="flex items-center gap-2">
                      <span className="font-medium">
                        {(metrics || realtimeMetrics)?.average_score?.toFixed(1) || 0}%
                      </span>
                      {(metrics || realtimeMetrics)?.performance_trend && (
                        (() => {
                          const trend = (metrics || realtimeMetrics).performance_trend;
                          const TrendIcon = trend === 'improving' ? TrendingUp : 
                                           trend === 'declining' ? TrendingDown : Activity;
                          const color = trend === 'improving' ? 'text-green-500' : 
                                       trend === 'declining' ? 'text-red-500' : 'text-gray-500';
                          return <TrendIcon className={`w-4 h-4 ${color}`} />;
                        })()
                      )}
                    </div>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-muted-foreground">Engagement</span>
                    <div className="flex items-center gap-2">
                      <Progress 
                        value={(metrics || realtimeMetrics)?.engagement_level || 0} 
                        className="w-16 h-2" 
                      />
                      <span className="text-sm">
                        {(metrics || realtimeMetrics)?.engagement_level || 0}%
                      </span>
                    </div>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-muted-foreground">Last Updated</span>
                    <div className="flex items-center gap-1 text-xs text-muted-foreground">
                      <Clock className="w-3 h-3" />
                      {formatTime((metrics || realtimeMetrics)?.last_updated || new Date().toISOString())}
                    </div>
                  </div>
                </div>
              </>
            ) : (
              <div className="text-center py-4 text-muted-foreground">
                <Activity className="w-6 h-6 mx-auto mb-2 opacity-50" />
                <p className="text-sm">Loading metrics...</p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Recent Activities and Alerts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Recent Activities */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Activity className="w-5 h-5" />
              Recent Activities
              <Badge variant="outline" className="ml-auto">
                {recentActivities?.length || 0}
              </Badge>
            </CardTitle>
          </CardHeader>
          <CardContent>
            {recentActivities && recentActivities.length > 0 ? (
              <div className="space-y-3 max-h-64 overflow-y-auto">
                {recentActivities.slice(0, 10).map((activity, index) => (
                  <div key={index} className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg">
                    <div className="flex-shrink-0 mt-0.5">
                      <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900">
                        {activity.type === 'module_progress' ? `Module: ${activity.title}` :
                         activity.type === 'assessment_completed' ? `Assessment: ${activity.title}` :
                         'Learning Activity'}
                      </p>
                      <p className="text-xs text-gray-500">
                        {activity.status && `Status: ${activity.status}`}
                        {activity.score && ` • Score: ${activity.score}%`}
                      </p>
                      <p className="text-xs text-gray-400">
                        {formatTime(activity.timestamp)}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-muted-foreground">
                <Activity className="w-8 h-8 mx-auto mb-2 opacity-50" />
                <p>No recent activities</p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Live Alerts */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="w-5 h-5" />
              Live Alerts
              {unreadCount > 0 && (
                <Badge variant="destructive" className="ml-auto">
                  {unreadCount} New
                </Badge>
              )}
            </CardTitle>
          </CardHeader>
          <CardContent>
            {alerts && alerts.length > 0 ? (
              <div className="space-y-3 max-h-64 overflow-y-auto">
                {alerts.slice(0, 10).map((alert, index) => {
                  const severityInfo = getAlertSeverity(alert.severity);
                  const AlertIcon = severityInfo.icon;
                  
                  return (
                    <div key={index} className="flex items-start gap-3 p-3 border rounded-lg">
                      <div className="flex-shrink-0 mt-0.5">
                        <AlertIcon className="w-4 h-4" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <Badge variant={severityInfo.variant} className="text-xs">
                            {alert.type}
                          </Badge>
                          <span className="text-xs text-gray-400">
                            {formatTime(alert.timestamp)}
                          </span>
                        </div>
                        <p className="text-sm font-medium text-gray-900 mb-1">
                          {alert.title}
                        </p>
                        <p className="text-xs text-gray-600 mb-2">
                          {alert.message}
                        </p>
                        {alert.actionable && (
                          <Button 
                            variant="outline" 
                            size="sm"
                            onClick={() => acknowledgeAlert(alert.id)}
                            className="text-xs"
                          >
                            Acknowledge
                          </Button>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="text-center py-8 text-muted-foreground">
                <CheckCircle className="w-8 h-8 mx-auto mb-2 opacity-50" />
                <p>No active alerts</p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Dashboard Insights */}
      {dashboardData?.insights && dashboardData.insights.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Target className="w-5 h-5" />
              Personalized Insights
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {dashboardData.insights.map((insight, index) => (
                <div key={index} className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                  <div className="flex items-start gap-3">
                    <div className="flex-shrink-0 mt-0.5">
                      <CheckCircle className="w-5 h-5 text-blue-500" />
                    </div>
                    <p className="text-sm text-blue-800">{insight}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default RealTimeDashboard;