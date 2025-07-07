from fastapi import FastAPI, Depends 
from src.user.routes import user_routers
from src.shop.routes import shop_routers
from src.user.schemas import UserResponse
from src.user.utils.auth_utils import get_request_user


# Initialize the app
app = FastAPI(
    title="FASTQR DINE API",
    description="API for managing digital restaurant orders.",
    version="0.0.1",
    debug=True
)

# Include routers
app.include_router(user_routers.userRouter, prefix="/user", tags=["User"])
app.include_router(shop_routers.shopRouter, prefix="/shop", tags=["Shop"])



@app.get("/")
def read_root(user: UserResponse = Depends(get_request_user)):
    return {"Hello": "World", "user": user}
