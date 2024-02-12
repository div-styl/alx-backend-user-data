#!/bin/bash
echo "# Basic Auth" > README.md
# # Create virtual environment
python -m venv env

# # Create directories
mkdir -p api/v1/auth api/v1/views models

# # Create __init__.py file for api
echo "#!/usr/bin/env python3" > api/__init__.py

# # Create Python files in root
my_files=("main_9" "main_10" "main_11" "main_3" "main_4", "main_7", "main_8", "main_100" )

for file in "${my_files[@]}"; do
    echo "#!/usr/bin/env python3" > "${file}.py"
    chmod +x "${file}.py"
done

# # Create files in models directory
cd models
models_files=("__init__" "base" "user") 
for file in "${models_files[@]}"; do
    echo "#!/usr/bin/env python3" > "${file}.py"
    chmod +x "${file}.py"
done
cd ..

# # Create __init__.py and app.py files for api/v1 directory
echo "#!/usr/bin/env python3" > api/v1/__init__.py
echo "#!/usr/bin/env python3" > api/v1/app.py
chmod +x api/v1/*.py

# # Create files in api/v1/auth directory
cd api/v1/auth/
auth_files=("__init__" "auth" "basic_auth")
for file in "${auth_files[@]}"; do
    echo "#!/usr/bin/env python3" > "${file}.py"
    chmod +x "${file}.py"
done
cd ../..

# Create files in api/v1/views directory
cd api/v1/views/
views_files=("__init__" "index" "users")
for file in "${views_files[@]}"; do
    echo "#!/usr/bin/env python3" > "${file}.py"
    chmod +x "${file}.py"
done

