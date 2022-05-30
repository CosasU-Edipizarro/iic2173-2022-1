FROM node:lts-alpine

WORKDIR /app

COPY package.json yarn.lock ./

RUN yarn
ADD . .
RUN yarn build

# EXPOSE 8080
# CMD ["yarn", "preview"]