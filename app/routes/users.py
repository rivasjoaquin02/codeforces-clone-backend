from fastapi import APIRouter, Body, Depends, HTTPException, status
from app.dependencies import current_active_user

from app.models.user import UserSchema, UpdateUserSchema
from app.models.user_crud import delete_user, update_user

router = APIRouter()


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_description="Retrieves the current user if loggin",
    response_model=UserSchema,
)
async def get_user(user: UserSchema = Depends(current_active_user)):
    return user


@router.put(
    "/me",
    status_code=status.HTTP_206_PARTIAL_CONTENT,
    response_description="Updates the user info",
    response_model=UserSchema,
)
async def update_user_data(
    user: UserSchema = Depends(current_active_user),
    user_data: UpdateUserSchema = Body(),
):
    updated_user = await update_user(user.id, user_data)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Could not update user info"
        )

    return updated_user


@router.delete(
    "/me",
    status_code=status.HTTP_200_OK,
    response_description="Deletes the current user",
    response_model=UserSchema,
)
async def delete_user_data(user: UserSchema = Depends(current_active_user)):
    deleted_user = await delete_user(user.id)
    if not deleted_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Could not delete user info"
        )

    return deleted_user
