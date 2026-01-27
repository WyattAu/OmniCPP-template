#!/usr/bin/env python3
"""
Install script for OmniCpp project

This script provides a command-line interface for installing dependencies
and built artifacts using the omni_scripts.controller.install_controller module.
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path to import omni_scripts
sys.path.insert(0, str(Path(__file__).parent.parent))

from omni_scripts.controller.install_controller import install


def main():
    """Main entry point for install script."""
    parser = argparse.ArgumentParser(
        description="Install OmniCpp dependencies and artifacts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Install all targets (release)
  %(prog)s --target engine    # Install engine only
  %(prog)s --config debug     # Install debug configuration
  %(prog)s --install-dependencies  # Install dependencies first
  %(prog)s --prefix /usr/local    # Install to custom prefix
        """
    )

    parser.add_argument(
        "--target",
        choices=["engine", "game", "standalone", "all"],
        default="all",
        help="Target to install (default: all)"
    )

    parser.add_argument(
        "--config",
        choices=["debug", "release"],
        default="release",
        help="Build configuration (default: release)"
    )

    parser.add_argument(
        "--install-dependencies",
        action="store_true",
        help="Install dependencies (Conan, vcpkg) before installing"
    )

    parser.add_argument(
        "--prefix",
        help="Installation prefix path"
    )

    args = parser.parse_args()

    # Call the install function from the controller
    return install(args)


if __name__ == "__main__":
    sys.exit(main())
