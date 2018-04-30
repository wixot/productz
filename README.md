# ProductZ

Management and tracking software for the inapp and adnetwork's expenses and incomes software for mobile apps and games.


```markdown
this version of project is marked beta and still on development to be stable
```

## Features

* Easy to setup for supported network channels and predefined apps on adnetworks
* Easy to setup for inapp store credentials
* Adnetwork income plots
* Inapp order validation, data storage and tracking

## Roadmap

* New adnetwork and mobile app store channels
* More intensive income and expense management
* Inapp purchase's plots
* Campaign management for adnetwork's
* Inapp campaign module


## Supported Channels
* Google Play
* iTunesConnect
* Facebook
* Chartboost
* UnityAds
* Admob 
* ..and spreads

# Setup

## Airflow Setup

```markdown
export PYTHONPATH=/path/to/your/projects/for/productz:$PYTHONPATH

cp -R dags ~/airflow
airflow initdb
airflow list_dags
airflow list_tasks reporting
```

## Frontend Setup

```markdown
cd frontend
npm install
npm run build
```

## Project Setup

```markdown
configure app/config.py
python products.py
```
