import motor.motor_asyncio
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb+srv://lsy44415:Lsy4986881@cluster0.vls4aqs.mongodb.net/"
#MONGO_DETAILS = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.bcis

bci_collection = database.get_collection("bcis_collection")


def bci_helper(bci) -> dict:
    return {
        "id": str(bci["_id"]),
        "pid": bci["pid"],
        "time": bci["time"],
        "emo": bci["emo"],

    }

async def retrieve_bcis():
    bcis = []
    async for bci in bci_collection.find():
        bcis.append(bci_helper(bci))
    return bcis


# Add a new bci into to the database
async def add_bci(bci_data: dict) -> dict:
    bci = await bci_collection.insert_one(bci_data)
    new_bci = await bci_collection.find_one({"_id": bci.inserted_id})
    return bci_helper(new_bci)


# Retrieve a bci with a matching ID
async def retrieve_bci(pid: str) -> dict:
    bcis = []
    async for bci in bci_collection.find({"pid": pid}).sort("_id",-1).limit(1):
        bcis.append(bci_helper(bci))
    return bcis[0]
    # bci = await bci_collection.find({"pid": pid})
    # if bci:
        # return bci_helper(bci)


# Update a bci with a matching pid
async def update_bci(pid: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    bci = await bci_collection.find_one({"pid": pid})
    if bci:
        updated_bci = await bci_collection.update_one(
            {"pid": pid}, {"$set": data}
        )
        if updated_bci:
            return True
        return False
    else:
        print("update error: bci not found")

