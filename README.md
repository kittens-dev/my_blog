## The simple blog for simple use wroted on Python Django.

### Installation

1. Install Python 3 (version 3.8 recomended)

2. Create Python env:
```bash
python -m venv env
```

3. Activate your env:
```bash
source env/bin/activate
```

4. Install Python modules (from requirements.txt)
```bash
pip install <module_name>
bash

5. Make migrate App:
```bash
python manage.py makemigrations blog
python manage.py migrate
```

6. Run server
```bash
python manage.py runserver
```