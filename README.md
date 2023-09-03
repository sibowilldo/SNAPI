# Smart Nutrition API powered by AI
## About
The Smart Nutrition API (S.N.A.P.I) is a versatile RESTful API Powered by Artificial Intelligence that can been consumed
and used by any application that supports JSON-RPC protocol such as Mobile Applications, JavaScript Application such as
browser Extensions, for users who are conscious about the foods their consume, whether they are following a meal plan
provide by a Nutrition specialist due to health complications, or they are trying to change their lifestyle by watching
or keeping track of their daily macros.

SNAPI is trained to recognize different kinds of foods consumed by humans and works by allowing Applications to feed it
various kinds of raw data such images, voice prompts and text prompts (constrained to human food), depending on the type
of information given, SNAPI then uses either image processing to analyze the image and categories the type of food
contained in the image (e.g Banana). It then takes that data and compose a phrase such as “Nutritional Value in a Banana”, to
which the phrase is then posed to ChatGPT API, and receives a response that is further analyzed and returned to the
consumer/client of the API as a JSON response.

## Project Setup
Under the hood, SNAPI uses FastAPI to handle requests
### Requirements (Windows 10 or Later)
- [Visual Studio Code](https://code.visualstudio.com/download) OR [PyCharm Community Edition](https://www.jetbrains.com/pycharm/download/?section=windows)
- [Python 10](https://www.python.org/downloads/release/python-31013/)
- [Postgres 14](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
- [pgAdmin](https://www.pgadmin.org/download/pgadmin-4-windows/)
- [Postman](https://www.postman.com/downloads/)

### FastAPI Setup
```bash 
pip install fastapi
```

You will also need Uvicorn as an ASGI server

```bash
pip install "uvicorn[standard]"
```

To run the project type

```bash
uvicorn main:app --reload
```

## Roadmap
The future of SNAPI will be trained to allow it to accept request in various formats such as voice prompts and text prompts (constrained to human food),
depending on the type of information given, SNAPI will then use Natural Language Processing (NLP) to process Voice and Text (e.g “How many
calories are in this Banana”). It then takes that data and compose a phrase such as “Nutritional Value in a Banana”, to
which the phrase is then posed to ChatGPT API, and receives a response that is further analyzed and returned to the
consumer/client of the API as either JSON response or voice output using NLP.
