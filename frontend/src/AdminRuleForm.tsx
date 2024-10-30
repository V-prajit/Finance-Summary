import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface AdminRule {
  id: number;
  name: string;
  words: string;
  match_method: 'all' | 'any' | 'exact';
  tag: string;
}

const AdminRuleForm: React.FC = () => {
  const [rules, setRules] = useState<AdminRule[]>([]);
  const [newRule, setNewRule] = useState<Omit<AdminRule, 'id'>>({
    name: '',
    words: '',
    match_method: 'all',
    tag: ''
  });

  useEffect(() => {
    fetchRules();
  }, []);

  const fetchRules = async () => {
    try {
      const response = await axios.get('/api/transactions/admin-rules/', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      setRules(response.data);
    } catch (error) {
      console.error('Error fetching rules:', error);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setNewRule(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axios.post('/api/transactions/admin-rules/', newRule, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      fetchRules();  // Refresh the list after adding
      setNewRule({ name: '', words: '', match_method: 'all', tag: '' });
    } catch (error) {
      console.error('Error adding rule:', error);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await axios.delete(`/api/transactions/admin-rules/${id}/`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      fetchRules();  // Refresh the list after deleting
    } catch (error) {
      console.error('Error deleting rule:', error);
    }
  };

  return (
    <div>
      <h2>Admin Rule Management</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="name"
          value={newRule.name}
          onChange={handleInputChange}
          placeholder="Rule Name"
          required
        />
        <textarea
          name="words"
          value={newRule.words}
          onChange={handleInputChange}
          placeholder="Words (space-separated)"
          required
        />
        <select
          name="match_method"
          value={newRule.match_method}
          onChange={handleInputChange}
          required
        >
          <option value="all">All words</option>
          <option value="any">Any word</option>
          <option value="exact">Exact phrase</option>
        </select>
        <input
          type="text"
          name="tag"
          value={newRule.tag}
          onChange={handleInputChange}
          placeholder="Tag"
          required
        />
        <button type="submit">Add Admin Rule</button>
      </form>

      <h3>Existing Admin Rules:</h3>
      <ul>
        {rules.map((rule) => (
          <li key={rule.id}>
            <strong>{rule.name}</strong>
            <br />
            Words: {rule.words}
            <br />
            Match Method: {rule.match_method}
            <br />
            Tag: {rule.tag}
            <br />
            <button onClick={() => handleDelete(rule.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AdminRuleForm;