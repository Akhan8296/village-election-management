from services.auth_service import create_user

create_user(
    username="power",
    password="Power@123",
    full_name="Power User",
    role="POWER",
    village_id=None,
    permissions=[],
    access_start=None,
    access_end=None
)

print("Power user created successfully.")