FROM ubuntu


RUN apt-get update && apt-get -y install cron python3-pip

COPY requirements.txt requirements.txt
COPY store_locations.py store_locations.py
COPY store_predictions.py store_predictions.py
COPY database.py database.py
COPY entrypoint.sh entrypoint.sh
RUN ["chmod", "+x", "entrypoint.sh"]
RUN pip3 install -r requirements.txt
ENTRYPOINT [ "entrypoint.sh" ]


# Add crontab file in the cron directory
# ADD crontab /etc/cron.d/hello-cron

# Give execution rights on the cron job
# RUN chmod 0644 /etc/cron.d/hello-cron

# Apply cron job
# RUN crontab /etc/cron.d/hello-cron

# Create the log file to be able to run tail
# RUN touch /var/log/cron.log

# Run the command on container startup
# CMD cron && tail -f /var/log/cron.log



