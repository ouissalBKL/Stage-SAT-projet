from services.specialist_service import get_specialist
from database import get_db

db_generator = get_db()
db = next(db_generator)

emails = ["salwa@gmail.com", "user@example.com", "inconnu@example.com"]

for email in emails:
    is_specialist = get_specialist(email, db)
    print(f"Email: {email} -> Specialist: {is_specialist}")

db.close()
