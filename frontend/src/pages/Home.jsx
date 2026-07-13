import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { jobAPI, applicationAPI } from '../api';
import { MapPin, IndianRupee, Briefcase as BriefcaseIcon, Clock } from 'lucide-react';

const Home = () => {
  const { user } = useAuth();
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [newJob, setNewJob] = useState({ title: '', description: '', location: '', salary: '', experience: '' });
  
  // For candidates to track what they applied for (mapping job_id to status)
  const [applications, setApplications] = useState({});

  useEffect(() => {
    fetchJobs();
    if (user?.role === 'candidate') {
      fetchApplications();
    }
  }, [user]);

  const fetchJobs = async () => {
    try {
      const res = await jobAPI.getJobs();
      setJobs(res.data);
    } catch (err) {
      console.error('Failed to fetch jobs', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchApplications = async () => {
    try {
      const res = await applicationAPI.getApplications();
      const appMap = {};
      res.data.forEach(app => {
        appMap[app.job_id] = app.status;
      });
      setApplications(appMap);
    } catch (err) {
      console.error('Failed to fetch applications', err);
    }
  };

  const handleCreateJob = async (e) => {
    e.preventDefault();
    try {
      await jobAPI.createJob(newJob);
      setShowModal(false);
      setNewJob({ title: '', description: '', location: '', salary: '', experience: '' });
      fetchJobs();
    } catch (err) {
      alert('Failed to create job');
    }
  };

  const handleApply = async (jobId) => {
    try {
      await applicationAPI.applyForJob(jobId);
      alert('Successfully applied!');
      fetchApplications();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to apply');
    }
  };

  const handleDeleteJob = async (jobId) => {
    if (window.confirm('Are you sure you want to delete this job?')) {
      try {
        await jobAPI.deleteJob(jobId);
        fetchJobs();
      } catch (err) {
        alert('Failed to delete job');
      }
    }
  };

  if (loading) {
    return <div className="flex justify-center" style={{ marginTop: '3rem' }}>Loading jobs...</div>;
  }

  // Recruiters see only their jobs. (Simple implementation since backend returns all jobs without filter by default)
  const displayJobs = user?.role === 'recruiter' 
    ? jobs.filter(j => j.recruiter_id === user.id) 
    : jobs;

  return (
    <div>
      <div className="flex justify-between items-center" style={{ marginBottom: '2rem' }}>
        <div>
          <h1 className="text-gradient" style={{ fontSize: '2.25rem' }}>
            {user?.role === 'recruiter' ? 'Your Job Postings' : 'Available Jobs'}
          </h1>
          <p style={{ color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
            {user?.role === 'recruiter' 
              ? 'Manage your job listings and find the best candidates.' 
              : 'Discover your next career opportunity.'}
          </p>
        </div>
        
        {user?.role === 'recruiter' && (
          <button className="btn btn-primary" onClick={() => setShowModal(true)}>
            Post a New Job
          </button>
        )}
      </div>

      {displayJobs.length === 0 ? (
        <div className="glass-panel" style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-secondary)' }}>
          {user?.role === 'recruiter' ? 'You haven\'t posted any jobs yet.' : 'No jobs available right now.'}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3" style={{ gap: '1.5rem' }}>
          {displayJobs.map(job => (
            <div key={job.id} className="glass-panel" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column' }}>
              <div style={{ flexGrow: 1 }}>
                <h3 style={{ fontSize: '1.25rem', marginBottom: '0.5rem', color: 'white' }}>{job.title}</h3>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginBottom: '1rem', display: '-webkit-box', WebkitLineClamp: 3, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                  {job.description}
                </p>
                
                <div className="flex flex-col gap-2" style={{ marginBottom: '1.5rem', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                  {job.location && (
                    <div className="flex items-center gap-2"><MapPin size={16} /> {job.location}</div>
                  )}
                  {job.salary && (
                    <div className="flex items-center gap-2"><IndianRupee size={16} /> {job.salary}</div>
                  )}
                  {job.experience && (
                    <div className="flex items-center gap-2"><BriefcaseIcon size={16} /> {job.experience} experience</div>
                  )}
                </div>
              </div>
              
              <div style={{ borderTop: '1px solid var(--border-color)', paddingTop: '1rem', marginTop: 'auto' }}>
                {user?.role === 'candidate' ? (
                  <button 
                    className={`btn ${applications[job.id] ? (applications[job.id] === 'rejected' ? 'btn-danger' : 'btn-secondary') : 'btn-primary'}`} 
                    style={{ width: '100%', cursor: applications[job.id] ? 'default' : 'pointer' }}
                    onClick={() => handleApply(job.id)}
                    disabled={!!applications[job.id]}
                  >
                    {applications[job.id] ? `Applied • ${applications[job.id].toUpperCase()}` : 'Apply Now'}
                  </button>
                ) : (
                  <button 
                    className="btn btn-danger" 
                    style={{ width: '100%' }}
                    onClick={() => handleDeleteJob(job.id)}
                  >
                    Delete Job
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Simple Modal for creating jobs */}
      {showModal && (
        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.7)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 100, padding: '1rem' }}>
          <div className="glass-panel" style={{ width: '100%', maxWidth: '600px', padding: '2rem', maxHeight: '90vh', overflowY: 'auto' }}>
            <h2 style={{ fontSize: '1.5rem', marginBottom: '1.5rem' }}>Create Job Posting</h2>
            
            <form onSubmit={handleCreateJob}>
              <div className="form-group">
                <label className="form-label">Job Title</label>
                <input className="form-input" required value={newJob.title} onChange={e => setNewJob({...newJob, title: e.target.value})} />
              </div>
              
              <div className="form-group">
                <label className="form-label">Description</label>
                <textarea className="form-input" required rows={4} value={newJob.description} onChange={e => setNewJob({...newJob, description: e.target.value})} />
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2" style={{ gap: '1rem' }}>
                <div className="form-group">
                  <label className="form-label">Location</label>
                  <input className="form-input" value={newJob.location} onChange={e => setNewJob({...newJob, location: e.target.value})} placeholder="e.g. Remote, New York" />
                </div>
                
                <div className="form-group">
                  <label className="form-label">Salary</label>
                  <input className="form-input" value={newJob.salary} onChange={e => setNewJob({...newJob, salary: e.target.value})} placeholder="e.g. ₹10L - ₹15L" />
                </div>
              </div>
              
              <div className="form-group">
                <label className="form-label">Experience Required</label>
                <input className="form-input" value={newJob.experience} onChange={e => setNewJob({...newJob, experience: e.target.value})} placeholder="e.g. 3-5 years" />
              </div>
              
              <div className="flex justify-end gap-4" style={{ marginTop: '2rem' }}>
                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>Cancel</button>
                <button type="submit" className="btn btn-primary">Post Job</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Home;
