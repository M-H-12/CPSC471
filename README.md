
# Group 12 CPSC 471 Final Project

We have built a backend and a small portion of our proposed front end.
Thus, to see both you have to have two different consoles.

##Required prerequisites
- Python
- Django
- django-polymorphic
- NodeJS
- npm
- Bootstrap

If you have any other problems with running the problem you can email Bryce Cayanan at
*bryce.cayanan1@ucalgary.ca*, cause our group might have some software already installed,
that we never realized, that others might not have. 

However, in summary, install all prerequisites needed to run a Bootstrap React and Django app,
with django-polymorphism

##Running backend Django
Open a console, within the same directory that contains this README.md file

Write out "source venv\Scripts\activate" to start your virtual environment. Then, 
write out "python manage.py runserver"

It is here, where you will check if you have all of the prerequisites needed to run our program.
If everything goes well, you will see something like this:

````
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
December 10, 2020 - 23:52:34
Django version 3.1.4, using settings 'CPSC471.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
````

##Running backend Django
Open another console, within the _frontend_ directory on this project
Then, write the line: "npm run start", hit to start up the website. You will see this:

````
> frontend@0.1.0 start C:\Users\bryce\OneDrive\Desktop\CPSC471\frontend
> react-scripts start
````

Then press enter again, and the website will automatically popup.

##Postman requests
When making postman requests, make sure the cookies have session_id within it, because
we use Django's session and authentication software for how we restrict access for different
users
