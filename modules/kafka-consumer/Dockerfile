FROM python:3.7-slim-buster

WORKDIR .

#RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev g++ postgresql-dev python3-dev libffi-dev && pip3 install --upgrade pip setuptools && pip3 install --no-cache-dir  --force-reinstall -Iv grpcio
COPY requirements.txt requirements.txt
# RUN python -m pip install --upgrade setuptools
# RUN pip install --no-cache-dir  --force-reinstall -Iv grpcio
RUN pip install -r requirements.txt

EXPOSE 5000

COPY . .
CMD ["python", "consumer.py"]