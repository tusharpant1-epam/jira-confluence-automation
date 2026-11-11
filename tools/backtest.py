"""Standalone acceptance-test simulation for project-register integrity.

This exercises a small in-memory model, not an application API or database.
"""

import unittest


REQUIRED_FIELDS = ("project_code", "project_name", "program", "status", "health")


class ProjectRegister:
    def __init__(self, programs):
        self.programs = set(programs)
        self.projects = {}

    def add_project(self, project):
        missing_fields = [
            field
            for field in REQUIRED_FIELDS
            if project.get(field) is None
            or (
                isinstance(project.get(field), str)
                and not project[field].strip()
            )
        ]
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        owner = project.get("delivery_manager")
        if owner is None or (isinstance(owner, str) and not owner.strip()):
            raise ValueError("Project must have an accountable delivery manager")
        if project["program"] not in self.programs:
            raise ValueError(f"Unknown program: {project['program']}")
        if project["project_code"] in self.projects:
            raise ValueError(f"Duplicate project code: {project['project_code']}")

        stored_project = dict(project)
        stored_project["archived"] = False
        self.projects[stored_project["project_code"]] = stored_project

    def archive_project(self, project_code):
        self.projects[project_code]["archived"] = True

    def active_projects(self):
        return [
            project
            for project in self.projects.values()
            if not project["archived"]
        ]


class RegisterIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.register = ProjectRegister(programs={"Payments"})

    def valid_project(self, **overrides):
        project = {
            "project_code": "PAY-001",
            "project_name": "Payment modernization",
            "program": "Payments",
            "status": "active",
            "health": "green",
            "delivery_manager": "Morgan Lee",
        }
        project.update(overrides)
        return project

    def test_project_codes_must_be_unique(self):
        self.register.add_project(self.valid_project())
        with self.assertRaisesRegex(ValueError, "Duplicate project code"):
            self.register.add_project(
                self.valid_project(project_name="Another project")
            )

    def test_required_fields_must_be_present(self):
        for field in REQUIRED_FIELDS:
            with self.subTest(field=field):
                project = self.valid_project()
                project[field] = ""
                with self.assertRaisesRegex(ValueError, "Missing required fields"):
                    self.register.add_project(project)

    def test_project_must_reference_an_existing_program(self):
        with self.assertRaisesRegex(ValueError, "Unknown program"):
            self.register.add_project(self.valid_project(program="Unknown"))

    def test_project_must_have_an_accountable_owner(self):
        for owner in (None, ""):
            with self.subTest(owner=owner):
                with self.assertRaisesRegex(ValueError, "delivery manager"):
                    self.register.add_project(
                        self.valid_project(delivery_manager=owner)
                    )

    def test_archiving_preserves_record_and_removes_it_from_active_list(self):
        self.register.add_project(self.valid_project())
        self.register.archive_project("PAY-001")

        self.assertIn("PAY-001", self.register.projects)
        self.assertTrue(self.register.projects["PAY-001"]["archived"])
        self.assertEqual(self.register.active_projects(), [])

    def test_missing_optional_value_is_distinct_from_zero(self):
        missing_budget = self.valid_project()
        zero_budget = self.valid_project(project_code="PAY-002", budget=0)

        self.register.add_project(missing_budget)
        self.register.add_project(zero_budget)

        self.assertNotIn("budget", self.register.projects["PAY-001"])
        self.assertEqual(self.register.projects["PAY-002"]["budget"], 0)


if __name__ == "__main__":
    unittest.main()
