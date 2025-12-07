# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN groupadd -r -g 1000 basicuser && \
    useradd -r -u 1000 -g basicuser basicuser

WORKDIR /app

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY . /app

RUN chown -R basicuser:basicuser /app

USER basicuser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]