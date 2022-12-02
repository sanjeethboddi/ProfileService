from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router as book_router
from fastapi.middleware.cors import CORSMiddleware

config = dotenv_values(".env")

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"],
                # username=config["MONGO_INITDB_ROOT_USERNAME"],
                # password=config["MONGO_INITDB_ROOT_PASSWORD"]
                )
    app.database = app.mongodb_client[config["DB_NAME"]]
    app.auth_service = config["AUTH_SERVICE_URL"]
    app.graph_service = config["GRAPH_SERVICE_URL"]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(book_router, tags=["profiles"], prefix="")
