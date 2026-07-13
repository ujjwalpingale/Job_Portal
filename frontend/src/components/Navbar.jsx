import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Briefcase, User, LogOut } from 'lucide-react';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="glass-panel" style={{ position: 'sticky', top: 0, zIndex: 50, borderRadius: 0, borderTop: 'none', borderLeft: 'none', borderRight: 'none' }}>
      <div className="container flex justify-between items-center" style={{ height: '4rem' }}>
        <Link to="/" className="flex items-center gap-2">
          <Briefcase color="var(--accent-color)" size={28} />
          <span className="text-gradient" style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>
            JobPortal
          </span>
        </Link>

        <div className="flex items-center gap-4">
          {user ? (
            <>
              <Link to="/" className="text-secondary hover:text-primary">Home</Link>
              <Link to="/profile" className="flex items-center gap-2" style={{ color: 'var(--text-secondary)' }}>
                <User size={18} />
                <span style={{ transition: 'color 0.2s ease' }} onMouseOver={(e) => e.target.style.color = 'var(--accent-color)'} onMouseOut={(e) => e.target.style.color = 'inherit'}>Profile</span>
              </Link>
              <button onClick={handleLogout} className="flex items-center gap-2 btn btn-secondary btn-sm">
                <LogOut size={16} />
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="btn btn-secondary btn-sm">Login</Link>
              <Link to="/register" className="btn btn-primary btn-sm">Sign Up</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
