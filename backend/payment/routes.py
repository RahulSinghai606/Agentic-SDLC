from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import stripe
import os

# Environment variables for Stripe secret key
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY", "defaultstripekey")
stripe.api_key = STRIPE_API_KEY

# Models
class PaymentIntent(BaseModel):
    amount: int
    currency: str

class PaymentResponse(BaseModel):
    client_secret: str

# Router initialization
payment_router = APIRouter()

# Routes
@payment_router.post("/create-payment-intent", response_model=PaymentResponse)
async def create_payment_intent(payment_intent: PaymentIntent):
    try:
        intent = stripe.PaymentIntent.create(
            amount=payment_intent.amount,
            currency=payment_intent.currency,
        )
        return {"client_secret": intent.client_secret}
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=f"Stripe Error: {e.error.message}")

@payment_router.post("/confirm-payment")
async def confirm_payment(payment_id: str):
    try:
        payment_intent = stripe.PaymentIntent.retrieve(payment_id)

        if payment_intent.status == "succeeded":
            return {"detail": "Payment succeeded"}

        return {"detail": "Payment not completed", "status": payment_intent.status}
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=f"Stripe Error: {e.error.message}")

@payment_router.get("/payment-status")
async def get_payment_status(payment_id: str):
    try:
        payment_intent = stripe.PaymentIntent.retrieve(payment_id)
        return {"status": payment_intent.status}
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=f"Stripe Error: {e.error.message}")