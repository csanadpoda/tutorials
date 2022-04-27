FROM python:3.8-slim

WORKDIR /app
COPY . .

# Install Python dependencies.
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python load_model.py

ENV PORT 5000

# to be equal to the cores available.
CMD exec gunicorn --bind :$PORT --workers 1 --log-level debug --timeout 25000 --threads 1 app:app
