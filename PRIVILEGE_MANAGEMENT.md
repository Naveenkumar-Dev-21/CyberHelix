# Privilege Management System

## Overview

The Automated Pentesting Framework includes a comprehensive privilege management system that securely handles sudo operations and classifies tasks by their privilege requirements. This system ensures that:

1. **Security**: Passwords are handled securely without exposing them in command line arguments
2. **Safety**: Commands are classified and validated before execution
3. **Transparency**: All privilege escalations are logged and justified
4. **Compliance**: Only authorized operations are performed automatically

## Features

### Task Classification

The system classifies pentesting tasks into privilege levels:

- **USER**: No special privileges required (e.g., web scanning, SQL injection testing)
- **SUDO**: Requires root/administrator privileges (e.g., SYN scanning, packet capture)
- **NETWORK**: Network-related operations that may need privileges
- **SYSTEM**: System-level operations (typically requires root)

### Safety Validation

Each command is validated for:
- **Safe for Automation**: Whether the command can be run automatically
- **Requires Confirmation**: Whether user confirmation is needed before execution
- **Dangerous Patterns**: Detection of potentially harmful commands

### Secure Password Handling

- Passwords are never exposed in command line arguments
- Environment variables and temporary scripts are used securely
- Automatic cleanup of sensitive temporary files

## Usage

### Setting Sudo Password

```bash
# Set sudo password securely (interactive prompt)
python -m src.main privilege --set-password
```

The password is stored in the environment variable `PENTEST_SUDO_PASS` for the session.

### Checking System Status

```bash
# View privilege management status
python -m src.main privilege --status
```

### Listing Task Classifications

```bash
# List all classified pentesting tasks
python -m src.main privilege --list-tasks
```

### Testing Command Classification

```bash
# Test how a command would be classified
python -m src.main privilege --test-command "nmap -sS 192.168.1.1"
```

### Classifying Specific Tasks

```bash
# Get detailed requirements for a specific task
python -m src.main privilege --classify nmap_syn_scan
```

## Programmatic Usage

### Basic Usage

```python
from src.privilege_manager import PrivilegeManager

# Initialize privilege manager
privilege_manager = PrivilegeManager()

# Classify a command
command = ["nmap", "-sS", "192.168.1.1"]
classification = privilege_manager.classify_command(command)

# Execute with appropriate privileges
sudo_password = os.getenv('PENTEST_SUDO_PASS')
result = privilege_manager.execute_with_privileges(command, sudo_password)
```

### Safety Validation

```python
# Validate command safety
command = ["nmap", "-sT", "example.com"]
is_safe, safety_message = privilege_manager.validate_safe_execution(command)

if is_safe:
    result = privilege_manager.execute_with_privileges(command)
else:
    print(f"Command blocked: {safety_message}")
```

## Task Classifications

### Network Scanning

| Task | Privilege Level | Auto-Safe | Justification |
|------|----------------|-----------|---------------|
| `nmap_tcp_connect` | USER | ✅ | Uses standard socket connections |
| `nmap_syn_scan` | SUDO | ✅ | Requires raw socket access for stealth |
| `nmap_udp_scan` | SUDO | ✅ | UDP scanning requires raw socket access |
| `nmap_os_detection` | SUDO | ✅ | OS detection requires raw socket access |

### Web Application Testing

| Task | Privilege Level | Auto-Safe | Justification |
|------|----------------|-----------|---------------|
| `web_directory_scan` | USER | ✅ | Uses HTTP requests |
| `sql_injection_test` | USER | ✅ | Testing through web interfaces |
| `nuclei_scan` | USER | ✅ | Network connection-based testing |

### Wireless Operations

| Task | Privilege Level | Auto-Safe | Justification |
|------|----------------|-----------|---------------|
| `wifi_monitor_mode` | SUDO | ❌ | Requires interface control, needs confirmation |
| `wifi_deauth` | SUDO | ❌ | Attack operation, needs confirmation |
| `wifi_handshake_capture` | SUDO | ✅ | Passive monitoring operation |

### System Operations

| Task | Privilege Level | Auto-Safe | Justification |
|------|----------------|-----------|---------------|
| `packet_capture` | SUDO | ✅ | Raw packet capture requires root |
| `mac_address_change` | SUDO | ❌ | Interface modification, needs confirmation |
| `port_binding` | SUDO | ✅ | Binding to privileged ports (<1024) |

## Integration with Framework

### Reconnaissance Module

The reconnaissance module automatically uses the privilege manager:

```python
# In reconnaissance.py
def nmap_scan_with_root(self, classification):
    privilege_manager = PrivilegeManager()
    
    # Validate safety
    is_safe, safety_msg = privilege_manager.validate_safe_execution(nmap_cmd)
    if not is_safe:
        logger.warning(f"Command safety check failed: {safety_msg}")
        return self.nmap_scan_basic(target)
    
    # Execute with secured sudo password
    sudo_password = os.getenv('PENTEST_SUDO_PASS')
    result = run_command(nmap_cmd, use_sudo=True, sudo_password=sudo_password)
```

### Utils Module

The `run_command` function automatically integrates with the privilege manager:

```python
def run_command(command, timeout=60, use_sudo=False, sudo_password=None):
    privilege_manager = PrivilegeManager()
    
    # Automatically determine privilege requirements
    if use_sudo or privilege_manager.classify_command(command).privilege_level.value != 'user':
        return privilege_manager.execute_with_privileges(command, sudo_password, timeout)
    
    # Execute normally for user-level commands
    # ...
```

## Security Considerations

### Password Security

- Passwords are stored in environment variables, not files
- Temporary askpass scripts are created with restricted permissions (700)
- Automatic cleanup of sensitive temporary files
- No passwords are logged or exposed in command output

### Command Validation

- Commands are classified before execution
- Dangerous patterns are detected and blocked
- User confirmation required for high-risk operations
- All privilege escalations are logged with justification

### Principle of Least Privilege

- Commands run with the minimum required privileges
- Automatic fallback to user-level execution when possible
- Root privileges only used when absolutely necessary

## Demo Script

Run the included demo script to see the privilege management system in action:

```bash
python privilege_demo.py
```

This will show:
- System status and capabilities
- Command classification examples
- Execution tests with different privilege levels

## Environment Variables

- `PENTEST_SUDO_PASS`: Securely stored sudo password for the session
- Set via the CLI command: `python -m src.main privilege --set-password`

## Logging

All privilege operations are logged with:
- Command being executed
- Privilege level used
- Justification for privilege escalation
- Execution results and any errors

## Troubleshooting

### Sudo Not Available

If sudo is not available on the system, the framework will:
- Log a warning message
- Fall back to user-level operations where possible
- Skip operations that absolutely require root privileges

### Password Verification Fails

If the sudo password verification fails:
- The error is logged without exposing the password
- The operation falls back to user-level if possible
- User is prompted to re-enter the password

### Command Blocked by Safety Check

If a command is blocked by the safety validation:
- The reason is clearly displayed
- Alternative safer approaches are suggested where available
- User can override with manual confirmation (not automated)

## Best Practices

1. **Set Password Once**: Use `--set-password` at the start of your session
2. **Review Classifications**: Check `--list-tasks` to understand privilege requirements
3. **Test Commands**: Use `--test-command` to verify how commands will be classified
4. **Monitor Logs**: Review logs for all privilege escalations
5. **Principle of Least Privilege**: Run with minimum required privileges
