import os
from abc import ABC, abstractmethod
import json

from base_data.models import JobCategory, Job, Province, City

base_reletive_path = "loaders/files"


class Loader(ABC):

    @abstractmethod
    def load(self):
        pass


class ProvinceLoader(Loader):

    def load(self):
        with open(os.path.join(base_reletive_path, 'provinces.json'), encoding="utf-8") as f:
            data = json.load(f)
            for province in data:
                Province.objects.update_or_create(id=province["id"], name=province["name"])


class CityLoader(Loader):

    def load(self):
        with open(os.path.join(base_reletive_path, 'cities.json'), encoding="utf-8") as f:
            data = json.load(f)
            for city in data:
                City.objects.update_or_create(id=city["id"], name=city["name"],
                                              province=Province.objects.get(id=city["province_id"]))


class JobCategoryLoader(Loader):

    def load(self):
        with open(os.path.join(base_reletive_path, 'job_categories.json'), encoding="utf-8") as f:
            data = json.load(f)
            for job_category in data["job_categories"]:
                JobCategory.objects.update_or_create(name=job_category["name"])


class JobLoader(Loader):

    def load(self):
        with open(os.path.join(base_reletive_path, 'job.json'), encoding="utf-8") as f:
            data = json.load(f)
            for item in data["job_categories"]:
                job_category, created = JobCategory.objects.get_or_create(name=item["name"])
                for job in item["jobs"]:
                    Job.objects.get_or_create(name=job["name"], category=job_category)


class DataLoder(Loader):

    def load(self):
        JobCategoryLoader().load()
        ProvinceLoader().load()
        JobLoader().load()
        CityLoader().load()
