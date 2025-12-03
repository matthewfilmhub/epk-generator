import React, { useState } from 'react';
import { Upload, FileText, Download, CheckCircle, AlertCircle, Film } from 'lucide-react';
import { generateEPKHTML } from './epkGenerator';

// No API needed - everything runs client-side!

function App() {
  const [activeStep, setActiveStep] = useState(0);
  const [projectId, setProjectId] = useState(null);
  const [config, setConfig] = useState({
    metadata: {
      title: '',
      tagline: '',
      logline: '',
      synopsis: '',
      genre: '',
      runtime: '',
      rating: 'NR',
      release_date: '',
      language: 'English',
      country: 'USA',
      director: ''
    },
    team: [],
    awards: [],
    festivals: [],
    reviews: [],
    press_coverage: [],
    distribution: {},
    technical: {
      aspect_ratio: '16:9',
      sound: '5.1 Surround',
      color: 'Color'
    },
    contact: {
      distribution_company: 'Filmhub',
      name: '',
      email: '',
      phone: '',
      website: ''
    }
  });
  
  const [assets, setAssets] = useState({
    poster: null,
    stills: [],
    teamPhotos: []
  });
  
  const [validation, setValidation] = useState(null);
  const [generating, setGenerating] = useState(false);
  const [downloadUrls, setDownloadUrls] = useState(null);
  const [error, setError] = useState(null);

  const genres = [
    'Horror', 'Sci-Fi', 'Fantasy', 'Comedy', 'Drama', 
    'Action', 'Documentary', 'Romance', 'Thriller'
  ];

  const handleConfigChange = (section, field, value) => {
    setConfig(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [field]: value
      }
    }));
  };

  const addTeamMember = () => {
    setConfig(prev => ({
      ...prev,
      team: [...prev.team, { name: '', role: '', bio: '', photo: '' }]
    }));
  };

  const updateTeamMember = (index, field, value) => {
    setConfig(prev => ({
      ...prev,
      team: prev.team.map((member, i) => 
        i === index ? { ...member, [field]: value } : member
      )
    }));
  };

  const removeTeamMember = (index) => {
    setConfig(prev => ({
      ...prev,
      team: prev.team.filter((_, i) => i !== index)
    }));
  };

  const addAward = () => {
    setConfig(prev => ({
      ...prev,
      awards: [...prev.awards, { festival_name: '', award: '', year: '' }]
    }));
  };

  const updateAward = (index, field, value) => {
    setConfig(prev => ({
      ...prev,
      awards: prev.awards.map((award, i) => 
        i === index ? { ...award, [field]: value } : award
      )
    }));
  };

  const removeAward = (index) => {
    setConfig(prev => ({
      ...prev,
      awards: prev.awards.filter((_, i) => i !== index)
    }));
  };

  const addReview = () => {
    setConfig(prev => ({
      ...prev,
      reviews: [...prev.reviews, { quote: '', source: '', rating: '5' }]
    }));
  };

  const updateReview = (index, field, value) => {
    setConfig(prev => ({
      ...prev,
      reviews: prev.reviews.map((review, i) => 
        i === index ? { ...review, [field]: value } : review
      )
    }));
  };

  const removeReview = (index) => {
    setConfig(prev => ({
      ...prev,
      reviews: prev.reviews.filter((_, i) => i !== index)
    }));
  };

  const handleFileChange = (type, files) => {
    if (type === 'poster') {
      setAssets(prev => ({ ...prev, poster: files[0] }));
    } else if (type === 'stills') {
      setAssets(prev => ({ ...prev, stills: Array.from(files) }));
    } else if (type === 'teamPhotos') {
      setAssets(prev => ({ ...prev, teamPhotos: Array.from(files) }));
    }
  };

  const createProject = async () => {
    try {
      setError(null);
      setGenerating(true);

      // Client-side validation
      const errors = [];
      const warnings = [];

      if (!config.metadata.title) errors.push('Film title is required');
      if (!config.metadata.logline) errors.push('Logline is required');
      if (!config.metadata.synopsis) errors.push('Synopsis is required');
      if (!config.metadata.genre) errors.push('Genre is required');
      if (!config.metadata.runtime) errors.push('Runtime is required');
      if (!config.contact.email) errors.push('Contact email is required');
      if (!assets.poster) errors.push('Poster image is required');

      if (assets.stills.length < 8) {
        warnings.push(`Only ${assets.stills.length} stills provided. Recommended: 8-12`);
      }

      if (config.metadata.synopsis && config.metadata.synopsis.length < 200) {
        warnings.push(`Synopsis is short (${config.metadata.synopsis.length} chars). Recommended: 200-400 words`);
      }

      setValidation({
        is_valid: errors.length === 0,
        errors,
        warnings
      });

      if (errors.length === 0) {
        // Generate a simple project ID
        setProjectId(`epk-${Date.now()}`);
        setActiveStep(1);
      } else {
        throw new Error('Please fix the validation errors before continuing');
      }

    } catch (err) {
      setError(err.message);
    } finally {
      setGenerating(false);
    }
  };

  const generateEPK = async () => {
    try {
      setError(null);
      setGenerating(true);

      // Generate HTML client-side
      const htmlContent = generateEPKHTML(config, assets);
      
      // Create a blob and download URL
      const blob = new Blob([htmlContent], { type: 'text/html' });
      const url = URL.createObjectURL(blob);
      
      setDownloadUrls({
        html: url,
        htmlFilename: `${config.metadata.title?.replace(/[^a-z0-9]/gi, '_').toLowerCase() || 'epk'}_epk.html`
      });
      
      setActiveStep(2);

    } catch (err) {
      setError(err.message);
    } finally {
      setGenerating(false);
    }
  };

  const downloadFile = (type) => {
    if (downloadUrls && downloadUrls.html) {
      const link = document.createElement('a');
      link.href = downloadUrls.html;
      link.download = downloadUrls.htmlFilename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };
  
  const openHTMLPreview = () => {
    if (downloadUrls && downloadUrls.html) {
      window.open(downloadUrls.html, '_blank');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-4">
            <Film className="w-12 h-12 text-orange-500 mr-3" />
            <h1 className="text-5xl font-bold text-white">EPK Generator</h1>
          </div>
          <p className="text-xl text-gray-400">Create professional Electronic Press Kits for your films</p>
        </div>

        {/* Progress Steps */}
        <div className="flex justify-center mb-12">
          <div className="flex items-center space-x-4">
            {['Configure', 'Review', 'Download'].map((step, index) => (
              <div key={step} className="flex items-center">
                <div className={`flex items-center justify-center w-10 h-10 rounded-full ${
                  activeStep >= index ? 'bg-orange-500' : 'bg-gray-700'
                } text-white font-bold`}>
                  {activeStep > index ? <CheckCircle className="w-6 h-6" /> : index + 1}
                </div>
                <span className={`ml-2 ${activeStep >= index ? 'text-white' : 'text-gray-600'}`}>
                  {step}
                </span>
                {index < 2 && <div className="w-16 h-1 bg-gray-800 ml-4" />}
              </div>
            ))}
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="max-w-4xl mx-auto mb-6 bg-red-900 border border-red-700 rounded-lg p-4 flex items-start">
            <AlertCircle className="w-6 h-6 text-red-400 mr-3 flex-shrink-0 mt-0.5" />
            <div className="text-red-100">{error}</div>
          </div>
        )}

        {/* Step 1: Configuration */}
        {activeStep === 0 && (
          <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-lg shadow-2xl p-8">
              <h2 className="text-3xl font-bold mb-6 text-gray-800">Film Configuration</h2>

              {/* Basic Metadata */}
              <div className="mb-8">
                <h3 className="text-xl font-semibold mb-4 text-gray-700">Basic Information</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <input
                    type="text"
                    placeholder="Film Title *"
                    className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                    value={config.metadata.title}
                    onChange={(e) => handleConfigChange('metadata', 'title', e.target.value)}
                  />
                  <input
                    type="text"
                    placeholder="Director *"
                    className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                    value={config.metadata.director}
                    onChange={(e) => handleConfigChange('metadata', 'director', e.target.value)}
                  />
                  <select
                    className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                    value={config.metadata.genre}
                    onChange={(e) => handleConfigChange('metadata', 'genre', e.target.value)}
                  >
                    <option value="">Select Genre *</option>
                    {genres.map(genre => (
                      <option key={genre} value={genre}>{genre}</option>
                    ))}
                  </select>
                  <input
                    type="text"
                    placeholder="Runtime (e.g., 90 minutes) *"
                    className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                    value={config.metadata.runtime}
                    onChange={(e) => handleConfigChange('metadata', 'runtime', e.target.value)}
                  />
                </div>
                <input
                  type="text"
                  placeholder="Tagline"
                  className="mt-4 w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                  value={config.metadata.tagline}
                  onChange={(e) => handleConfigChange('metadata', 'tagline', e.target.value)}
                />
                <textarea
                  placeholder="Logline (1-2 sentences) *"
                  className="mt-4 w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500 h-20"
                  value={config.metadata.logline}
                  onChange={(e) => handleConfigChange('metadata', 'logline', e.target.value)}
                />
                <textarea
                  placeholder="Synopsis (2-3 paragraphs) *"
                  className="mt-4 w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500 h-40"
                  value={config.metadata.synopsis}
                  onChange={(e) => handleConfigChange('metadata', 'synopsis', e.target.value)}
                />
              </div>

              {/* Asset Uploads */}
              <div className="mb-8">
                <h3 className="text-xl font-semibold mb-4 text-gray-700">Assets</h3>
                
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Poster Image * (Recommended: 2000x3000px)
                  </label>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={(e) => handleFileChange('poster', e.target.files)}
                    className="w-full px-4 py-2 border rounded-lg"
                  />
                  {assets.poster && (
                    <p className="mt-2 text-sm text-green-600">✓ {assets.poster.name}</p>
                  )}
                </div>

                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Production Stills (8-12 recommended, 1920x1080px)
                  </label>
                  <input
                    type="file"
                    accept="image/*"
                    multiple
                    onChange={(e) => handleFileChange('stills', e.target.files)}
                    className="w-full px-4 py-2 border rounded-lg"
                  />
                  {assets.stills.length > 0 && (
                    <p className="mt-2 text-sm text-green-600">
                      ✓ {assets.stills.length} stills selected
                    </p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Team Photos (Name files matching team member names)
                  </label>
                  <input
                    type="file"
                    accept="image/*"
                    multiple
                    onChange={(e) => handleFileChange('teamPhotos', e.target.files)}
                    className="w-full px-4 py-2 border rounded-lg"
                  />
                  {assets.teamPhotos.length > 0 && (
                    <p className="mt-2 text-sm text-green-600">
                      ✓ {assets.teamPhotos.length} photos selected
                    </p>
                  )}
                </div>
              </div>

              {/* Team Members */}
              <div className="mb-8">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-xl font-semibold text-gray-700">Cast & Crew</h3>
                  <button
                    onClick={addTeamMember}
                    className="px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors"
                  >
                    + Add Member
                  </button>
                </div>
                {config.team.map((member, index) => (
                  <div key={index} className="mb-4 p-4 border rounded-lg bg-gray-50">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-2">
                      <input
                        type="text"
                        placeholder="Name"
                        className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                        value={member.name}
                        onChange={(e) => updateTeamMember(index, 'name', e.target.value)}
                      />
                      <input
                        type="text"
                        placeholder="Role (e.g., Director, Lead Actor)"
                        className="px-4 py-2 border rounded-lg"
                        value={member.role}
                        onChange={(e) => updateTeamMember(index, 'role', e.target.value)}
                      />
                    </div>
                    <textarea
                      placeholder="Bio"
                      className="w-full px-4 py-2 border rounded-lg mb-2"
                      rows="2"
                      value={member.bio}
                      onChange={(e) => updateTeamMember(index, 'bio', e.target.value)}
                    />
                    <button
                      onClick={() => removeTeamMember(index)}
                      className="text-red-600 hover:text-red-800 text-sm"
                    >
                      Remove
                    </button>
                  </div>
                ))}
              </div>

              {/* Awards */}
              <div className="mb-8">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-xl font-semibold text-gray-700">Awards (Optional)</h3>
                  <button
                    onClick={addAward}
                    className="px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors"
                  >
                    + Add Award
                  </button>
                </div>
                {config.awards.map((award, index) => (
                  <div key={index} className="mb-4 p-4 border rounded-lg bg-gray-50">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-2">
                      <input
                        type="text"
                        placeholder="Festival Name"
                        className="px-4 py-2 border rounded-lg"
                        value={award.festival_name}
                        onChange={(e) => updateAward(index, 'festival_name', e.target.value)}
                      />
                      <input
                        type="text"
                        placeholder="Award"
                        className="px-4 py-2 border rounded-lg"
                        value={award.award}
                        onChange={(e) => updateAward(index, 'award', e.target.value)}
                      />
                      <input
                        type="text"
                        placeholder="Year"
                        className="px-4 py-2 border rounded-lg"
                        value={award.year}
                        onChange={(e) => updateAward(index, 'year', e.target.value)}
                      />
                    </div>
                    <button
                      onClick={() => removeAward(index)}
                      className="text-red-600 hover:text-red-800 text-sm"
                    >
                      Remove
                    </button>
                  </div>
                ))}
              </div>

              {/* Reviews */}
              <div className="mb-8">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-xl font-semibold text-gray-700">Reviews (Optional)</h3>
                  <button
                    onClick={addReview}
                    className="px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors"
                  >
                    + Add Review
                  </button>
                </div>
                {config.reviews.map((review, index) => (
                  <div key={index} className="mb-4 p-4 border rounded-lg bg-gray-50">
                    <textarea
                      placeholder="Quote"
                      className="w-full px-4 py-2 border rounded-lg mb-2"
                      rows="2"
                      value={review.quote}
                      onChange={(e) => updateReview(index, 'quote', e.target.value)}
                    />
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-2">
                      <input
                        type="text"
                        placeholder="Source (e.g., The Hollywood Reporter)"
                        className="px-4 py-2 border rounded-lg"
                        value={review.source}
                        onChange={(e) => updateReview(index, 'source', e.target.value)}
                      />
                      <select
                        className="px-4 py-2 border rounded-lg"
                        value={review.rating}
                        onChange={(e) => updateReview(index, 'rating', e.target.value)}
                      >
                        <option value="5">5 Stars</option>
                        <option value="4">4 Stars</option>
                        <option value="3">3 Stars</option>
                        <option value="2">2 Stars</option>
                        <option value="1">1 Star</option>
                      </select>
                    </div>
                    <button
                      onClick={() => removeReview(index)}
                      className="text-red-600 hover:text-red-800 text-sm"
                    >
                      Remove
                    </button>
                  </div>
                ))}
              </div>

              {/* Contact Information */}
              <div className="mb-8">
                <h3 className="text-xl font-semibold mb-4 text-gray-700">Contact Information</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <input
                    type="text"
                    placeholder="Contact Name"
                    className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                    value={config.contact.name}
                    onChange={(e) => handleConfigChange('contact', 'name', e.target.value)}
                  />
                  <input
                    type="email"
                    placeholder="Email *"
                    className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                    value={config.contact.email}
                    onChange={(e) => handleConfigChange('contact', 'email', e.target.value)}
                  />
                  <input
                    type="tel"
                    placeholder="Phone"
                    className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                    value={config.contact.phone}
                    onChange={(e) => handleConfigChange('contact', 'phone', e.target.value)}
                  />
                  <input
                    type="url"
                    placeholder="Website"
                    className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                    value={config.contact.website}
                    onChange={(e) => handleConfigChange('contact', 'website', e.target.value)}
                  />
                </div>
              </div>

              {/* Submit Button */}
              <button
                onClick={createProject}
                disabled={generating}
                className="w-full py-3 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed font-semibold text-lg"
              >
                {generating ? 'Creating Project...' : 'Create EPK Project'}
              </button>
            </div>
          </div>
        )}

        {/* Step 2: Review & Validation */}
        {activeStep === 1 && (
          <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-lg shadow-2xl p-8">
              <h2 className="text-3xl font-bold mb-6 text-gray-800">Review & Validation</h2>

              {validation && (
                <div className="mb-6">
                  {validation.is_valid ? (
                    <div className="bg-green-100 border border-green-400 rounded-lg p-4 flex items-start">
                      <CheckCircle className="w-6 h-6 text-green-600 mr-3 flex-shrink-0 mt-0.5" />
                      <div>
                        <h3 className="font-semibold text-green-800">Validation Passed!</h3>
                        <p className="text-green-700">Your project is ready to generate.</p>
                      </div>
                    </div>
                  ) : (
                    <div className="bg-red-100 border border-red-400 rounded-lg p-4 flex items-start">
                      <AlertCircle className="w-6 h-6 text-red-600 mr-3 flex-shrink-0 mt-0.5" />
                      <div>
                        <h3 className="font-semibold text-red-800">Validation Errors</h3>
                        <ul className="list-disc list-inside text-red-700">
                          {validation.errors.map((error, i) => (
                            <li key={i}>{error}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  )}

                  {validation.warnings && validation.warnings.length > 0 && (
                    <div className="mt-4 bg-yellow-100 border border-yellow-400 rounded-lg p-4 flex items-start">
                      <AlertCircle className="w-6 h-6 text-yellow-600 mr-3 flex-shrink-0 mt-0.5" />
                      <div>
                        <h3 className="font-semibold text-yellow-800">Warnings</h3>
                        <ul className="list-disc list-inside text-yellow-700">
                          {validation.warnings.map((warning, i) => (
                            <li key={i}>{warning}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  )}
                </div>
              )}

              <div className="flex space-x-4">
                <button
                  onClick={() => setActiveStep(0)}
                  className="flex-1 py-3 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors font-semibold"
                >
                  ← Back to Edit
                </button>
                <button
                  onClick={generateEPK}
                  disabled={generating || (validation && !validation.is_valid)}
                  className="flex-1 py-3 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed font-semibold"
                >
                  {generating ? 'Generating EPK...' : 'Generate EPK'}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Step 3: Download */}
        {activeStep === 2 && (
          <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-lg shadow-2xl p-8">
              <div className="text-center mb-8">
                <CheckCircle className="w-16 h-16 text-green-600 mx-auto mb-4" />
                <h2 className="text-3xl font-bold text-gray-800 mb-2">EPK Generated Successfully!</h2>
                <p className="text-gray-600">Your Electronic Press Kit is ready to download.</p>
              </div>

              <div className="grid grid-cols-1 gap-4 mb-8">
                <button
                  onClick={() => downloadFile('html')}
                  className="flex items-center justify-center py-4 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors font-semibold"
                >
                  <FileText className="w-6 h-6 mr-2" />
                  Download HTML EPK
                </button>
                <button
                  onClick={openHTMLPreview}
                  className="flex items-center justify-center py-4 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors font-semibold"
                >
                  <FileText className="w-6 h-6 mr-2" />
                  Preview in Browser
                </button>
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-sm">
                  <p className="text-blue-800 font-semibold mb-2">📄 Create PDF from HTML:</p>
                  <ol className="list-decimal list-inside text-blue-700 space-y-1">
                    <li>Click "Preview in Browser" or download HTML</li>
                    <li>Press Ctrl/Cmd + P (Print)</li>
                    <li>Choose "Save as PDF"</li>
                    <li>Click "Save"</li>
                  </ol>
                  <p className="text-blue-600 mt-2 text-xs">The HTML is print-optimized for professional PDF output!</p>
                </div>
              </div>

              <button
                onClick={() => {
                  setActiveStep(0);
                  setProjectId(null);
                  setValidation(null);
                  setDownloadUrls(null);
                  setError(null);
                }}
                className="w-full py-3 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors font-semibold"
              >
                Create Another EPK
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
