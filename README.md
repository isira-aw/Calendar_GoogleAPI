Frontend: React

npx create-react-app calendar-app
cd calendar-app
npm install axios react-router-dom @mui/material @emotion/react @emotion/styled

Remove-Item -Recurse -Force node_modules
Remove-Item -Force package-lock.json

npm install
npm audit

npm audit fix

