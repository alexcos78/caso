import datetime
import uuid

import caso.record

valid_record_fields = dict(
    uuid=uuid.uuid4().hex,
    site_name="TEST-Site",
    name="VM Name",
    user_id=uuid.uuid4().hex,
    group_id=uuid.uuid4().hex,
    fqan="VO FQAN",
    start_time=datetime.datetime.now() - datetime.timedelta(days=5),
    end_time=datetime.datetime.now(),
    compute_service="Fake Cloud Service",
    status="ACTIVE",
    image_id=uuid.uuid4().hex,
    user_dn="User DN",
    benchmark_type=None,
    benchmark_value=None,
    memory=16,
    cpu_count=8,
    disk=250,
    public_ip_count=7,
)


def test_cloud_record():
    record = caso.record.CloudRecord(
        **valid_record_fields
    )

    wall = datetime.timedelta(days=5).total_seconds()
    cpu = wall * record.cpu_count
    assert record.wall_duration == wall
    assert record.cpu_duration == cpu


def test_cloud_record_custom_wall():
    record = caso.record.CloudRecord(
        **valid_record_fields
    )

    wall = 200
    cpu = wall * record.cpu_count
    record.wall_duration = 200
    assert record.wall_duration == wall
    assert record.cpu_duration == cpu


def test_cloud_record_custom_cpu():
    record = caso.record.CloudRecord(
        **valid_record_fields
    )

    wall = datetime.timedelta(days=5).total_seconds()
    cpu = wall * record.cpu_count * 10
    record.cpu_duration = cpu
    assert record.wall_duration == wall
    assert record.cpu_duration == cpu
