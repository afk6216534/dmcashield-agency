# DMCAShield Agency - Quick Deploy

## Step 1: Login to GitHub
Run this command and follow the web browser login:
```bash
gh auth login
```

## Step 2: Create Repo & Push (One command)
After login, run:
```bash
cd dmcashield-agency
gh repo create dmcashield-agency --public --source=. --push
```

## Step 3: Deploy to Netlify
1. Go to https://netlify.com
2. Click "Add new site" → "Import an existing project"
3. Choose GitHub → Select dmcashield-agency
4. Build command: `npm run build`
5. Publish directory: `frontend/dist`
6. Click "Deploy"

## DONE! Auto-deploys on every push

---

## After Making Changes:

```bash
cd dmcashield-agency

# Stage changes
git add .

# Commit
git commit -m "Your updated changes"

# Push - Netlify auto-deploys!
git push
```

That's it! Every push to GitHub → Netlify auto-deploys in ~30 seconds.