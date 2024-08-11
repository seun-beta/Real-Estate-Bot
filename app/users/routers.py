# users/routers.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from app.config import settings
from users.auth import authenticate_user, create_access_token, hash_password
from users.models import User, UserPreference
from users.schemas import (UserLoginSchema, UserPreferenceSchema,
                           UserRegistrationSchema, UserResponseSchema)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/register", response_model=UserResponseSchema)
def register(user: UserRegistrationSchema):
    existing_user = User.objects(email_address=user.email_address).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    new_user = User(
        email_address=user.email_address, password=hash_password(user.password)
    )
    new_user.save()
    return UserResponseSchema(
        email_address=new_user.email_address, is_admin=new_user.is_admin
    )


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials"
        )

    access_token = create_access_token(data={"sub": user.email_address})
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = User.objects(email_address=email).first()
    if user is None:
        raise credentials_exception
    return user


@router.get("/users/me", response_model=UserResponseSchema)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/preferences/", response_model=UserPreferenceSchema)
async def set_user_preferences(
    preferences: UserPreferenceSchema, current_user=Depends(get_current_user)
):
    # Check if user preferences already exist
    user_preferences = UserPreference.objects(user=current_user).first()

    if user_preferences:
        # Update existing preferences
        user_preferences.update(
            preferred_location=preferences.preferred_location,
            min_rooms=preferences.min_rooms,
            max_rent=preferences.max_rent,
        )
    else:
        # Create new preferences
        user_preferences = UserPreference(
            user=current_user,
            preferred_location=preferences.preferred_location,
            min_rooms=preferences.min_rooms,
            max_rent=preferences.max_rent,
        )
        user_preferences.save()

    return preferences


@router.get("/preferences/", response_model=UserPreferenceSchema)
async def get_user_preferences(current_user=Depends(get_current_user)):
    user_preferences = UserPreference.objects(user=current_user).first()
    if not user_preferences:
        raise HTTPException(status_code=404, detail="Preferences not found")
    return UserPreferenceSchema(
        preferred_location=user_preferences.preferred_location,
        min_rooms=user_preferences.min_rooms,
        max_rent=user_preferences.max_rent,
    )
