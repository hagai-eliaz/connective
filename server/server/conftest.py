import pytest

from server.organizations.models import (
    Activity,
    Organization,
    OrganizationMember,
    SchoolActivityGroup,
    SchoolActivityOrder,
)
from server.organizations.tests.factories import (
    ActivityFactory,
    OrganizationFactory,
    SchoolActivityGroupFactory,
    SchoolActivityOrderFactory,
)
from server.schools.models import School, SchoolMember
from server.schools.tests.factories import SchoolFactory
from server.users.models import Consumer, Coordinator, Instructor, User, Vendor
from server.users.tests.factories import (
    ConsumerFactory,
    CoordinatorFactory,
    InstructorFactory,
    UserFactory,
    VendorFactory,
)


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def coordinator() -> Coordinator:
    return CoordinatorFactory()


@pytest.fixture
def consumer() -> Consumer:
    return ConsumerFactory()


@pytest.fixture
def vendor() -> Vendor:
    return VendorFactory()


@pytest.fixture
def instructor() -> Instructor:
    return InstructorFactory()


@pytest.fixture
def school() -> School:
    return SchoolFactory()


@pytest.fixture
def organization() -> Organization:
    return OrganizationFactory()


@pytest.fixture
def activity() -> Activity:
    return ActivityFactory()


@pytest.fixture
def school_activity_order() -> SchoolActivityOrder:
    return SchoolActivityOrderFactory()


@pytest.fixture
def school_activity_group() -> SchoolActivityGroup:
    return SchoolActivityGroupFactory()


@pytest.fixture
def all_entities(
    school_activity_group, coordinator, consumer, vendor, instructor
) -> dict:
    activity_order = school_activity_group.activity_order
    activity = activity_order.activity
    organization = activity.originization

    SchoolMember.objects.create(user=coordinator, school=activity_order.school)
    SchoolMember.objects.create(user=consumer, school=activity_order.school)
    OrganizationMember.objects.create(user=vendor, organization=organization)
    OrganizationMember.objects.create(user=instructor, organization=organization)

    return {
        "activity_group": school_activity_group,
        "activity_order": activity_order,
        "school": activity_order.school,
        "activity": activity,
        "organization": organization,
        "coord": coordinator,
        "consumer": consumer,
        "vendor": vendor,
        "instructor": instructor,
    }


school1 = school
