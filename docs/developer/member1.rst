Parts Implemented by Emre ÖZDİL
================================

I implemented user, user details, company details and university entities and related operations.

   .. figure:: images/userEr.png
      :scale: 80 %
      :alt: map to buried treasure
      
      Users table keeps **user_id(PK)**, user_email, user_password, and user_type.
      
      User detail table keeps **user_id(FK)**, user_name, user_surname, phone, and address.
      
      Company detail table keeps **user_id(FK)**, company_name, company_phone, and company_address.
      
      University detail table keeps **user_id(FK)**, university_name, and university_address.

Tables
------

**Creating Tables**

Users table keeps user_id(PK), user_email, user_password, and user_type.

.. code-block:: sql

    CREATE TABLE IF NOT EXISTS `cl48-humannet`.`users` (
      `user_id` INT(11) NOT NULL AUTO_INCREMENT,
      `user_email` VARCHAR(25) NOT NULL,
      `user_password` VARCHAR(16) NOT NULL,
      `user_type` INT(1) NOT NULL,
      PRIMARY KEY (`user_id`))
    DEFAULT CHARACTER SET = utf8;

User detail table keeps user_id(FK), user_name, user_surname, phone, and address.

.. code-block:: sql

    CREATE TABLE IF NOT EXISTS `cl48-humannet`.`user_detail` (
      `user_id` INT(11) NOT NULL,
      `user_name` VARCHAR(20) NOT NULL,
      `user_surname` VARCHAR(20) NULL DEFAULT NULL,
      `phone` VARCHAR(15) NULL DEFAULT NULL,
      `address` VARCHAR(45) NULL DEFAULT NULL,
      INDEX `fk_user_detail_users1_idx` (`user_id` ASC),
      CONSTRAINT `fk_user_detail_users1`
        FOREIGN KEY (`user_id`)
        REFERENCES `cl48-humannet`.`users` (`user_id`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION)
    DEFAULT CHARACTER SET = utf8;

Company detail table keeps user_id(FK), company_name, company_phone, and company_address.

.. code-block:: sql

    CREATE TABLE IF NOT EXISTS `cl48-humannet`.`company_detail` (
      `user_id` INT(11) NOT NULL,
      `company_name` VARCHAR(45) NOT NULL,
      `company_address` VARCHAR(45) NULL DEFAULT NULL,
      `company_phone` VARCHAR(45) NULL DEFAULT NULL,
      INDEX `fk_company_detail_users1_idx` (`user_id` ASC),
      CONSTRAINT `fk_company_detail_users1`
        FOREIGN KEY (`user_id`)
        REFERENCES `cl48-humannet`.`users` (`user_id`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION)
    DEFAULT CHARACTER SET = utf8;

University detail table keeps user_id(FK), university_name, and university_address.

.. code-block:: sql


    CREATE TABLE IF NOT EXISTS `cl48-humannet`.`university_detail` (
      `user_id` INT(11) NOT NULL,
      `university_name` VARCHAR(45) NOT NULL,
      `university_address` VARCHAR(45) NULL DEFAULT NULL,
      INDEX `fk_university_detail_users1_idx` (`user_id` ASC),
      CONSTRAINT `fk_university_detail_users1`
        FOREIGN KEY (`user_id`)
        REFERENCES `cl48-humannet`.`users` (`user_id`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION)
    DEFAULT CHARACTER SET = utf8;
    
    
Classes
-------

User: Holds all data a user has.

.. code-block:: python

    class User:
    def __init__(self, user_id="", user_type="", user_email="", user_password="", 
                  user_name="", user_surname="", user_phone="", user_address=""):
        self.user_id = user_id
        self.user_type = user_type
        self.user_email = user_email
        self.user_password = user_password
        self.user_name = user_name
        self.user_surname = user_surname
        self.user_phone = user_phone
        self.user_address = user_address

        if user_type == 1:
            self.add_user_detail(user_name, user_surname, user_phone, user_address)
        elif user_type == 2:
            self.add_company_detail(user_name, user_phone, user_address)
        elif user_type == 3:
            self.add_university_detail(user_name, user_address)

    def add_user_detail(self, user_name="", user_surname="", user_phone="", 
                        user_address=""):
        self.user_name = user_name
        self.user_surname = user_surname
        self.user_phone = user_phone
        self.user_address = user_address
        print('add user detail')

    def add_company_detail(self, user_name="", user_phone="", user_address=""):
        self.user_name = user_name
        self.user_phone = user_phone
        self.user_address = user_address
        print('add company detail')

    def add_university_detail(self, user_name="", user_address=""):
        self.user_name = user_name
        self.user_address = user_address
        print('add university detail')


Users: Stores users in a dictionary.

.. code-block:: python

    class Users:
    def __init__(self):
        self.users = {}
        self.key = 0

    def add_user(self, user):
        self.key += 1
        # user.key = self.key
        self.users[self.key] = user

    def get_user(self, key):
        return self.users[key]

    def get_users(self):
        return sorted(self.users.items())


Functions
---------

**Profile page function**

.. code-block:: python

      @app.route('/profile/<int:user_id>', methods=['GET', 'POST'])
      def profile_id(user_id):
          if request.method == 'GET':
              if 'user_email' in session:
                  user = user_show(user_id)
                  current_id = int(get_id(session["user_email"]))
                  print(session['user_email'])
                  print(type(user_id))
                  print(type(user.user_id))
                  return render_template('profile.html', user_id=user_id, 
                     user=user, current_id=current_id)
              else:
                  return redirect('../home')

          else:
              if 'logout' in request.form:
                  logout()
              elif 'edit_user' in request.form:
                  user_id = request.form['edit_user']
                  user_name = request.form['name']
                  user_surname = request.form['surname']
                  user_phone = request.form['phone']
                  user_address = request.form['address']
                  print(user_name)
                  print(user_surname)
                  print(user_phone)
                  print(user_address)
                  user_edit(user_id, user_name, user_surname, user_phone, user_address)
              elif 'edit_company' in request.form:
                  user_id = request.form['edit_company']
                  user_name = request.form['name']
                  user_phone = request.form['phone']
                  user_address = request.form['address']
                  user_edit(user_id=user_id, user_name=user_name, 
                     user_phone=user_phone, user_address=user_address)
              elif 'edit_university' in request.form:
                  user_id = request.form['edit_university']
                  user_name = request.form['name']
                  user_address = request.form['address']
                  user_edit(user_id=user_id, user_name=user_name, user_address=user_address)
              elif 'delete_user' in request.form:
                  user_id = request.form['delete_user']
                  user_delete(user_id=user_id)
                  logout()
          return redirect('../profile')
          
**Sign up Function**

.. code-block:: python

    def signup():
        if 'signup' in request.form:
            print("Sign Up")
            user_name = request.form['name']
            user_email = request.form['email']
            print(user_email)
            user_password = request.form['password']
            user_type = request.form['type']
            print(user_type)

            try:
                conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
                c = conn.cursor()
                sql = """INSERT INTO users(user_email, user_password, user_type)
                                       VALUES ('%s', '%s', '%d' )""" % (
                    user_email, user_password, int(user_type))
                c.execute(sql)
                print(sql)
                print(user_name)
                if user_type == '1':
                    print('add user detail')
                    print(user_email)
                    sql = """SELECT user_id FROM users WHERE  user_email = '%s' """ % (
                        user_email)
                    c.execute(sql)
                    for row in c:
                        user_id = row[0]

                    c.execute(sql)
                    sql = """INSERT INTO user_detail(user_name,user_id) 
                              VALUES ('%s', '%d')""" % (
                        user_name, int(user_id))
                    c.execute(sql)
                    print(sql)

                elif user_type == '2':
                    print('add company detail')
                    sql = """SELECT user_id FROM users WHERE  user_email = '%s' """ % (
                        user_email)
                    c.execute(sql)
                    print(sql)
                    for row in c:
                        user_id = row[0]

                    sql = """INSERT INTO company_detail(company_name, user_id) 
                              VALUES ('%s', '%d')""" % (
                        user_name, int(user_id))

                    c.execute(sql)

                elif user_type == '3':
                    print('add university detail')
                    print(user_email)
                    sql = """SELECT user_id FROM users WHERE  user_email = '%s' """ % (
                        user_email)
                    c.execute(sql)
                    for row in c:
                        user_id = row[0]
                    print('insert')
                    sql = """INSERT INTO university_detail(university_name, user_id) 
                              VALUES ('%s', '%d')""" % (
                        user_name, int(user_id))
                    print(sql)
                    c.execute(sql)

                conn.commit()
                c.close()
                conn.close()

            except Exception as e:
                print(str(e))

**Login function**

.. code-block:: python

    def login():
        if 'login' in request.form:
            print("Login")
            user_email = request.form['email']
            user_password = request.form['password']
            print(user_email)
            print(user_password)
            if valid_login(user_email, user_password):
                print('logged in')
                session['user_email'] = request.form['email']
                return redirect(url_for('timeline'))
                
    def valid_login(user_email, user_password):
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                       passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()
        sql = """SELECT * FROM users WHERE user_email='%s' and 
                  user_password='%s'""" % (
                  user_email, user_password)

        c.execute(sql)

        data = c.fetchone()

        if data:
            return True
        else:
            return False
            
**Logout function**

.. code-block:: python

    def logout():
        session.pop('user_email', None)
        print('logout')
        return redirect(url_for('home'))
        
**Get current user id function**

.. code-block:: python  
    
    def get_id(user_email):
      try:
          conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                         passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
          c = conn.cursor()
          sql = """select user_id from users where user_email = '%s'""" % user_email

          c.execute(sql)

          for row in c:
              user_id = row[0]

          c.close()
          conn.close()

          return user_id
      except Exception as e:
          print(str(e))
          
**Show unique profile page function**

.. code-block:: python 

    def user_show(user_id):
        user = User()
        try:
            conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                           passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
            c = conn.cursor()
            sql = """SELECT user_id, user_type, user_email, user_password FROM users 
                     WHERE  user_id = %d """ % (
                int(user_id))

            c.execute(sql)
            print(user_id)
            for row in c:
                user_id, user_type, user_email, user_password = row
                user = User(user_id=user_id, user_type=user_type, 
                  user_email=user_email, user_password=user_password)
                if user_type == 1:
                    sql = """SELECT user_name, user_surname, phone, address
                              FROM user_detail WHERE  user_id = %d """ % (
                        int(user_id))
                    print(sql)

                    c.execute(sql)
                    for row_user in c:
                        user_name, user_surname, phone, address = row_user
                        user.add_user_detail(user_name, user_surname, phone, address)

                elif user_type == 2:
                    sql = """SELECT company_name, company_phone, company_address
                              FROM company_detail WHERE user_id = %d """ % (
                        int(user_id))
                    print(sql)

                    c.execute(sql)
                    for row_user in c:
                        company_name, company_phone, company_address = row_user
                        user.add_company_detail(user_name=company_name,
                           user_phone=company_phone, user_address=company_address)

                elif user_type == 3:
                    sql = """SELECT university_name, university_address
                              FROM university_detail WHERE  user_id = %d """ % (
                        int(user_id))
                    print(sql)

                    c.execute(sql)
                    for row_user in c:
                        university_name, university_address = row_user
                        user.add_user_detail(user_name=university_name, 
                                 user_address=university_address)

            c.close()
            conn.close()

        except Exception as e:
            print(str(e))
        print(user)
        return user
        
**Edit user information function**

.. code-block:: python 

    def user_edit(user_id, user_name="", user_surname="", user_phone="",
                  user_address=""):
        try:
            conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                           passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
            c = conn.cursor()
            sql = """SELECT user_type FROM users WHERE  user_id = %d """ % (
                int(user_id))

            c.execute(sql)
            for row in c:
                user_type = row[0]
                if user_type == 1:
                    f = '%Y-%m-%d'
                    print('update user detail')
                    sql = """UPDATE user_detail SET user_name = '%s', user_surname = '%s',
                                 phone = '%s', address = '%s' WHERE user_id = %d """ % (
                        user_name, user_surname, user_phone, user_address, int(user_id))
                    c.execute(sql)

                elif user_type == 2:
                    print('update company detail')
                    sql = """UPDATE company_detail SET company_name = '%s', 
                           company_phone = '%s', company_address = '%s' 
                           WHERE user_id = %d """ % (
                        user_name, user_phone, user_address, int(user_id))
                    c.execute(sql)

                elif user_type == 3:
                    print('update university detail')
                    sql = """UPDATE university_detail SET university_name = '%s',
                           university_address = '%s' WHERE user_id = %d """ % (
                        user_name, user_address, int(user_id))
                    print(sql)
                    c.execute(sql)

            conn.commit()
            c.close()
            conn.close()

        except Exception as e:
            print(str(e))
            
**Delete user function**

.. code-block:: python 

    def user_delete(user_id):
        try:
            conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                           passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
            c = conn.cursor()
            sql = """DELETE FROM recommended 
                     WHERE following_id = (%d) """ % int(user_id)
            print(sql)
            c.execute(sql)
            sql = """DELETE FROM connections_detail 
                     WHERE user_id = (%d) """ % int(user_id)
            print(sql)
            c.execute(sql)
            sql = """DELETE FROM connections 
                     WHERE following_id = (%d) """ % int(user_id)
            print(sql)
            c.execute(sql)
            sql = """DELETE FROM conversations 
                     WHERE participant_id = (%d) """ % int(user_id)
            print(sql)
            c.execute(sql)
            sql = """DELETE FROM jobs 
                     WHERE user_id = (%d) """ % int(user_id)
            print(sql)
            c.execute(sql)
            sql = """DELETE FROM comment 
                     WHERE user_id = (%d) """ % int(user_id)
            print(sql)
            c.execute(sql)
            sql = """DELETE FROM posts 
                     WHERE user_id = (%d) """ % int(user_id)
            print(sql)
            c.execute(sql)
            sql = """DELETE FROM likes 
                     WHERE user_id = (%d) """ % int(user_id)
            print(sql)
            c.execute(sql)
            sql = """DELETE FROM job_appliers 
                     WHERE user_id = (%d) """ % int(user_id)
            print(sql)
            c.execute(sql)
            sql = """DELETE FROM location 
                     WHERE user_id = (%d) """ % int(user_id)
            print(sql)
            c.execute(sql)
            sql = """DELETE FROM user_detail 
                     WHERE user_id = (%d) """ % (int(user_id))
            print(sql)
            c.execute(sql)
            sql = """DELETE FROM company_detail 
                     WHERE user_id = (%d) """ % (int(user_id))
            print(sql)
            c.execute(sql)
            sql = """DELETE FROM university_detail 
                     WHERE user_id = (%d) """ % (int(user_id))
            print(sql)
            c.execute(sql)
            sql = """DELETE FROM users 
                     WHERE user_id = (%d) """ % int(user_id)
            print(sql)
            c.execute(sql)

            conn.commit()
            c.close()
            conn.close()

        except Exception as e:
            print(str(e))
