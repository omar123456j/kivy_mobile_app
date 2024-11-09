import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Initialize Firebase Admin SDK
firebase_credentials = {
  "type": "service_account",
  "project_id": "mobile-seriales",
  "private_key_id": "a0094cb03d914ef49d1854db2d2b588f1a95266d",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQC708wdzKHHdGHG\nB/wMTkeEDWgd5cDjtSY5kM8gbSQExfsc8Gf3RdHqG3rEEcyUTDg9ntdcdElqwYa/\nqqbqIZyKLS2a+qLuqPnJ5cSZizQx4uf2JQqsuwFiVWbENCLdCTAfYSMYf6pFiENI\nBYocF41egpOXTAXG7JYgLz5P+lB6j66bmcqyWSVuNHLlUAetEBExJmL5NyU8I0Mr\nlJe0y0Yu1GHW+7eu5VbihXIYcUBSyHdxIc/vGUrbI5EhMskg1wN8OYgUw8M3d0Ha\nLD76egeckagh3//ahFlhMD+lsGICAJMlP6Mu0XS2FgIcHYOHp3kbgme0LE7+TbNj\nS4aDFECnAgMBAAECggEAGB92iqk6aeRvnkBuRaJUGwihw507bcNZOnF3uKFry9Ul\nkCzsHVzxPdDzrnTewnkbjAZ3gF9LApQCW2FueImCkliFD+96t44qLpz85/9x36pV\nwk41lcOaxOdVAIP1qk/Ax3bxS/cxhiafBYP4ne0EcgvxKrBP2aGPEmke5qSua18K\naRNnzWGNpDa+ZHTdAVaRGpx3BuvGheTxdKBKZiOZpk53CUwyJ3qEEd5ZfZi5S9RH\nb2NF5MD9kbxZYesMbbaSHPg8l++1WdbhTZJTOrZTE1oDxKmmcq1vCMmWPI+1aDN0\nwQnYoF9iPKOh7A6S8Z0BUwnw+jqfb8JRQdahsXIEcQKBgQDc8ftT2mxjBoFBLKVe\nexeJ7j1suWBa+saQFzO4YxJV6LhGOIKGl3x6WsljLX8eZH+4ttV4CBWgDV62LjqZ\nus9AAklskd/wxXRDQrLwTPSDlS5cwJwTR4jzseMSUcUGGpSR3Ypd7M5yzMFjpmkI\nlW4ONQJwSxszAwA+cIwzkicViQKBgQDZoK7FKupi6QLkfhSM9tuXMXcR8gOTyvGZ\nVN169+CqoI83hDfwSaolHkY4lmL5XwtMpw38HDaKgwMkDsknUMVAhl3q50eK/BZN\nr7nDEtDb96knOgxSor2K59LJr1jxo1PjNyTu0BQFaI8W2bF4HKd9c7T6ibbB8VWE\nJpuSFF5IrwKBgQCy+q7uWXUNrrpL8n+vjqUdzckiZvTAHn91P+ZcypySzSdhcuuB\nXfuvHhYfaj6cfyrblfhM+LeT5ODBUaeU2riCkJesBGtVHo604bYUZTJ52QIqjrig\nAYXWa1aXg3fIHwYVN1KcDXWbl3RdZfOVyX7SsWxdTOomo5qx+fgI2q8giQKBgQCe\nT28TasaaMRqzkKvuZ10SPR965GyJxGW/vqZm346FUMsd/Yabu1qUKdO3Ml7JPMSB\nfDyGGxfp5qgQQNk/SlhTOet0B85ZYkvvM1eUekmI2j4olOeF7XCobT8/C9lN3hwV\n+3VYa/FEhe0hGDcrQtzsO5F5d1iE+MPWoCcnOr3jbQKBgQDVgpbFjmU7DSrPldRQ\n+k/N8AGU/9x+zRyFAYbqrCyUtTpp0rmNXV2FXiNHXvdZ/KXA7qG2l9c/dcVo/fIO\nCXpqtSCp7DhNlL5+FAZ+vZNDLVzKrI5Y1Pvpk2m8K8oonYNhcJx4MATlihr3FK8w\nhikueD2tRC4uB+K1SjiMU4e8yw==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-rzn5b@mobile-seriales.iam.gserviceaccount.com",
  "client_id": "102051051220972778161",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-rzn5b%40mobile-seriales.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
cred = credentials.Certificate(firebase_credentials)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://mobile-seriales-default-rtdb.europe-west1.firebasedatabase.app/'  # Replace with your Firebase project ID
})

def send_data(user_name,serial_number):
        # Get a reference to the database
        ref = db.reference()

        # Example data
      

        # Store data in the database
        ref.child("users").push({
            "name": user_name,
            "serial_number": serial_number
        })


