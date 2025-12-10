import redis
import time
from datetime import datetime

class JobStorage:
    def __init__(self):
        """
        Remote Redis connection.
        Example:
        storage = JobStorage(
            host="redis-12345.c1.ap-south-1-1.ec2.cloud.redislabs.com",
            port=12345,
            password="your_password",
            ssl=True
        )
        """
        self.r = redis.Redis(
            host="redis-16983.c62.us-east-1-4.ec2.cloud.redislabs.com",
            port=16983,
            password="xrFSwC0ZWKj0fCFvr4SkBDM3dlHK8esd",
            ssl=False,
            decode_responses=True
        )

    def _key(self, hr_email):
        """Unique key = HR email"""
        return f"job:{hr_email.lower()}"

    # def save_job(self, payload):
    #     """Save job details into Redis"""
    #     hr_email = payload["application_email"]["HR_email_address"]
    #     key = self._key(hr_email)

    #     data = {
    #         "company_name": payload["job_details"]["company_name"],
    #         "job_role": payload["job_details"]["job_role"],
    #         "experience_required": payload["job_details"]["required_experience_years"],
    #         "subject_line": payload["application_email"]["subject_line"],
    #         "hr_email": hr_email,
    #         "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     }

    #     self.r.hset(key, mapping=data)
    #     return key

    from datetime import datetime

    def save_job(self, 
                 company_name, 
                 job_role, 
                 experience_required, 
                 job_description, 
                 hr_email):
        """
        Save job details into Redis using individual arguments.

        Args:
            company_name (str): Name of the company
            job_role (str): Job title
            experience_required (str): Required experience (e.g., "Fresher – 1 Year")
            subject_line (str): Email subject line
            hr_email (str): HR email (used as unique key)
        """
        key = self._key(hr_email)

        data = {
            "company_name": company_name,
            "job_role": job_role,
            "experience_required": experience_required,
            "job_description": job_description,
            "hr_email": hr_email,
            "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # human-readable date/time
        }

        self.r.hset(key, mapping=data)
        return key

    def get_job(self, hr_email):
        key = self._key(hr_email)
        return self.r.hgetall(key)

    def list_jobs(self):
        keys = self.r.keys("job:*")
        return {k: self.r.hgetall(k) for k in keys}

    def delete_job(self, hr_email):
        key = self._key(hr_email)
        return self.r.delete(key)


# ------------------------------------------------------------
#                   TEST THE CLASS
# ------------------------------------------------------------
if __name__ == "__main__":

    # 🔥 ENTER YOUR REDIS HOST, PORT, PASSWORD HERE
    storage = JobStorage()

    # Test payload
    payload = {
        "application_email": {
            "subject_line": "Application for AIML Developer Position",
            "HR_email_address": "moxa@tekpillarr.com"
        },
        "job_details": {
            "company_name": "Tekpillar",
            "job_role": "AIML Developer",
            "required_experience_years": "Fresher – 1 Year"
        }
    }

    print("\n=== Saving Job ===")
    key = storage.save_job(payload["job_details"]["company_name"],
                           payload["job_details"]["job_role"],
                           payload["job_details"]["required_experience_years"],
                           "Sample job description here...",
                           payload["application_email"]["HR_email_address"]
                    )
    print("Saved at key:", key)

    print("\n=== Retrieving Job ===")
    job = storage.get_job("moxa@tekpillarr.com")
    print(job)

    print("\n=== Listing All Jobs ===")
    all_jobs = storage.list_jobs()
    print(all_jobs)
