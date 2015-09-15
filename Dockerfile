FROM python:2-onbuild
EXPOSE 5000
ENV DB_FILE /tmp/db.json
CMD [ "python", "./app.py" ]
