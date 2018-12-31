cd /Users/zhouligang/Money/python3/social/sh
rsync -azP --exclude=.git --exclude=__pycache__ ../../social aws:source

ssh dajin << EOF
svc restart social:social-8300
svc restart social:social-8301
svc restart social:social-8302
svc restart social:social-8303
EOF

