from crypto_portfolio import create_app

app = create_app()

if __name__ == "__main__":
    from werkzeug.serving import run_simple
    run_simple('0.0.0.0', 5000, app)