import pymysql
from dbconnection import MySQL


class Jobs:
    def __init__(self):
        self.jobs = {}
        self.key = 0

    def add_job(self, job):
        self.key += 1
        self.jobs[self.key] = job

    def get_job(self, key):
        return self.jobs[key]

    def get_jobs(self):
        return sorted(self.jobs.items())


class Job:
    def __init__(self, job_id, title, description, user_id, location_id):
        self.job_id = job_id
        self.title = title
        self.description = description
        self.user_id = user_id
        self.location_id = location_id
        self.appliers = {}
        self.key = 0

    def add_appliers(self, user):
        self.key += 1
        self.appliers[self.key] = user

    def get_appliers(self):
        return sorted(self.appliers)

    def get_location_name(self):
        try:
            conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                                   passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
            c = conn.cursor()
            sql = """SELECT location_state,location_country FROM location WHERE location_id = (%d) """ % \
                  self.location_id
            c.execute(sql)
            for row in c:
                 location_state,location_country = row
            print(location_state)
            conn.commit()
            c.close()
            conn.close()
        except Exception as e:
            print(str(e))

        return location_state


def applier_name(user_id):
    try:
        user_name = "NAME"
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()

        sql = """SELECT user_type FROM users WHERE user_id = %d""" % user_id
        c.execute(sql)
        for row in c:
            user_type = row[0]

        if user_type == 1:
            sql = """SELECT user_name, user_surname FROM user_detail WHERE user_id = %d""" % user_id
            c.execute(sql)

            for row in c:
                user_name, user_surname = row
                user_name = user_name + " " + user_surname

        elif user_type == 2:
            sql = """SELECT company_name FROM company_detail WHERE user_id = %d""" % user_id
            c.execute(sql)
            for row in c:
                company_name = row[0]
                user_name = company_name

        elif user_type == 3:
            sql = """SELECT university_name FROM university_detail WHERE user_id = %d""" % user_id
            c.execute(sql)
            for row in c:
                university_name = row[0]
                user_name = university_name

        c.close()
        conn.close()
    except Exception as e:
        print(str(e))

    return user_name


def job_share():
    archive = Jobs()
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()
        sql = """SELECT * FROM jobs"""

        c.execute(sql)

        for row in c:
            job_id, user_id, location_id, title, description = row
            job = Job(job_id=job_id, user_id=user_id, location_id=location_id, title=title, description=description
                      )
            d = conn.cursor()
            sql = """SELECT user_id FROM job_appliers WHERE job_id= (%d) """ % job_id
            d.execute(sql)
            for row2 in d:
                user_name = applier_name(row2[0])
                job.add_appliers((row2[0], user_name))
                print(row2[0])
            archive.add_job(job=job)
            print(job)
        c.close()
        conn.close()
        return archive.get_jobs()

    except Exception as e:
        print(str(e))
        return archive.get_jobs()


def job_add(title, description, user_id, location):
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()
        sql = """INSERT INTO location(location_state, location_country, location_zipcode, user_id)
                         VALUES ('%s', '%s','%s','%d') """ % (location, '', '', user_id)
        c.execute(sql)
        conn.commit()
        sql = """SELECT location_id,location_state FROM location WHERE location_state= ('%s') """ % location
        c.execute(sql)
        for row in c:
            location_id, location_state = row
        c = conn.cursor()
        sql = """INSERT INTO jobs(user_id, location_id, title, description)
                               VALUES ('%d', '%d' , '%s', '%s' )""" % (int(user_id),int(location_id), title, description,)
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
        sql = """SELECT location_id, job_id FROM jobs WHERE job_id = (%d) """ % int(job_id)
        c.execute(sql)
        for row in c:
            location_id, job_id = row
        sql = """UPDATE location SET  location_state = '%s'  WHERE location_id = '%d' """ % (location, int(location_id))
        c.execute(sql)
        conn.commit()
        sql = """UPDATE jobs SET title = '%s', description = '%s', location_id='%d'  WHERE job_id = '%d '"""\
              % (title, description, int(location_id), int(job_id))
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
        sql = """SELECT location_id, title FROM jobs WHERE job_id = (%d) """ % (int(job_id))
        c.execute(sql)
        for row in c:
            location_id, title = row

        sql = """DELETE FROM jobs WHERE job_id = (%d) """ % (int(job_id))
        c.execute(sql)
        conn.commit()
        sql = """DELETE FROM location WHERE location_id = (%d) """ % (int(location_id))
        c.execute(sql)
        conn.commit()
        c.close()
        conn.close()

    except Exception as e:
        print(str(e))


def apply_job(job_id, user_id):
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()
        sql = """INSERT INTO job_appliers (job_id, user_id) VALUES ('%d', '%d') """ % (job_id, user_id)
        c.execute(sql)
        conn.commit()
        c.close()
        conn.close()

    except Exception as e:
        print(str(e))
