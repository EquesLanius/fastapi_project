# FastAPI pet project
API for storing your film viewing history - uViews

## Technologies used
* FastAPI: The web framework for building APIs with Python
* PostgreSQL: A powerful, open source object-relational database
* Redis: The world's fastest in-memory database, provides cloud and on-prem solutions for caching

## Short description
* The Film Tracking API allows users to log and track their film-watching habits.
* Users can register personal account.
* Each user can track an self film-watching history.
* Every time a user watches a film, they can log it into the API, which records the date watched.
* Users can get a history of their views with details for each view.

## Catalog management
Initially, the application catalog does not contain information about existing films.
If the catalog does not contain the film the user needs,
the application accesses open databases and saves it to its own database.
Additionaly for the superuser, the application provides the ability to manage catalog.