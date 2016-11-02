import pymysql
from dbconnection import MySQL


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


def job_share():
    archive = Jobs()
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()
        sql = """SELECT * FROM jobs"""

        c.execute(sql)

        for row in c:
            job_id, title, description = row
            job = Job(job_id=job_id, title=title, description=description)
            archive.add_job(job=job)

        c.close()
        conn.close()
        return archive.get_jobs()

    except Exception as e:
        print(str(e))
        return archive.get_jobs()


def job_add(title, description):
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()
        sql = """INSERT INTO jobs(TITLE, DESCRIPTION)
                                       VALUES ('%s', '%s' )""" % (title, description)

        c.execute(sql)

        conn.commit()
        c.close()
        conn.close()

    except Exception as e:
        print(str(e))


def job_edit(job_id, title, description):
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()
        sql = """UPDATE jobs SET title = '%s', description = '%s'  WHERE job_id = %d """ % (
            title, description, int(job_id))
        c.execute(sql)
        conn.commit()
        c.close()
        conn.close()

    except Exception as e:
        print(str(e))


def job_delete(job_id):
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()
        sql = """DELETE FROM jobs WHERE job_id = (%d) """ % (int(job_id))
        c.execute(sql)
        conn.commit()
        c.close()
        conn.close()

    except Exception as e:
        print(str(e))
