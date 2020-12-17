FROM python:3.7.3

COPY requirements.txt /

RUN pip install -r /requirements.txt
RUN pip install torch==1.7.1+cpu torchvision==0.8.2+cpu torchaudio==0.7.2 -f https://download.pytorch.org/whl/torch_stable.html

WORKDIR /app

COPY ./ .

WORKDIR TradingAgent/

EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
