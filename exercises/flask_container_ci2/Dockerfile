FROM ubuntu:18.04
COPY app/main.py requirements.txt /app/
RUN apt-get update && \
    apt-get --assume-yes dist-upgrade && \
    apt-get --assume-yes install --no-install-recommends \
        locales='2.27-3ubuntu1' \
        python3-minimal='3.6.7-1~18.04' \
        python3-pip='9.0.1-2.3~ubuntu1.18.04.1' \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    locale-gen 'en_US.UTF-8' && \
    pip3 install --no-cache -r /app/requirements.txt
ENV LC_ALL='en_US.UTF-8' \
    LANG='en_US.UTF-8' \
    LANGUAGE='en_US.UTF-8' \
    FLASK_APP='/app/main.py'
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
