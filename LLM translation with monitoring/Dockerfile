FROM nvidia/cuda:12.6.1-runtime-ubuntu22.04

WORKDIR /app

# Install pip
RUN apt-get update && apt-get install -y python3-pip
RUN pip install --upgrade pip

# Copy only requirements.txt first to cache the installation step
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Now copy the rest of the application code, which will not invalidate the previous cache
COPY . /app

EXPOSE 7860 8000

CMD ["python3", "translator_app.py"]
