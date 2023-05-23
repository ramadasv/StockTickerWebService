# pull the image from docker hub and update it
FROM python:3.10.11-slim
RUN apt-get update -y

# Create a directory for logs
RUN mkdir -p /app/StockTicker/logs

# Create Python Virtual environment and set the path
RUN python -m venv /app/StockTicker/venv
ENV PATH="/app/StockTicker/venv/bin:$PATH"

# Sets the working directory in the container 
WORKDIR /app/StockTicker

# Copies everything to the working directory and Install dependencies
COPY StockTickerRestAPI.py requirements.txt .env /app/StockTicker/
RUN pip install --no-cache-dir -r requirements.txt

# Command to run on container start. Web service runs on Port 5000
EXPOSE 5000
CMD ["python", "-m", "flask", "--app", "StockTickerRestAPI", "run", "--host=0.0.0.0"]