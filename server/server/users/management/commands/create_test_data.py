from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.utils import timezone

from server.events.models import Event
from server.organizations.models import (
    Activity,
    Organization,
    SchoolActivityGroup,
    SchoolActivityOrder,
)
from server.schools.models import School, SchoolMember
from server.users.models import Consumer, Coordinator, Instructor, Vendor

from .constants import activity_payloads, organization_payload, school_payload


class Command(BaseCommand):
    help = "Creates test users for development"

    def add_arguments(self, parser):
        "parser.add_argument('some_number', nargs='+', type=int)"
        pass

    def create_admin(self):
        try:
            user = get_user_model().objects.create_superuser(
                "admin", "admin@example.com", "Aa123456789"
            )
            self.stdout.write(
                self.style.SUCCESS(f"Successfully created user with {user.email}")
            )
            return user
        except IntegrityError:
            self.stdout.write(
                self.style.WARNING("Dev admin already exists. Skipping...")
            )

    def create_user(self, user_model, email, password, name):
        try:
            user = user_model.objects.create(email=email, password=password, name=name)
            user.set_password(user.password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f"Successfully created user with {user.email}")
            )
            return user

        except IntegrityError:
            self.stdout.write(
                self.style.WARNING(f"{email} already exists. Skipping...")
            )

    def create_all(self):
        self.create_admin()
        coord = self.create_user(
            Coordinator,
            "coord@example.com",
            "Aa123456789",
            "David Cohen",
        )
        consumer = self.create_user(
            Consumer,
            "consumer@example.com",
            "Aa123456789",
            "Daniel Levi",
        )
        consumer_two = self.create_user(
            Consumer,
            "consumer2@example.com",
            "Aa123456789",
            "Liora Weirshtrass",
        )
        consumer_three = self.create_user(
            Consumer,
            "consumer3@example.com",
            "Aa123456789",
            "Maor Azulay",
        )
        instructor = self.create_user(
            Instructor,
            "instructor@example.com",
            "Aa123456789",
            "Dan Yusopov",
        )
        vendor = self.create_user(
            Vendor,
            "vendor@example.com",
            "Aa123456789",
            "Meshi Bar-El",
        )

        if not (
            coord
            and consumer
            and consumer_two
            and consumer_three
            and instructor
            and vendor
        ):
            return self.stdout.write(
                self.style.ERROR(
                    "Users creation failed.\n\
                    You may flush all db using: `python manage.py flush`\n\
                    USE WITH CAUTION - THIS DELETES EVERYTHING"
                )
            )

        org = Organization.objects.create(**organization_payload)
        self.stdout.write(self.style.SUCCESS("Successfully created Organization"))

        school = School.objects.create(**school_payload)
        self.stdout.write(self.style.SUCCESS("Successfully created School"))

        SchoolMember.objects.bulk_create(
            [
                SchoolMember(school=school, user=coord),
                SchoolMember(school=school, user=consumer),
                SchoolMember(school=school, user=consumer_two),
                SchoolMember(school=school, user=consumer_three),
            ]
        )
        self.stdout.write(
            self.style.SUCCESS("Successfully created SchoolMember relations")
        )

        activity_one, activity_two = Activity.objects.bulk_create(
            map(
                lambda activity: Activity(**activity, originization=org),
                activity_payloads,
            )
        )
        self.stdout.write(self.style.SUCCESS("Successfully created Activities"))

        activity_order_one = SchoolActivityOrder.objects.create(
            school=school,
            activity=activity_one,
            status=SchoolActivityOrder.Status.APPROVED,
        )
        SchoolActivityOrder.objects.create(
            school=school,
            activity=activity_two,
            status=SchoolActivityOrder.Status.PENDING_ADMIN_APPROVAL,
        )
        self.stdout.write(self.style.SUCCESS("Successfully created ActivityOrders"))

        group_one = SchoolActivityGroup.objects.create(
            activity_order=activity_order_one,
            name="Group One",
            description="Group One Description",
            instructor=instructor,
        )
        group_two = SchoolActivityGroup.objects.create(
            activity_order=activity_order_one,
            name="Container Only",
            description="Container Only",
            group_type=SchoolActivityGroup.GroupTypes.CONTAINER_ONLY,
        )
        SchoolActivityGroup.objects.create(
            activity_order=activity_order_one,
            name="Cancelled Group",
            description="Cancelled Group",
            group_type=SchoolActivityGroup.GroupTypes.DISABLED_CONSUMERS,
        )

        group_one.consumers.add(consumer)
        group_two.consumers.add(consumer_two)
        self.stdout.write(
            self.style.SUCCESS("Successfully created SchoolActivityGroups")
        )

        today = datetime.now(tz=timezone.utc).replace(microsecond=0, second=0, minute=0)
        events = []
        for i in range(20):
            events.append(
                Event(
                    school_group=group_one,
                    locations_name="Room 202",
                    start_time=today + timedelta(days=i * 7),
                    end_time=today + timedelta(days=i * 7) + timedelta(hours=1.5),
                )
            )

        Event.objects.bulk_create(events)
        self.stdout.write(self.style.SUCCESS("Successfully created Events"))

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise RuntimeError("create_test_data is meant for dev environments.")
        self.create_all()
