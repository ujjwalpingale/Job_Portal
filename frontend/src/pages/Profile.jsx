import { useState, useRef, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { userAPI, applicationAPI, jobAPI } from '../api';
import { User, Mail, Phone, Upload, FileText, Briefcase } from 'lucide-react';

const Profile = () => {
  const { user, setUser } = useAuth();
  const [applications, setApplications] = useState([]);
  const [jobsDict, setJobsDict] = useState({});
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef(null);

  useEffect(() => {
    const loadApplications = async () => {
      try {
        const appsRes = await applicationAPI.getApplications();
        setApplications(appsRes.data);
        
        // Fetch all jobs to match job_ids to job titles
        const jobsRes = await jobAPI.getJobs();
        const dict = {};
        jobsRes.data.forEach(j => dict[j.id] = j);
        setJobsDict(dict);
      } catch (err) {
        console.error("Failed to load applications", err);
      }
    };
    
    loadApplications();
  }, [user]);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    
    setUploading(true);
    try {
      await userAPI.uploadResume(file);
      alert('Resume uploaded successfully!');
      const profileRes = await userAPI.getProfile();
      setUser(profileRes.data);
      setFile(null);
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to upload resume');
    } finally {
      setUploading(false);
    }
  };

  const handleUpdateStatus = async (appId, status) => {
    try {
      await applicationAPI.updateStatus(appId, status);
      const appsRes = await applicationAPI.getApplications();
      setApplications(appsRes.data);
    } catch (err) {
      alert('Failed to update status');
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2" style={{ gap: '2rem' }}>
      <div className="flex flex-col gap-6">
        <div className="glass-panel" style={{ padding: '2rem' }}>
          <h2 className="text-gradient" style={{ fontSize: '1.5rem', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <User size={24} /> Profile Information
          </h2>
          
          <div className="flex flex-col gap-4" style={{ color: 'var(--text-secondary)' }}>
            <div>
              <label style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-secondary)' }}>Full Name</label>
              <div style={{ color: 'white', fontSize: '1.125rem', marginTop: '0.25rem' }}>{user?.name}</div>
            </div>
            
            <div>
              <label style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-secondary)' }}>Role</label>
              <div style={{ color: 'var(--accent-color)', fontSize: '1rem', marginTop: '0.25rem', textTransform: 'capitalize' }}>{user?.role}</div>
            </div>

            <div className="flex items-center gap-3">
              <Mail size={18} />
              <span style={{ color: 'white' }}>{user?.email}</span>
            </div>

            <div className="flex items-center gap-3">
              <Phone size={18} />
              <span style={{ color: 'white' }}>{user?.phone || 'Not provided'}</span>
            </div>
          </div>
        </div>

        {user?.role === 'candidate' && (
          <div className="glass-panel" style={{ padding: '2rem' }}>
            <h2 style={{ fontSize: '1.25rem', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <FileText size={20} /> Resume Management
            </h2>
            
            {user?.resume_path ? (
              <div style={{ padding: '1rem', backgroundColor: 'var(--bg-tertiary)', borderRadius: 'var(--border-radius-sm)', marginBottom: '1.5rem', border: '1px solid var(--border-color)', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <div style={{ padding: '0.5rem', backgroundColor: 'var(--bg-secondary)', borderRadius: '50%' }}>
                  <FileText size={20} color="var(--success)" />
                </div>
                <div>
                  <div style={{ fontWeight: '500', color: 'white' }}>Resume uploaded</div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>{user.resume_path.split('_').pop()}</div>
                </div>
              </div>
            ) : (
              <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem', fontSize: '0.875rem' }}>
                You haven't uploaded a resume yet. Upload one to help recruiters find you!
              </p>
            )}

            <div className="flex flex-col gap-3">
              <input 
                type="file" 
                ref={fileInputRef} 
                onChange={handleFileChange} 
                style={{ display: 'none' }} 
                accept=".pdf,.doc,.docx"
              />
              <div className="flex items-center gap-2">
                <button className="btn btn-secondary" style={{ flexGrow: 1 }} onClick={() => fileInputRef.current.click()}>
                  Select File
                </button>
                {file && (
                  <button className="btn btn-primary flex items-center gap-2" onClick={handleUpload} disabled={uploading}>
                    <Upload size={16} />
                    {uploading ? 'Uploading...' : 'Upload'}
                  </button>
                )}
              </div>
              {file && (
                <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                  Selected: {file.name}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
      
      <div>
        <div className="glass-panel" style={{ padding: '2rem', height: '100%' }}>
          <h2 style={{ fontSize: '1.5rem', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Briefcase size={24} color="var(--accent-color)" /> 
            {user?.role === 'recruiter' ? 'Received Applications' : 'Your Applications'}
          </h2>
          
          {applications.length === 0 ? (
            <div style={{ textAlign: 'center', color: 'var(--text-secondary)', padding: '2rem 0' }}>
              {user?.role === 'recruiter' ? 'No applications received yet.' : 'You haven\'t applied to any jobs yet.'}
            </div>
          ) : (
            <div className="flex flex-col gap-3">
              {applications.map(app => {
                const job = jobsDict[app.job_id];
                return (
                  <div key={app.id} style={{ padding: '1rem', backgroundColor: 'var(--bg-tertiary)', borderRadius: 'var(--border-radius-sm)', border: '1px solid var(--border-color)' }}>
                    <div className="flex justify-between items-start" style={{ marginBottom: '0.5rem' }}>
                      <h4 style={{ fontWeight: '500', color: 'white' }}>{job?.title || 'Unknown Job'}</h4>
                      <span style={{ 
                        fontSize: '0.75rem', 
                        padding: '0.25rem 0.5rem', 
                        borderRadius: '999px',
                        backgroundColor: app.status === 'pending' ? 'rgba(234, 179, 8, 0.2)' : app.status === 'approved' ? 'rgba(16, 185, 129, 0.2)' : 'rgba(239, 68, 68, 0.2)',
                        color: app.status === 'pending' ? '#eab308' : app.status === 'approved' ? 'var(--success)' : 'var(--danger)'
                      }}>
                        {app.status.toUpperCase()}
                      </span>
                    </div>
                    {user?.role === 'recruiter' ? (
                      <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                        <div style={{ marginBottom: '0.75rem', color: 'white' }}>
                          <span style={{ fontWeight: '500' }}>{app.candidate?.name}</span> ({app.candidate?.email})
                        </div>
                        {app.candidate?.resume_path ? (
                          <a 
                            href={`http://localhost:8000/${app.candidate.resume_path}`} 
                            target="_blank" 
                            rel="noopener noreferrer" 
                            className="btn btn-secondary btn-sm flex items-center gap-2" 
                            style={{ display: 'inline-flex' }}
                          >
                            <FileText size={16} /> View Resume
                          </a>
                        ) : (
                          <span style={{ fontStyle: 'italic', color: 'var(--danger)' }}>No resume uploaded</span>
                        )}

                        {app.status === 'pending' && (
                          <div className="flex gap-2" style={{ marginTop: '1rem' }}>
                            <button 
                              className="btn btn-primary btn-sm" 
                              onClick={() => handleUpdateStatus(app.id, 'approved')}
                            >
                              Approve
                            </button>
                            <button 
                              className="btn btn-danger btn-sm" 
                              onClick={() => handleUpdateStatus(app.id, 'rejected')}
                            >
                              Reject
                            </button>
                          </div>
                        )}
                      </div>
                    ) : (
                      <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                        {job?.location} • {job?.salary}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Profile;
