import importlib.util
import io
import subprocess
import unittest
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "termux_for_hack"
    / "m-termux.py"
)
SPEC = importlib.util.spec_from_file_location("termux_setup", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Could not load the Termux setup module.")
setup = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(setup)


class ProfileTests(unittest.TestCase):
    def test_basic_profile_is_small(self):
        self.assertEqual(
            setup.PROFILE_PACKAGES["basic"],
            ("curl", "git", "python", "wget"),
        )

    def test_all_profile_contains_unique_packages(self):
        packages = setup.PROFILE_PACKAGES["all"]
        self.assertEqual(len(packages), len(set(packages)))
        for name in ("basic", "developer", "security"):
            self.assertTrue(set(setup.PROFILE_PACKAGES[name]) <= set(packages))

    def test_termux_detection(self):
        self.assertTrue(
            setup.is_termux({"PREFIX": "/data/data/com.termux/files/usr"})
        )
        self.assertTrue(setup.is_termux({"TERMUX_VERSION": "0.118.0"}))
        self.assertFalse(setup.is_termux({}))

    def test_planned_commands(self):
        commands = setup.planned_commands(
            "/fake/pkg",
            ("git", "python"),
            upgrade=True,
        )
        self.assertEqual(
            commands,
            [
                ["/fake/pkg", "update"],
                ["/fake/pkg", "upgrade", "-y"],
                ["/fake/pkg", "install", "-y", "git", "python"],
            ],
        )


class CliTests(unittest.TestCase):
    def test_default_run_is_dry_run(self):
        output = io.StringIO()
        result = setup.main([], run=self.fail, output=output, environment={})
        self.assertEqual(result, 0)
        self.assertIn("Dry run only", output.getvalue())
        self.assertIn("curl, git, python, wget", output.getvalue())

    def test_list_profiles(self):
        output = io.StringIO()
        result = setup.main(["--list"], run=self.fail, output=output, environment={})
        self.assertEqual(result, 0)
        self.assertIn("developer", output.getvalue())
        self.assertIn("nmap", output.getvalue())

    def test_install_is_blocked_outside_termux(self):
        output = io.StringIO()
        result = setup.main(
            ["--install", "--yes"],
            run=self.fail,
            output=output,
            environment={},
            which=lambda _name: "/fake/pkg",
        )
        self.assertEqual(result, 1)
        self.assertIn("inside the Termux", output.getvalue())

    def test_declining_confirmation_skips_commands(self):
        output = io.StringIO()
        environment = {"PREFIX": "/data/data/com.termux/files/usr"}
        result = setup.main(
            ["--install"],
            run=self.fail,
            input_fn=lambda _prompt: "n",
            output=output,
            environment=environment,
            which=lambda _name: "/fake/pkg",
        )
        self.assertEqual(result, 0)
        self.assertIn("cancelled", output.getvalue().lower())

    def test_confirmed_install_runs_expected_command(self):
        output = io.StringIO()
        calls = []
        environment = {"PREFIX": "/data/data/com.termux/files/usr"}

        def fake_run(command, check):
            calls.append((command, check))
            return subprocess.CompletedProcess(command, 0)

        result = setup.main(
            ["--profile", "developer", "--install"],
            run=fake_run,
            input_fn=lambda _prompt: "yes",
            output=output,
            environment=environment,
            which=lambda _name: "/fake/pkg",
        )
        self.assertEqual(result, 0)
        self.assertEqual(len(calls), 1)
        command, check = calls[0]
        self.assertEqual(
            command,
            [
                "/fake/pkg",
                "install",
                "-y",
                "clang",
                "cmake",
                "git",
                "make",
                "pkg-config",
                "python",
            ],
        )
        self.assertFalse(check)

    def test_upgrade_runs_before_install(self):
        calls = []
        environment = {"PREFIX": "/data/data/com.termux/files/usr"}

        def fake_run(command, check):
            calls.append(command)
            return subprocess.CompletedProcess(command, 0)

        result = setup.main(
            ["--upgrade", "--install", "--yes"],
            run=fake_run,
            output=io.StringIO(),
            environment=environment,
            which=lambda _name: "/fake/pkg",
        )
        self.assertEqual(result, 0)
        self.assertEqual(calls[0], ["/fake/pkg", "update"])
        self.assertEqual(calls[1], ["/fake/pkg", "upgrade", "-y"])
        self.assertEqual(calls[2][:3], ["/fake/pkg", "install", "-y"])

    def test_failed_command_stops_sequence(self):
        calls = []
        environment = {"PREFIX": "/data/data/com.termux/files/usr"}

        def fake_run(command, check):
            calls.append(command)
            return subprocess.CompletedProcess(command, 3)

        result = setup.main(
            ["--upgrade", "--install", "--yes"],
            run=fake_run,
            output=io.StringIO(),
            environment=environment,
            which=lambda _name: "/fake/pkg",
        )
        self.assertEqual(result, 3)
        self.assertEqual(len(calls), 1)

    def test_yes_requires_install(self):
        with self.assertRaises(SystemExit) as raised:
            setup.main(["--yes"], output=io.StringIO(), environment={})
        self.assertEqual(raised.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
