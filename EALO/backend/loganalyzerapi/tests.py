import csv
import json
import shutil
import tempfile
from collections import Counter
from pathlib import Path
from unittest import mock
from zipfile import ZIP_DEFLATED, ZipFile

from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import connection
from django.test import SimpleTestCase, TestCase, TransactionTestCase
from django.test.utils import override_settings
from django.test.utils import CaptureQueriesContext
from django.urls import resolve
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from dynamic_models.models import FieldSchema, ModelSchema

from loganalyzerapi.models import LogAnalysisJob, LogDetailV2, LogFile, LogMaster
from loganalyzerapi.parsers import get_parser, validate_log_line
from loganalyzerapi.views import (
    DynamicLogDetailViewSet,
    _xview_response_time_ms,
    _xview_status_group,
    _xview_uri,
)


FIXTURE_DIR = Path(__file__).resolve().parent / "testdata" / "access_logs"
MANIFEST_PATH = FIXTURE_DIR / "expected_results.json"


def load_manifest():
    with MANIFEST_PATH.open(encoding="utf-8") as manifest_file:
        return json.load(manifest_file)


class AuthenticationApiContractTests(TestCase):
    """Keep the SPA-facing authentication URLs and token responses stable."""

    def setUp(self):
        self.client = APIClient()
        self.password = "ContractPass123!"
        self.user = User.objects.create_user(
            username="auth-contract-user",
            email="auth-contract@example.test",
            password=self.password,
        )

    def test_login_and_logout_token_contract(self):
        login_response = self.client.post(
            "/mwla/rest-auth/login/",
            {"username": self.user.username, "password": self.password},
            format="json",
        )

        self.assertEqual(login_response.status_code, 200)
        self.assertIn("key", login_response.data)
        token_key = login_response.data["key"]
        self.assertTrue(
            Token.objects.filter(key=token_key, user=self.user).exists()
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token_key)
        logout_response = self.client.post("/mwla/rest-auth/logout/")

        self.assertEqual(logout_response.status_code, 200)
        self.assertFalse(Token.objects.filter(key=token_key).exists())

    def test_registration_contract(self):
        response = self.client.post(
            "/mwla/rest-auth/registration/",
            {
                "username": "registered-contract-user",
                "email": "registered-contract@example.test",
                "password1": "RegistrationPass123!",
                "password2": "RegistrationPass123!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn("key", response.data)
        self.assertTrue(
            User.objects.filter(username="registered-contract-user").exists()
        )


class RouterContractTests(SimpleTestCase):
    """Ensure removing duplicate router registrations keeps SPA action URLs."""

    def test_post_action_urls_resolve(self):
        action_urls = {
            "/mwla/logmaster/create_dynamic_logdetail/": "post",
            "/mwla/logmaster/delete_dynamic_logdetail/": "post",
            "/mwla/logdetail_dynamic/start_end/": "post",
            "/mwla/logdetail_dynamic/statistics/": "post",
            "/mwla/logdetail_dynamic/chartdata/": "post",
            "/mwla/logdetail_dynamic/chartdata_diff/": "post",
            "/mwla/logdetail_dynamic/xview/": "post",
            "/mwla/logdetail_dynamic/findings/": "post",
            "/mwla/logdetail_dynamic/get_before_after_detail/": "post",
            "/mwla/logdetail_dynamic/uridetail/": "post",
            "/mwla/logformat/assist/": "post",
            "/mwla/logformatstring/formatkind_list/": "get",
            "/mwla/user/active/": "post",
        }

        for url, method in action_urls.items():
            with self.subTest(url=url):
                match = resolve(url)
                self.assertIn(method, match.func.actions)

    def test_sample_validation_url_resolves(self):
        match = resolve('/mwla/logfile/validate_sample/')
        self.assertEqual(match.func.actions['post'], 'validate_sample')

    def test_v2_readonly_url_resolves(self):
        match = resolve('/mwla/logdetail_v2/')
        self.assertEqual(match.func.cls.__name__, 'LogDetailV2ViewSet')


class XViewContractTests(SimpleTestCase):
    def test_request_uri_and_response_time_normalization(self):
        self.assertEqual(_xview_uri('GET /orders?id=7 HTTP/1.1'), '/orders?id=7')
        self.assertEqual(_xview_uri('/health'), '/health')
        self.assertEqual(_xview_response_time_ms(250000, 'D'), 250.0)
        self.assertEqual(_xview_response_time_ms(0.25, 'T'), 250.0)
        self.assertIsNone(_xview_response_time_ms(-1, 'D'))

    def test_status_groups_match_xview_colors(self):
        self.assertEqual(_xview_status_group(200), '20x')
        self.assertEqual(_xview_status_group(302), '30x')
        self.assertEqual(_xview_status_group(404), '40x')
        self.assertEqual(_xview_status_group(503), '50x')
        self.assertEqual(_xview_status_group('-'), 'other')


class AccessLogFixtureContractTests(SimpleTestCase):
    """Validate the fixture contract without requiring a database."""

    def test_fixture_counts_follow_manifest_invariant(self):
        manifest = load_manifest()

        for filename, expected in manifest["fixtures"].items():
            with self.subTest(filename=filename):
                lines = (FIXTURE_DIR / filename).read_text(
                    encoding="utf-8"
                ).splitlines()
                comment_count = sum(line.startswith("#") for line in lines)
                data_count = len(lines) - comment_count

                self.assertEqual(len(lines), expected["physical_line_count"])
                self.assertEqual(
                    comment_count, expected["comment_line_count"]
                )
                self.assertEqual(data_count, expected["data_line_count"])
                self.assertEqual(
                    expected["expected_parsed_count"]
                    + expected["expected_rejected_count"],
                    data_count,
                )

    def test_line_counter_includes_final_line_without_newline(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "no-final-newline.log"
            path.write_bytes(b"first\nsecond")

            self.assertEqual(
                DynamicLogDetailViewSet().get_total_lines(str(path)), 2
            )

    def test_zip_upload_requires_one_safe_member(self):
        parser = DynamicLogDetailViewSet()
        with tempfile.TemporaryDirectory() as temporary_directory:
            archive = Path(temporary_directory) / "single.zip"
            with ZipFile(archive, "w", ZIP_DEFLATED) as zip_file:
                zip_file.writestr("access.log", "127.0.0.1 - -")
            output = parser.decompress_file(str(archive), temporary_directory)
            self.assertEqual(Path(output).read_text(), "127.0.0.1 - -")

            multi_archive = Path(temporary_directory) / "multiple.zip"
            with ZipFile(multi_archive, "w", ZIP_DEFLATED) as zip_file:
                zip_file.writestr("one.log", "one")
                zip_file.writestr("two.log", "two")
            with self.assertRaises(ValueError):
                parser.get_original_filesize(str(multi_archive))

            unsafe_archive = Path(temporary_directory) / "unsafe.zip"
            with ZipFile(unsafe_archive, "w", ZIP_DEFLATED) as zip_file:
                zip_file.writestr("../outside.log", "unsafe")
            with self.assertRaises(ValueError):
                parser.decompress_file(str(unsafe_archive), temporary_directory)

    def test_format_parser_contracts(self):
        apache_index = {'t': 0, 's': 1, 'b': 2}
        self.assertIsNone(validate_log_line(
            '[12/Aug/2026:00:00:00 200 12',
            'apache', 'combined', apache_index, 3,
        ))
        for nonstandard_status in ('000', '099', '600', '700', '999'):
            self.assertIsNone(validate_log_line(
                '[12/Aug/2026:00:00:00 %s 12' % nonstandard_status,
                'apache', 'combined', apache_index, 3,
            ))
        for invalid_status in ('99', '1000', 'BAD', '2O0'):
            self.assertEqual(validate_log_line(
                '[12/Aug/2026:00:00:00 %s 12' % invalid_status,
                'apache', 'combined', apache_index, 3,
            )[0], 'invalid_status')
        self.assertEqual(
            validate_log_line('raw', 'unknown', 'unknown', {}, None)[0],
            'unsupported_format',
        )
        self.assertEqual(get_parser('apache').format_kind, 'apache')
        self.assertEqual(get_parser('IIS-NCSA').format_kind, 'IIS-W3C')
        self.assertIsNone(get_parser('unknown'))

        nginx_index = {'$time_local': 0, '$status': 1, '$body_bytes_sent': 2,
                       '$request_time': 3}
        self.assertIsNone(validate_log_line(
            '[12/Aug/2026:00:00:00 200 12 0.001',
            'nginx', 'combined', nginx_index, 4,
        ))

    def test_apache_cookie_field_counts_as_a_physical_field(self):
        parser = DynamicLogDetailViewSet()
        log_format = (
            r'%h %l %u %t \"%r\" %>s %b %D '
            r'\"%{Referer}i\" \"%{User-Agent}i\" \"%{Cookie}i\"'
        )
        format_index = parser.get_logformat_index(log_format, 'apache')
        expected_count = max(format_index.values()) + 1

        self.assertEqual(format_index['Cookie'], 11)
        self.assertEqual(expected_count, 12)
        self.assertIsNone(validate_log_line(
            '127.0.0.1 - user [12/Aug/2026:00:00:00 +0900] '
            '"GET / HTTP/1.1" 200 123 42 "-" "Test Agent" "session=abc"',
            'apache', 'combined', format_index, expected_count,
        ))

    def test_sample_validation_api_returns_preview(self):
        expected = load_manifest()['fixtures']['apache_combined.log']
        response = APIClient().post(
            '/mwla/logfile/validate_sample/',
            {
                'file_object': SimpleUploadedFile(
                    'sample.log',
                    (FIXTURE_DIR / 'apache_combined.log').read_bytes(),
                ),
                'format_kind': expected['format_kind'],
                'format_name': expected['format_name'],
                'file_format': expected['format_string'],
            },
            format='multipart',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['sample_count'], 5)
        self.assertEqual(response.data['valid_count'], 5)


class AccessLogParserRegressionTests(TestCase):
    """Lock down the current normal-input parser results."""

    @classmethod
    def setUpTestData(cls):
        cls.project = LogMaster.objects.create(
            project_name="parser-regression",
            project_description="synthetic test project",
            creator="test-suite",
        )
        cls.manifest = load_manifest()

    def _parse_fixture(self, filename, diff_hour=0):
        expected = self.manifest["fixtures"][filename]
        logfile = LogFile.objects.create(
            project=self.project,
            file_name=filename,
            file_object="test-only/unused.log",
            file_format=expected["format_string"],
            format_kind=expected["format_kind"],
            format_name=expected["format_name"],
            file_size=(FIXTURE_DIR / filename).stat().st_size,
            server_name="test-server",
            instance_name="test-instance",
        )

        with tempfile.TemporaryDirectory() as temporary_directory:
            source_path = Path(temporary_directory) / filename
            shutil.copyfile(FIXTURE_DIR / filename, source_path)
            parser = DynamicLogDetailViewSet()

            if expected["format_kind"] == "app":
                output_name = parser.parse_log_div_app(
                    str(source_path),
                    str(logfile.logfile_id),
                    0,
                    None,
                    None,
                    0,
                    diff_hour,
                )
            else:
                output_name = parser.parse_log_div(
                    str(source_path),
                    str(logfile.logfile_id),
                    0,
                    None,
                    None,
                    0,
                    diff_hour,
                )

            with open(output_name, newline="", encoding="utf-8") as output:
                return list(csv.DictReader(output))

    def _assert_web_fixture(self, filename):
        expected = self.manifest["fixtures"][filename]
        rows = self._parse_fixture(filename)

        self.assertEqual(len(rows), expected["expected_parsed_count"])
        self.assertEqual(
            Counter(row["fstatus"] for row in rows),
            Counter(expected["status_counts"]),
        )
        self.assertEqual(
            sum(int(row["fbyte"]) for row in rows), expected["bytes_sum"]
        )
        self.assertEqual(
            rows[0]["fdatetime"],
            expected["first_timestamp"][:19]
            .replace("-", "")
            .replace("T", "")
            .replace(":", ""),
        )
        self.assertEqual(
            rows[-1]["fdatetime"],
            expected["last_timestamp"][:19]
            .replace("-", "")
            .replace("T", "")
            .replace(":", ""),
        )

    def test_apache_baseline(self):
        self._assert_web_fixture("apache_combined.log")

    def test_nginx_baseline(self):
        self._assert_web_fixture("nginx_combined.log")

    def test_iis_w3c_baseline(self):
        self._assert_web_fixture("iis_w3c.log")

    def test_application_time_format_2_baseline(self):
        expected = self.manifest["fixtures"]["app_time_format_2.log"]
        rows = self._parse_fixture("app_time_format_2.log")

        self.assertEqual(len(rows), expected["expected_parsed_count"])
        self.assertEqual(rows[0]["fdatetime"], "20260811103000")
        self.assertEqual(rows[-1]["fdatetime"], "20260811103004")
        self.assertEqual(
            [row["log_line"] for row in rows],
            (FIXTURE_DIR / "app_time_format_2.log").read_text(
                encoding="utf-8"
            ).splitlines(),
        )


class CoreModelRegressionTests(TestCase):
    def test_project_and_logfile_relationship(self):
        project = LogMaster.objects.create(
            project_name="model-regression",
            project_description="synthetic model test",
            creator="test-suite",
        )
        logfile = LogFile.objects.create(
            project=project,
            file_name="synthetic.log",
            file_object="test-only/synthetic.log",
            file_format="%h %l %u %t \\\"%r\\\" %>s %b",
            format_kind="apache",
            format_name="test",
            file_size=123,
            server_name="server-a",
            instance_name="instance-a",
        )

        self.assertEqual(logfile.project, project)
        self.assertEqual(project.logfile_set.count(), 1)
        project.delete()
        self.assertFalse(LogFile.objects.filter(pk=logfile.pk).exists())


class AuthenticationApiRegressionTests(TestCase):
    def test_username_and_password_login_returns_token(self):
        User.objects.create_user(
            username="regression-user",
            email="regression-user@example.test",
            password="synthetic-test-password",
        )

        response = APIClient().post(
            "/mwla/rest-auth/login/",
            {
                "username": "regression-user",
                "password": "synthetic-test-password",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("key", response.data)


class DynamicLogSchemaRegressionTests(TransactionTestCase):
    """Exercise real dynamic table creation in the isolated test database."""

    def test_project_delete_drops_dynamic_table_without_deleting_its_rows(self):
        client = APIClient()
        with tempfile.TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                project = LogMaster.objects.create(
                    project_name='fast-project-delete',
                    project_description='delete regression',
                    creator='test-suite',
                )
                project_id = str(project.project_id)
                response = client.post(
                    '/mwla/logmaster/create_dynamic_logdetail/',
                    {'project_id': project_id}, format='json',
                )
                self.assertEqual(response.status_code, 200)
                logfile = LogFile.objects.create(
                    project=project,
                    file_name='delete.log',
                    file_object=SimpleUploadedFile('delete.log', b'log data'),
                    file_format='%h %>s',
                    format_kind='apache',
                    format_name='delete-test',
                    file_size=8,
                    server_name='server',
                    instance_name='instance',
                )
                schema = ModelSchema.objects.get(name='logdetail_' + project_id)
                dynamic_model = schema.as_model()
                dynamic_model.objects.bulk_create([
                    dynamic_model(logfile_id=str(logfile.logfile_id))
                    for _ in range(100)
                ])
                LogDetailV2.objects.create(logfile=logfile, status=200)
                table_name = dynamic_model._meta.db_table
                storage_delete_atomic_states = []
                original_storage_delete = logfile.file_object.storage.delete

                def tracked_storage_delete(name):
                    storage_delete_atomic_states.append(connection.in_atomic_block)
                    return original_storage_delete(name)

                with mock.patch.object(
                    logfile.file_object.storage, 'delete',
                    side_effect=tracked_storage_delete,
                ), CaptureQueriesContext(connection) as queries:
                    response = client.delete('/mwla/logmaster/%s/' % project_id)

                self.assertEqual(response.status_code, 204)
                sql = [item['sql'] for item in queries.captured_queries]
                self.assertTrue(any(
                    'DROP TABLE' in query and table_name in query
                    for query in sql
                ))
                self.assertFalse(any(
                    'DELETE FROM' in query and table_name in query
                    for query in sql
                ))
                self.assertEqual(storage_delete_atomic_states, [False])
                self.assertFalse(LogMaster.objects.filter(pk=project.pk).exists())
                self.assertFalse(ModelSchema.objects.filter(name='logdetail_' + project_id).exists())
                self.assertFalse(LogDetailV2.objects.filter(logfile_id=logfile.pk).exists())

    def test_create_and_delete_project_logdetail_schema(self):
        project = LogMaster.objects.create(
            project_name="dynamic-schema-regression",
            project_description="synthetic dynamic schema test",
            creator="test-suite",
        )
        project_id = str(project.project_id)
        model_name = "logdetail_" + project_id
        client = APIClient()

        create_response = client.post(
            "/mwla/logmaster/create_dynamic_logdetail/",
            {"project_id": project_id},
            format="json",
        )

        self.assertEqual(create_response.status_code, 200)
        self.assertTrue(ModelSchema.objects.filter(name=model_name).exists())
        dynamic_model = ModelSchema.objects.get(name=model_name).as_model()
        self.assertEqual(dynamic_model.objects.count(), 1)

        delete_response = client.post(
            "/mwla/logmaster/delete_dynamic_logdetail/",
            {"project_id": project_id},
            format="json",
        )

        self.assertEqual(delete_response.status_code, 200)
        self.assertFalse(ModelSchema.objects.filter(name=model_name).exists())

    def test_analysis_work_directory_is_removed_after_failure(self):
        client = APIClient()

        with tempfile.TemporaryDirectory() as parent_directory:
            work_directory = Path(parent_directory) / "failed-analysis-work"

            def create_work_directory(**kwargs):
                work_directory.mkdir()
                return str(work_directory)

            with mock.patch(
                "loganalyzerapi.views.tempfile.mkdtemp",
                side_effect=create_work_directory,
            ):
                response = client.post(
                    "/mwla/logdetail_dynamic/",
                    {
                        "project_id": "00000000-0000-0000-0000-000000000000",
                        "logfile_id": [],
                        "diff_hour": 0,
                    },
                    format="json",
                )

            self.assertEqual(response.status_code, 500)
            self.assertFalse(work_directory.exists())

    def test_minimal_upload_and_analysis_api_workflow(self):
        manifest = load_manifest()
        expected = manifest["fixtures"]["apache_combined.log"]
        client = APIClient()

        with tempfile.TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                project_response = client.post(
                    "/mwla/logmaster/",
                    {
                        "project_name": "api-workflow-regression",
                        "project_description": "synthetic API workflow",
                        "creator": "test-suite",
                    },
                    format="json",
                )
                self.assertEqual(project_response.status_code, 201)
                project_id = project_response.data["project_id"]
                model_name = "logdetail_" + project_id

                schema_response = client.post(
                    "/mwla/logmaster/create_dynamic_logdetail/",
                    {"project_id": project_id},
                    format="json",
                )
                self.assertEqual(schema_response.status_code, 200)
                self.assertEqual(
                    set(
                        FieldSchema.objects.filter(
                            model_schema__name=model_name,
                            name__in=('log_line', 'frequest', 'freferer', 'fuser_agent'),
                        ).values_list('name', 'data_type', 'max_length')
                    ),
                    {
                        ('log_line', 'text', None),
                        ('frequest', 'text', None),
                        ('freferer', 'text', None),
                        ('fuser_agent', 'text', None),
                    },
                )

                upload = SimpleUploadedFile(
                    "apache_combined.log",
                    (FIXTURE_DIR / "apache_combined.log").read_bytes(),
                    content_type="text/plain",
                )
                logfile_response = client.post(
                    "/mwla/logfile/",
                    {
                        "project": project_id,
                        "file_name": "apache_combined.log",
                        "file_object": upload,
                        "file_format": expected["format_string"],
                        "format_kind": expected["format_kind"],
                        "format_name": expected["format_name"],
                        "file_size": upload.size,
                        "server_name": "test-server",
                        "instance_name": "test-instance",
                    },
                    format="multipart",
                )
                self.assertEqual(logfile_response.status_code, 201)
                logfile_id = logfile_response.data["logfile_id"]

                duplicate_upload = SimpleUploadedFile(
                    "apache_combined-copy.log",
                    (FIXTURE_DIR / "apache_combined.log").read_bytes(),
                    content_type="text/plain",
                )
                duplicate_response = client.post(
                    "/mwla/logfile/",
                    {
                        "project": project_id,
                        "file_name": "apache_combined-copy.log",
                        "file_object": duplicate_upload,
                        "file_format": expected["format_string"],
                        "format_kind": expected["format_kind"],
                        "format_name": expected["format_name"],
                        "file_size": duplicate_upload.size,
                        "server_name": "test-server",
                        "instance_name": "test-instance",
                    },
                    format="multipart",
                )
                self.assertEqual(duplicate_response.status_code, 400)
                self.assertIn("file_object", duplicate_response.data)

                analysis_work_directory = Path(media_root) / "analysis-work"

                def create_analysis_work_directory(**kwargs):
                    analysis_work_directory.mkdir()
                    return str(analysis_work_directory)

                with override_settings(LOG_PARSER_SPLIT_SIZE_BYTES=300):
                    with mock.patch(
                        "loganalyzerapi.views.tempfile.mkdtemp",
                        side_effect=create_analysis_work_directory,
                    ):
                        analysis_response = client.post(
                            "/mwla/logdetail_dynamic/",
                            {
                                "project_id": project_id,
                                "logfile_id": [logfile_id],
                                "diff_hour": 0,
                            },
                            format="json",
                        )
                self.assertEqual(analysis_response.status_code, 200)
                self.assertFalse(analysis_work_directory.exists())
                self.assertEqual(analysis_response.data["source_count"], 5)
                self.assertEqual(analysis_response.data["parsed_count"], 5)
                self.assertEqual(analysis_response.data["rejected_count"], 0)
                self.assertEqual(analysis_response.data["stored_count"], 5)
                expected_v2_count = 0 if settings.LOG_STORAGE_MODE == 'dynamic' else 5
                self.assertEqual(analysis_response.data["files"][0]["v2_count"], expected_v2_count)
                self.assertTrue(
                    analysis_response.data["files"][0]["v2_comparison"]["matches"]
                )
                self.assertEqual(analysis_response.data["status"], "COMPLETED")
                job = LogAnalysisJob.objects.get(
                    job_id=analysis_response.data["files"][0]["job_id"]
                )
                self.assertEqual(job.status, "COMPLETED")
                self.assertEqual(job.source_count, 5)
                self.assertEqual(job.stored_count, 5)
                self.assertEqual(job.phase, 'VERIFYING')
                self.assertIsNotNone(job.run_id)
                job_response = client.get(
                    "/mwla/loganalysisjob/",
                    {"logfile": logfile_id, "run_id": str(job.run_id)},
                )
                self.assertEqual(job_response.status_code, 200)
                self.assertEqual(job_response.data["count"], 1)
                self.assertEqual(
                    job_response.data["results"][0]["status"], "COMPLETED"
                )

                retry_response = client.post(
                    "/mwla/logdetail_dynamic/",
                    {
                        "project_id": project_id,
                        "logfile_id": [logfile_id],
                        "diff_hour": 0,
                    },
                    format="json",
                )
                self.assertEqual(retry_response.status_code, 200)
                self.assertEqual(
                    retry_response.data["files"][0]["status"],
                    "ALREADY_COMPLETED",
                )
                self.assertEqual(
                    LogAnalysisJob.objects.filter(
                        logfile_id=logfile_id
                    ).count(),
                    2,
                )

                dynamic_model = ModelSchema.objects.get(
                    name=model_name
                ).as_model()
                self.assertEqual(
                    dynamic_model.objects.filter(
                        logfile_id=logfile_id
                    ).count(),
                    expected["expected_parsed_count"],
                )
                self.assertEqual(
                    LogDetailV2.objects.filter(logfile_id=logfile_id).count(),
                    expected_v2_count,
                )

                empty_filter = {
                    "dateFromValue": "",
                    "dateToValue": "",
                    "timeFromValue": "",
                    "timeToValue": "",
                    "ttFromValue": "",
                    "ttToValue": "",
                    "conditionValue": "",
                    "searchValue": "",
                    "excludeSearch": "",
                    "project_id": project_id,
                    "projectServers": None,
                }
                statistics_response = client.post(
                    "/mwla/logdetail_dynamic/statistics/",
                    {
                        "project_id": project_id,
                        "type": 1,
                        "N": 1,
                        "filter": empty_filter,
                    },
                    format="json",
                )
                self.assertEqual(statistics_response.status_code, 200)
                self.assertEqual(statistics_response.data["results"], [])

                chart_response = client.post(
                    "/mwla/logdetail_dynamic/chartdata/",
                    {
                        "project_id": project_id,
                        "type": "1",
                        "kind": 1,
                        "filter": empty_filter,
                    },
                    format="json",
                )
                self.assertEqual(chart_response.status_code, 200)
                self.assertEqual(chart_response.data["resultX"], [])
                self.assertEqual(chart_response.data["resultY"], [])

                findings_response = client.post(
                    "/mwla/logdetail_dynamic/findings/",
                    {
                        "project_id": project_id,
                        "filter": empty_filter,
                    },
                    format="json",
                )
                self.assertEqual(findings_response.status_code, 200)
                self.assertEqual(findings_response.data["findingsResult"], [])
                self.assertEqual(findings_response.data["totalCnt"], 0)

                delete_response = client.post(
                    "/mwla/logmaster/delete_dynamic_logdetail/",
                    {"project_id": project_id},
                    format="json",
                )
                self.assertEqual(delete_response.status_code, 200)

    @override_settings(LOG_STORAGE_MODE='dynamic')
    def test_dynamic_mode_never_calls_v2_mirroring_or_comparison(self):
        with mock.patch.object(DynamicLogDetailViewSet, 'mirror_dynamic_rows_to_v2') as mirror, mock.patch.object(DynamicLogDetailViewSet, 'compare_dynamic_v2') as compare:
            self.test_minimal_upload_and_analysis_api_workflow()
            mirror.assert_not_called()
            compare.assert_not_called()

    @override_settings(LOG_STORAGE_MODE='dual')
    def test_explicit_dual_mode_remains_available(self):
        self.test_minimal_upload_and_analysis_api_workflow()

    def test_invalid_rows_are_counted_and_persisted(self):
        self._check_row_loss(300, True)

    def test_exactly_one_percent_row_loss_fails(self):
        self._check_row_loss(295, False)

    def test_above_one_percent_row_loss_fails(self):
        self._check_row_loss(0, False)

    def test_nul_row_below_one_percent_completes(self):
        self._check_row_loss(300, True, nul_row=True)

    def _check_row_loss(self, extra_valid_rows, succeeds, nul_row=False):
        manifest = load_manifest()
        expected = manifest["fixtures"]["apache_mixed_invalid.log"]
        client = APIClient()
        project = LogMaster.objects.create(
            project_name="reject-regression",
            project_description="synthetic reject test",
            creator="test-suite",
        )
        project_id = str(project.project_id)
        model_name = "logdetail_" + project_id

        with tempfile.TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                schema_response = client.post(
                    "/mwla/logmaster/create_dynamic_logdetail/",
                    {"project_id": project_id},
                    format="json",
                )
                self.assertEqual(schema_response.status_code, 200)

                source = (FIXTURE_DIR / "apache_mixed_invalid.log").read_bytes().splitlines()
                if nul_row:
                    source[1] = b'\0' * 1174 + source[0]
                upload = SimpleUploadedFile(
                    "apache_mixed_invalid.log",
                    b'\n'.join(source) + b'\n'
                    + (source[0] + b'\n') * extra_valid_rows,
                    content_type="text/plain",
                )
                logfile = LogFile.objects.create(
                    project=project,
                    file_name="apache_mixed_invalid.log",
                    file_object=upload,
                    file_format=expected["format_string"],
                    format_kind=expected["format_kind"],
                    format_name=expected["format_name"],
                    file_size=upload.size,
                    server_name="test-server",
                    instance_name="test-instance",
                )

                response = client.post(
                    "/mwla/logdetail_dynamic/",
                    {
                        "project_id": project_id,
                        "logfile_id": [str(logfile.logfile_id)],
                        "diff_hour": 0,
                    },
                    format="json",
                )

                if not succeeds:
                    self.assertEqual(response.status_code, 500)
                    self.assertEqual(response.data['status'], 'FAILED')
                    self.assertEqual(response.data['rejected_count'], 3)
                    self.assertEqual(response.data['stored_count'], 0)
                    self.assertEqual(len(response.data['files'][0]['failure_samples']), 3)
                    job = LogAnalysisJob.objects.get(logfile=logfile)
                    self.assertEqual(job.status, 'FAILED')
                    self.assertIn('below 1%', job.error_message)
                    dynamic_model = ModelSchema.objects.get(name=model_name).as_model()
                    self.assertEqual(dynamic_model.objects.filter(logfile_id=logfile.pk).count(), 0)
                    client.post('/mwla/logmaster/delete_dynamic_logdetail/',
                                {'project_id': project_id}, format='json')
                    return
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data["source_count"], 5 + extra_valid_rows)
                self.assertEqual(response.data["parsed_count"], 2 + extra_valid_rows)
                self.assertEqual(response.data["rejected_count"], 3)
                self.assertEqual(response.data["stored_count"], 2 + extra_valid_rows)
                self.assertEqual(response.data["status"], "COMPLETED")
                job = LogAnalysisJob.objects.get(
                    job_id=response.data["files"][0]["job_id"]
                )
                self.assertEqual(job.status, "COMPLETED")
                self.assertEqual(job.rejected_count, 3)
                details = response.data['files'][0]
                self.assertEqual(sum(item['count'] for item in details['failure_reasons']), 3)
                self.assertEqual(len(details['failure_samples']), 3)
                if nul_row:
                    self.assertEqual(details['failure_samples'][0]['error_code'], 'invalid_nul')
                    self.assertNotIn('\0', details['failure_samples'][0]['raw_line_excerpt'])
                    self.assertTrue(details['failure_samples'][0]['truncated'])
                self.assertEqual(
                    response.data["source_count"],
                    response.data["parsed_count"]
                    + response.data["rejected_count"],
                )

                rejects = list(logfile.parse_rejects.values_list(
                    "line_number", "error_code"
                ))
                self.assertEqual(rejects, [
                    (2, "invalid_nul" if nul_row else "field_count_mismatch"),
                    (3, "invalid_status"),
                    (4, "invalid_timestamp"),
                ])
                repeated = client.post('/mwla/logdetail_dynamic/', {
                    'project_id': project_id, 'logfile_id': [str(logfile.logfile_id)], 'diff_hour': 0,
                }, format='json')
                self.assertEqual(repeated.status_code, 200)
                self.assertEqual(repeated.data['source_count'], 5 + extra_valid_rows)
                self.assertEqual(repeated.data['rejected_count'], 3)
                self.assertEqual(repeated.data['files'][0]['failure_samples'], details['failure_samples'])
                dynamic_model = ModelSchema.objects.get(
                    name=model_name
                ).as_model()
                self.assertEqual(
                    dynamic_model.objects.filter(
                        logfile_id=str(logfile.logfile_id)
                    ).count(),
                    2 + extra_valid_rows,
                )

                delete_response = client.post(
                    "/mwla/logmaster/delete_dynamic_logdetail/",
                    {"project_id": project_id},
                    format="json",
                )
                self.assertEqual(delete_response.status_code, 200)

    def test_copy_failure_removes_partial_rows_and_marks_job_failed(self):
        manifest = load_manifest()
        expected = manifest["fixtures"]["apache_combined.log"]
        client = APIClient()
        project = LogMaster.objects.create(
            project_name="copy-failure-regression",
            project_description="synthetic COPY failure",
            creator="test-suite",
        )
        project_id = str(project.project_id)
        model_name = "logdetail_" + project_id

        with tempfile.TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                schema_response = client.post(
                    "/mwla/logmaster/create_dynamic_logdetail/",
                    {"project_id": project_id},
                    format="json",
                )
                self.assertEqual(schema_response.status_code, 200)
                upload = SimpleUploadedFile(
                    "apache_combined.log",
                    (FIXTURE_DIR / "apache_combined.log").read_bytes(),
                    content_type="text/plain",
                )
                logfile = LogFile.objects.create(
                    project=project,
                    file_name="apache_combined.log",
                    file_object=upload,
                    file_format=expected["format_string"],
                    format_kind=expected["format_kind"],
                    format_name=expected["format_name"],
                    file_size=upload.size,
                    server_name="test-server",
                    instance_name="test-instance",
                )

                with mock.patch(
                    "loganalyzerapi.views.DynamicLogDetailViewSet.copy_csv_to_model",
                    side_effect=RuntimeError("synthetic COPY failure"),
                ):
                    response = client.post(
                        "/mwla/logdetail_dynamic/",
                        {
                            "project_id": project_id,
                            "logfile_id": [str(logfile.logfile_id)],
                            "diff_hour": 0,
                        },
                        format="json",
                    )

                self.assertEqual(response.status_code, 500)
                job = LogAnalysisJob.objects.get(logfile=logfile)
                self.assertEqual(job.status, "FAILED")
                self.assertIn("synthetic COPY failure", job.error_message)
                dynamic_model = ModelSchema.objects.get(
                    name=model_name
                ).as_model()
                self.assertEqual(
                    dynamic_model.objects.filter(
                        logfile_id=str(logfile.logfile_id)
                    ).count(),
                    0,
                )
                self.assertEqual(logfile.parse_rejects.count(), 0)

                delete_response = client.post(
                    "/mwla/logmaster/delete_dynamic_logdetail/",
                    {"project_id": project_id},
                    format="json",
                )
                self.assertEqual(delete_response.status_code, 200)
