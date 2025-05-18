###########
# BUILDER #
###########

# Pull official base image
FROM node:18.17.0 AS builder

# Set work directory
WORKDIR /usr/src/app

# Install dependencies
COPY package*.json ./
RUN yarn install

# Compile project
COPY . ./
RUN yarn generate

# List the contents of the directory to verify the build output
RUN ls -la /usr/src/app/dist

#########
# FINAL #
#########

# Pull official base image
FROM node:18.17.0 AS runner

# Create directory for the app user
RUN mkdir -p /home/app

# Create the app user
RUN addgroup --system app && adduser --system --group app

# Create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/frontend
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# Copy project
COPY --from=builder /usr/src/app/dist $APP_HOME

# Chown all the files to the app user
RUN chown -R app:app $APP_HOME

# Change to the app user
USER app
