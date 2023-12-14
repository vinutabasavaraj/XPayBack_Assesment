from fastapi import APIRouter
from sqlalchemy import create_engine
from fastapi import HTTPException
from pathlib import Path
import base64
import os

from src.schemas.metadata_schema import MetadataTable_PostgreSQL
from src.models.postgres_orm_model import Base
from src.common.encrypt_decrypt import *


router=APIRouter(tags=["CreateTable"])

cwd = Path(__file__).parents[1]
filepath = cwd/'common'/'metadata_info.json'



async def metadata_configuration(new_data):
    with open(filepath,'r+',encoding='utf-8') as file:
        file_data = json.load(file)
        file_data["metadata_config"]=new_data
        file.seek(0)
        file.truncate()
        json.dump(file_data, file,ensure_ascii = False, indent = 4)

@router.post('/create_table')
async def create_tables(db_details:MetadataTable_PostgreSQL):
    """API to Create the Tables:
    Request Body:

    - DatabaseType : Database type should be Postgresql. 
    - Host : Host/IP address of the database server. Example: hostname.domain.com/192.168.0.1
    - Port : Port number of the database server. Example: 5432
    - Username : Database username.
    - Psswrd : Database psswrd.
    - DatabaseName : Database name.
    """
    SQLALCHEMY_DATABASE_URL = db_details.databaseType.lower() + "://" + db_details.username.lower() + ":" + db_details.psswrd + "@" + db_details.host.lower() + ":" + str(db_details.port) + "/" + db_details.databaseName.lower()
    engine = create_engine(SQLALCHEMY_DATABASE_URL,pool_size=20, max_overflow=0)
    engine.connect()
    if engine:
        Base.metadata.create_all(engine)
        engine.connect()
        enc_data = json_encrypt(str(db_details.psswrd))
        enc_data = base64.b64encode(enc_data).decode('utf-8')
        metadata_config = {
                            "databaseType": db_details.databaseType,
                            "host": db_details.host,
                            "port": db_details.port,
                            "username": db_details.username,
                            "psswrd":enc_data,
                            "databaseName": db_details.databaseName
                        }
                    
        await metadata_configuration(metadata_config)
        return {"detail": {"message": "Tables created successfully.", "statusCode": 201, "errorCode": None}} 
    else:
        raise HTTPException(status_code=statuscode,detail={"message":"Creation of tabel failed","statusCode": 422,"errorCode": errorcode})

    



