import traceback

try:
    from app.schemas.transaction import TransactionCreate
    print("TransactionCreate OK")
except Exception as e:
    with open("error.txt", "w") as f:
        traceback.print_exc(file=f)
    traceback.print_exc()

try:
    from app.main import app
    print("app OK")
except Exception as e:
    with open("error2.txt", "w") as f:
        traceback.print_exc(file=f)
    traceback.print_exc()
