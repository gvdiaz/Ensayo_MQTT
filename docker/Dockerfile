# Fuente: https://stackoverflow.com/questions/58300046/how-to-make-lightweight-docker-image-for-python-app-with-pipenv
# 
FROM python:3.10 as builder
RUN pip install pipenv
COPY ./piplock_creator/Pipfile* .
WORKDIR /
# The presence of a .venv folder triggers pipenv to use it by default
RUN mkdir /.venv
RUN pipenv install --deploy

FROM python:3.10-slim
COPY --from=builder /.venv /.venv
# Activate virtualenv!
ENV PATH="/.venv/bin:$PATH"
WORKDIR /myapp
COPY ./proposal/meteo_mqtt_bridge/* .
# CMD ["python3", "app.py"]