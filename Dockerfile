FROM python:3.6.10-buster

RUN apt-get update

WORKDIR /home/app

RUN groupadd -r frinx && \
    useradd --no-log-init -r -g frinx frinx && \ 
    chown -R frinx:frinx /home/app && \
    mkdir -p /home/frinx && \
    chown -R frinx:frinx /home/frinx

# Copy conductor integration files
COPY ./conductor-client /home/app/conductor-client

# Install dependencies of conductor client
WORKDIR /home/app/conductor-client/python
RUN pip3 install setuptools
RUN python3 setup.py install

# Install dependencies of workers
COPY requirements.txt /home/app/requirements.txt
WORKDIR /home/app
RUN pip3 install -r requirements.txt

# Copy workers and workflows
COPY ./workers /home/app/workers
COPY ./workflows /home/app/workflows

WORKDIR /home/app/workers
RUN python3 -m unittest uniconfig_worker_test.py
RUN python3 -m unittest netconf_worker_test.py
RUN python3 -m unittest cli_worker_test.py

USER frinx

ENTRYPOINT [ "python3", "main.py" ]
