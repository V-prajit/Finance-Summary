// src/TransactionTable.tsx
import React, { useState, useEffect } from "react";
import axios from 'axios';
import { refreshToken, isTokenExpired } from "./auth";

interface Tag {
  id: number;
  tag: string;
}

interface Transaction {
  id: number;
  description: string;
  tags: Tag[];
}

const API_URL = "http://localhost:3000/api/";

const TransactionTable: React.FC = () => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);

  useEffect(() => {
    fetchTransactions();
  }, []);

  const fetchTransactions = async () => {
    try {
        const token = localStorage.getItem('access_token');
        if (token && isTokenExpired(token)) {
          const refreshed = await refreshToken();
          if (!refreshed) {
            throw new Error('Session expired. Please login again.');
          }
        }

        const response = await axios.get(`${API_URL}transactions/get-transaction-with-tags/`, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('access_token')}`
              }
        });

        setTransactions(response.data);

    } catch (error) {
      console.error("Error fetching transactions:", error);
    }
  };

  return (
    <table>
      <thead>
        <tr>
          <th>Description</th>
          <th>Tags</th>
        </tr>
      </thead>
      <tbody>
        {transactions.map((transaction) => (
          <tr key={transaction.id}>
            <td>{transaction.description}</td>
            <td>{transaction.tags.map(tag => tag.tag).join(', ')}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default TransactionTable;