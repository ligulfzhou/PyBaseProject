FROM pybase:latest

WORKDIR /app

ADD . /app

EXPOSE 9090

CMD ["python", "init.py", "--port=9090", "--debug=True"]
