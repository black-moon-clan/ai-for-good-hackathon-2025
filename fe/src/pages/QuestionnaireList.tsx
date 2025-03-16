import React, { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  Alert,
  CircularProgress
} from '@mui/material';

interface Question {
  text: string;
  type: string;
  options?: string[];
}

interface Questionnaire {
  title: string;
  questions: Question[];
  created_at: string;
}

const QuestionnaireList: React.FC = () => {
  const [questionnaires, setQuestionnaires] = useState<Questionnaire[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchQuestionnaires = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/questionnaires/');
        if (!response.ok) {
          throw new Error('Failed to fetch questionnaires');
        }
        const data = await response.json();
        setQuestionnaires(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load questionnaires');
      } finally {
        setLoading(false);
      }
    };

    fetchQuestionnaires();
  }, []);

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

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Questionnaires
      </Typography>
      
      {questionnaires.length === 0 ? (
        <Alert severity="info">No questionnaires available</Alert>
      ) : (
        <List>
          {questionnaires.map((questionnaire, index) => (
            <ListItem key={index} sx={{ mb: 2, px: 0 }}>
              <Card sx={{ width: '100%' }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    {questionnaire.title}
                  </Typography>
                  <Typography color="text.secondary" gutterBottom>
                    Created: {new Date(questionnaire.created_at).toLocaleDateString()}
                  </Typography>
                  <Typography variant="body2">
                    Number of questions: {questionnaire.questions.length}
                  </Typography>
                  <Box mt={2}>
                    <Typography variant="subtitle2" color="text.secondary">
                      Questions:
                    </Typography>
                    <List>
                      {questionnaire.questions.map((question, qIndex) => (
                        <ListItem key={qIndex} sx={{ pl: 2 }}>
                          <Typography variant="body2">
                            {qIndex + 1}. {question.text} ({question.type})
                          </Typography>
                        </ListItem>
                      ))}
                    </List>
                  </Box>
                </CardContent>
              </Card>
            </ListItem>
          ))}
        </List>
      )}
    </Box>
  );
};

export default QuestionnaireList; 