from fastapi import FastAPI


app = FastAPI()


@app.health("/health")
def health_check():
    return {"status": "healthy"}