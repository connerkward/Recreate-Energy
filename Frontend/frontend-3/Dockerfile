# pull official base image
# FROM node:latest
FROM nginx

# set working directory
# WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
# Is this necessary?
# ENV PATH /app/node_modules/.bin:$PATH

# EXPOSE 80

# # install app dependencies
# COPY package.json ./
# COPY package-lock.json ./
# # using --legacy-peer-deps because react version is too new
# RUN npm install --legacy-peer-deps
# RUN npm install react-scripts@3.4.1 -g

# add app
# COPY src /src
COPY build /usr/share/nginx/html

# start app, npm start is not intended for produciton
# technically speaking, you should run "npm run build"
# and run using node 
# CMD ["npm", "start"]