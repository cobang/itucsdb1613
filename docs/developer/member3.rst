Parts Implemented by Göksel ÇOBAN
=================================

I implemented post, comment and like entities/relations and related operations.

   .. figure:: ../../static/images/wiki/timeline_er.png
      :scale: 50 %
      :alt: map to buried treasure

      Post table has four attributes: user_id, post_text, post_date and **post_id** which is primary key.

      Comment table has five attributes: user_id, comment_text, comment_date, post_id and **comment_id** which is primary key.

      Likes table has two attributes: **user_id** and **post_id** which are primary keys.

TABLES
------

**Creating Tables**

Post table keeps post id(PK), post text, post date and user id(FK).

.. code-block:: sql

    CREATE TABLE IF NOT EXISTS `cl48-humannet`.`posts` (
        `post_id` INT(11) NOT NULL AUTO_INCREMENT,
        `user_id` INT(11) NOT NULL,
        `post_text` VARCHAR(140) NOT NULL,
        `post_date` DATETIME NOT NULL,
        PRIMARY KEY (`post_id`),
        INDEX `fk_posts_users1_idx` (`user_id` ASC),
        CONSTRAINT `fk_posts_users1`
        FOREIGN KEY (`user_id`)
        REFERENCES `cl48-humannet`.`users` (`user_id`)
        ON DELETE CASCADE
        ON UPDATE NO ACTION)
    DEFAULT CHARACTER SET = utf8;

Comment table keeps comment_id(PK, FK), user_id(FK), comment_text, comment_date and post_id.

.. code-block:: sql

    CREATE TABLE IF NOT EXISTS `cl48-humannet`.`comment` (
        `comment_id` INT(11) NOT NULL AUTO_INCREMENT,
        `comment_text` VARCHAR(140) NOT NULL,
        `comment_date` DATETIME NOT NULL,
        `post_id` INT(11) NOT NULL,
        `user_id` INT(11) NOT NULL,
        PRIMARY KEY (`comment_id`),
        INDEX `fk_comment_posts1_idx` (`post_id` ASC),
        INDEX `fk_comment_users1_idx` (`user_id` ASC),
        CONSTRAINT `fk_comment_posts1`
        FOREIGN KEY (`post_id`)
        REFERENCES `cl48-humannet`.`posts` (`post_id`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
        CONSTRAINT `fk_comment_users1`
        FOREIGN KEY (`user_id`)
        REFERENCES `cl48-humannet`.`users` (`user_id`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION)
    DEFAULT CHARACTER SET = utf8;

Likes table keeps user_id(PK, FK) and post_id(PK, FK).

.. code-block:: sql

    CREATE TABLE IF NOT EXISTS `cl48-humannet`.`likes` (
        `user_id` INT(11) NOT NULL,
        `post_id` INT(11) NOT NULL,
        PRIMARY KEY (`user_id`, `post_id`),
        INDEX `fk_likes_users1_idx` (`user_id` ASC),
        INDEX `fk_likes_posts1_idx` (`post_id` ASC),
        CONSTRAINT `fk_likes_posts1`
        FOREIGN KEY (`post_id`)
        REFERENCES `cl48-humannet`.`posts` (`post_id`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
        CONSTRAINT `fk_likes_users1`
        FOREIGN KEY (`user_id`)
        REFERENCES `cl48-humannet`.`users` (`user_id`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION)
    DEFAULT CHARACTER SET = utf8;

CLASSES
-------

Comment: Holds all data a comment has.

.. code-block:: python

    class Comment:
        def __init__(self, comment_id, comment_text, comment_date, post_id, user_id, user_name=" ", user_surname=" "):
            self.comment_id = comment_id
            self.comment_text = comment_text
            self.comment_date = comment_date
            self.post_id = post_id
            self.user_id = user_id
            self.user_name = user_name
            self.user_surname = user_surname

Comments: Stores comments in a dictionary.

.. code-block:: python

    class Comments:
        def __init__(self,):
            self.comments = {}
            self.key = 0

        def add_comment(self, comment):
            self.key += 1
            self.comments[self.key] = comment

        def delete_comment(self, key):
            del self.comments[key]

        def get_comment(self, key):
            return self.comments[key]

        def get_comments(self):
            return sorted(self.comments.items())

Post: Holds all data a post has.

.. code-block:: python

    class Post:
        def __init__(self, post_id, user, text, date, user_name=" ", like_num=0, likes=Users(), comments=Comments()):
            self.post_id = post_id
            self.user = user
            self.text = text
            self.date = date
            self.user_name = user_name
            self.like_num = like_num
            self.likes = likes
            self.comments = comments

Posts: Stores posts in a dictionary.

.. code-block:: python

    class Posts:
        def __init__(self):
            self.posts = {}
            self.key = 0

        def add_post(self, post):
            self.key += 1
            self.posts[self.key] = post

        def delete_post(self, key):
            del self.posts[key]

        def get_post(self, key):
            return self.posts[key]

        def get_posts(self):
            return sorted(self.posts.items())

*Note:* Some class use "User" class. Documentation of this class can be found in Emre Özdil's parts of developer guide.

FUNCTIONS
---------

posts_get: Takes current user id as input. This function gets post which are shared by current user and followed user
by current user. To get this information the following sql is used. Also, this function call get_likes and
get_post_comments functions to get all information about a post.

.. code-block:: sql

    """SELECT P1.post_id, P1.user_id, post_text,post_date,like_num, name FROM
        (SELECT T1.post_id, user_id, post_text,post_date,like_num FROM (SELECT *  FROM posts INNER JOIN
        (SELECT following_id FROM connections where user_id = %d
        UNION SELECT user_id FROM connections where user_id= %d) AS follow
        ON posts.user_id = follow.following_id) AS T1 LEFT JOIN
        (SELECT post_id, COUNT(*) AS like_num FROM likes GROUP BY post_id) AS T2
        ON T1.post_id = T2.post_id) AS P1 LEFT JOIN (SELECT u.user_id ,(CASE
                          WHEN u.user_type = 3
                              THEN uni.university_name
                          WHEN u.user_type = 2
                              THEN com.company_name
                          WHEN u.user_type = 1
                              THEN CONCAT_WS(' ', ud.user_name, ud.user_surname)
                          ELSE
                              NULL
                        END)AS name
                  FROM users AS u
                  LEFT JOIN user_detail AS ud
                      ON ud.user_id = u.user_id
                  LEFT JOIN university_detail AS uni
                      ON uni.user_id = u.user_id
                  LEFT JOIN company_detail AS com
                      ON com.user_id = u.user_id
                  ) AS P2 ON P1.user_id= P2.user_id;""" % (current_user_id, current_user_id)

post_share: Takes user id, post text and post date as input. It adds new post. So, it adds new tuple to posts table.

.. code-block:: sql

    """INSERT INTO posts(USER_ID, POST_TEXT, POST_DATE) VALUES (%d, '%s', '%s')""" % (user_id, text, date.strftime(f))

post_delete: Takes post id as input. It firstly deletes comments and likes of this post because foreign constraint.
After that, it deletes the comment.

.. code-block:: sql

    """DELETE FROM comment WHERE post_id = (%d) """ % (int(post_id))

    """DELETE FROM likes WHERE post_id = (%d) """ % (int(post_id))

    """DELETE FROM posts WHERE POST_ID = (%d) """ % (int(post_id))

post_update: Takes post id, current user id and action which indicates the operation. According to action, a post is
liked or disliked. A new tuple is added to like table for like operation. A tuple is deleted for dislike operation.

.. code-block:: sql

    """INSERT INTO likes ( user_id, post_id ) VALUES( %d, %d )""" % (current_user_id, int(post_id))

.. code-block:: sql

    """DELETE FROM likes WHERE %d = user_id and %d = post_id""" % (current_user_id, int(post_id))

update_post_text: Takes new text, post id and date as input. It updates a tuple from post table.

.. code-block:: sql

    """UPDATE posts SET post_text = '%s', post_date = '%s'  WHERE post_id = %d """ % (text, date.strftime(f), int(post_id))

update_comment_text: Takes new text, comment id and date as input. It updates a tuple from post table.

.. code-block:: sql

    """UPDATE comment SET comment_text = '%s', comment_date = '%s'  WHERE comment_id = %d """ % (text, date.strftime(f), int(comment_id))

delete_comment: Takes comment id as input and deletes a tuple from comment table.

.. code-block:: sql

    """DELETE FROM comment WHERE comment_id = (%d) """ % (int(comment_id))

post_comment_add: Takes comment_text, post_id, date and user_id as input. It add a new tuple to comment table.

.. code-block:: sql

    """INSERT INTO comment(comment_text, comment_date, post_id, user_id) VALUES ('%s', '%s', '%s', %d)""" % (comment_text, date.strftime(f), int(post_id), user_id)

get_likes: Takes post id as input. It get information of users who liked the post.

.. code-block:: sql

    """SELECT P1.user_id,  P1.user_type, name  FROM
        (SELECT users.user_id, user_type FROM users INNER JOIN
                (SELECT user_id FROM likes WHERE post_id= %d) AS who_like
                ON users.user_id IN (who_like.user_id)) AS P1 LEFT JOIN (SELECT u.user_id ,(CASE
                          WHEN u.user_type = 3
                              THEN uni.university_name
                          WHEN u.user_type = 2
                              THEN com.company_name
                          WHEN u.user_type = 1
                              THEN CONCAT_WS(' ', ud.user_name, ud.user_surname)
                          ELSE
                              NULL
                        END)AS name
                  FROM users AS u
                  LEFT JOIN user_detail AS ud
                      ON ud.user_id = u.user_id
                  LEFT JOIN university_detail AS uni
                      ON uni.user_id = u.user_id
                  LEFT JOIN company_detail AS com
                      ON com.user_id = u.user_id
                  ) AS P2 ON P1.user_id= P2.user_id""" % post_id

get_post_comments: Takes post id as input. It gets comments of corresponding post.

.. code-block:: sql

    """SELECT P1.*, name FROM
        (SELECT comment_id, comment_text, comment_date,
        post_id, users.user_id
        FROM users INNER JOIN
        (SELECT * FROM comment WHERE post_id = %d) AS comments
        ON users.user_id = comments.user_id) AS P1 LEFT JOIN (SELECT u.user_id ,(CASE
                          WHEN u.user_type = 3
                              THEN uni.university_name
                          WHEN u.user_type = 2
                              THEN com.company_name
                          WHEN u.user_type = 1
                              THEN CONCAT_WS(' ', ud.user_name, ud.user_surname)
                          ELSE
                              NULL
                        END)AS name
                  FROM users AS u
                  LEFT JOIN user_detail AS ud
                      ON ud.user_id = u.user_id
                  LEFT JOIN university_detail AS uni
                      ON uni.user_id = u.user_id
                  LEFT JOIN company_detail AS com
                      ON com.user_id = u.user_id
                  ) AS P2 ON P1.user_id= P2.user_id""" % id_post