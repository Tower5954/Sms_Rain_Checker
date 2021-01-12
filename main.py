import os
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

account_sid = "**********************************"
auth_token = "********************************"
OWN_ENDPOINT = "http://api.openweathermap.org/data/2.5/onecall"
api_key = "********************************"


weather_params = {
    "lat":"**.****",
    "lon":"-*.****",
    "appid":api_key,
    "exclude":"current,minutely,daily"

}



response = requests.get(OWN_ENDPOINT, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True
        # print("Bring an umbrella ☂️ ")


if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https':os.environ['https_proxy']}
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        to="+************",
        from_="+***********",
        body="It's going to rain so take an umbrella ☂️ ")

    print(message.status)

