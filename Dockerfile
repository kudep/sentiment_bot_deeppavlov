# use slim versions or alpine
FROM ubuntu:22.04 

# join to one RUN
RUN apt-get update -qy && apt-get install -qy python3.10 python3-pip git git-lfs

COPY . /sentiment_bot_deeppavlov
WORKDIR /sentiment_bot_deeppavlov

# join to one RUN
RUN mkdir -p cardiffnlp/twitter-roberta-base-sentiment && git clone https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment cardiffnlp/twitter-roberta-base-sentiment

# it should be in the least
RUN pip3 install -r requirements.txt


CMD ["python3", "./bot.py"]
