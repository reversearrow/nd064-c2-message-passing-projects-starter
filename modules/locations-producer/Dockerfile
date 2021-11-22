FROM python:3.9-alpine

WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev build-base
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5005

COPY . .
CMD ["python", "main.py"]