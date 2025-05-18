# Pull offcial base image 
FROM nginx:1.25

# Create certificate directory
RUN mkdir /etc/nginx/.certs

# Replace default configuration
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

# Copy certificates
COPY ./certificates /etc/nginx/.certs