from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from decouple import config
from db import MeterList, MeterData

app = FastAPI()

allowed_hosts = config("ALLOWED_HOSTS").split(",")


@app.middleware("http")
async def check_hosts(request: Request, call_next):
    global allowed_hosts
    client_host = request.client.host
    if client_host in allowed_hosts:
        response = await call_next(request)
        return response
    else:
        data = {"message": "Host not allowed"}
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=data)


@app.post("/api/v1/meters")
async def meter_list():
    code = status.HTTP_500_INTERNAL_SERVER_ERROR

    meters = []
    data = {"message": "failed", "data": meters}

    try:
        meters = MeterList().get_meter_list()
        data = {
            "message": "success",
            "data": meters
        }
        code = status.HTTP_200_OK
    except Exception as e:
        print(e)
        code = status.HTTP_500_INTERNAL_SERVER_ERROR
        data = {"message": "failed", "data": meters}
    finally:
        return JSONResponse(status_code=code, content=data)

@app.post("/api/v1/meters/active")
async def meter_list_active():
    code = status.HTTP_500_INTERNAL_SERVER_ERROR

    meters = []
    data = {"message": "failed", "data": meters}

    try:
        meters = MeterList().get_active_meters()
        data = {
            "message": "success",
            "data": meters
        }
        code = status.HTTP_200_OK
    except Exception as e:
        print(e)
        code = status.HTTP_500_INTERNAL_SERVER_ERROR
        data = {"message": "failed", "data": meters}
    finally:
        return JSONResponse(status_code=code, content=data)

@app.post("/api/v1/meters/inactive")
async def meter_list_inactive():
    code = status.HTTP_500_INTERNAL_SERVER_ERROR

    meters = []
    data = {"message": "failed", "data": meters}

    try:
        meters = MeterList().get_inactive_meters()
        data = {
            "message": "success",
            "data": meters
        }
        code = status.HTTP_200_OK
    except Exception as e:
        print(e)
        code = status.HTTP_500_INTERNAL_SERVER_ERROR
        data = {"message": "failed", "data": meters}
    finally:
        return JSONResponse(status_code=code, content=data)

@app.post("/api/v1/meter/{meter_id}")
async def meter_detail(meter_id):
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    data = {"message": "failed", "data": []}

    try:
        meters = MeterList().meter_list
        for meter in meters:
            if meter["socket_id"] == meter_id:
                data = {
                    "message": "success",
                    "data": meter
                }
                code = status.HTTP_200_OK
                break
    except Exception as e:
        print(e)
        code = status.HTTP_500_INTERNAL_SERVER_ERROR
        data = {"message": "failed", "data": []}
    finally:
        return JSONResponse(status_code=code, content=data)


@app.post("/api/v1/full-meter/{meter_id}")
async def meter_detail(meter_id):
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    data = {"message": "failed", "data": []}

    try:
        meter = MeterData(meter_id).get_meter_data()
        data = {
            "message": "success",
            "data": meter
        }
        code = status.HTTP_200_OK
    except Exception as e:
        print(e)
        code = status.HTTP_500_INTERNAL_SERVER_ERROR
        data = {"message": "failed", "data": []}
    finally:
        return JSONResponse(status_code=code, content=data)


@app.get("/api/v1/meter-lateral/{meter_id}")
async def meter_detail(meter_id):
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    data = {"message": "failed", "data": []}

    try:
        meter = MeterData(meter_id).get_meter_lateral()
        data = {
            "message": "success",
            "data": meter
        }
        code = status.HTTP_200_OK
    except Exception as e:
        print(e)
        code = status.HTTP_500_INTERNAL_SERVER_ERROR
        data = {"message": "failed", "data": []}
    finally:
        return JSONResponse(status_code=code, content=data)

@app.get("/api/v1/meter-readings/{meter_id}")
async def meter_detail(meter_id):
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    data = {"message": "failed", "data": []}

    try:
        meter = MeterData(meter_id).get_meter_readings()
        data = {
            "message": "success",
            "data": meter
        }
        code = status.HTTP_200_OK
    except Exception as e:
        print(e)
        code = status.HTTP_500_INTERNAL_SERVER_ERROR
        data = {"message": "failed", "data": []}
    finally:
        return JSONResponse(status_code=code, content=data)

@app.get("/api/v1/sgma-usage/{meter_id}")
async def meter_sgma_usage(meter_id):
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    data_obj = {"message": "failed", "data": []}

    try:
        data = MeterData(meter_id).get_sgma_usage()
        data_obj = {
            "message": "success",
            "data": data
        }
        code = status.HTTP_200_OK
    except Exception as e:
        print(e)
        code = status.HTTP_500_INTERNAL_SERVER_ERROR
        data_obj = {"message": "failed", "data": []}
    finally:
        return JSONResponse(status_code=code, content=data_obj)


@app.get("/api/v1/meter-status/{meter_id}")
async def meter_status(meter_id):
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    data_obj = {"message": "failed", "data": {
        "readings": "no",
        "transactions": "no",
    }}

    try:
        data = MeterData(meter_id)
        reading_data = data.get_meter_readings()
        readings = "no"
        for r in reading_data:
            value = float(r['metered'])
            if value != 0:
                readings = "yes"
                break

        transactions = data.get_sgma_usage()
        if len(transactions) > 0:
            transactions = "yes"
        else:
            transactions = "no"

        data_obj = {
            "message": "success",
            "data": {
                "readings": readings,
                "transactions": transactions,
            }
        }
        code = status.HTTP_200_OK
    except Exception as e:
        print(e)
    finally:
        return JSONResponse(status_code=code, content=data_obj)
