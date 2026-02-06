FROM python:3.12

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY extract.py .

COPY transform.py .

COPY load.py .

CMD ["sh", "-c", "python extract.py && python transform.py && python load.py"]