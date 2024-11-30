FROM python:3.11-slim

WORKDIR /UserService

COPY . /UserService

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001

CMD ["python", "api.py"]