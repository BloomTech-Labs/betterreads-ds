## Readrr Recommendations API
![MIT](https://img.shields.io/packagist/l/doctrine/orm.svg)
![Python 3.6.5](https://img.shields.io/badge/python-3.6.5-blue)
![spacy](https://img.shields.io/github/pipenv/locked/dependency-version/Lambda-School-Labs/betterreads-ds/spacy)
![scikit-learn](https://img.shields.io/github/pipenv/locked/dependency-version/Lambda-School-Labs/betterreads-ds/scikit-learn)
![flask](https://img.shields.io/github/pipenv/locked/dependency-version/Lambda-School-Labs/betterreads-ds/flask)
![gunicorn](https://img.shields.io/github/pipenv/locked/dependency-version/Lambda-School-Labs/betterreads-ds/gunicorn)

- Visit the [Readrr web application](https://www.readrr.app/)
- Primary API [Documention](https://documenter.getpostman.com/view/10879384/SztBbTgd?version=latest)
- Labs 21 Search API [Documentation](https://documenter.getpostman.com/view/10879384/SzYXXz7Z?version=latest)

## DS teams
##### Labs 23
|Developer      | Github | LinkedIn |Portfolio|
|---------------|:------:|:--------:|:---------:|
|Patrick Wolf   |[<img src="https://github.com/favicon.ico" width="15">](https://github.com/patrickjwolf)|[<img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15">](https://www.linkedin.com/in/patrick-wolf-14356b19/)|🤷
|Ryan Zernach   |[<img src="https://github.com/favicon.ico" width="15">](https://github.com/Zernach)|[<img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15">](https://www.linkedin.com/in/zernach/)|[💼](https://ryan.zernach.com/portfolio/)
|Michael Rowland|[<img src="https://github.com/favicon.ico" width="15">](https://github.com/michael-rowland)|[<img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15">](https://www.linkedin.com/in/michaelrowland3/)|[💼](https://www.michaelrow.land/)
|Jose Marquez   |[<img src="https://github.com/favicon.ico" width="15">](https://github.com/jose-marquez89)|[<img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15">](https://www.linkedin.com/in/jose-marquez89/)|[💼](https://www.josemarquez.tech)

##### Labs 21
|Developer      | Github | LinkedIn |Portfolio|
|---------------|:------:|:--------:|:---------:|
|Claudia Chajon   |[<img src="https://github.com/favicon.ico" width="15">](https://github.com/claudiasofiac)|[<img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15">](https://www.linkedin.com/in/claudia-chajon-129ab8197/)|🤷
|Enrique Collado   |[<img src="https://github.com/favicon.ico" width="15">](https://github.com/fwechino)|[<img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15">](https://www.linkedin.com/in/enrique-collado-fernández-b649504b/)|🤷
|Dylan Nason|[<img src="https://github.com/favicon.ico" width="15">](https://github.com/DNason1999)|[<img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15">](https://www.linkedin.com/in/dylan-nason-768001171/)|🤷
|Kumar Veeravel   |[<img src="https://github.com/favicon.ico" width="15">](https://github.com/mvkumar14)|[<img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15">](https://www.linkedin.com/in/kumar-veeravel-b8a70a4a/)|🤷

## Project Overview

 [Deployed Front End](https://www.readrr.app/)

 [Trello Board](https://trello.com/b/pfNUGgG3/betterreads)

 [Product Canvas](https://www.notion.so/betterReads-66b5ba5a4c7e4036ab786e10b8c2de4d)

The aim of this project is to provide a clean, uncluttered user interface that allows a user to track books, in a similar fashion to something like GoodReads. More details can be found in the [product vision document](https://www.notion.so/Vision-Problem-Objectives-bb24ca087420443e8503115552bf4b25) (PVD accessible only to team members)

The core DS role on this project is to provide recommendations. If there are other DS utilties that you would like to add, communicate with Web, UI and iOS in order to get UI design input on the feature and identify the necessary data.

### Tech Stack

Currently, the application uses a simple nearest-neighbors-based search engine which funnels title matches into a system that references a cosine similarity matrix. The matrix is born out of a combination of collaborative and content based recommendation approaches. This method ultimately provides the best recommendations we have encountered to date. Unfortunately, the current data is limited to less than 10k books; in order to prevent empty recommendations where data for a book is non-existent, the hybrid engine falls back to a purely description-based recommendation wherever necessary. This means that there are _two_ recommendation engines working together to provide a seamless experience.

The hybrid engine is an aggregation of cosine similarities from a collaborative filtering method and a content-based one, using descriptions. Alternatively, the content-based system uses a combination of spacy for tokenization, tfidf for vectorization and a scikit-learn nearest-neighbors model to find the closest matches to a book in question.

All of these techniques are served to Web and iOS through a Flask application, with a gunicorn HTTP server, deployed inside of a Docker container to AWS elastic beanstalk.

### Data Sources

-   [10k Books, 6m Ratings](https://github.com/zygmuntz/goodbooks-10k)
-   [Book Crossing Dataset](http://www2.informatik.uni-freiburg.de/~cziegler/BX/) (Mostly used for publishers to populate database)

### Python Notebooks

[Collaborative Filtering](https://github.com/Lambda-School-Labs/betterreads-ds/blob/master/notebooks/Collaborative_Filtering_Model_Process.ipynb)

[Description Based Recommendations](https://github.com/Lambda-School-Labs/betterreads-ds/blob/master/notebooks/Content_Model_Process.ipynb)

[Hybrid Model and Title Search](https://github.com/Lambda-School-Labs/betterreads-ds/blob/master/notebooks/Hybrid_Exploration.ipynb)

### Connecting to the web API

Details on how to connect to the Web API are located at the top of [this](https://www.notion.so/Architecture-Details-21cb8620660946b68e16762429d778c5) document.

### Connecting to the DS API

Currently, the domain for the data science API is [dsapi.readrr.app](https://dsapi.readrr.app)

The account used for the postman collection is the betterreadslabs21@gmail.com account (Sign in using google). See TL or SL for login credentials (you can also get login credentials for AWS, which the api is deployed on).

## Contributing

When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.

Please note we have a [code of conduct](./code_of_conduct.md.md). Please follow it in all your interactions with the project.

### Issue/Bug Request

 **If you are having an issue with the existing project code, please submit a bug report under the following guidelines:**
 - Check first to see if your issue has already been reported.
 - Check to see if the issue has recently been fixed by attempting to reproduce the issue using the latest master branch in the repository.
 - Create a live example of the problem.
 - Submit a detailed bug report including your environment & browser, steps to reproduce the issue, actual and expected outcomes,  where you believe the issue is originating from, and any potential solutions you have considered.

### Feature Requests

We would love to hear from you about new features which would improve this app and further the aims of our project. Please provide as much detail and information as possible to show us why you think your new feature should be implemented.

### Pull Requests

If you have developed a patch, bug fix, or new feature that would improve this app, please submit a pull request. It is best to communicate your ideas with the developers first before investing a great deal of time into a pull request to ensure that it will mesh smoothly with the project.

Remember that this project is licensed under the MIT license, and by submitting a pull request, you agree that your work will be, too.

#### Pull Request Guidelines

- Ensure any install or build dependencies are removed before the end of the layer when doing a build.
- Update the README.md with details of changes to the interface, including new plist variables, exposed ports, useful file locations and container parameters.
- Ensure that your code conforms to our existing code conventions and test coverage.
- Include the relevant issue number, if applicable.
- You may merge the Pull Request in once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.

### Attribution

These contribution guidelines have been adapted from [this good-Contributing.md-template](https://gist.github.com/PurpleBooth/b24679402957c63ec426).

More info on using badges [here](https://github.com/badges/shields)
