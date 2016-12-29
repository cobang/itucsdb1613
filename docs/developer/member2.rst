Parts Implemented by Merve ECEVİT
=================================

Tables
------

Jobs, location and job appliers tables are implemented.

First Table: Jobs
^^^^^^^^^^^^^^^^^

Job has the following attributes.

* Job ID
* User ID
* Location ID
* Title
* Description

User ID takes the current User ID.

.. code-block:: sql

    CREATE TABLE IF NOT EXISTS `cl48-humannet`.`jobs` (
    `job_id` INT(11) NOT NULL AUTO_INCREMENT,
    `user_id` INT(11) NOT NULL,
    `location_id` INT(11) NOT NULL,
    `title` VARCHAR(30) NOT NULL,
    `description` VARCHAR(140) NOT NULL,
    PRIMARY KEY (`job_id`),
    INDEX `fk_jobs_location1_idx` (`location_id` ASC),
    INDEX `fk_jobs_users1_idx` (`user_id` ASC),
    CONSTRAINT `fk_jobs_location1`
        FOREIGN KEY (`location_id`)
        REFERENCES `cl48-humannet`.`location` (`location_id`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
    CONSTRAINT `fk_jobs_users1`
        FOREIGN KEY (`user_id`)
        REFERENCES `cl48-humannet`.`users` (`user_id`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION)


Second Table: Location
^^^^^^^^^^^^^^^^^^^^^^

Location has the following attributes.

* Location ID
* Location State
* Location Country
* Location_Zipcode
* User ID

User ID is equal to the ID of the job owner.

.. code-block:: sql

    CREATE TABLE IF NOT EXISTS `cl48-humannet`.`location` (
    `location_id` INT(11) NOT NULL AUTO_INCREMENT,
    `location_state` VARCHAR(45) NOT NULL,
    `location_country` VARCHAR(45) NOT NULL,
    `location_zipcode` VARCHAR(45) NULL DEFAULT NULL,
    `user_id` INT(11) NOT NULL,
    PRIMARY KEY (`location_id`),
    INDEX `fk_location_users1_idx` (`user_id` ASC),
    CONSTRAINT `fk_location_users1`
        FOREIGN KEY (`user_id`)
        REFERENCES `cl48-humannet`.`users` (`user_id`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION)

Third Table: Job Appliers
^^^^^^^^^^^^^^^^^^^^^^^^^

Job Appliers has the following attributes.

* Job ID
* User ID

User ID is equal to the ID of the applier.

.. code-block:: sql

    CREATE TABLE IF NOT EXISTS `cl48-humannet`.`job_appliers` (
    `job_id` INT(11) NULL,
    `user_id` INT(11) NULL,
    INDEX `fk_job_appliers_jobs1_idx` (`job_id` ASC),
    INDEX `fk_job_appliers_users1_idx` (`user_id` ASC),
    PRIMARY KEY (`job_id`, `user_id`),
    CONSTRAINT `fk_job_appliers_jobs1`
        FOREIGN KEY (`job_id`)
        REFERENCES `cl48-humannet`.`jobs` (`job_id`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
    CONSTRAINT `fk_job_appliers_users1`
        FOREIGN KEY (`user_id`)
        REFERENCES `cl48-humannet`.`users` (`user_id`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION)

Software Design
---------------
Python classes are implemented for add-delete-update-select operations.

**server.py:**

- Following code gets list of jobs which are in database.
.. code-block:: python

        @app.route('/jobs', methods=['GET', 'POST'])
        def jobs():
        jobs_archive = job_share()

- If the method is GET, this function returns the 'jobs.html' with list of jobs and current user's ID.

.. code-block:: python

    if request.method == 'GET':
        if 'user_email' in session:
            print(session['user_email'])
            current_email = session['user_email']
            current_user_id = get_id(current_email)
            return render_template('jobs.html', jobs=jobs_archive, id=current_user_id)
        else:
            return redirect(url_for('home'))

- If the method is POST, needed information will be taken from 'jobs.html' and wanted operation will be performed.

.. code-block:: python

       else:
        current_email = session['user_email']
        current_user_id = get_id(current_email)
        if 'logout' in request.form:
            logout()
        elif 'addJob' in request.form:
            title = request.form['title']
            description = request.form['description']
            user_id = current_user_id
            location = request.form['location']
            job_add(title, description, user_id, location)
        elif 'editJob' in request.form:
            job_id = request.form['editJob']
            title = request.form['title']
            description = request.form['description']
            location = request.form['location']
            job_edit(job_id, title, description, location)
        elif 'deleteJob' in request.form:
            job_id = request.form['deleteJob']
            job_delete(job_id)
        elif 'applyJob' in request.form:
            job_id = int(request.form['applyJob'])
            user_id = current_user_id
            apply_job(job_id, user_id)

       return redirect('jobs')


Database Operations
-------------------

Functions
^^^^^^^^^

**Add Job**:

- This function takes the job object from jobs class by html form.

.. code-block:: sql

    """INSERT INTO location(location_state, location_country, location_zipcode, user_id)
                         VALUES     ('%s', '%s','%s','%d') """ % (location, '', '', user_id)

    """SELECT location_id,location_state FROM location WHERE location_state= ('%s') """ % location
        for row in c:
            location_id, location_state = row

    """INSERT INTO jobs(user_id, location_id, title, description)
                               VALUES ('%d', '%d' , '%s', '%s' )""" % (int(user_id),int(location_id), title, description)


- Queries add job's information to jobs and location tables.

**Update Job:**

- This function takes job's new information from html in order to update.

.. code-block:: sql

    """SELECT location_id, job_id FROM jobs WHERE job_id = (%d) """ % int(job_id)
        for row in c:
            location_id, job_id = row
    """UPDATE location SET  location_state = '%s'  WHERE location_id = '%d' """ % (location, int(location_id))
    """UPDATE jobs SET title = '%s', description = '%s', location_id='%d'  WHERE job_id = '%d '"""\
              % (title, description, int(location_id), int(job_id))

- Queries update the related rows in the jobs and location tables.

**Delete Job**:

- This function takes job id from html in order to delete it.

.. code-block:: sql

     """SELECT location_id, title FROM jobs WHERE job_id = (%d) """ % (int(job_id))
        for row in c:
            location_id, title = row
        """DELETE FROM job_appliers WHERE job_id = (%d) """ % (int(job_id))
        """DELETE FROM jobs WHERE job_id = (%d) """ % (int(job_id))
        """DELETE FROM location WHERE location_id = (%d) """ % (int(location_id))

- Queries delete job's information from jobs and location tables.

**Get Job**

- This function gets job from database and adds to Job list.
- Also function gets user ID from job appliers table using job ID and takes user's name using applier_name function.

.. code-block:: sql

     """SELECT * FROM jobs"""
        for row in c:
            job_id, user_id, location_id, title, description = row
            job = Job(job_id=job_id, user_id=user_id, location_id=location_id, title=title, description=description
                      )
            """SELECT user_id FROM job_appliers WHERE job_id= (%d) """ % job_id
            for row2 in d:
                user_name = applier_name(row2[0])
                job.add_appliers((row2[0], user_name))
                print(row2[0])
            archive.add_job(job=job)

**Apply Job**

- This function adds applier to job applier table by using current user ID and job ID .

.. code-block:: sql

    """INSERT INTO job_appliers (job_id, user_id) VALUES ('%d', '%d') """ % (job_id, user_id)

**Applier Name**

- This function gets user's name using user type. User's information should be selected from different tables according to the type of user.

.. code-block:: sql

     """SELECT user_type FROM users WHERE user_id = %d""" % user_id
        for row in c:
            user_type = row[0]

        if user_type == 1:
            sql = """SELECT user_name, user_surname FROM user_detail WHERE user_id = %d""" % user_id
            for row in c:
                user_name, user_surname = row
                user_name = user_name + " " + user_surname

        elif user_type == 2:
            sql = """SELECT company_name FROM company_detail WHERE user_id = %d""" % user_id
            for row in c:
                company_name = row[0]
                user_name = company_name

        elif user_type == 3:
            sql = """SELECT university_name FROM university_detail WHERE user_id = %d""" % user_id
            for row in c:
                university_name = row[0]
                user_name = university_name




