FROM python:3.9.6

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY . .

RUN apt-get update && apt-get install -y wget unzip && \
  wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
  apt install -y ./google-chrome-stable_current_amd64.deb && \
  rm google-chrome-stable_current_amd64.deb && \
  apt-get clean

CMD ["tail", "-f", "/dev/null"]
