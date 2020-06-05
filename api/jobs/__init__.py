from jobs.content import JOBS as content_jobs
from jobs.science_feedback import JOBS as science_feedback_jobs
from jobs.user import JOBS as user_jobs


JOBS = content_jobs \
       + user_jobs  \
       + science_feedback_jobs
