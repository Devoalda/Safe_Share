FROM python:3.10

# Install Netcat
RUN apt-get update && \
    apt-get -y install netcat-traditional && \
    apt-get clean

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

RUN chmod a+x start.sh
CMD ["./start.sh"]