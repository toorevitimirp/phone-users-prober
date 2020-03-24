#!/bin/bash
mongo <<EOF
use admin;
db.createUser({ user: 'root', pwd: 'root', roles: [ { role: "userAdminAnyDatabase", db: "admin" } ] });
EOF
