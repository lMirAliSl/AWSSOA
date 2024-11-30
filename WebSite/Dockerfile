FROM python:3.11-slim

WORKDIR /WebSite

COPY . /WebSite

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "main.py"]