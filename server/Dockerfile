FROM python:3.12-bookworm

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY src /app/

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=base.settings

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
