/**
 * Collaboration Page
 * 
 * Main page for collaboration features with routing.
 * 
 * Author: Cavin Otieno
 * Created: 2025-11-26
 */

import React from 'react'
import { Routes, Route } from 'react-router-dom'
import MainLayout from '../components/layout/MainLayout'
import { CollaborationDashboard, StudyGroupDetail } from '../components/collaboration'

const CollaborationPage: React.FC = () => {
  return (
    <MainLayout>
      <Routes>
        <Route path="/" element={<CollaborationDashboard />} />
        <Route path="/study-groups/:groupId" element={<StudyGroupDetail />} />
      </Routes>
    </MainLayout>
  )
}

export default CollaborationPage