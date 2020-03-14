# Samson
E-mail your Google Calendar daily activities directly to your email via Google's API!

**Advised to use virtualenv**

## Dependancies

1. $pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
2. $export EMAIL='{ENTER YOUR EMAIL}'
3. Google permissions/authorizations - just the first time to make the token.pickle file
4. Google API `credentials.json` file (can get your own [here - go to 'Enable the Google Calendar'](https://developers.google.com/calendar/quickstart/python)
5. Python 3.

## To Run

`$python samson.py`

### References

* https://developers.google.com/gmail/api/quickstart/python
* https://developers.google.com/calendar/overview
* https://medium.com/better-programming/a-beginners-guide-to-the-google-gmail-api-and-its-documentation-c73495deff08
