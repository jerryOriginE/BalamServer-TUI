## BALAM Server TUI

**BALAM Server TUI** is a lightweight, single-binary **terminal UI** for monitoring and managing systemd-based BALAM servers.

It features a **log viewer** with real-time tracking, per-service log following, and keyboard-driven navigation. The interface provides **global commands** (database backups, backend updates, start/stop all services) as well as **per-service command management** (start, stop, restart, inspect).

A persistent **status bar** displays server information such as hostname, uptime, load, disk usage, and current log mode. Additional panels expose **service details** including PID, state, memory usage, and **PostgreSQL general status**.

A new **command bar** for complex and scripted operations is currently **work in progress**. Designed for SSH usage, zero setup, and single-binary deployment.

### Other Utilities ###

**todo.txt** - List of TODO utitlies and features to be added to BALAM SERVER TUI
**build.sh** -- Single script to build the single binary for compatibility for many linux/ubuntu versions
 e
