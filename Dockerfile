FROM python:3.9.6-alpine

WORKDIR /bot

COPY dist /bot

RUN pip install booktt-0.1.0-py3-none-any.whl

CMD ["booktt"]