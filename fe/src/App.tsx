import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import TaskList from './pages/TaskList';
import TaskDetail from './pages/TaskDetail';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>Document Processing Pipeline</h1>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<TaskList />} />
            <Route path="/:taskId" element={<TaskDetail />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App; 