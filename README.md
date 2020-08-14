## REST User Info

**Key Features:**

1. Can store User info like first name, last name, address, street, city, state and zip_code.
2. GET, POST, PATCH, DELETE using a single API endpoint.
3. Use Django's default SQLite as DB

**Tools And Technology Used**

1. Python3
2. Django
3. Django Rest Framework
4. SQLite

**Notes**

* I am asuming that you already installed Python3, Git and Virtual Environment in you system.
 
**Virtual Environment Setup Commands for Linux Machines**
> **`mkdir venvs`**\
> **`pip3 install virtualenv --user`**\
> **`virtualenv -p python3 venvs/test_venv`**\
> **`source venvs/test_venv/bin/activate`**
>

**Project Execution Commands**
> **`git clone git clone https://github.com/tssovi/user-info.git `**\
> **`cd user-info`**\
> **`pip install -r requirements.txt`**\
> **`python manage.py makemigrations`**\
> **`python manage.py migrate`**\
> **`python manage.py runserver`**
> 

**Project Testing Execution Command**
> **`python manage.py test`**
> 

##### Don't want to take above mentioned hassle than simply download the run.sh file and execute that file

**Bash File Execution Command**
> **`bash run.sh`**
> 

**Postman Collection Link To Expose API Endpoints**
> **`https://www.getpostman.com/collections/f686cb07f45ed15aa0a5`**
> 

**N.B:**
- [ ] ***I haven't test this in windows machine. If you face any problem in windows machine then please let me know.*** 