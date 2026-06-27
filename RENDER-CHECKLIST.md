# Render.com Deployment Checklist

## Pre-Deployment ✓

- [ ] GitHub repository created and pushed
- [ ] `render.yaml` file present (✓ created)
- [ ] `Procfile` file present (✓ created)
- [ ] `requirements.txt` file present (✓ created)
- [ ] All code committed and pushed to `main` branch

## API Keys Needed

- [ ] **GROQ API Key** - Get from https://console.groq.com
- [ ] **Qdrant Cloud URL** - Get from https://cloud.qdrant.io
- [ ] **Qdrant Cloud API Key** - Get from https://cloud.qdrant.io

## Render Setup Steps

1. [ ] Create account at https://render.com (free, no credit card)
2. [ ] Click "New +" → "Web Service"
3. [ ] Connect GitHub account
4. [ ] Select `PDF-RAG-Application` repository
5. [ ] Set service name: `pdf-rag-app`
6. [ ] Keep build/start commands as default (uses render.yaml)
7. [ ] Add environment variables:
   - [ ] `GROQ_API_KEY` = (your key)
   - [ ] `QDRANT_URL` = `https://your-cluster.qdrant.io`
   - [ ] `QDRANT_API_KEY` = (your key)
   - [ ] `PYTHON_VERSION` = `3.11`
8. [ ] Click "Deploy"
9. [ ] Wait 2-3 minutes for deployment to complete

## Post-Deployment ✓

- [ ] Check deployment logs for errors
- [ ] Visit your live URL (shown in Render dashboard)
- [ ] Test upload with sample PDF
- [ ] Ask a question to verify it works
- [ ] Share the public URL with users!

## Your Render URL

```
https://pdf-rag-app.onrender.com
```

## Automatic Redeployment

After initial setup, any push to GitHub auto-redeploys:

```powershell
git add .
git commit -m "Your changes"
git push origin main
# Render will automatically rebuild in 2-3 minutes
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Build failed" | Check logs tab, ensure `requirements.txt` exists |
| "Connection refused" | Verify `QDRANT_URL` and `QDRANT_API_KEY` are correct |
| "Upload fails" | Check `GROQ_API_KEY` is set and valid |
| "App keeps restarting" | Check logs for Python errors |

See [RENDER-DEPLOY.md](RENDER-DEPLOY.md) for detailed guide.
