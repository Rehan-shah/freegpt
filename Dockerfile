ARG PORT=443
FROM cypress/broswer:latest
RUN apt-get install python 3 -y
RUN echo $(python3 -m site --user-base)
COPY requirements.txt .
RUN PATH /home/root/.local/bin:${PATH}
RUN apt-get update && apt-get install -y python3-pip && pip install -r requirements
COPY ..
CMD uvicorn main:app --host 0.0.0.0 - -port $PORT
