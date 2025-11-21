import React from 'react';
import { Upload, FileText } from 'lucide-react';

const FileUpload = ({ onFileSelect, selectedFile }) => {
  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      onFileSelect(e.target.files[0]);
    }
  };

  return (
    <div className="file-upload-container">
      <input
        type="file"
        accept=".pdf"
        onChange={handleFileChange}
        id="resume-upload"
        className="file-input-hidden"
      />
      <label htmlFor="resume-upload" className="upload-btn">
        <Upload size={20} />
        {selectedFile ? 'Change Resume' : 'Upload Resume (PDF)'}
      </label>

      {selectedFile && (
        <div className="selected-file-info">
          <FileText size={16} color="#a855f7" />
          <span>{selectedFile.name}</span>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
