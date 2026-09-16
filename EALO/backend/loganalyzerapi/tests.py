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
from django.test import SimpleTestCase, TestCase, TransactionTestCase
from django.test.utils import override_settings
from django.urls import resolve
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from dynamic_models.models import ModelSchema

from loganalyzerapi.models import LogAnalysisJob, LogDetailV2, LogFile, LogMaster
from loganalyzerapi.parsers import get_parser, validate_log_line
from loganalyzerapi.views import DynamicLogDetailViewSet


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
        self.assertEqual(
            validate_log_line(
                '[12/Aug/2026:00:00:00 700 12',
                'apache', 'combined', apache_index, 3,
            )[0],
            'invalid_status',
        )
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

                upload = SimpleUploadedFile(
                    "apache_mixed_invalid.log",
                    (FIXTURE_DIR / "apache_mixed_invalid.log").read_bytes(),
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

                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data["source_count"], 5)
                self.assertEqual(response.data["parsed_count"], 2)
                self.assertEqual(response.data["rejected_count"], 3)
                self.assertEqual(response.data["stored_count"], 2)
                self.assertEqual(response.data["status"], "PARTIAL")
                job = LogAnalysisJob.objects.get(
                    job_id=response.data["files"][0]["job_id"]
                )
                self.assertEqual(job.status, "PARTIAL")
                self.assertEqual(job.rejected_count, 3)
                self.assertEqual(
                    response.data["source_count"],
                    response.data["parsed_count"]
                    + response.data["rejected_count"],
                )

                rejects = list(logfile.parse_rejects.values_list(
                    "line_number", "error_code"
                ))
                self.assertEqual(rejects, [
                    (2, "field_count_mismatch"),
                    (3, "invalid_status"),
                    (4, "invalid_timestamp"),
                ])
                dynamic_model = ModelSchema.objects.get(
                    name=model_name
                ).as_model()
                self.assertEqual(
                    dynamic_model.objects.filter(
                        logfile_id=str(logfile.logfile_id)
                    ).count(),
                    2,
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
