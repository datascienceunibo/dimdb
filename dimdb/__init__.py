from flask import Flask

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY="3f9rwhv0e8ht9c49y5437ytc9",
    TWITTER_CONSUMER_KEY="JF1mKj5iIbxnSJR1dOMlwgeVo",
    TWITTER_CONSUMER_SECRET="6rKsmpnpcUDCBRLd6DGejQEafEU51xGGTbL7E0sc1CM55pV4N6"
)

from . import pages
