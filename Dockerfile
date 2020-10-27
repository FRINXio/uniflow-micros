FROM python:3.6.10-buster

# Install unzip
RUN apt-get update \
 && apt-get install unzip

WORKDIR /home/app/

# Download and unpack terraform(unpacks to an executable)
ADD https://releases.hashicorp.com/terraform/0.11.10/terraform_0.11.10_linux_amd64.zip .
RUN unzip terraform_0.11.10_linux_amd64.zip

# Download and unpack terraform-aws-vpc pluigin
ADD https://github.com/terraform-aws-modules/terraform-aws-vpc/archive/v1.46.0.zip .
RUN unzip v1.46.0.zip \
 && mv terraform-aws-vpc-1.46.0 terraform-aws-vpc

# Add terraform executable ot path
ENV PATH="$PATH:/home/app"

WORKDIR /home/app

COPY . .
COPY ./conductor-client ./conductor-client

### Install application setup
WORKDIR /home/app/conductor-client/python
RUN pip3 install setuptools
RUN python3 setup.py install
RUN pip3 install psycopg2
RUN pip3 install marshmallow-dataclass
RUN pip3 install jinja2

WORKDIR /home/app/workers
CMD [ "python3", "main.py" ]
RUN python3 -m unittest uniconfig_worker_test.py
RUN python3 -m unittest netconf_worker_test.py
RUN python3 -m unittest cli_worker_test.py

WORKDIR /home/app/

# This can be run from docker-compose aswell
# RUN ["chmod", "+x", "/home/app/wait_for_it.sh"]
# CMD ["/home/app/wait_for_it.sh", "-t", "180",  "conductor-server:8080", "--", "python", "/home/app/workers/main.py"]