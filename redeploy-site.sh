cd portfolio/pe-portfolio-site

echo "--> Updating repo…"
git fetch && git reset origin/main --hard


echo "--> Installing deps…"
source venv/bin/activate
pip install -r requirements.txt

systemctl daemon-reload
systemctl restart myportfolio
