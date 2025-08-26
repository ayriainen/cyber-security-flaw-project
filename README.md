This is a course project for University of Helsinki Cyber Security Base 2025 demonstrating common security flaws for software. This is a note app for the browser that has 5 flaws from the [OWASP top ten list](https://owasp.org/www-project-top-ten/). The fixes to the flaws are in the files, simply commented out as instructed.

The project uses Python and Django, with the course's TMC exercise files as basis. As per the course project guidelines, it's assumed you know how to get both ready on your computer.

With everything ready, run at root of the project:

```
python3 manage.py runserver
```

and then go to:

```
http://localhost:8000/
```

in your browser.

The manage.py creates a new db.sqlite3 next to db.sql, and if you want to reset the db just delete the db.sqlite3.
