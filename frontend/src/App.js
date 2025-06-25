import React, { useState } from "react";
import axios from "axios";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [downloadLinks, setDownloadLinks] = useState([]);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
    setDownloadLinks([]);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;
    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const res = await axios.post("http://localhost:5000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      const files = res.data.files;
      setDownloadLinks(files);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div style={{ padding: 40 }}>
      <h2>PDF to JPG Converter</h2>
      <input type="file" accept=".pdf" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload and Convert</button>

      {downloadLinks.length > 0 && (
        <div>
          <h3>Download JPG(s):</h3>
          {downloadLinks.map((file) => (
            <div key={file}>
              <a href={`http://localhost:5000/download/${file}`} target="_blank" rel="noreferrer">
                {file}
              </a>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
