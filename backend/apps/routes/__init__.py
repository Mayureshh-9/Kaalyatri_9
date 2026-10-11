from fastapi import APIRouter
from .user import router as user_router
from .destination import router as destination_router
from .booking import router as booking_router
from .contact_message import router as contact_message_router
from .newsletter_subscriber import router as newsletter_subscriber_router
from .review import router as review_router
from .tour_itinerary import router as tour_itinerary_router
from .payment import router as payment_router
from .auth import router as auth_router
from .era import router as era_router
from .addon import router as addon_router
from .admin_dashboard import router as admin_dashboard_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(era_router)
api_router.include_router(addon_router)
api_router.include_router(user_router)
api_router.include_router(destination_router)
api_router.include_router(booking_router)
api_router.include_router(contact_message_router)
api_router.include_router(newsletter_subscriber_router)
api_router.include_router(review_router)
api_router.include_router(tour_itinerary_router)
api_router.include_router(payment_router)
api_router.include_router(admin_dashboard_router)
