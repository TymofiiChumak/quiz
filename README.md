**A simple site for take a quiz.**
-----
**Installation:**

install Django:
```bash
pacman -S python-django  
```

install PostgreSQL:
```bash
pacman -S postgresql
#change user
sudo -u postgres -i
#create data base
createdb quiz_db
```

download:
```bash
git clone https://github.com/TymofiiChumak/quiz.git MyQuiz
cd MyQuiz
```

apply migrations:
```bash
python manage.py migrate quiz
python manage.py makemigrations
```

**Run:**

For run server on port 8000
```bash
python manage.py runserver 8000
```
Now you can visit page
 
[localhost:8000](http://localhost:8000/)



    

