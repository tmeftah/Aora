FROM python:3.12-slim

WORKDIR /backend

COPY . /backend/

RUN python -m venv aora_venv
RUN . aora_venv/bin/activate
RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["bash", "-c"]
CMD ["source aora_venv/bin/activate && fastapi run"]
#TODO do not use reload for production
