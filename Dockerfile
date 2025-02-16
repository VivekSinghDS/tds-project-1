FROM python:3.12

# Create a user but keep root access
RUN useradd -ms /bin/bash 1000
WORKDIR /home/1000

# Install dependencies
# RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install scikit-learn

RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs
# Switch to root user to avoid permission issues
RUN pip install pandas
USER root

# Ensure /data is writable
# RUN mkdir -p /data && chmod -R 777 /data

EXPOSE 8000
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
