# Git Push Authentication Troubleshooting

## Error Analysis
```
remote: Invalid username or token. Password authentication is not supported for Git operations.
fatal: Authentication failed for 'https://github.com/OumaCavin/jac-interactive-learning-platform.git/'
```

## Common Causes & Solutions

### 1. **Expired or Invalid PAT**
**Symptoms:** "Invalid username or token"
**Check PAT validity:**
```bash
curl -H "Authorization: token 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" https://api.github.com/user
```
**Solution:** Generate a new PAT with proper permissions (repo, workflow)

### 2. **Wrong Token Format**
**Current issue:** Using PAT incorrectly in URL
**Incorrect:** `https://username:token@github.com/...`
**Correct:** `https://token@github.com/...` or `https://OumaCavin:token@github.com/...`

### 3. **Insufficient PAT Permissions**
**Required scopes:**
- `repo` (Full control of private repositories)
- `workflow` (Update GitHub Action workflows)

### 4. **HTTPS vs SSH Protocol**
**Problem:** Repository configured for SSH but using HTTPS
**Check current remote:**
```bash
git remote -v
```
**If shows:** `git@github.com:...` → Need SSH key setup
**If shows:** `https://...` → Continue with HTTPS fixes

## Debug Commands
```bash
# Check authentication
git config --global credential.helper

# Check remote URL
git remote -v

# Test PAT validity
curl -H "Authorization: token YOUR_PAT" https://api.github.com/user

# Check PAT scopes
curl -H "Authorization: token YOUR_PAT" -H "Accept: application/vnd.github.v3+json" https://api.github.com/user
```