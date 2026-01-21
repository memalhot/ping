# Browser Automation Tests for OPE Classes
## Brief Overview
student_sim.py simulates a student using their Jupyter terminal and ping.sh checks for ping timeout in logs<br>
to test for any latency issues

To run:
1. Run `./create_nb.sh`. This generates the notebooks and pvcs that the users use on the cluster.
2. Then run `python3 student_sim.py`
3. If you are logged into the cluster, you can then run `ping.sh` to check for clientside connection timeouts.
