FROM node:18-alpine

WORKDIR /app

# 패키지 설치
COPY package.json package-lock.json* ./
RUN npm install

# 애플리케이션 복사
COPY . .

# 포트 노출
EXPOSE 3000

# 실행
CMD ["npm", "start"]
