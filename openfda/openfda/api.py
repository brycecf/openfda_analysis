import os
from requests import request
from urllib import parse


class OpenFdaEvents:
    def __init__(self, auth_env_var="openfda"):
        self.base_url = "https://api.fda.gov/drug/event.json"
        self.payload = {}
        self.headers = {"Authorization": f"Basic {os.environ[auth_env_var]}"}


class QuestionOneData(OpenFdaEvents):
    def __init__(self, auth_env_var="openfda"):
        super().__init__(auth_env_var)

    def get_all_occur_countries(self):
        resource = parse.urljoin(self.base_url, "?count=occurcountry.exact&limit=1000")
        response = request("GET", resource, headers=self.headers, data=self.payload)
        response.raise_for_status()
        return response.json()["results"]

    def get_all_patient_reactions(self):
        resource = parse.urljoin(
            self.base_url, "?count=patient.reaction.reactionmeddrapt.exact&limit=1000"
        )
        response = request("GET", resource, headers=self.headers, data=self.payload)
        response.raise_for_status()
        return response.json()["results"]

    def get_all_patient_reactions_for_country(self, country):
        resource = parse.urljoin(
            self.base_url,
            f"?search=occurcountry:{country}&count=patient.reaction.reactionmeddrapt.exact&limit=1000",
        )
        response = request("GET", resource, headers=self.headers, data=self.payload)
        response.raise_for_status()
        return response.json()["results"]

    def get_all_patient_reactions_for_country_and_drug(self, country, drug):
        resource = parse.urljoin(
            self.base_url,
            f"?search=occurcountry:{country}+AND+patient.drug.medicinalproduct:{drug}&count=patient.reaction.reactionmeddrapt.exact&limit=1000",
        )
        response = request("GET", resource, headers=self.headers, data=self.payload)
        response.raise_for_status()
        return response.json()["results"]
