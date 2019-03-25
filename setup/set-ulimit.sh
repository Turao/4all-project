#!/bin/sh

# know that this only appends the lines to the files
# I'd suggest you to either read the documentation or
# the files you're altering, to understand what this is doing

set_pam() {
  echo "session optional pam_limits.so" >> /etc/pam.d/common-session
  echo "session optional pam_limits.so" >> /etc/pam.d/common-session-noninteractive
}

set_ulimit() {
  user=$1
  limit=$2
  echo "$user soft nofile $limit" >> /etc/security/limits.conf
  echo "$user hard nofile $limit" >> /etc/security/limits.conf
}

main() {
  set_pam
  set_ulimit "$1" "$2"
}

main "$1" "$2"