FROM python

RUN pip3 install coverage flask lxml pytest pytest-cov requests xmljson

COPY ./consts /consts

COPY ./exceptions /exceptions

COPY ./tests /tests

COPY *.py /

RUN chmod +x /api.py

RUN ln -s /api.py /enricher-api

CMD ["/enricher-api"]
