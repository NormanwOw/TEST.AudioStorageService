## About  
Audio storage API with Yandex OAuth

## Install  

To get started:

1. Edit file .env:

   * CLIENT_ID
   * CLIENT_SECRET
   * SECRET_KEY   
   
2. `$ cd deploy && docker compose up -d`

Interactive documentation will be here: `http://127.0.0.1:8000/api/v1/docs` 

## Yandex Auth

For the first auth go to https://oauth.yandex.ru/authorize?response_type=code&client_id=CLIENT_ID&redirect_uri=http://127.0.0.1:8000/api/v1/auth/yandex where `CLIENT_ID` is CLIENT_ID from .env file  
Аfter which you will registered in API and receive `Local API Bearer token`
