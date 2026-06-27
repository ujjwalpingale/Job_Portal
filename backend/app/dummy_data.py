from typing import List, Dict, Any

# In-memory database representation
# USERS table will store both Candidates and Recruiters
# Structure of a user:
# {
#     "id": int,
#     "email": str,
#     "hashed_password": str,
#     "role": str, # "candidate" or "recruiter"
#     "profile": dict # specific profile details based on role
# }
USERS: List[Dict[str, Any]] = []

# JOBS table
# Structure of a job:
# {
#     "id": int,
#     "recruiter_id": int,
#     "title": str,
#     "description": str,
#     "location": str,
#     "experience": str,
#     "job_type": str,
#     "salary": str,
#     "keywords": List[str]
# }
JOBS: List[Dict[str, Any]] = []

# APPLICATIONS table
# Structure of an application:
# {
#     "id": int,
#     "job_id": int,
#     "candidate_id": int,
#     "status": str # "pending", "accepted", "rejected"
# }
APPLICATIONS: List[Dict[str, Any]] = []

# Auto-incrementing counters
_user_id_counter = 1
_job_id_counter = 1
_application_id_counter = 1

def generate_user_id() -> int:
    global _user_id_counter
    current = _user_id_counter
    _user_id_counter += 1
    return current

def generate_job_id() -> int:
    global _job_id_counter
    current = _job_id_counter
    _job_id_counter += 1
    return current

def generate_application_id() -> int:
    global _application_id_counter
    current = _application_id_counter
    _application_id_counter += 1
    return current
