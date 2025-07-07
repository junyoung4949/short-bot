FROM public.ecr.aws/lambda/python:3.11

WORKDIR /var/task

COPY . .
RUN rm -rf local

RUN yum update -y && yum install -y gcc gcc-c++ make
RUN pip install --no-cache-dir -r requirements.txt

CMD ["lambda_function.lambda_handler"] 