FROM python:3.11-slim

WORKDIR /CalculationService

COPY . /CalculationService

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5002

CMD ["python", "api.py"]