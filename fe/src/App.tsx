import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import TaskList from './pages/TaskList';
import TaskDetail from './pages/TaskDetail';
import QuestionnaireList from './pages/QuestionnaireList';
import QuestionnaireEdit from './pages/QuestionnaireEdit';
import { Box } from '@mui/material';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>Document Processing Pipeline</h1>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<QuestionnaireList />} />
            <Route path="/questionnaire/new" element={<QuestionnaireEdit />} />
            <Route path="/questionnaire/:id" element={<QuestionnaireEdit />} />
            <Route path="/tasks/:taskId" element={<TaskDetail />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App; 