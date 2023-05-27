# GCP Cloud Function for Facebook Ads Events Reporting
GCP Cloud function that reports events to Facebook Ads.

## Setting environment variables
You must set the following environment variables:
- FACEBOOK_ACCESS_TOKEN
- FACEBOOK_PIXEL_ID
- TEST_EVENT_CODE
- ENV (dev, prod or testing)

The access token and pixel ID can be found in the Facebook Events Manager.

The ENV variable is used to determine if the function is running in production or not, used in conjunction with the TEST_EVENT_CODE to send test events to the Events Manager.

## Updating the function to suit your needs
You must update the **event_handler()** function to process your payload data.

## Testing
You may find pytest test files in app/tests.
Don't forget to set the TEST_EVENT_CODE environment variable. otherwise you'll polute the pixel data.

## Deploying
If you are on windows you can use the provided deploy.ps1 scrip
GCP will deploy the function as 1st gen. 
