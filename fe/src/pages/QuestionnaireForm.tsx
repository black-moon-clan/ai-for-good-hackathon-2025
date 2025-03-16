import React, { useState } from 'react';
import {
  Box,
  Button,
  TextField,
  Typography,
  Alert,
  Snackbar,
} from '@mui/material';
import QuestionItem from './QuestionItem';
import { apiRequest, api } from '../utils/api';

interface Question {
  text: string;
  type: string;
  options?: string[];
}

interface QuestionnaireFormProps {
  initialData?: {
    id: string;
    title: string;
    questions: Question[];
    status?: string;
  };
  onComplete?: () => void;
}

const QuestionnaireForm: React.FC<QuestionnaireFormProps> = ({ 
  initialData,
  onComplete 
}) => {
  const [title, setTitle] = useState(initialData?.title || '');
  const [questions, setQuestions] = useState<Question[]>(
    initialData?.questions || [{ text: '', type: 'open_ended' }]  // Default question when no initialData
  );
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const handleAddQuestion = () => {
    setQuestions([...questions, { text: '', type: 'open_ended' }]);
  };

  const handleUpdateQuestion = (index: number, field: string, value: any) => {
    const updatedQuestions = [...questions];
    updatedQuestions[index] = {
      ...updatedQuestions[index],
      [field]: value,
    };
    setQuestions(updatedQuestions);
  };

  const handleDeleteQuestion = (index: number) => {
    setQuestions(questions.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!title.trim()) {
      setError('Please enter a title');
      return;
    }

    if (questions.length === 0) {
      setError('Please add at least one question');
      return;
    }

    if (questions.some(q => !q.text.trim())) {
      setError('All questions must have text');
      return;
    }

    try {
      const endpoint = initialData
        ? `${api.endpoints.questionnaires}/${initialData.id}`
        : api.endpoints.questionnaires;
      
      const savedQuestionnaire = await apiRequest(endpoint, {
        method: initialData ? 'PUT' : 'POST',
        body: JSON.stringify({
          title,
          questions,
          status: initialData?.status || 'Not Started',
        }),
      });

      setSuccess(true);
      if (!initialData) {
        setTitle('');
        setQuestions([{ text: '', type: 'open_ended' }]);
      }
      onComplete?.();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ maxWidth: 800, mx: 'auto', p: 3 }}>
      <Typography variant="h4" gutterBottom>
        {initialData ? 'Edit Questionnaire' : 'Create Questionnaire'}
      </Typography>

      <TextField
        fullWidth
        label="Questionnaire Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        sx={{ mb: 3 }}
      />

      {questions.map((question, index) => (
        <QuestionItem
          key={index}
          question={question}
          index={index}
          onUpdate={handleUpdateQuestion}
          onDelete={handleDeleteQuestion}
        />
      ))}

      <Button
        variant="outlined"
        onClick={handleAddQuestion}
        sx={{ mr: 2, mt: 2 }}
      >
        Add Question
      </Button>

      <Button
        variant="contained"
        type="submit"
        sx={{ mt: 2 }}
      >
        Save Questionnaire
      </Button>

      <Snackbar
        open={error !== null}
        autoHideDuration={6000}
        onClose={() => setError(null)}
      >
        <Alert severity="error">{error}</Alert>
      </Snackbar>

      <Snackbar
        open={success}
        autoHideDuration={6000}
        onClose={() => setSuccess(false)}
      >
        <Alert severity="success">Questionnaire created successfully!</Alert>
      </Snackbar>
    </Box>
  );
};

export default QuestionnaireForm; 