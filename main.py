import os
import sys

import dotenv

from bot import GiftifyHelper

dotenv.load_dotenv()


if __name__ == "__main__":
    GiftifyHelper(
        token=os.environ["TOKEN"],
        application_id=int(os.environ["APPLICATION_ID"]),
        public_key=os.environ["PUBLIC_KEY"],
        sync="--sync" in sys.argv or "-S" in sys.argv,
    ).start()
