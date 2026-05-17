# Stripe CLI

## Commands

````shell
# Login
$ stripe login

# Testing webhooks
# stripe listen --forward-to localhost:80000/path/to/stripe_webhook_callback

$ stripe listen --forward-to localhost:8000/api/webhook/payment/checkout_session

# Trigger events using your terminal
# Ex: stripe trigger payment_intent.succeeded
$ stripe trigger [event_name]
````