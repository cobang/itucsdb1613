class Jobs:
    def __init__(self):
        self.jobs = {}
        self.key = 0

    def add_job(self, job):
        self.key += 1
        job.key = self.key
        self.jobs[self.key] = job

    def get_job(self, key):
        return self.jobs[key]

    def get_jobs(self):
        return sorted(self.jobs.items())


class Job:
    def __init__(self, job_id, title, description):
        self.job_id = job_id
        self.title = title
        self.description = description
