# Deploy on Render.com

**Render** is the easiest way to deploy this PDF-RAG application. It's free, requires no credit card, and takes 5 minutes.

---

## **Step 1: Push to GitHub**

```powershell
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

---

## **Step 2: Create Render Account & Project**

1. **Go to:** https://render.com
2. **Sign up** (free, no credit card needed)
3. **Click:** "New +" → "Web Service"
4. **Connect GitHub** and authorize Render to access your repos
5. **Select your repository:** `PDF-RAG-Application`
6. **Fill in the form:**
   - **Name:** `pdf-rag-app`
   - **Environment:** `Python 3`
   - **Region:** Choose closest to you
   - **Branch:** `main`
   - **Build Command:** Leave as is (uses render.yaml)
   - **Start Command:** Leave as is (uses render.yaml)
   - **Plan:** Free

---

## **Step 3: Set Environment Variables**

Before deploying, add your API keys:

1. **Scroll down** to "Environment"
2. **Add variables:**

   | Key | Value |
   |-----|-------|
   | `GROQ_API_KEY` | Your API key from https://console.groq.com |
   | `QDRANT_URL` | `https://your-cluster.qdrant.io` (from Qdrant Cloud) |
   | `QDRANT_API_KEY` | Your Qdrant API key |
   | `PYTHON_VERSION` | `3.11` |

---

## **Step 4: Deploy**

1. Click **"Deploy"** button
2. **Wait 2-3 minutes** for Render to build and deploy
3. You'll see a URL like: `https://pdf-rag-app.onrender.com`
4. Click it to access your app!

---

## **Set Up Qdrant Cloud (Required)**

Since Render is cloud-hosted, you need a cloud Qdrant instance:

1. **Go to:** https://cloud.qdrant.io
2. **Sign up** (free tier available)
3. **Create a cluster:**
   - Click "Create Cluster"
   - Name: `pdf-rag-db`
   - Size: Free tier (2GB)
4. **Get your credentials:**
   - Copy Cluster URL (looks like `https://xxx-qdrant.eastus-0.cloud.qdrant.io`)
   - Copy API Key
5. **Add to Render environment variables** (see Step 3)

---

## **Automatic Deployments**

After initial setup, **every push to GitHub automatically redeploys** your app!

```powershell
# Make changes locally
git add .
git commit -m "Your changes"
git push origin main

# Render automatically rebuilds and deploys
# (takes 2-3 minutes)
```

---

## **Troubleshooting**

### Build fails with "No module named..."
- Ensure `requirements.txt` is in root directory ✓
- Check Python version is 3.11 ✓

### App crashes after deployment
- Check logs in Render dashboard → "Logs" tab
- Verify all environment variables are set
- Ensure Qdrant Cloud cluster is running

### "Connection refused" error
- Verify `QDRANT_URL` and `QDRANT_API_KEY` are correct
- Make sure Qdrant Cloud cluster is active

### App running but upload fails
- Check `GROQ_API_KEY` is set correctly
- Verify Qdrant is accessible from Render

---

## **Monitoring & Logs**

1. Go to your Render dashboard
2. Click on your service (`pdf-rag-app`)
3. Click **"Logs"** tab to see real-time logs
4. Check for errors during PDF upload/query

---

## **Upgrade from Free Plan**

If you exceed free tier limits (5GB/month storage):
1. Click "Settings" → "Plan"
2. Upgrade to **Starter** ($7/month) or higher
3. No downtime during upgrade

---

## **Next: Share Your App**

Your app is now live at:
```
https://pdf-rag-app.onrender.com
```

Share this link with others! They can upload PDFs and ask questions without installing anything.

---

## **Comparison: Render vs Alternatives**

| Feature | Render | Railway | Heroku |
|---------|--------|---------|--------|
| **Free Tier** | ✅ Yes (5GB) | ✅ Yes ($5/month) | ❌ No |
| **Easy Setup** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Auto Deploy** | ✅ GitHub | ✅ GitHub | ✅ GitHub |
| **Custom Domain** | ❌ Paid | ❌ Paid | ❌ Paid |
| **Sleep Mode** | ✅ Free | ❌ No | - |

**Render is best for:** Quick free deployments with auto-restart

---

## **Questions?**

See [DEPLOYMENT.md](DEPLOYMENT.md) for more platforms and advanced options.
