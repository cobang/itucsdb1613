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
    def __init__(self, job_id, title, description, company_id, location_id):
        self.job_id = job_id
        self.title = title
        self.description = description
        self.company_id = company_id
        self.location_id = location_id

    def get_location_name(self):
        try:
            conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                                   passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
            c = conn.cursor()
            sql = """SELECT location_country, location_state FROM location WHERE location_id = (%d) """ % \
                  (int(self.location_id))
            c.execute(sql)
            for row in c:
                location_country, location_state = row
            conn.commit()
            c.close()
            conn.close()
        except Exception as e:
            print(str(e))

        return location_state


def job_share():
    archive = Jobs()
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()
        sql = """SELECT * FROM jobs"""

        c.execute(sql)

        for row in c:
            job_id, title, description, company_id, location_id = row
            job = Job(job_id=job_id, title=title, description=description, company_id=company_id,
                      location_id=location_id)
            archive.add_job(job=job)

        c.close()
        conn.close()
        return archive.get_jobs()

    except Exception as e:
        print(str(e))
        return archive.get_jobs()


def job_add(title, description, company_id, location_id):
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()
        '''sql = """INSERT INTO location(location_state, location_country, location_zipcode, user_id)
                         VALUES ('%s', '%s','%s','%d') """ % (location, 'Turkey', '12345', int(1))
        print('hey')
        c.execute(sql)
        conn.commit()
        sql = """SELECT location_id,location_state FROM location WHERE location_state= ('%s') """ % location
        c.execute(sql)
        for row in c:
            location_id, location_state = row

        c = conn.cursor() '''
        sql = """INSERT INTO jobs(TITLE, DESCRIPTION,COMPANY_ID, LOCATION_ID)
                               VALUES ('%s', '%s' , '%d', '%d' )""" % (title, description, int(company_id),
                                                                       int(location_id))
        c.execute(sql)

        conn.commit()
        c.close()
        conn.close()

    except Exception as e:
        print(str(e))


def job_edit(job_id, title, description, location):
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()
        sql = """INSERT INTO location WHERE location_state= ('%s') """ % location
        c.execute(sql)
        conn.commit()
        sql = """SELECT location_id,location_state FROM location WHERE location_state= ('%s') """ % location
        c.execute(sql)
        for row in c:
            location_id, location_state = row
        sql = """UPDATE jobs SET title = '%s', description = '%s', location_id='%d'  WHERE job_id = %d """ % (
            title, description, location_id,int(job_id))
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
        sql = """SELECT location.id,title FROM jobs WHERE job_id = (%d) """ % (int(job_id))
        c.execute(sql)
        for row in c:
            location_id, title = row
        sql = """DELETE FROM location WHERE location_id = (%d) """ % (int(location_id))
        c.execute(sql)
        conn.commit()
        sql = """DELETE FROM jobs WHERE job_id = (%d) """ % (int(job_id))
        c.execute(sql)
        conn.commit()
        c.close()
        conn.close()

    except Exception as e:
        print(str(e))


