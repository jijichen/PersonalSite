## How to set up

0.  Install the packages needed by this project
	Install django and related python package

	On Ubuntu:
    ```sh
	sudo apt-get install python-dev
	sudo apt-get install libxml2-dev libxslt-dev
	sudo apt-get install python-lxml
	sudo apt-get install python-pil
    ```
        
    ```sh
    pip install django
    pip install django-ckeditor
    pip install pyquery
    pip install django-imagekit
    ```



1. Run the Project
	1. change path to Project/src.
	1. Create database:
		"python manage.py syncdb"
		(no need to enter the admin account which can be imported in 1. 3)
	1. Import initialization data from initialize_data.json
		"python manage.py loaddata initialize_data.json"
	1. Run the server
		"python manage.py runserver"



##About the site

   This is a personal web site for myself to use in future. So I use django's default
 admin interface to manage the data and all visitors can do is to view the site and
 leave comments.
   To log in the admin site the current Username/Password is : "chen" "123456"

   There are 5 parts of content in my site, they are
   ```
   Project
     |___Home				#Home page, using a html to display my CV
     |___Blog				#My blog, managed by using django admin	interface
     |___Readings			#My reading list
     |___Photography		#My photography. Due to time limit, it is linked to another site
     |___Price Compare		#A cross site price parity site for price comparation.
   ```


##Things I wrote

  as you can see in START UP STEPS, this site use some packages which are not written by myself.
Below are what I wrote:

    ```
	Blog
      |-- admin.py
      |-- forms.py
      |-- models.py
      |-- templates
      |   |-- blog_detail.html
      |   `-- blog_list.html
      |-- tests.py
      |-- urls.py
      `-- views.py

    About
	  |-- urls.py
	  `-- views.py

	common
	  |
	  `-- templates
    	  |-- aboutme.html
    	  `-- base.html

    reading
	  |-- admin.py
	  |-- models.py
	  |-- templates
	  |   |-- reading_list.html
	  |   `-- reading_list.html.bak.html
	  |-- urls.py
	  `-- views.py

	price_compare
	  |-- models.py
	  |-- parser					#Parser for item information which took me lot of time
	  |   |-- GetItems.py
	  |   `-- test.py
	  |-- templates
	  |   `-- compare_list.html
	  |-- tests.py
	  |-- urls.py
	  `-- views.py
    ```

#Additinal packages I used

1. Duoshuo comment service.(internet conection needed)
2. django-imagekit	(For image process)
3. Python-PIL	  (For image process)
4. django-ckeditor (rich text editor)
5. django-angular


