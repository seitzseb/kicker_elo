import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:8000/data")
      .then(res => setData(res.data));
  }, []);

  const handleUpdate = (index, column, value) => {
    axios.post("http://localhost:8000/data", { index, column, value })
      .then(() => {
        const newData = [...data];
        newData[index][column] = value;
        setData(newData);
      });
  };

  return (
    <table>
      <thead>
        <tr>{data[0] && Object.keys(data[0]).map((col, i) => <th key={i}>{col}</th>)}</tr>
      </thead>
      <tbody>
        {data.map((row, i) => (
          <tr key={i}>
            {Object.entries(row).map(([col, val], j) => (
              <td key={j}>
                <input
                  value={val}
                  onChange={e => handleUpdate(i, col, e.target.value)}
                />
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default App;