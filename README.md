# Code for the blog post "Scaling NLP indexing pipelines with KEDA"

### Development

To run the consumer locally against localstack, we need to start localstack by running the following command:

```bash
# Start localstack
docker-compose up 
```

Afterwards, we install the dependencies and run the consumer:

```bash
pip3 install -r requirements.txt
python3 consumer.py
```

You should see logs like 
    
```bash
❯ python3 consumer.py
2023-04-21 15:34:26 [info     ] No files to upload
2023-04-21 15:34:31 [info     ] Found files                    files=[PosixPath('/tmp/test.txt'), PosixPath('/tmp/test.txt'), PosixPath('/tmp/test.txt'), PosixPath('/tmp/test.txt')]
2023-04-21 15:34:31 [info     ] No files to upload
2023-04-21 15:34:36 [info     ] No files to upload
```


To upload files to test the consumer, we can run the following command:

```bash
python3 upload.py
```