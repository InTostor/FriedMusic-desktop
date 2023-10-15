from lib.FriedMusic import *
from lib.Configuration import Configuration

filename = Configuration.getValue("musicStorageUrl") + "Дельфин - Сумерки.mp3"

print(filename)

client = Client()
client.authenticate(("InTostor","Cummunism"))