# FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
FROM python:3.9

COPY requirements.txt /

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

EXPOSE 80

COPY api_aws.py /
COPY api_main.py /
COPY api_ws.py /
COPY certificates /certificates
COPY TimeStream /TimeStream

ENTRYPOINT ["uvicorn", "api_main:app", "--host", "0.0.0.0", "--port", "80", "--timeout-keep-alive", "300"]
# CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80", --timeout-keep-alive, "300"]
