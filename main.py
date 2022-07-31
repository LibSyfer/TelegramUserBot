from create_connect import app

from handlers import Client

Client.register_handlers(app)

print("Запуск...")
app.run()
