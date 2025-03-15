import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';

interface Task {
  _id: string;
  name: string;
  status: string;
  sourceType: string;
  sourcePath: string;
  outputType: string;
  outputPath: string;
  googleApiKey: string;
  googleCredentials: string;
}

const TaskDetail: React.FC = () => {
  const { taskId } = useParams<{ taskId: string }>();
  const navigate = useNavigate();
  const [task, setTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [formData, setFormData] = useState({
    name: '',
    sourceType: 'google_drive',
    sourcePath: '',
    outputType: 'google_sheets',
    outputPath: '',
    googleApiKey: '',
    googleCredentials: ''
  });

  useEffect(() => {
    const fetchTask = async () => {
      try {
        if (taskId) {
          const response = await axios.get(`/api/tasks/${taskId}`);
          setTask(response.data);
          setFormData({
            name: response.data.name || '',
            sourceType: response.data.sourceType || 'google_drive',
            sourcePath: response.data.sourcePath || '',
            outputType: response.data.outputType || 'google_sheets',
            outputPath: response.data.outputPath || '',
            googleApiKey: response.data.googleApiKey || '',
            googleCredentials: response.data.googleCredentials || ''
          });
        }
        setLoading(false);
      } catch (error) {
        console.error('Error fetching task:', error);
        setLoading(false);
      }
    };

    fetchTask();
  }, [taskId]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axios.put(`/api/tasks/${taskId}`, formData);
      alert('Task configuration saved successfully!');
    } catch (error) {
      console.error('Error updating task:', error);
      alert('Failed to save task configuration.');
    }
  };

  const handleStartTask = async () => {
    try {
      await axios.post(`/api/tasks/${taskId}/start`);
      alert('Task started successfully!');
      // Refresh the task data
      const response = await axios.get(`/api/tasks/${taskId}`);
      setTask(response.data);
    } catch (error) {
      console.error('Error starting task:', error);
      alert('Failed to start task.');
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await axios.delete(`/api/tasks/${taskId}`);
        navigate('/');
      } catch (error) {
        console.error('Error deleting task:', error);
        alert('Failed to delete task.');
      }
    }
  };

  if (loading) {
    return <div>Loading task details...</div>;
  }

  if (!task) {
    return <div>Task not found.</div>;
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h2>Task Configuration</h2>
        <div>
          <button 
            onClick={() => navigate('/')}
            style={{ marginRight: '10px', backgroundColor: '#6c757d' }}
          >
            Back to List
          </button>
          <button 
            onClick={handleDelete}
            style={{ backgroundColor: '#dc3545' }}
          >
            Delete Task
          </button>
        </div>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Task Name</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="sourceType">Source Type</label>
          <select
            id="sourceType"
            name="sourceType"
            value={formData.sourceType}
            onChange={handleChange}
            required
          >
            <option value="google_drive">Google Drive</option>
            <option value="local">Local Directory</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="sourcePath">Source Path</label>
          <input
            type="text"
            id="sourcePath"
            name="sourcePath"
            value={formData.sourcePath}
            onChange={handleChange}
            placeholder={formData.sourceType === 'google_drive' ? 'Folder ID or Path' : 'Local Directory Path'}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="outputType">Output Type</label>
          <select
            id="outputType"
            name="outputType"
            value={formData.outputType}
            onChange={handleChange}
            required
          >
            <option value="google_sheets">Google Sheets</option>
            <option value="csv">CSV File</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="outputPath">Output Path</label>
          <input
            type="text"
            id="outputPath"
            name="outputPath"
            value={formData.outputPath}
            onChange={handleChange}
            placeholder={formData.outputType === 'google_sheets' ? 'Spreadsheet ID or New Spreadsheet Name' : 'Output File Path'}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="googleApiKey">Google API Key</label>
          <input
            type="text"
            id="googleApiKey"
            name="googleApiKey"
            value={formData.googleApiKey}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="googleCredentials">Google Service Account Credentials (JSON)</label>
          <textarea
            id="googleCredentials"
            name="googleCredentials"
            value={formData.googleCredentials}
            onChange={handleChange}
            rows={5}
            style={{ width: '100%', fontFamily: 'monospace' }}
            required
          />
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '20px' }}>
          <button type="submit">Save Configuration</button>
          <button 
            type="button" 
            onClick={handleStartTask}
            style={{ backgroundColor: '#007bff' }}
            disabled={task.status === 'in_progress'}
          >
            {task.status === 'in_progress' ? 'Task Running...' : 'Start Task'}
          </button>
        </div>
      </form>

      {task.status === 'completed' && (
        <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#d4edda', borderRadius: '4px', color: '#155724' }}>
          <h3>Task Completed Successfully</h3>
          <p>Your documents have been processed and the results are available at the specified output location.</p>
        </div>
      )}

      {task.status === 'failed' && (
        <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#f8d7da', borderRadius: '4px', color: '#721c24' }}>
          <h3>Task Failed</h3>
          <p>There was an error processing your documents. Please check your configuration and try again.</p>
        </div>
      )}
    </div>
  );
};

export default TaskDetail; 