def stripe_handler(func):
    try:
        obj = func()
        message = "OK"

    except stripe.error.CardError as e:
        # Since it's a decline, stripe.error.CardError will be caught
        body = e.json_body
        err = body.get('error', {})
        message = err.get('message')
        obj = None
        pass

    except stripe.error.RateLimitError as e:
        body = e.json_body
        err = body.get('error', {})
        message = err.get('message')
        obj = None
        pass

    except stripe.error.InvalidRequestError as e:
        body = e.json_body
        err = body.get('error', {})
        message = err.get('message')
        obj = None
        pass

    except stripe.error.AuthenticationError as e:
        body = e.json_body
        err = body.get('error', {})
        message = err.get('message')
        obj = None
        pass

    except stripe.error.APIConnectionError as e:
        body = e.json_body
        err = body.get('error', {})
        message = err.get('message')
        obj = None
        pass

    except stripe.error.StripeError as e:
        body = e.json_body
        err = body.get('error', {})
        message = err.get('message')
        obj = None
        pass

    except Exception as e:
        body = e.json_body
        err = body.get('error', {})
        message = err.get('message')
        obj = None
        pass

    return message, obj


