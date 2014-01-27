""" Instantiates the API

...that's all :)
"""

from ninja.api import NinjaAPI

from auth import ACCESS_TOKEN

api = NinjaAPI(ACCESS_TOKEN)

