FROM httpd:2.4-alpine3.20

# Install Python 3.12 and pip
RUN apk --update --no-cache add python3~3.12 python3-dev~3.12 py3-pip

# Install gcc
RUN apk --update --no-cache add gcc musl-dev

# Install mariadb connector
RUN apk --update --no-cache add mariadb-dev && \
	pip install mariadb --break-system-packages

# Install Google API Python Client
RUN pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib --break-system-packages

# Install Sendgrid Client
RUN pip install sendgrid --break-system-packages

# Install Utilities
RUN pip install multipart --break-system-packages