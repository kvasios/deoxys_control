#!/bin/bash
# Franka gripper control service launcher
# The service now manages its own lifecycle with internal retry logic

. $(dirname "$0")/color_variables.sh

# Launch the service - it will handle its own retries
# Exit code 0 = clean shutdown
# Exit code 1 = fatal error requiring intervention
exec bin/gripper-interface $@
