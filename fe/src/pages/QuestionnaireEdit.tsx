import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  CircularProgress,
  Stack,
  Alert,
} from '@mui/material';
import QuestionnaireForm from './QuestionnaireForm';

interface Question {
  text: string;
  type: string;
  options?: string[];
}

interface Questionnaire {
  id: string;
  title: string;
  questions: Question[];
  created_at: string;
  status: 'Not Started' | 'Running' | 'Stopped' | 'Complete';
}

const QuestionnaireEdit: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [questionnaire, setQuestionnaire] = useState<Questionnaire | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchQuestionnaire = async () => {
      if (!id || id === 'new') return;
      
      setLoading(true);
      try {
        const response = await fetch(`http://localhost:5000/api/questionnaires/${id}`);
        if (!response.ok) throw new Error('Failed to fetch questionnaire');
        const data = await response.json();
        setQuestionnaire(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchQuestionnaire();
  }, [id]);

  const handleComplete = () => {
    navigate('/');
  };

  const handleCancel = () => {
    navigate('/');
  };

  const handleStart = async () => {
    if (!questionnaire) return;

    const newStatus = questionnaire.status === 'Running' ? 'Stopped' : 'Running';
    
    try {
      const response = await fetch(`http://localhost:5000/api/questionnaires/${id}/status`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: newStatus }),
      });

      if (!response.ok) {
        throw new Error('Failed to update questionnaire status');
      }

      if (newStatus === 'Running') {
        navigate('/');
      } else {
        const updatedQuestionnaire = await response.json();
        setQuestionnaire(updatedQuestionnaire);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" m={4}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box m={2}>
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  }

  // Convert questionnaire to the expected format for initialData
  const formInitialData = questionnaire ? {
    id: questionnaire.id,
    title: questionnaire.title,
    questions: questionnaire.questions
  } : undefined;

  const isNewQuestionnaire = !id || id === 'new' || !questionnaire;

  return (
    <Box>
      <QuestionnaireForm
        initialData={formInitialData}
        onComplete={handleComplete}
      />
      <Stack
        direction="row"
        spacing={2}
        justifyContent="center"
        mt={3}
        mb={4}
      >
        <Button
          variant="outlined"
          color="error"
          onClick={handleCancel}
        >
          Cancel
        </Button>
        <Button
          variant="contained"
          color={questionnaire?.status === 'Running' ? 'error' : 'primary'}
          onClick={handleStart}
          disabled={isNewQuestionnaire}
          sx={{ 
            opacity: isNewQuestionnaire ? 0.6 : 1,
          }}
        >
          {questionnaire?.status === 'Running' ? 'Stop Questionnaire' : 'Start Questionnaire'}
        </Button>
      </Stack>
    </Box>
  );
};

export default QuestionnaireEdit; 