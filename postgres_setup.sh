#!/bin/bash
echo "=== PostgreSQL Database Setup ==="

# 1. Check if PostgreSQL container is running
echo "1. PostgreSQL container status:"
docker-compose ps postgres

# 2. Check PostgreSQL logs
echo -e "\n2. PostgreSQL logs:"
docker-compose logs postgres

# 3. Try to create the database manually
echo -e "\n3. Creating database 'jac_learning_db':"
docker-compose exec postgres createdb -U jac_user jac_learning_db || echo "Database may already exist"

# 4. Test database connection
echo -e "\n4. Testing database connection:"
docker-compose exec backend python manage.py dbshell << EOF
\l
\q
EOF

# 5. Run migrations
echo -e "\n5. Running migrations:"
docker-compose exec backend python manage.py migrate

echo -e "\n6. Final database check:"
docker-compose exec backend python manage.py check --database default