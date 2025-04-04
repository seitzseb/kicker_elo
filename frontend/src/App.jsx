import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const App = () => {
  const [csvData, setCsvData] = useState([]);
  const [modifiedData, setModifiedData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  // Fetch CSV data from backend
  const fetchCsvData = async () => {
    try {
      const response = await axios.get('http://localhost:8080/data'); // Adjust the URL if needed
      setCsvData(response.data);
      setModifiedData(response.data); // Initially, modifiedData is same as the fetched data
      setIsLoading(false);
    } catch (error) {
      console.error('Error fetching CSV data:', error);
      setIsLoading(false);
    }
  };

  // Handle data modification (editing a specific row)
  const handleEdit = (index, field, value) => {
    const updatedData = [...modifiedData];
    updatedData[index][field] = value;
    setModifiedData(updatedData);
  };

  // Submit modified CSV data to backend
  const handleSave = async () => {
    try {
      await axios.post('http://localhost:8080/data', modifiedData); // Send the modified data
      alert('CSV data saved successfully');
    } catch (error) {
      console.error('Error saving CSV data:', error);
    }
  };

  // Load CSV data on component mount
  useEffect(() => {
    fetchCsvData();
  }, []);

  // Render a table with CSV data and allow modification
  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Modify CSV Data</h1>
      <table>
        <thead>
          <tr>
            {csvData[0] && Object.keys(csvData[0]).map((key) => (
              <th key={key}>{key}</th>
            ))}
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {modifiedData.map((row, index) => (
            <tr key={index}>
              {Object.keys(row).map((key) => (
                <td key={key}>
                  <input
                    type="text"
                    value={row[key]}
                    onChange={(e) => handleEdit(index, key, e.target.value)}
                  />
                </td>
              ))}
              <td>
                <button onClick={() => handleSave()}>Save</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default App;
