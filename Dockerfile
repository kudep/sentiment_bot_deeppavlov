FROM ubuntu:22.04

RUN apt-get update -qy

RUN apt-get install -qy python3.10 python3-pip

COPY . /sentiment_bot_deeppavlov
WORKDIR /sentiment_bot_deeppavlov

RUN pip3 install -r requirements.txt
RUN apt-get install -qy git
RUN apt-get install -qy git-lfs

RUN mkdir -p cardiffnlp/twitter-roberta-base-sentiment
RUN git clone https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment \
    cardiffnlp/twitter-roberta-base-sentiment

CMD ["python3", "./bot.py"]
