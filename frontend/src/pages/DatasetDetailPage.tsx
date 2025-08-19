import React from 'react';
import { useParams } from 'react-router-dom';

const DatasetDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  
  return (
    <div className="container">
      <h1>Dataset Detail: {id}</h1>
      <p>Dataset detail page will be implemented here.</p>
    </div>
  );
};

export default DatasetDetailPage;