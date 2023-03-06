FROM python:3
LABEL version="1.2"
LABEL description="Basic django container"

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        sqlite3 ieee-data \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
#WORKDIR /opt/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

# This is mostly useless, as the volume doesn't persist.
# Use it to check for runtime errors.  Manually rerun migrate with -v option.
VOLUME ["/usr/db"]
RUN rm -f db.sqlite3 && ln -s /usr/db/db.sqlite3 && python manage.py migrate

EXPOSE 8000/tcp
STOPSIGNAL SIGTERM
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
