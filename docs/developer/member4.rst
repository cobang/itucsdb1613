Parts Implemented by Kaan ATUKALP
================================

**Messages Table:**
  * Message ID (Primary Key)
  * Content
  * Message Date & Time
  * Is Liked
  
	
*SQL:*

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS `cl48-humannet`.`messages` (
  	`message_id` INT(11) NOT NULL AUTO_INCREMENT,
  	`content` VARCHAR(140) NOT NULL,
  	`message_datetime` DATETIME NOT NULL,
  	`is_liked` INT(11) NOT NULL,
  	PRIMARY KEY (`message_id`));
	
Keeps the message id, the message text, date & time information and whether it is liked or not.


**Conversations Table:**
	* Message ID (Primary Key, Foreign Key)
	* In/Out (Primary Key)
	* Participant ID (Foreign Key)
	* User ID
	

*SQL:*
	
.. code-block:: sql

	CREATE TABLE IF NOT EXISTS `cl48-humannet`.`conversations` (
  	`in_out` INT(11) NOT NULL,
  	`message_id` INT(11) NOT NULL,
  	`participant_id` INT(11) NOT NULL,
  	`user_id` INT(11) NOT NULL,
  	PRIMARY KEY (`in_out`, `message_id`),
  	INDEX `fk_conversations_messages_idx` (`message_id` ASC),
  	INDEX `fk_conversations_users1_idx` (`participant_id` ASC),
  	CONSTRAINT `fk_conversations_messages`
    	FOREIGN KEY (`message_id`)
    	REFERENCES `cl48-humannet`.`messages` (`message_id`)
    	ON DELETE NO ACTION
    	ON UPDATE NO ACTION,
  	CONSTRAINT `fk_conversations_users1`
    	FOREIGN KEY (`participant_id`)
    	REFERENCES `cl48-humannet`.`users` (`user_id`)
    	ON DELETE NO ACTION
    	ON UPDATE NO ACTION);

2 rows are created in conversations table for each row insertion in messages table. That way, a user can still view his/her conversation if the participant has deleted his/her conversation with the user. This table keeps the message ID, user ID, partcipant ID and the direction of the message (from user to participant OR from participant to user).


================================

**Classes:**

*Message:*
Holds all data a message has.

.. code-block:: python

	class Message:
    def __init__(self, sender, receiver, content, datetime, is_liked=0, msg_id=0):
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.datetime = datetime
        self.is_liked = is_liked  # Integer value, from sql (0 or 1)
        self.msg_id = msg_id
				


*Chat:*
Used to hold all messages with the same participant.

.. code-block:: python

	class Chat:
    def __init__(self):
        self.messages = {}
        self.key = 0
        self.name = ''
        self.surname = ''

    def __getitem__(self, item):
        return self.messages[item]

    def add(self, message):
        self.key += 1
        # message.key = self.key
        self.messages[self.key] = message

    def delete(self, index):
        del self.messages[index]

    def get_last(self):
        if self.key == 0:
            return 0
        return self.messages[self.key]

    def get_list(self):
        return sorted(self.messages.items())

    def is_empty(self):
        return self.key == 0
				
*Inbox:*
Used to keep all chats in a single class.

.. code-block:: python

	class Inbox:
    def __init__(self):
        self.chats = []

    def add(self, chat, participant):
        if len(chat.messages) != 0:
            self.chats.append((chat, participant))
						

================================

**Functions:**

*get_inbox:*
Executes the SQL query below and handles the data by using all 3 Python classes. Takes the current user's ID as input.

.. code-block:: sql

	SELECT c.user_id, c.participant_id,
                        c.in_out, m.content, m.message_datetime,
                        m.message_id, m.is_liked,
                        (CASE
                             WHEN u.user_type = 3
                                THEN uni.university_name
                             WHEN u.user_type = 2
                                THEN com.company_name
                             WHEN u.user_type = 1
                                THEN CONCAT_WS(' ', ud.user_name, ud.user_surname)
                             ELSE
                                NULL
                        END) AS name

                 FROM messages AS m
                 INNER JOIN conversations AS c
                    ON c.message_id = m.message_id
                 INNER JOIN users AS u
                    ON u.user_id = c.participant_id

                 LEFT JOIN user_detail AS ud
                    ON ud.user_id = c.participant_id
                 LEFT JOIN university_detail AS uni
                    ON uni.user_id = c.participant_id
                 LEFT JOIN company_detail AS com
                    ON com.user_id = c.participant_id

                 WHERE c.user_id = %d
                 ORDER BY c.participant_id;


*send_message:*
Puts the message and the conversations into their corresponding tables. Takes sender ID, receiver ID, message content and message date & time as input. It executes the 3 SQL queries given below.

.. code-block:: python
	
	"""INSERT INTO messages(content, message_datetime, is_liked)
     		VALUES('%s', '%s', 0);""" % (content, date.strftime(f))
	"""INSERT INTO conversations(user_id, participant_id, in_out, message_id)
     	SELECT %d, %d, %d, MAX(message_id)
     		FROM messages;""" % (user_id, participant_id, 0)
	"""INSERT INTO conversations(user_id, participant_id, in_out, message_id)
     	SELECT %d, %d, %d, MAX(message_id)
     		FROM messages;""" % (participant_id, user_id, 1)
					 

*delete_conversation:*
Deletes all rows in conversations table for the given user and participant IDs. Takes user ID and participant ID as input.

.. code-block:: python

	"""DELETE FROM conversations
     		WHERE (user_id = %d)
      		AND (participant_id = %d);""" % (user_id, participant_id)
			

*like_message:*
Likes the message with the message ID given as input.

.. code-block:: sql

	UPDATE messages
  		SET is_liked = 1
      WHERE message_id = %d;


*unlike_message:*
Unikes the message with the message ID given as input.

.. code-block:: sql

	UPDATE messages
			SET is_liked = 0
			WHERE message_id = %d;


*delete_message:*
Deletes the messages and its referencing row in conversations table. Takes message ID as input.

.. code-block:: sql

	DELETE FROM conversations
         WHERE message_id = %d;
	DELETE FROM messages
         WHERE message_id = %d;


*get_name:*
Gets the name and surname (if it exists) of the given user ID. This function is used for the parametric route send_single_message.

.. code-block:: sql

	SELECT (CASE
                          WHEN u.user_type = 3
                              THEN uni.university_name
                          WHEN u.user_type = 2
                              THEN com.company_name
                          WHEN u.user_type = 1
                              THEN CONCAT_WS(' ', ud.user_name, ud.user_surname)
                          ELSE
                              NULL
                        END) AS name
                  FROM users AS u
                  LEFT JOIN user_detail AS ud
                      ON ud.user_id = u.user_id
                  LEFT JOIN university_detail AS uni
                      ON uni.user_id = u.user_id
                  LEFT JOIN company_detail AS com
                      ON com.user_id = u.user_id
                  WHERE u.user_id = %d;
