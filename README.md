# Termux Setup Helper

<p align="center">
  <strong>A small, interactive package setup CLI for Termux on Android.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Termux-1F8F4A?style=for-the-badge&logo=android&logoColor=white" alt="Termux">
  <img src="https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <a href="https://github.com/kaandgnsh/termux-for-hack/actions/workflows/tests.yml">
    <img src="https://github.com/kaandgnsh/termux-for-hack/actions/workflows/tests.yml/badge.svg?branch=main" alt="GitHub Actions">
  </a>
</p>

---

## Overview

**Termux Setup Helper** simplifies installation of a curated set of command-line packages in [Termux](https://termux.dev/). It provides a few practical profiles, previews the planned actions by default, and requires explicit confirmation before running package-manager commands.

It is a package setup helper, not an exploit framework or an automatic installer for every Python library.

## Features

- **Dry run by default:** preview the selected package list without changing the device.
- **Explicit opt-in:** pass `--install` and confirm before installing anything.
- **Curated profiles:** choose basic, developer, security-lab, or all listed packages.
- **Optional system updates:** `--upgrade` adds `pkg update` and `pkg upgrade` to the plan.
- **No third-party Python dependencies:** the script uses Python's standard library.
- **Failure handling:** stops if a package-manager command fails.
- **Termux check:** actual installation is refused outside a Termux environment.

## Requirements

- Android with [Termux](https://termux.dev/) installed.
- Python 3 available inside Termux.
- An internet connection for package downloads.

Install the minimal tools needed to download and inspect the repository:

```bash
pkg update
pkg install git python
```

These are manual commands; review them before running. Root access is not required for ordinary Termux package management.

## Quick Start

Clone the repository:

```bash
git clone https://github.com/kaandgnsh/termux-for-hack.git
cd termux-for-hack
```

List the available profiles:

```bash
python termux_for_hack/m-termux.py --list
```

Preview the default profile. This makes no changes:

```bash
python termux_for_hack/m-termux.py
```

Install the developer profile after reviewing the displayed plan:

```bash
python termux_for_hack/m-termux.py --profile developer --install
```

The script asks for confirmation. To also update the package index and upgrade existing packages, add `--upgrade`:

```bash
python termux_for_hack/m-termux.py --profile basic --upgrade --install
```

Only skip the final confirmation when you have reviewed the exact operations:

```bash
python termux_for_hack/m-termux.py --profile basic --install --yes
```

## Package Profiles

| Profile | Packages |
|:--|:--|
| `basic` | `curl`, `git`, `python`, `wget` |
| `developer` | `clang`, `cmake`, `git`, `make`, `pkg-config`, `python` |
| `security` | `curl`, `git`, `nmap`, `openssh`, `openssl`, `perl`, `php`, `python`, `ruby`, `wget` |
| `all` | The de-duplicated union of the listed profiles |

The `security` profile provides general command-line tools useful in authorized labs; installing them does not grant permission to scan or access systems you do not own.

## CLI Reference

| Option | Description |
|:--|:--|
| `--profile NAME` | Select `basic`, `developer`, `security`, or `all`. Default: `basic`. |
| `--list` | List profiles and package names. |
| `--upgrade` | Preview or run `pkg update` and `pkg upgrade -y` before installation. |
| `--install` | Proceed from preview to confirmed installation. |
| `--yes` | Skip confirmation; valid only with `--install`. |
| `-h, --help` | Display help. |

The script invokes `pkg` with argument lists rather than shell command strings. It installs only the packages shown in the selected profile and does not attempt to install Python's standard-library modules through `pip`.

## Troubleshooting

**“Run this command from inside the Termux Android app.”**  
Execute the script within Termux, not a desktop Linux terminal or a generic Python environment.

**A package command fails.**  
The script stops and reports the failing command's exit status. Check the package name, network connection, and Termux repository configuration, then retry the specific package operation manually if needed.

## Tests

Run the tests from the repository root:

```bash
python -m unittest discover -s tests -v
```

GitHub Actions runs the test suite on Python 3.10, 3.11, and 3.12. The tests mock package-manager execution and do not install packages on the CI runner.

## Project Structure

```text
termux-for-hack/
├── .github/
│   └── workflows/
│       └── tests.yml
├── termux_for_hack/
│   └── m-termux.py
├── tests/
│   └── test_termux_setup.py
└── README.md
```

## Responsible Use

Install only packages you need, review system update plans, and use network tools only in environments you own or are authorized to assess.

## Author

**Kaan DOĞAN** · [GitHub](https://github.com/kaandgnsh) · [LinkedIn](https://www.linkedin.com/in/kaan-do%C4%9Fan-911663280/) · [Instagram](https://instagram.com/kaandgn.sh)

<p align="center">
  <sub>Preview first. Confirm explicitly. Keep your environment under control.</sub>
</p>
