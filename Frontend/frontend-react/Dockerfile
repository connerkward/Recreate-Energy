# pull official base image
FROM node:latest

# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
# Is this necessary?
ENV PATH /app/node_modules/.bin:$PATH

EXPOSE 80

# install app dependencies
COPY package.json ./
COPY package-lock.json ./
RUN npm install
RUN npm install react-scripts@3.4.1 -g

# add app
COPY src /src
COPY public /public


# start app
CMD ["npm", "start"]