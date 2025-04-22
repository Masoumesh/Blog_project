FROM python:3.12.8-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . /app

# Run Django’s development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]