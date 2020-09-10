FROM python:3
ENV PYTHONUNBUFFERED 1

RUN mkdir /home/researcher
RUN mkdir /home/researcher/app
WORKDIR /home/researcher

COPY requirements.txt ./
RUN pip install -r ./requirements.txt
COPY ./run.sh ./

ENTRYPOINT [ "/bin/bash", "./run.sh" ]
