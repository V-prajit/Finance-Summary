import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

interface Rule {
    id: number;
    name: string;
    words: string;
    match_method: 'all' | 'any' | 'exact';
    tag: string;
    label?: string;
    label_display?: string;
    metadata_type?: 'next_n_words' | 'regex' | 'string_match';
    metadata_value?: string;
    auto_tag?: boolean;
}

const RuleManagement: React.FC = () => {
    const [isAdmin, setIsAdmin] = useState<boolean>(false);
    const [rules, setRules] = useState<Rule[]>([]);
    const [newRule, setNewRule] = useState<Omit<Rule, 'id'>>({ 
        name: '', 
        words: '', 
        match_method: 'all', 
        tag: '',
        metadata_type: 'string_match',
        metadata_value: '',
        auto_tag: true,
    });

    const checkIfUserIsAdmin = useCallback(() => {
      const token = localStorage.getItem('access_token');
      if (token) {
          const decodedToken: any = jwtDecode(token);
          console.log("Decoded token:", decodedToken);
          setIsAdmin(decodedToken.is_staff || false);
      }
  }, []);

    const fetchRules = useCallback(async () => {
        try {
            const endpoint = isAdmin ? 'admin-rules' : 'custom-rules';
            console.log("Fetching rules from endpoint:", endpoint);
            const response = await axios.get(`/api/transactions/${endpoint}/`, {
                headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
            });
            setRules(response.data);
        } catch (error) {
            console.error('Error fetching rules:', error);
        }
    }, [isAdmin]);

    useEffect(() => {
        checkIfUserIsAdmin();
    }, [checkIfUserIsAdmin]);

    useEffect(() => {
        fetchRules();
    }, [fetchRules]);

    useEffect(() => {
        console.log("isAdmin changed:", isAdmin);
    }, [isAdmin]);

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
        const { name, value } = e.target;
        setNewRule(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        console.log("Submitting as admin:", isAdmin);
        const endpoint = isAdmin ? 'admin-rules' : 'custom-rules';
        console.log("Using endpoint for submission:", endpoint);
        try {
            const response = await axios.post(`/api/transactions/${endpoint}/`, newRule, {
                headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
            });
            console.log("Rule submission response:", response.data);
            fetchRules();
            setNewRule({ 
                name: '', 
                words: '', 
                match_method: 'all', 
                tag: '',
                metadata_type: 'string_match',
                metadata_value: '',
                auto_tag: true,
            });
        } catch (error) {
            console.error('Error adding rule:', error);
            if (axios.isAxiosError(error) && error.response) {
                console.error('Server response:', error.response.data);
            }
        }
    };

    const handleDelete = async (id: number) => {
        try {
            const endpoint = isAdmin ? 'admin-rules' : 'custom-rules';
            console.log(`Deleting rule ${id} from endpoint:`, endpoint);
            await axios.delete(`/api/transactions/${endpoint}/${id}/`, {
                headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
            });
            fetchRules();
        } catch (error) {
            console.error('Error deleting rule:', error);
            if (axios.isAxiosError(error) && error.response) {
                console.error('Server response:', error.response.data);
            }
        }
    };

    return (
        <div>
            <h2>{isAdmin ? 'Admin Rule Management' : 'Custom Rule Management'}</h2>
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
                />
                <select
                    name="metadata_type"
                    value={newRule.metadata_type || ''}
                    onChange={handleInputChange}
                >
                    <option value="next_n_words">Next N Words</option>
                    <option value="regex">Regular Expression</option>
                    <option value="string_match">String Match</option>
                </select>
                <input
                    type="text"
                    name="metadata_value"
                    value={newRule.metadata_value || ''}
                    onChange={handleInputChange}
                    placeholder="Metadata Value"
                />
                <input
                    type="text"
                    name="label"
                    value={newRule.label || ''}
                    onChange={handleInputChange}
                    placeholder="Label (e.g., Person, Category)"
                />
                <input
                    type="checkbox"
                    name="auto_tag"
                    checked={newRule.auto_tag}
                    onChange={(e) => setNewRule(prev => ({ ...prev, auto_tag: e.target.checked }))}
                />
                <label htmlFor="auto_tag">Auto Tag</label>
                <button type="submit">Add Rule</button>
            </form>

            <h3>Existing Rules:</h3>
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
                        Metadata Type: {rule.metadata_type || 'N/A'}
                        <br />
                        Metadata Value: {rule.metadata_value || 'N/A'}
                        <br />
                        Label: {rule.label || 'N/A'}
                        <br />
                        Auto Tag: {rule.auto_tag ? 'Yes' : 'No'}
                        <br />
                        <button onClick={() => handleDelete(rule.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default RuleManagement;