Parts Implemented by Güneş Yurdakul
================================



Tables
-----------------


**Connections Table:**
  * User ID (Primary Key)
  * Following ID (Primary Key, Foreign Key)
  * Added to Favorites
  * Connection Date


*SQL:*

.. code-block:: sql

    DROP TABLE IF EXISTS `cl48-humannet`.`connections` ;
    CREATE TABLE IF NOT EXISTS `cl48-humannet`.`connections` (
      `user_id` INT(11) NOT NULL,
      `following_id` INT(11) NOT NULL,
      `added_to_favorites` INT(11) NOT NULL DEFAULT '0',
      `connection_date` DATETIME NOT NULL,
      PRIMARY KEY (`user_id`, `following_id`),
      INDEX `fk_connections_users1_idx` (`following_id` ASC),
      CONSTRAINT `fk_connections_users1`
        FOREIGN KEY (`following_id`)
        REFERENCES `cl48-humannet`.`users` (`user_id`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION)
    DEFAULT CHARACTER SET = utf8;
                    """



**Recommended Table:**
	* Following ID (Primary Key, Foreign Key)
	* User ID (Primary Key)


*SQL:*

.. code-block:: sql

    DROP TABLE IF EXISTS `cl48-humannet`.`recommended` ;
    CREATE TABLE IF NOT EXISTS `cl48-humannet`.`recommended` (
      `following_id` INT(11) NOT NULL,
      `user_id` INT(11) NOT NULL,
      PRIMARY KEY (`following_id`, `user_id`),
      INDEX `fk_recomended_users1_idx` (`following_id` ASC),
      CONSTRAINT `fk_recomended_users1`
        FOREIGN KEY (`following_id`)
        REFERENCES `cl48-humannet`.`users` (`user_id`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION)
    DEFAULT CHARACTER SET = utf8;"""


**Connections Detail:**
  * User ID (Primary Key)
  * Number of Connections

*SQL:*

.. code-block:: sql

        DROP TABLE IF EXISTS `cl48-humannet`.`connections_detail` ;
    CREATE TABLE IF NOT EXISTS `cl48-humannet`.`connections_detail` (
      `user_id` INT(11) NOT NULL,
      `num_of_connections` INT(11) NOT NULL DEFAULT '0',
      PRIMARY KEY (`user_id`),
      INDEX `fk_connections_detail_users1_idx` (`user_id` ASC),
      CONSTRAINT `fk_connections_detail_users1`
        FOREIGN KEY (`user_id`)
        REFERENCES `cl48-humannet`.`users` (`user_id`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION)
    DEFAULT CHARACTER SET = utf8;
            """


================================

Classes
-----------------

*Connection:*

Holds all data of a connection, which are used both for interface and database operations.

.. code-block:: python

    class Connection:
        def __init__(self, user_id, following_id, fav, date):
            self.user = user_id
            self.following = following_id
            self.date = date
            self.added_to_favorites = fav
            self.userd = user_show(self.following)
            self.num = 0
            self.conList = self.get_List()

        def get_name(self):
            u_name = ""
            if self.userd.user_type==1:
                if self.userd.user_surname is None:
                    surname=""
                else:
                    surname = self.userd.user_surname
                u_name = self.userd.user_name+ " " + surname
            else:
                u_name=self.userd.user_name
            return u_name

        def get_detail(self):
            return self.userd.user_address


        def get_num_of_connections(self):

            conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                                       passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
            c = conn.cursor()
            sql = """SELECT num_of_connections,user_id FROM connections_detail WHERE user_id = (%d)""" % (int(self.following))
            c.execute(sql)
            for row in c:
                numC, user_id = row
            c.close()
            conn.close()
            print("num")
            return numC

        def get_email(self):
            return self.userd.user_email

        def get_List(self):
            user_list = Users()
            try:
                conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                                       passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
                c = conn.cursor()
                print("followingicfor")

                sql = """SELECT users.user_id, users.user_type FROM connections JOIN users WHERE connections.user_id = (%d) AND connections.following_id=users.user_id"""% (int(self.following))
                c.execute(sql)
                for row in c:
                    user_id, user_type = row
                    user = User(user_id=user_id, user_type=user_type, user_name=user_show(user_id).user_name)
                    user_list.add_user(user=user)
                    self.num += 1
                    print(user.user_name)
                    print("liste döngüsü")
                c.close()
                conn.close()
                if user_list.key == 0:
                    user = User(user_id=0, user_type=0, user_name="user does not follow anyone")
                    user_list.add_user(user=user)
            except Exception as e:
                print(str(e))

            return user_list.get_users()

*Connections:*

Connections class includes connections list and methods for that list including database operations.

.. code-block:: python

    class Connections:
        def __init__(self):
            self.connections = {}
            self.counter = 0

        def add_connection(self, connection):
            self.counter += 1
            self.connections[self.counter] = connection

        def delete_connection(self, counter):
            del self.connections[counter]
            self.counter -= 1

        def get_connection(self, counter):
            return self.connections[counter]

        def get_connections(self):
            return self.connections.items()

        def add_forhtml(self,id):
            conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                                   passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
            c = conn.cursor()

            sql = """SELECT following_id, user_id FROM connections WHERE user_id = (%d)""" % (int(id))
            c.execute(sql)
            for row in c:
                following_id, user_id =row
                connection_new = Connection(id, following_id=user_id, fav=0, date=0)
                self.add_connection(connection_new)
            c.close()
            conn.close()
            return self.connections.items()

*Recommendations:*

Recommendations class includes recommended connections list and methods for that list including database operations.

.. code-block:: python

    class Recommendations:
        def __init__(self):
            self.recommendations = {}
            self.key = 0
            self.get=0

        def add_recommendation(self, connection):
            self.key += 1
            self.recommendations[self.key] = connection

        def delete_recommendation(self, key):
            print(key)
            del self.recommendations[key]
            self.key -= 1

        def delet_byid(self, id):
            for c in self.recommendations:
                if id == self.get_recommendation(c).following:
                    self.delete_recommendation(c)

        def is_item(self, id):
            for c in self.recommendations:
                if id == self.get_recommendation(c).following:
                    return 0
            return 1
        def get_recommendation(self, key):
            return self.recommendations[key]

        def get_recommendations(self):
            return self.recommendations.items()



================================

Functions
-----------------

*Adding a connection to connections table:*

INSERT INTO query for new connection. This function is called whenever a user follows any other user and also recommendation
remove function is also called, so that the user will be listed only on the added connections page.

.. code-block:: python

     def connection_add(u_id, fol_id, time):
        try:
            conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                                   passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
            f = '%Y-%m-%d %H:%M:%S'
            c = conn.cursor()
            sql = """INSERT INTO connections(user_id,following_id,connection_date)
                                  VALUES (%d, '%d', '%s' )""" % (u_id, fol_id, time.strftime(f))
            c.execute(sql)
            conn.commit()
            c.close()
            conn.close()
        except Exception as e:
            print(str(e))


*Removing a connection from connections list:*

DELETE query for deleting a row from connections table.
This function is called whenever a user unfollows any of their existing connections. After this function add
recommendation_add function is also called, so that the user will be listed on the recommended page.

.. code-block:: python

    def connection_remove(u_id, fol_id):
        try:
            conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                                   passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
            c = conn.cursor()
            print(fol_id)
            sql = """DELETE FROM connections WHERE user_id = (%d) AND  following_id = (%d)""" % (int(u_id), int(fol_id))
            c.execute(sql)
            conn.commit()
            c.close()
            conn.close()
            print("afterdelete")

        except Exception as e:
            print(str(e))


*Adding a recommendation to recommended table:*

INSERT INTO query for new recommendation.
This function is called while creating recommended users for a newly signed up user or after unfollow operation.

.. code-block:: python

    def recommendation_add(u_id, fol_id):
        try:
            print("add to rec table")
            conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                                   passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
            c = conn.cursor()
            sql = """INSERT INTO recommended(following_id,user_id)
                                  VALUES (%d, '%d' )""" % (fol_id,u_id)
            c.execute(sql)
            conn.commit()
            c.close()
            conn.close()
        except Exception as e:
            print(str(e))


*Removing a recommendation from connections list:*

DELETE query for deleting a row from recommended table.
This function is called when the logged in user follows some user.

.. code-block:: python

    def recommendation_remove(u_id, fol_id):
        try:
            conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                                   passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
            c = conn.cursor()
            print(fol_id)
            sql = """DELETE FROM recommended WHERE user_id = (%d) AND  following_id = (%d)""" % (int(u_id), int(fol_id))
            c.execute(sql)
            conn.commit()
            c.close()
            conn.close()
            print("afterdelete")

        except Exception as e:
            print(str(e))


*Updating a connection as favorite users:*

Connection table's add_to_favorites column is updated, if logged in user adds a followed user as favorite users.

.. code-block:: python

    def add_to_favorites (u_id, fol_id):
        try:
            conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                                   passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
            c = conn.cursor()

            sql = """UPDATE connections
                      SET added_to_favorites = 1
                      WHERE user_id = (%d) AND  following_id = (%d)""" % (int(u_id), int(fol_id))
            c.execute(sql)

            conn.commit()
            c.close()
            conn.close()

        except Exception as e:
            print(str(e))



*Removing a user from favorites:*

Connection table's add_to_favorites column is updated, if logged in user removes a followed user from favorite users.


.. code-block:: python

    def remove_from_favorites (u_id, fol_id):
        try:
            conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                                   passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
            c = conn.cursor()

            sql = """UPDATE connections
                      SET added_to_favorites = 0
                      WHERE user_id = (%d) AND  following_id = (%d)""" % (int(u_id), int(fol_id))
            c.execute(sql)

            conn.commit()
            c.close()
            conn.close()

        except Exception as e:
            print(str(e))



*Adding connection detail:*

A row is inserted into connections detail table, if the logged in user follows any user.

.. code-block:: python

    def conDetail_add(u_id):

            try:
                conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                                       passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
                c = conn.cursor()

                sql = """SELECT COUNT(*), user_id FROM connections WHERE user_id = (%d)""" % (int(u_id))
                c.execute(sql)
                for row in c:
                    number, user_id = row

                sql = """SELECT COUNT(*),user_id FROM connections_detail WHERE user_id = (%d)""" % (int(u_id))
                c.execute(sql)
                for row in c:
                    is_there, user_id = row
                print("isthere")
                print(is_there)

                if is_there == 0:
                    sql = """INSERT INTO connections_detail(user_id,num_of_connections)
                                          VALUES (%d, %d )""" % (int(u_id), int(number))
                    c.execute(sql)
                    conn.commit()
                    print(number)
                    print("if 0")
                else:
                    sql = """UPDATE connections_detail SET num_of_connections = (%d) WHERE user_id = (%d)""" % (int(number), int(u_id))
                    c.execute(sql)
                    conn.commit()
                    print("else")
                c.close()
                conn.close()
            except Exception as e:
                print(str(e))


*Updating connection detail:*

A row of connections detail is updated when  new follow operation is performed.

.. code-block:: python

    def conDetail_decrease(u_id):

            try:
                conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                                       passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
                c = conn.cursor()
                sql = """UPDATE connections_detail SET num_of_connections = num_of_connections - 1 WHERE user_id = (%d)""" % (int(u_id))
                c.execute(sql)
                conn.commit()
                c.close()
                conn.close()
            except Exception as e:
                print(str(e))
