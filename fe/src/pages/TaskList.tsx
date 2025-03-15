import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

interface Task {
  _id: string;
  name: string;
  status: string;
  createdAt: string;
}

const TaskList: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await axios.get('/api/tasks');
        setTasks(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching tasks:', error);
        setLoading(false);
      }
    };

    fetchTasks();
  }, []);

  const handleCreateTask = async () => {
    try {
      const response = await axios.post('/api/tasks', { name: 'New Task' });
      navigate(`/${response.data._id}`);
    } catch (error) {
      console.error('Error creating task:', error);
    }
  };

  if (loading) {
    return <div>Loading tasks...</div>;
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h2>Document Processing Tasks</h2>
        <button onClick={handleCreateTask}>+ Create Task</button>
      </div>
      
      {tasks.length === 0 ? (
        <div>No tasks found. Create a new task to get started.</div>
      ) : (
        <div className="task-list">
          {tasks.map((task) => (
            <Link to={`/${task._id}`} key={task._id} style={{ textDecoration: 'none', color: 'inherit' }}>
              <div className="card">
                <h3>{task.name}</h3>
                <p>Status: <span style={{ 
                  color: task.status === 'completed' ? 'green' : 
                         task.status === 'in_progress' ? 'orange' : 
                         task.status === 'failed' ? 'red' : 'gray' 
                }}>{task.status}</span></p>
                <p>Created: {new Date(task.createdAt).toLocaleString()}</p>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
};

export default TaskList; 