###########
# BUILDER #
###########

# Pull official base image
FROM python:3.11.4-slim-buster as builder

# Set work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

# Lint
#RUN pip install --upgrade pip
#RUN pip install flake8==6.0.0
COPY . /usr/src/app/
#RUN flake8 --ignore=E501,F401 .

# Install python dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#########
# FINAL #
#########

# Pull official base image
FROM python:3.11.4-slim-buster

# Create directory for the app user
RUN mkdir -p /home/app

# Add MS SQL Server conf file driver 
ADD ./odbcinst.ini /etc/

# Install MS SQL Server driver
RUN apt-get update -y && apt-get install -y curl gnupg
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update -y && apt-get install -y unixodbc unixodbc-dev tdsodbc freetds-common freetds-bin freetds-dev
RUN apt-get update && ACCEPT_EULA=Y apt-get -y install mssql-tools msodbcsql17
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
RUN apt-get update

# Install weasyprint dependencies
RUN apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info -y

# Create the app user
RUN addgroup --system app && adduser --system --group app

# Create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/backend
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/mediafiles
WORKDIR $APP_HOME

# Install dependencies
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# Copy project
COPY . $APP_HOME

# Chown all the files to the app user
RUN chown -R app:app $APP_HOME

# Change to the app user
USER app