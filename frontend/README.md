# How to run React Server

## 1. Install nodejs (sudo 빼고 입력)
Nodejs 다운로드
- sudo mkdir nodejs
- cd nodejs
- sudo wget https://nodejs.org/dist/v16.17.0/node-v16.17.0-linux-x64.tar.xz

압축 풀기
- sudo xz -d node-v16.17.0-linux-x64.tar.xz
- sudo tar xf node-v16.17.0-linux-x64.tar
- sudo ln -s {nodejs폴더 경로}/node-v16.17.0-linux-x64 {nodejs폴더 경로}/node

환경변수 등록
- vim ~/.bashrc
- 제일 마지막 줄에 아래 라인 추가 export PATH="$PATH:{nodejs폴더 경로}/node/bin"
- source ~/.bashrc

Nodejs 버전확인
- node -v

## 2. npm install
- `npm install`
- `npm install` `react-bootstrap bootstrap`
`axios express mysql`
`mysql2`
`express`
`express-session`
`express-mysql-session`
`body-parser`
`bcrypt`
`axios`

## 3. npm run build
- Creates a file for use in the deployment environment.
- Available in compressed form

## 4. npm start or npm run start

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.





