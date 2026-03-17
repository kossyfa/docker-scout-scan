# Workout Tracker API by kossyfa
FROM python:3.9-slim

LABEL org.opencontainers.image.title="workout-tracker-api"
LABEL org.opencontainers.image.description="Personal workout planner with splits and motivation"
LABEL org.opencontainers.image.author="kossyfa"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
