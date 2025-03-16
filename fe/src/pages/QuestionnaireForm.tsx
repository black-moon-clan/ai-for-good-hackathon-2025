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
  } | undefined;
  onComplete?: () => void;
}

const QuestionnaireForm: React.FC<QuestionnaireFormProps> = ({ 
  initialData,
  onComplete 
}) => {
  const [title, setTitle] = useState(initialData?.title || '');
  const [questions, setQuestions] = useState<Question[]>(initialData?.questions || []);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const handleAddQuestion = () => {
    setQuestions([...questions, { text: '', type: 'multiple_choice' }]);
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
      const url = initialData
        ? `http://localhost:5000/api/questionnaires/${initialData.id}`
        : 'http://localhost:5000/api/questionnaires/';
      
      const response = await fetch(url, {
        method: initialData ? 'PUT' : 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title,
          questions,
          created_at: new Date().toISOString(),
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to save questionnaire');
      }

      setSuccess(true);
      if (!initialData) {
        setTitle('');
        setQuestions([]);
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