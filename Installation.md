# Installation steps

## 1. Clone repository

- Clone this repository to your local computer.

```
git clone https://github.com/TAGCH/ku-polls.git DirectoryName
```
**NOTED**: ```DirectoryName``` is your desired directory name.

## 2. Create virtual environment and install dependencies

- Create virtual environment.

```
python -m venv env
```

- Change to your newly created virtual environment.

```
. env/bin/activate
```

- Install packages from requirements.txt

```
pip install -r requirements.txt
```

## 3. Run migration

- Run migration.

```
python manage.py migrate
```

## 4. Run tests

- Checking all tests.

```
python manage.py test
```

## 5. Install data from the data fixtures

- Load questions and choice version 1.

```
python manage.py loaddata data/polls-v1.json
```

- Load questions and choice continue version.

```
python manage.py loaddata data/polls.json
```

- Load users data.

```
python manage.py loaddata data/users.json
```