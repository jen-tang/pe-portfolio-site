echo "--> Killing old tmux sessions (if any)…"
tmux kill-server


cd portfolio/pe-portfolio-site

echo "--> Updating repo…"
git fetch && git reset origin/main --hard


echo "--> Installing deps…"
source venv/bin/activate
pip install -r requirements.txt


echo "--> Starting Flask in new tmux session…"

SESSION=automate
LOG=$HOME/automate.log

tmux new-session -d -s "$SESSION" \
  "bash -lc 'cd ~/portfolio/pe-portfolio-site && \
             source venv/bin/activate && \
             export FLASK_APP=app.py && \
             exec python -m flask run --host 0.0.0.0 --port 8000'"

echo "Done!  Flask is running inside tmux session '$SESSION'."

