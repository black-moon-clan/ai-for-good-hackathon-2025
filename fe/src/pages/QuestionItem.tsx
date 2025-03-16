import React from 'react';
import { TextField, Select, MenuItem, IconButton, Box } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';

interface QuestionItemProps {
  question: {
    text: string;
    type: string;
    options?: string[];
  };
  index: number;
  onUpdate: (index: number, field: string, value: any) => void;
  onDelete: (index: number) => void;
}

const QuestionItem: React.FC<QuestionItemProps> = ({
  question,
  index,
  onUpdate,
  onDelete,
}) => {
  return (
    <Box sx={{ mb: 2, p: 2, border: '1px solid #ddd', borderRadius: 1 }}>
      <TextField
        fullWidth
        label="Question Text"
        value={question.text}
        onChange={(e) => onUpdate(index, 'text', e.target.value)}
        sx={{ mb: 2 }}
      />
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
        <Select
          value={question.type}
          onChange={(e) => onUpdate(index, 'type', e.target.value)}
          sx={{ minWidth: 200 }}
        >
          <MenuItem value="multiple_choice">Multiple Choice</MenuItem>
          <MenuItem value="essay">Essay</MenuItem>
        </Select>
        <IconButton onClick={() => onDelete(index)} color="error">
          <DeleteIcon />
        </IconButton>
      </Box>
    </Box>
  );
};

export default QuestionItem; 