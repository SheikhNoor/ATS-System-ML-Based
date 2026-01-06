/**
 * Dashboard Component - Advanced ATS Resume Optimization System
 * Modern, professional interface with predefined job roles
 */

import React, { useState, useCallback } from 'react';

const Dashboard = () => {
  // State management
  const [file, setFile] = useState(null);
  const [jobCategory, setJobCategory] = useState('IT'); // IT or Non-IT
  const [selectedRole, setSelectedRole] = useState('');
  const [experienceLevel, setExperienceLevel] = useState(''); // Fresher or Experienced
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isDragging, setIsDragging] = useState(false);

  // API endpoint configuration
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  // Predefined job roles organized by IT and Non-IT categories
  const jobRoles = {
    'IT': {
      'Software Development': [
        'Full Stack Developer',
        'Frontend Developer',
        'Backend Developer',
        'Mobile App Developer',
        'DevOps Engineer',
        'Software Architect',
        'UI/UX Developer'
      ],
      'Data & AI': [
        'Data Scientist',
        'Machine Learning Engineer',
        'Data Analyst',
        'AI Engineer',
        'Business Intelligence Analyst',
        'Data Engineer'
      ],
      'Cloud & Infrastructure': [
        'Cloud Solutions Architect',
        'Cloud Engineer (AWS/Azure/GCP)',
        'Site Reliability Engineer',
        'System Administrator',
        'Network Engineer'
      ],
      'Security': [
        'Cybersecurity Analyst',
        'Security Engineer',
        'Penetration Tester',
        'Information Security Manager'
      ],
      'Design': [
        'UI/UX Designer',
        'Product Designer',
        'Graphic Designer',
        'Motion Designer'
      ],
      'Other Tech Roles': [
        'QA Engineer',
        'Technical Writer',
        'Database Administrator',
        'Blockchain Developer',
        'Game Developer'
      ]
    },
    'Non-IT': {
      'Management & Leadership': [
        'Product Manager',
        'Project Manager',
        'Operations Manager',
        'Team Lead',
        'Department Head'
      ],
      'Business & Finance': [
        'Business Analyst',
        'Financial Analyst',
        'Accountant',
        'Investment Banker',
        'Business Consultant'
      ],
      'Marketing & Sales': [
        'Digital Marketing Manager',
        'Content Strategist',
        'Sales Manager',
        'Marketing Analyst',
        'Brand Manager',
        'Social Media Manager'
      ],
      'Human Resources': [
        'HR Manager',
        'Recruitment Specialist',
        'Training & Development Manager',
        'HR Business Partner',
        'Compensation & Benefits Specialist'
      ],
      'Healthcare': [
        'Medical Officer',
        'Nurse',
        'Healthcare Administrator',
        'Pharmacist',
        'Medical Researcher'
      ],
      'Education': [
        'Teacher',
        'Professor',
        'Training Coordinator',
        'Academic Counselor',
        'Educational Administrator'
      ],
      'Legal': [
        'Corporate Lawyer',
        'Legal Advisor',
        'Compliance Officer',
        'Contract Manager',
        'Paralegal'
      ],
      'Operations & Logistics': [
        'Supply Chain Manager',
        'Logistics Coordinator',
        'Operations Analyst',
        'Procurement Manager',
        'Warehouse Manager'
      ]
    }
  };

  /**
   * Handle file drop
   */
  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);
    setError(null);

    const droppedFile = e.dataTransfer.files[0];
    validateAndSetFile(droppedFile);
  }, []);

  /**
   * Handle file selection via input
   */
  const handleFileSelect = (e) => {
    const selectedFile = e.target.files[0];
    validateAndSetFile(selectedFile);
  };

  /**
   * Validate and set the selected file
   */
  const validateAndSetFile = (selectedFile) => {
    if (!selectedFile) return;

    // Validate file type
    const allowedTypes = [
      'application/pdf',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ];
    const allowedExtensions = ['.pdf', '.docx'];
    const fileExtension = '.' + selectedFile.name.split('.').pop().toLowerCase();

    if (!allowedTypes.includes(selectedFile.type) && !allowedExtensions.includes(fileExtension)) {
      setError('Invalid file type. Please upload a PDF or DOCX file.');
      return;
    }

    // Validate file size (max 10MB)
    const maxSize = 10 * 1024 * 1024; // 10MB in bytes
    if (selectedFile.size > maxSize) {
      setError('File size exceeds 10MB limit.');
      return;
    }

    setFile(selectedFile);
    setError(null);
  };

  /**
   * Handle drag over event
   */
  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  /**
   * Handle drag leave event
   */
  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  /**
   * Handle form submission and API call
   */
  const handleAnalyze = async (e) => {
    e.preventDefault();
    setError(null);
    setResults(null);

    // Validation
    if (!file) {
      setError('Please upload a resume file.');
      return;
    }

    if (!jobCategory) {
      setError('Please select a job category (IT or Non-IT).');
      return;
    }

    if (!selectedRole) {
      setError('Please select a target job role.');
      return;
    }

    if (!experienceLevel) {
      setError('Please select your experience level.');
      return;
    }

    setLoading(true);

    try {
      // Prepare form data
      const formData = new FormData();
      formData.append('file', file);
      formData.append('job_category', jobCategory);
      formData.append('job_role', selectedRole);
      formData.append('experience_level', experienceLevel);

      // Make API request
      const response = await fetch(`${API_BASE_URL}/analyze`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to analyze resume');
      }

      const data = await response.json();
      setResults(data.analysis);
    } catch (err) {
      setError(err.message || 'An error occurred while analyzing the resume.');
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Reset form and results
   */
  const handleReset = () => {
    setFile(null);
    setJobCategory('IT');
    setSelectedRole('');
    setExperienceLevel('');
    setResults(null);
    setError(null);
  };

  /**
   * Handle category change and reset selected role
   */
  const handleCategoryChange = (newCategory) => {
    setJobCategory(newCategory);
    setSelectedRole(''); // Reset role when category changes
  };

  /**
   * Get score color based on value
   */
  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-400';
    if (score >= 60) return 'text-yellow-400';
    return 'text-red-400';
  };

  /**
   * Get verdict badge color
   */
  const getVerdictColor = (verdict) => {
    if (verdict === 'Perfect') return 'bg-green-500/20 text-green-300 border-green-500/30';
    if (verdict === 'Good') return 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30';
    return 'bg-red-500/20 text-red-300 border-red-500/30';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Animated Background Elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse"></div>
        <div className="absolute top-1/3 right-1/4 w-96 h-96 bg-indigo-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse"></div>
        <div className="absolute bottom-1/4 left-1/3 w-96 h-96 bg-pink-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse"></div>
      </div>

      <div className="relative z-10 min-h-screen py-8 px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center mb-4">
            <div className="p-3 bg-gradient-to-r from-purple-600 to-indigo-600 rounded-2xl shadow-lg">
              <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
          </div>
          <h1 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-pink-400 to-indigo-400 mb-3">
            AI-Powered ATS Optimizer
          </h1>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Advanced resume analysis with machine learning • Get your dream job faster
          </p>
        </div>

        {/* Main Content - Single Page Layout */}
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Left Column - Input Section */}
            <div className="lg:col-span-2 space-y-6">
              {/* Upload Resume Card */}
              <div className="bg-white/10 backdrop-blur-md rounded-2xl shadow-2xl border border-white/20 p-8">
                <div className="flex items-center mb-6">
                  <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg flex items-center justify-center mr-3">
                    <span className="text-white font-bold text-lg">1</span>
                  </div>
                  <h2 className="text-2xl font-bold text-white">
                    Upload Resume
                  </h2>
                </div>

                {/* File Upload Zone */}
                <div
                  className={`mb-6 border-2 border-dashed rounded-xl p-8 text-center transition-all duration-300 ${
                    isDragging
                      ? 'border-purple-400 bg-purple-500/20 scale-105'
                      : file
                      ? 'border-green-400 bg-green-500/10'
                      : 'border-gray-600 bg-gray-800/50 hover:border-purple-400 hover:bg-purple-500/10'
                  }`}
                  onDrop={handleDrop}
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                >
                  {file ? (
                    <div className="space-y-4">
                      <div className="flex items-center justify-center">
                        <div className="p-3 bg-green-500/20 rounded-full">
                          <svg className="w-12 h-12 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                        </div>
                      </div>
                      <div>
                        <p className="text-lg font-semibold text-white">{file.name}</p>
                        <p className="text-sm text-gray-400 mt-1">
                          {(file.size / 1024).toFixed(2)} KB • Ready to analyze
                        </p>
                      </div>
                      <button
                        type="button"
                        onClick={() => setFile(null)}
                        className="inline-flex items-center px-4 py-2 bg-red-500/20 text-red-400 rounded-lg hover:bg-red-500/30 transition-colors"
                      >
                        <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                        Remove File
                      </button>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      <svg className="mx-auto h-16 w-16 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                      </svg>
                      <div>
                        <label htmlFor="file-upload" className="cursor-pointer">
                          <span className="text-purple-400 hover:text-purple-300 font-semibold text-lg">
                            Click to upload
                          </span>
                          <span className="text-gray-400"> or drag and drop</span>
                          <input
                            id="file-upload"
                            name="file-upload"
                            type="file"
                            className="sr-only"
                            accept=".pdf,.docx"
                            onChange={handleFileSelect}
                          />
                        </label>
                      </div>
                      <p className="text-sm text-gray-500">PDF or DOCX • Maximum 10MB</p>
                    </div>
                  )}
                </div>
              </div>

              {/* Job Details Selection Card */}
              <div className="bg-white/10 backdrop-blur-md rounded-2xl shadow-2xl border border-white/20 p-8">
                <div className="flex items-center mb-6">
                  <div className="w-10 h-10 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-lg flex items-center justify-center mr-3">
                    <span className="text-white font-bold text-lg">2</span>
                  </div>
                  <h2 className="text-2xl font-bold text-white">
                    Job Details
                  </h2>
                </div>

                <div className="space-y-6">
                  {/* Job Category (IT/Non-IT) */}
                  <div className="space-y-3">
                    <label className="block text-sm font-semibold text-gray-300 uppercase tracking-wide">
                      Job Category
                    </label>
                    <div className="grid grid-cols-2 gap-4">
                      <button
                        type="button"
                        onClick={() => handleCategoryChange('IT')}
                        className={`px-6 py-4 rounded-xl font-semibold text-lg transition-all duration-300 ${
                          jobCategory === 'IT'
                            ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-lg transform scale-105'
                            : 'bg-gray-800/50 border border-gray-600 text-gray-300 hover:border-purple-400 hover:bg-purple-500/10'
                        }`}
                      >
                        <div className="flex items-center justify-center">
                          <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M3 5a2 2 0 012-2h10a2 2 0 012 2v8a2 2 0 01-2 2h-2.22l.123.489.804.804A1 1 0 0113 18H7a1 1 0 01-.707-1.707l.804-.804L7.22 15H5a2 2 0 01-2-2V5zm5.771 7H5V5h10v7H8.771z" clipRule="evenodd" />
                          </svg>
                          IT
                        </div>
                      </button>
                      <button
                        type="button"
                        onClick={() => handleCategoryChange('Non-IT')}
                        className={`px-6 py-4 rounded-xl font-semibold text-lg transition-all duration-300 ${
                          jobCategory === 'Non-IT'
                            ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-lg transform scale-105'
                            : 'bg-gray-800/50 border border-gray-600 text-gray-300 hover:border-purple-400 hover:bg-purple-500/10'
                        }`}
                      >
                        <div className="flex items-center justify-center">
                          <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                          </svg>
                          Non-IT
                        </div>
                      </button>
                    </div>
                  </div>

                  {/* Target Job Role */}
                  <div className="space-y-3">
                    <label className="block text-sm font-semibold text-gray-300 uppercase tracking-wide">
                      Target Job Role
                    </label>
                    <select
                      value={selectedRole}
                      onChange={(e) => setSelectedRole(e.target.value)}
                      className="w-full px-4 py-3 bg-gray-800/50 border border-gray-600 rounded-xl text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                    >
                      <option value="">Select a role...</option>
                      {jobRoles[jobCategory] && Object.entries(jobRoles[jobCategory]).map(([subcategory, roles]) => (
                        <optgroup key={subcategory} label={subcategory}>
                          {roles.map((role) => (
                            <option key={role} value={role}>
                              {role}
                            </option>
                          ))}
                        </optgroup>
                      ))}
                    </select>
                    {selectedRole && (
                      <div className="flex items-center text-sm text-green-400">
                        <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                        Selected: {selectedRole}
                      </div>
                    )}
                  </div>

                  {/* Experience Level */}
                  <div className="space-y-3">
                    <label className="block text-sm font-semibold text-gray-300 uppercase tracking-wide">
                      Experience Level
                    </label>
                    <div className="grid grid-cols-2 gap-4">
                      <button
                        type="button"
                        onClick={() => setExperienceLevel('Fresher')}
                        className={`px-6 py-4 rounded-xl font-semibold text-lg transition-all duration-300 ${
                          experienceLevel === 'Fresher'
                            ? 'bg-gradient-to-r from-green-600 to-teal-600 text-white shadow-lg transform scale-105'
                            : 'bg-gray-800/50 border border-gray-600 text-gray-300 hover:border-green-400 hover:bg-green-500/10'
                        }`}
                      >
                        <div className="flex items-center justify-center">
                          <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M10.394 2.08a1 1 0 00-.788 0l-7 3a1 1 0 000 1.84L5.25 8.051a.999.999 0 01.356-.257l4-1.714a1 1 0 11.788 1.838L7.667 9.088l1.94.831a1 1 0 00.787 0l7-3a1 1 0 000-1.838l-7-3zM3.31 9.397L5 10.12v4.102a8.969 8.969 0 00-1.05-.174 1 1 0 01-.89-.89 11.115 11.115 0 01.25-3.762zM9.3 16.573A9.026 9.026 0 007 14.935v-3.957l1.818.78a3 3 0 002.364 0l5.508-2.361a11.026 11.026 0 01.25 3.762 1 1 0 01-.89.89 8.968 8.968 0 00-5.35 2.524 1 1 0 01-1.4 0zM6 18a1 1 0 001-1v-2.065a8.935 8.935 0 00-2-.712V17a1 1 0 001 1z" />
                          </svg>
                          Fresher
                        </div>
                      </button>
                      <button
                        type="button"
                        onClick={() => setExperienceLevel('Experienced')}
                        className={`px-6 py-4 rounded-xl font-semibold text-lg transition-all duration-300 ${
                          experienceLevel === 'Experienced'
                            ? 'bg-gradient-to-r from-blue-600 to-cyan-600 text-white shadow-lg transform scale-105'
                            : 'bg-gray-800/50 border border-gray-600 text-gray-300 hover:border-blue-400 hover:bg-blue-500/10'
                        }`}
                      >
                        <div className="flex items-center justify-center">
                          <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M6 6V5a3 3 0 013-3h2a3 3 0 013 3v1h2a2 2 0 012 2v3.57A22.952 22.952 0 0110 13a22.95 22.95 0 01-8-1.43V8a2 2 0 012-2h2zm2-1a1 1 0 011-1h2a1 1 0 011 1v1H8V5zm1 5a1 1 0 011-1h.01a1 1 0 110 2H10a1 1 0 01-1-1z" clipRule="evenodd" />
                            <path d="M2 13.692V16a2 2 0 002 2h12a2 2 0 002-2v-2.308A24.974 24.974 0 0110 15c-2.796 0-5.487-.46-8-1.308z" />
                          </svg>
                          Experienced
                        </div>
                      </button>
                    </div>
                    {experienceLevel && (
                      <div className="flex items-center text-sm text-green-400">
                        <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                        Experience: {experienceLevel}
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Error Message */}
              {error && (
                <div className="bg-red-500/20 border border-red-500/50 rounded-xl p-4 backdrop-blur-sm">
                  <div className="flex items-start">
                    <svg className="w-5 h-5 text-red-400 mt-0.5 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                    </svg>
                    <div className="text-sm text-red-200 whitespace-pre-line">{error}</div>
                  </div>
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex gap-4">
                <button
                  onClick={handleAnalyze}
                  disabled={loading}
                  className="flex-1 bg-gradient-to-r from-purple-600 to-indigo-600 text-white py-4 px-8 rounded-xl font-bold text-lg hover:from-purple-700 hover:to-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 shadow-lg hover:shadow-purple-500/50 transform hover:scale-105"
                >
                  {loading ? (
                    <span className="flex items-center justify-center">
                      <svg className="animate-spin -ml-1 mr-3 h-6 w-6 text-white" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                      </svg>
                      Analyzing with AI...
                    </span>
                  ) : (
                    <span className="flex items-center justify-center">
                      <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                      </svg>
                      Analyze Resume
                    </span>
                  )}
                </button>
                <button
                  onClick={handleReset}
                  className="px-6 py-4 bg-gray-800/50 border border-gray-600 text-gray-300 rounded-xl font-semibold hover:bg-gray-700/50 transition-all"
                >
                  Reset
                </button>
              </div>
            </div>

            {/* Right Column - Results */}
            <div className="lg:col-span-1 space-y-6">
              {results ? (
                <>
                  {/* Score Card */}
                  <div className="bg-gradient-to-br from-white/10 to-white/5 backdrop-blur-md rounded-2xl shadow-2xl border border-white/20 p-8 sticky top-8">
                    <div className="text-center mb-6">
                      <div className="relative inline-block">
                        <svg className="w-48 h-48 transform -rotate-90">
                          <circle cx="96" cy="96" r="88" stroke="rgba(255,255,255,0.1)" strokeWidth="12" fill="none" />
                          <circle
                            cx="96"
                            cy="96"
                            r="88"
                            stroke={results.overall_score >= 80 ? '#10b981' : results.overall_score >= 60 ? '#f59e0b' : '#ef4444'}
                            strokeWidth="12"
                            fill="none"
                            strokeDasharray={`${(results.overall_score / 100) * 553} 553`}
                            strokeLinecap="round"
                            className="transition-all duration-1000 ease-out"
                          />
                        </svg>
                        <div className="absolute inset-0 flex flex-col items-center justify-center">
                          <div className={`text-6xl font-extrabold ${getScoreColor(results.overall_score)}`}>
                            {results.overall_score}%
                          </div>
                          <span className={`inline-block mt-3 px-4 py-2 rounded-full text-sm font-bold border ${getVerdictColor(results.verdict)}`}>
                            {results.verdict}
                          </span>
                        </div>
                      </div>
                    </div>

                    {/* Score Breakdown */}
                    <div className="space-y-4 mt-6">
                      <h3 className="text-lg font-bold text-white mb-4">Performance Metrics</h3>
                      
                      <div className="space-y-3">
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-gray-300 flex items-center">
                            <span className="w-2 h-2 bg-purple-500 rounded-full mr-2"></span>
                            Keywords Match
                          </span>
                          <span className="font-bold text-white">{results.breakdown.keyword_score}%</span>
                        </div>
                        <div className="w-full bg-gray-700/50 rounded-full h-3 overflow-hidden">
                          <div
                            className="bg-gradient-to-r from-purple-500 to-pink-500 h-3 rounded-full transition-all duration-1000 ease-out"
                            style={{ width: `${results.breakdown.keyword_score}%` }}
                          />
                        </div>
                      </div>

                      <div className="space-y-3">
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-gray-300 flex items-center">
                            <span className="w-2 h-2 bg-indigo-500 rounded-full mr-2"></span>
                            Formatting Quality
                          </span>
                          <span className="font-bold text-white">{results.breakdown.formatting_score}%</span>
                        </div>
                        <div className="w-full bg-gray-700/50 rounded-full h-3 overflow-hidden">
                          <div
                            className="bg-gradient-to-r from-indigo-500 to-blue-500 h-3 rounded-full transition-all duration-1000 ease-out"
                            style={{ width: `${results.breakdown.formatting_score}%` }}
                          />
                        </div>
                      </div>

                      <div className="space-y-3">
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-gray-300 flex items-center">
                            <span className="w-2 h-2 bg-cyan-500 rounded-full mr-2"></span>
                            Context Relevance
                          </span>
                          <span className="font-bold text-white">{results.breakdown.context_score}%</span>
                        </div>
                        <div className="w-full bg-gray-700/50 rounded-full h-3 overflow-hidden">
                          <div
                            className="bg-gradient-to-r from-cyan-500 to-teal-500 h-3 rounded-full transition-all duration-1000 ease-out"
                            style={{ width: `${results.breakdown.context_score}%` }}
                          />
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Keywords Section */}
                  <div className="bg-white/10 backdrop-blur-md rounded-2xl shadow-2xl border border-white/20 p-6">
                    <h3 className="text-lg font-bold text-white mb-4 flex items-center">
                      <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M12.395 2.553a1 1 0 00-1.45-.385c-.345.23-.614.558-.822.88-.214.33-.403.713-.57 1.116-.334.804-.614 1.768-.84 2.734a31.365 31.365 0 00-.613 3.58 2.64 2.64 0 01-.945-1.067c-.328-.68-.398-1.534-.398-2.654A1 1 0 005.05 6.05 6.981 6.981 0 003 11a7 7 0 1011.95-4.95c-.592-.591-.98-.985-1.348-1.467-.363-.476-.724-1.063-1.207-2.03zM12.12 15.12A3 3 0 017 13s.879.5 2.5.5c0-1 .5-4 1.25-4.5.5 1 .786 1.293 1.371 1.879A2.99 2.99 0 0113 13a2.99 2.99 0 01-.879 2.121z" clipRule="evenodd" />
                      </svg>
                      Keyword Analysis
                    </h3>
                    
                    {results.missing_keywords && results.missing_keywords.length > 0 && (
                      <div className="mb-4">
                        <p className="text-xs text-red-400 font-semibold uppercase tracking-wide mb-2">Missing Keywords</p>
                        <div className="flex flex-wrap gap-2">
                          {results.missing_keywords.slice(0, 8).map((keyword, index) => (
                            <span key={index} className="inline-flex items-center px-3 py-1 bg-red-500/20 text-red-300 text-xs font-medium rounded-full border border-red-500/30">
                              <svg className="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                              </svg>
                              {keyword}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {results.matched_keywords && results.matched_keywords.length > 0 && (
                      <div>
                        <p className="text-xs text-green-400 font-semibold uppercase tracking-wide mb-2">Matched Keywords</p>
                        <div className="flex flex-wrap gap-2">
                          {results.matched_keywords.slice(0, 8).map((keyword, index) => (
                            <span key={index} className="inline-flex items-center px-3 py-1 bg-green-500/20 text-green-300 text-xs font-medium rounded-full border border-green-500/30">
                              <svg className="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                              </svg>
                              {keyword}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Recommendations */}
                  {results.recommendations && results.recommendations.length > 0 && (
                    <div className="bg-white/10 backdrop-blur-md rounded-2xl shadow-2xl border border-white/20 p-6">
                      <h3 className="text-lg font-bold text-white mb-4 flex items-center">
                        <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                        </svg>
                        AI Recommendations
                      </h3>
                      <div className="space-y-2">
                        {results.recommendations.map((rec, index) => (
                          <div key={index} className="flex items-start text-gray-300 text-sm bg-white/5 p-3 rounded-lg border border-white/10">
                            <svg className="w-5 h-5 text-blue-400 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            <span>{rec}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Summary Analysis Section */}
                  {results.summary_analysis && (
                    <div className="bg-white/10 backdrop-blur-md rounded-2xl shadow-2xl border border-white/20 p-6">
                      <div className="flex items-center justify-between mb-4">
                        <h3 className="text-lg font-bold text-white flex items-center">
                          <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
                            <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd" />
                          </svg>
                          Professional Summary Analysis
                        </h3>
                        <div className="flex items-center">
                          <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                            results.summary_analysis.quality === 'Excellent' ? 'bg-green-500/20 text-green-300 border border-green-500/30' :
                            results.summary_analysis.quality === 'Good' ? 'bg-blue-500/20 text-blue-300 border border-blue-500/30' :
                            results.summary_analysis.quality === 'Needs Improvement' ? 'bg-yellow-500/20 text-yellow-300 border border-yellow-500/30' :
                            results.summary_analysis.quality === 'Missing' ? 'bg-red-500/20 text-red-300 border border-red-500/30' :
                            'bg-orange-500/20 text-orange-300 border border-orange-500/30'
                          }`}>
                            {results.summary_analysis.quality}
                          </span>
                          {results.summary_analysis.has_summary && (
                            <span className="ml-3 text-2xl font-bold text-white">
                              {Math.round(results.summary_analysis.score)}%
                            </span>
                          )}
                        </div>
                      </div>

                      {/* Current Summary */}
                      {results.summary_analysis.has_summary && results.summary_analysis.summary_text && (
                        <div className="mb-6 p-4 bg-white/5 rounded-lg border border-white/10">
                          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Your Current Summary:</p>
                          <p className="text-sm text-gray-300 leading-relaxed italic">
                            "{results.summary_analysis.summary_text}"
                          </p>
                        </div>
                      )}

                      {/* Analysis Metrics */}
                      {results.summary_analysis.has_summary && results.summary_analysis.analysis && (
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                          <div className="p-3 bg-white/5 rounded-lg border border-white/10 text-center">
                            <p className="text-xs text-gray-400 mb-1">Word Count</p>
                            <p className="text-lg font-bold text-white">{results.summary_analysis.analysis.word_count}</p>
                            <p className="text-xs text-gray-500">{results.summary_analysis.analysis.length_category}</p>
                          </div>
                          <div className="p-3 bg-white/5 rounded-lg border border-white/10 text-center">
                            <p className="text-xs text-gray-400 mb-1">Action Words</p>
                            <p className="text-lg font-bold text-white">{results.summary_analysis.analysis.action_words.length}</p>
                            <p className={`text-xs ${results.summary_analysis.analysis.action_words.length >= 2 ? 'text-green-400' : 'text-orange-400'}`}>
                              {results.summary_analysis.analysis.action_words.length >= 2 ? '✓ Good' : 'Need More'}
                            </p>
                          </div>
                          <div className="p-3 bg-white/5 rounded-lg border border-white/10 text-center">
                            <p className="text-xs text-gray-400 mb-1">Metrics</p>
                            <p className="text-lg font-bold text-white">{results.summary_analysis.analysis.numbers.length}</p>
                            <p className={`text-xs ${results.summary_analysis.analysis.has_numbers ? 'text-green-400' : 'text-orange-400'}`}>
                              {results.summary_analysis.analysis.has_numbers ? '✓ Good' : 'Add Numbers'}
                            </p>
                          </div>
                          <div className="p-3 bg-white/5 rounded-lg border border-white/10 text-center">
                            <p className="text-xs text-gray-400 mb-1">Role Match</p>
                            <p className="text-lg font-bold text-white">
                              {results.summary_analysis.analysis.role_mentioned ? '✓' : '✗'}
                            </p>
                            <p className={`text-xs ${results.summary_analysis.analysis.role_mentioned ? 'text-green-400' : 'text-red-400'}`}>
                              {results.summary_analysis.analysis.role_mentioned ? 'Mentioned' : 'Missing'}
                            </p>
                          </div>
                        </div>
                      )}

                      {/* AI Suggestions */}
                      <div className="mb-6">
                        <h4 className="text-sm font-semibold text-gray-300 uppercase tracking-wide mb-3">
                          ✨ AI-Powered Suggestions:
                        </h4>
                        <div className="space-y-2">
                          {results.summary_analysis.suggestions.map((suggestion, index) => (
                            <div key={index} className="flex items-start text-sm bg-white/5 p-3 rounded-lg border border-white/10">
                              <span className={`mr-2 flex-shrink-0 ${
                                suggestion.startsWith('✓') ? 'text-blue-400' :
                                suggestion.startsWith('❌') ? 'text-red-400' :
                                suggestion.startsWith('⚠️') ? 'text-yellow-400' :
                                suggestion.startsWith('✅') ? 'text-green-400' :
                                'text-gray-400'
                              }`}>
                                {suggestion.match(/^[✓❌⚠️✅]/)?.[0] || '•'}
                              </span>
                              <span className="text-gray-300">{suggestion.replace(/^[✓❌⚠️✅]\s*/, '')}</span>
                            </div>
                          ))}
                        </div>
                      </div>

                      {/* Improved Example */}
                      {results.summary_analysis.has_summary && results.summary_analysis.improved_example && (
                        <div className="p-4 bg-gradient-to-br from-purple-500/10 to-indigo-500/10 rounded-lg border border-purple-500/30">
                          <div className="flex items-center mb-2">
                            <svg className="w-4 h-4 text-purple-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                            </svg>
                            <p className="text-xs font-semibold text-purple-300 uppercase tracking-wide">
                              AI-Generated Example (Reference Only):
                            </p>
                          </div>
                          <p className="text-sm text-gray-200 leading-relaxed italic">
                            "{results.summary_analysis.improved_example}"
                          </p>
                          <p className="text-xs text-gray-400 mt-2">
                            💡 Use this as inspiration to improve your own summary with your unique experiences
                          </p>
                        </div>
                      )}
                    </div>
                  )}
                </>
              ) : (
                <div className="bg-white/10 backdrop-blur-md rounded-2xl shadow-2xl border border-white/20 p-12 text-center">
                  <div className="w-20 h-20 bg-gradient-to-r from-purple-500/20 to-pink-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg className="w-10 h-10 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-bold text-white mb-2">
                    Ready to Analyze
                  </h3>
                  <p className="text-gray-400">
                    Upload your resume and provide job details to get instant AI-powered insights
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
