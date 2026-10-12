# Termux Setup Helper

<p align="center">
  <strong>A legacy helper for preparing a Termux environment for command-line development and security learning.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Termux-1F8F4A?style=for-the-badge&logo=android&logoColor=white" alt="Termux">
  <img src="https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Status-Legacy%20Project-8A5A00?style=for-the-badge" alt="Legacy project">
</p>

---

## Overview

**Termux Setup Helper** is an older, single-file Python script intended to install a collection of command-line packages in Termux. It was created as a quick setup shortcut, rather than as a configurable package manager.

> [!WARNING]
> **Do not run the current script blindly on a primary device.** It performs broad package updates and installations, uses outdated package names, contains a malformed shell command, and does not reliably launch its optional companion installer. The companion `all-pip-installer` script also tries to install Python standard-library modules as third-party packages. Review the source and install only the packages you actually need.

This README documents the repository as it exists today; it does not claim the legacy installer is fully functional or compatible with current Termux releases.

## Intended Features

- Automate a basic Termux package setup.
- Offer an optional follow-up step for Python packages.
- Keep the implementation as a small, inspectable Python script.
- Serve as a learning example of shell-command automation from Python.

## Requirements

- Android with [Termux](https://termux.dev/) installed.
- Python available inside Termux.
- An internet connection for package downloads.

Typical Termux setup commands include `pkg update` and `pkg install python git`. Run package operations manually so you can review what will change. Root access is not normally required for these basic Termux package operations.

## Inspect the Source

Clone this repository and review the script before considering any execution:

```bash
git clone https://github.com/kaandgnsh/termux-for-hack.git
cd termux-for-hack
sed -n '1,220p' termux_for_hack/m-termux.py
```

**Execution is not recommended until the issues below have been fixed.** Do not follow the original instruction to accept every prompt automatically.

## Known Limitations

- **Outdated package list:** the script attempts to install packages such as Python 2 and separate `pip` commands that may no longer be appropriate.
- **Malformed command:** `pkg;install openssh` is not a valid `pkg install openssh` command.
- **Unreliable companion setup:** the script clones a separate repository and then runs `cd` in a different shell process, so the next command may execute from the wrong directory.
- **Weak error handling:** command failures are not checked before the script reports success.
- **Unmaintained dependency workflow:** the companion installer attempts to install standard-library modules (for example, `os`, `sys`, and `json`) and other questionable package names through `pip`.
- **No automated tests:** compatibility with current Termux versions has not been verified.

## Recommended Improvements

- Replace shell strings with individually validated package operations.
- Check and report each command's exit status.
- Maintain a small, configurable list of supported Termux packages.
- Remove obsolete package names and the unreliable companion-installation flow.
- Add tests and verify behavior on a current Termux installation.

## Responsible Use

Use package setup scripts only on devices and environments you control. Inspect commands before execution, and avoid installing large collections of unrelated packages without a specific need.

## Author

**Kaan DOĞAN** · [GitHub](https://github.com/kaandgnsh) · [LinkedIn](https://www.linkedin.com/in/kaan-do%C4%9Fan-911663280/) · [Instagram](https://instagram.com/kaandgn.sh)

<p align="center">
  <sub>Legacy project · Review before use</sub>
</p>
