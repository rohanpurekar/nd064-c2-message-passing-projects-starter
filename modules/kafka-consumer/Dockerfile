FROM python:3.7-alpine

WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev
COPY requirements.txt requirements.txt
RUN python3 -m pip install --upgrade setuptools
RUN pip install --no-cache-dir  --force-reinstall -Iv grpcio
RUN pip install -r requirements.txt

EXPOSE 5000

COPY . .
CMD ["python", "consumer.py"]