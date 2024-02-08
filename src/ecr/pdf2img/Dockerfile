FROM python:3.11.6-slim

RUN apt-get update && apt-get install -y \
    poppler-utils libopencv-dev \
    && rm -rf /var/lib/apt/lists/*

COPY entry.sh "/entry.sh"

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

ENTRYPOINT [ "/bin/bash", "/entry.sh" ]
CMD [ "app.lambda_handler" ]
