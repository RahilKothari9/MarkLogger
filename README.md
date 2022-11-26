# MarkLogger - A web app that makes it easy to keep track of your marks.
#### Video Demo: https://youtu.be/VeyqFfF8phM
#### Description
## Uses Flask for the backend, sqlite3 for the database and HTML, CSS for the front end.
## Files in the project
1. [README.md](~/README.md)
        An explanation of the project and its specifications.
2. [app.py](~/app.py)
        Contains the majority of the functionality
        Register:
        Allows the user to create an account with a unique username and a password.
        The username and password are stored in a database, the password as a hash.

        Login:
        Asks the user for the username and password and queries the database to check if the username and password are valid and correct.

        Homepage:
        Displays all the tests which have been inputted by the user in the form of a table.
        the table contains a unique test id, the subject, the type, marks obtained, the total marks, the percentage and the date.
        Allows the user to sort the tests by
        a particular subject,
        a particular type,
        ordering them by percentage obtained(ascending or descending)
        and any combination of the above 3.
        Also allows the user to delete a test.

        Configure tests and types:
        Allows the user to add or remove subjects and types, which are stored in a database.
        Only these subjects and types can be used while adding a test.

        Add a Test:
        Allows the user to add a test by entering the relevant information.

        Logout:
        Ends the session and logs the user out.

3.[helpers.py](~/helpers.py)
        Contains two helper functions which are used in app.py
        1. login_required
                Used as a decorator in several other functions in app.py.
                Makes sure that the user is logged in beforing allowing them to access a function.
        2. error
                makes it easier to return an error in case of user error or an unexpected scenario.

4.[marks.db](~/marks.db)
        A database with several tables to keep track of users, tests, subjects and types.
        The users table contains a unique id for each user, his username and his password.(stored as a hash)
        The subjects table contains a unique id for each of the subjects and the subjects name and users unique id as a foreign key.
        The types table contains a unique id for each of the types and the types name and users unique id as a foreign key.
        The tests table contains a primary key id for each test, the subject, the type, the marks obtained, the total marks, the percentage and the date and users unique id as a foreign key.

5.[requirements.txt](~/requirements.txt)
        A text file containing the names of all the files which flask needs to import

6.[templates](~/templates)
        Contains html files for each page.
        Contains layout.html which other files extend from.
        Bootstrap is used as a framework, and the website is responsive.

7.[static](~/static)
        Contains styles.css a css file used to style and modify the webpage.



