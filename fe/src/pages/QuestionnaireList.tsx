import React, { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  Alert,
  CircularProgress,
  IconButton,
  CardActions,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import QuestionnaireForm from './QuestionnaireForm';
import { useNavigate } from 'react-router-dom';
import AddIcon from '@mui/icons-material/Add';
import { apiRequest, api } from '../utils/api';

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

const QuestionnaireList: React.FC = () => {
  const [questionnaires, setQuestionnaires] = useState<Questionnaire[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editingQuestionnaire, setEditingQuestionnaire] = useState<Questionnaire | null>(null);
  const [deleteConfirmId, setDeleteConfirmId] = useState<string | null>(null);
  const navigate = useNavigate();

  const fetchQuestionnaires = async () => {
    try {
      const data = await apiRequest(api.endpoints.questionnaires);
      setQuestionnaires(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load questionnaires');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQuestionnaires();
  }, []);

  const handleDelete = async (id: string) => {
    try {
      await apiRequest(`${api.endpoints.questionnaires}/${id}`, {
        method: 'DELETE',
      });
      setQuestionnaires(questionnaires.filter(q => q.id !== id));
      setDeleteConfirmId(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete questionnaire');
    }
  };

  const handleEditComplete = () => {
    setEditingQuestionnaire(null);
    fetchQuestionnaires();
  };

  const handleEditClick = (questionnaire: Questionnaire) => {
    navigate(`/questionnaire/${questionnaire.id}`);
  };

  const handleDeleteClick = (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    setDeleteConfirmId(id);
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

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', p: 3 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">
          Questionnaires
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => navigate('/questionnaire/new')}
        >
          Create Questionnaire
        </Button>
      </Box>
      
      {questionnaires.length === 0 ? (
        <Alert severity="info">No questionnaires available</Alert>
      ) : (
        <List>
          {questionnaires.map((questionnaire) => (
            <ListItem 
              key={questionnaire.id} 
              sx={{ mb: 2, px: 0 }}
              onClick={() => handleEditClick(questionnaire)}
              style={{ cursor: 'pointer' }}
            >
              <Card sx={{ width: '100%' }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    {questionnaire.title}
                  </Typography>
                  <Box display="flex" justifyContent="space-between" alignItems="center">
                    <Typography color="text.secondary" gutterBottom>
                      Created: {new Date(questionnaire.created_at).toLocaleDateString()}
                    </Typography>
                    <Typography
                      sx={{
                        px: 2,
                        py: 0.5,
                        borderRadius: 1,
                        backgroundColor: (() => {
                          switch (questionnaire.status) {
                            case 'Running': return 'success.light';
                            case 'Stopped': return 'warning.light';
                            case 'Complete': return 'info.light';
                            default: return 'grey.200';
                          }
                        })(),
                      }}
                    >
                      {questionnaire.status}
                    </Typography>
                  </Box>
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
                <CardActions onClick={(e) => e.stopPropagation()}>
                  <IconButton 
                    onClick={(e) => handleEditClick(questionnaire)}
                    color="primary"
                  >
                    <EditIcon />
                  </IconButton>
                  <IconButton 
                    onClick={(e) => handleDeleteClick(e, questionnaire.id)}
                    color="error"
                  >
                    <DeleteIcon />
                  </IconButton>
                </CardActions>
              </Card>
            </ListItem>
          ))}
        </List>
      )}

      {/* Edit Dialog */}
      <Dialog 
        open={!!editingQuestionnaire} 
        onClose={() => setEditingQuestionnaire(null)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Edit Questionnaire</DialogTitle>
        <DialogContent>
          {editingQuestionnaire && (
            <QuestionnaireForm
              initialData={editingQuestionnaire}
              onComplete={handleEditComplete}
            />
          )}
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <Dialog
        open={!!deleteConfirmId}
        onClose={() => setDeleteConfirmId(null)}
      >
        <DialogTitle>Confirm Delete</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete this questionnaire?
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteConfirmId(null)}>Cancel</Button>
          <Button 
            onClick={() => deleteConfirmId && handleDelete(deleteConfirmId)} 
            color="error"
            variant="contained"
          >
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default QuestionnaireList; 