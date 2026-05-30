# W2 Dispatch 14 - Windows install path normalization

## Result

Completed. `install.sh` now accepts Windows drive-letter absolute skill targets such as `C:/Users/.../.codex/skills/project-init` while preserving the existing POSIX absolute target guard and relative-path rejection.

## Code Changes

- Added `is_safe_skill_target` to centralize allowed target patterns.
- Allowed `[A-Za-z]:/*/skills/project-init` alongside `/*/skills/project-init`.
- Hardened ancestor symlink walk termination for drive-letter paths by stopping on `/`, `.`, or unchanged `dirname` output.
- Normalized `install.sh` to LF so Git Bash can parse it consistently on Windows.

## Validation

Evidence directory: `evidence/dispatch14_windows_install_path_normalization/`

- Git Bash syntax: pass (`01_bash_syntax_install_sh.txt`).
- Line endings: pass, `crlf_count=0` (`02_line_endings.txt`).
- Windows drive-letter target accepted: pass (`03_guard_windows_drive_accepts.txt`).
- POSIX target accepted: pass (`04_guard_posix_accepts.txt`).
- Relative target rejected with rc 3: pass (`05_guard_relative_rejects.txt`).
- Wrong suffix rejected with rc 3: pass (`06_guard_wrong_suffix_rejects.txt`).
- Windows drive-letter ancestor walk terminates: pass (`07_windows_drive_walk_terminates.txt`).
- Actual `codex` install smoke with drive-letter `CODEX_HOME`: pass (`08_actual_codex_drive_install_workspace.txt`, `09_actual_install_checks.json`).
- Actual relative `CODEX_HOME` install rejected and created no target dir: pass (`10_actual_relative_codex_rejects.txt`, `11_actual_relative_checks.txt`).
- `git diff --check`: pass (`12_git_diff_check.txt`).

Relevant validation summary: 15/15 checks recorded ok. `13_git_status_short.txt` is informational and includes unrelated in-flight repo changes from earlier dispatches.

## Install Smoke Details

- Temporary smoke parent: `C:\Users\hamst\AppData\Local\Temp\d14_project_init_smoke_3ex53pwx`
- CODEX_HOME: `C:/Users/hamst/AppData/Local/Temp/d14_project_init_smoke_3ex53pwx/codex_home`
- Installed `SKILL.md`: `True`
- Installed `templates/`: `True`
- Installed `scripts/`: `True`
- Did not copy `reports/`: `True`
- Did not copy `evidence/`: `True`
