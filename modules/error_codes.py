# Create a new error_codes.py module with known error codes and their meanings
from pathlib import Path

error_code_dict = '''"""
error_codes.py – Maps known Windows HRESULTs, WU_E errors, and MSI codes to explanations and suggested actions.
"""

ERROR_CODES = {
    "0x800f081f": {
        "meaning": "The source files could not be found.",
        "fix": "Run: DISM /Online /Cleanup-Image /RestoreHealth with /Source."
    },
    "0x80070002": {
        "meaning": "The system cannot find the file specified.",
        "fix": "Ensure all update components and required files are present."
    },
    "0x80073701": {
        "meaning": "Assembly missing from manifest.",
        "fix": "Use DISM or reapply component update."
    },
    "1603": {
        "meaning": "Fatal MSI error during install.",
        "fix": "Check for permission issues or previous app remnants."
    },
    "0x800705b4": {
        "meaning": "Timeout expired.",
        "fix": "Reboot system and retry the installation or update."
    },
    "WU_E_NOT_INITIALIZED": {
        "meaning": "Windows Update Agent not initialized.",
        "fix": "Restart Windows Update service or run Update Troubleshooter."
    },
    "WU_E_NO_SERVICE": {
        "meaning": "Windows Update Service is not running.",
        "fix": "Start 'wuauserv' service manually or with troubleshooter."
    },
    "0x80240017": {
        "meaning": "Unspecified install failure.",
        "fix": "Try downloading the update manually or re-running the setup with logs."
    },
    "0x80070020": {
        "meaning": "The process cannot access the file because it is being used by another process.",
        "fix": "Temporarily disable antivirus or reboot and try again."
    }
}
'''

# Save to file
error_code_file = Path("/mnt/data/skc_log_reader/modules/error_codes.py")
error_code_file.parent.mkdir(parents=True, exist_ok=True)
error_code_file.write_text(error_code_dict)

error_code_file.name
