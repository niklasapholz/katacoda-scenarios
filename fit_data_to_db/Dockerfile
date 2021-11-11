FROM python:3.9-buster

WORKDIR /code

# copy the requirements
COPY requirements.txt .

# install the requirements
RUN pip install -r requirements.txt

# copy our code
COPY . .

# start our app
CMD ["python", "./our_app.py"]