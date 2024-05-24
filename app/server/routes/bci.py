from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from ..database import (
    add_bci,
    retrieve_bci,
    retrieve_bcis,
    update_bci,
)
from ..models.bci import (
    ErrorResponseModel,
    ResponseModel,
    BciSchema,
    UpdateBciModel,
)

router = APIRouter()

@router.post("/", response_description="bci data added into the database")
async def add_bci_data(bci: BciSchema = Body(...)):
    bci = jsonable_encoder(bci)
    new_bci = await add_bci(bci)
    return ResponseModel(new_bci, "bci added successfully.")

@router.get("/", response_description="bcis retrieved")
async def get_bcis():
    bcis = await retrieve_bcis()
    if bcis:
        return ResponseModel(bcis, "bcis data retrieved successfully")
    return ResponseModel(bcis, "Empty list returned")



@router.get("/{pid}", response_description="bci data retrieved")
async def get_bci_data(pid):
    bci = await retrieve_bci(pid)
    if bci:
        return ResponseModel(bci, "bci data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "bci doesn't exist.")


@router.put("/{pid}")
async def update_bci_data(pid: str, req: UpdateBciModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_bci = await update_bci(pid, req)
    if updated_bci:
        return ResponseModel(
            "bci with participantID: {}  update is successful".format(pid),
            "bci updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the bci data.",
    )
