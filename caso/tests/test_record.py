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

valid_record = {
    'CloudComputeService': 'Fake Cloud Service',
    'CpuCount': 8,
    'CpuDuration': 3456000,
    'Disk': 250,
    'StartTime': int(valid_record_fields["start_time"].timestamp()),
    'EndTime': int(valid_record_fields["end_time"].timestamp()),
    'FQAN': 'VO FQAN',
    'GlobalUserName': 'User DN',
    'ImageId': valid_record_fields["image_id"],
    'LocalGroupId': valid_record_fields["group_id"],
    'LocalUserId': valid_record_fields["user_id"],
    'MachineName': 'VM Name',
    'Memory': 16,
    'PublicIPCount': 7,
    'SiteName': 'TEST-Site',
    'Status': 'ACTIVE',
    'VMUUID': uuid.UUID(valid_record_fields["uuid"]),
    'WallDuration': 432000
}


def test_cloud_record():
    record = caso.record.CloudRecord(
        **valid_record_fields
    )

    wall = datetime.timedelta(days=5).total_seconds()
    cpu = wall * record.cpu_count

    assert record.wall_duration == wall
    assert record.cpu_duration == cpu

    assert isinstance(record.start_time, int)
    assert isinstance(record.end_time, int)


def test_cloud_record_map_opts():
    record = caso.record.CloudRecord(
        **valid_record_fields
    )

    opts = {
        "by_alias": True,
        "exclude_unset": True,
        "exclude_none": True,
    }

    assert record.model_dump(**opts) == valid_record


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
