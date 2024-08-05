import React, { useState } from 'react';
import axios from 'axios';

const AddRuleForm: React.FC = () => {
    const [Name, setName] = useState('');
    const [Pattern, setPattern] = useState('');
    const [Tag, setTag] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:3000/api/transactions/custon-rules/', {
                Name,
                Pattern,
                Tag
            }, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            });
            console.log('Rule added:', response.data);
        } catch (error) {
            console.error('Error adding rule:', error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={Name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Rule Name"
            required
          />
          <input
            type="text"
            value={Pattern}
            onChange={(e) => setPattern(e.target.value)}
            placeholder="Pattern"
            required
          />
          <input
            type="text"
            value={Tag}
            onChange={(e) => setTag(e.target.value)}
            placeholder="Tag"
            required
          />
          <button type="submit">Add Rule</button>
        </form>
      );
    };

export default AddRuleForm;