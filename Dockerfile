
FROM deepset/haystack:base-gpu-v1.15.1
WORKDIR /home/user

COPY . .
RUN pip3 install -r requirements.txt


CMD ["python3", "app.py"]