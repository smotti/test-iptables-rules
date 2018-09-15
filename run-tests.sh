#!/bin/bash

USER="vagrant"
PASS="vagrant"
RUN_ON=$1
HOW=$2
PYTHON_PATH=$(pwd)/tests
GUEST_IP=$(cat tests/guest_iface_info | cut -d ',' -f 1)

#
# Setup for non-interactive SSH login, required to start tests on the guest
# via ssh.
#
SSH_ASKPASS_SCRIPT=/tmp/ssh-askpass-script
cat > $SSH_ASKPASS_SCRIPT <<EOL
#!/bin/bash
echo $PASS
EOL
chmod u+x $SSH_ASKPASS_SCRIPT

export DISPLAY=:0
export SSH_ASKPASS=$SSH_ASKPASS_SCRIPT

#
# Some preconditions
#
if [ $(whoami) != "root" ]; then
  echo "Must be run as root"
  exit 1
fi

#
# Run tests locally
#
if [[ -z $HOW || $HOW != "remote" ]]; then
  echo "Running tests for $RUN_ON locally"

  if [[ $RUN_ON == 'host' ]]; then
    echo "Start fake servers on guest"
    setsid ssh "$USER@$GUEST_IP" \
      "sudo /etc/init.d/cfengine3 stop; sudo /etc/init.d/td-agent stop; cd /vagrant; sudo nohup python tests/syslog_srv.py > /dev/null 2>&1 &"
  fi

  for t in tests/$RUN_ON/test_*.py; do
    PYTHONPATH=$PYTHON_PATH python2 $t
  done
fi

#
# Run tests on guest invoked by host
#
if [[ -n $HOW && $HOW == "remote" && $RUN_ON == "guest" ]]; then
  echo "Running tests on guest via remote invocation"
  echo "Starting test ntp server"
  python2 tests/ntp_srv.py &

  echo "Starting test smtp server"
  python tests/smtp_srv.py &
  
  echo "Execute tests on guest"
  setsid ssh "$USER@$GUEST_IP" "cd /vagrant; sudo ./run-tests.sh guest"

  echo "Stop test servers"
  for p in $(jobs -p); do
    kill -9 $p > /dev/null
  done

  rm $SSH_ASKPASS_SCRIPT
fi
