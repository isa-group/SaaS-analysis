FROM minizinc/minizinc

RUN apt-get -y update && apt-get install -y wget tar xz-utils nano && apt-get clean
RUN wget https://nodejs.org/dist/v20.18.1/node-v20.18.1-linux-x64.tar.xz
RUN tar xf node-v20.18.1-linux-x64.tar.xz -C /usr/local && rm node-v20.18.1-linux-x64.tar.xz
RUN ln -s /usr/local/node-v20.18.1-linux-x64/bin/* /usr/local/bin/
COPY . /experiment
WORKDIR /experiment
RUN npm ci
CMD [ "npm", "run", "experiment"]