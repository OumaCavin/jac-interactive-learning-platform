#!/bin/bash
echo "=== Git Authentication Debug ==="

cd ~/projects/jac-interactive-learning-platform

# 1. Check current PAT and test it
echo "1. Testing PAT validity..."
PAT="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"

echo "Testing PAT with GitHub API..."
response=$(curl -s -w "%{http_code}" -H "Authorization: token $PAT" https://api.github.com/user)
http_code="${response: -3}"
body="${response:0:-3}"

echo "HTTP Status: $http_code"
if [ "$http_code" = "200" ]; then
    echo "✅ PAT is valid!"
    echo "User info: $(echo $body | jq -r '.login // "N/A"')"
else
    echo "❌ PAT is invalid!"
    echo "Response: $body"
    echo "Need to generate new PAT"
fi

# 2. Check current remote URL
echo -e "\n2. Current remote configuration:"
git remote -v

# 3. Check git configuration
echo -e "\n3. Git configuration:"
git config --list | grep -E "(user|remote|credential)"

# 4. Check current commit
echo -e "\n4. Current commit:"
git log --oneline -1

# 5. Try different push methods
echo -e "\n5. Testing push methods..."

# Method 1: Token in URL (username:token format)
echo "Testing: username:token format..."
git push https://OumaCavin:$PAT@github.com/OumaCavin/jac-interactive-learning-platform.git main
echo "Method 1 result: $?"

# If method 1 fails, show manual alternatives
echo -e "\nIf push fails, try these manual methods:"
echo "Method 2: git remote set-url origin https://$PAT@github.com/OumaCavin/jac-interactive-learning-platform.git"
echo "Method 3: git remote set-url origin https://OumaCavin:$PAT@github.com/OumaCavin/jac-interactive-learning-platform.git"
echo "Then: git push origin main"