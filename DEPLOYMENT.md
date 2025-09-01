# 🚀 Deployment Guide for Streamlit Cloud

## Prerequisites
- GitHub account
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))

## Step 1: Prepare Your Repository

### 1.1 Create a .env file (for local development)
```bash
# Copy the example file
cp env.example .env

# Edit .env with your actual MongoDB credentials
MONGODB_URI=mongodb+srv://your-username:your-password@your-cluster.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=course_dss
```

### 1.2 Update .gitignore
Make sure your `.gitignore` includes:
```
.env
__pycache__/
*.pyc
.DS_Store
```

## Step 2: Deploy to Streamlit Cloud

### 2.1 Push to GitHub
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### 2.2 Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set the main file path: `app.py`
6. Click "Deploy!"

### 2.3 Set Environment Variables
In Streamlit Cloud dashboard:
1. Go to your app settings
2. Click "Secrets"
3. Add your MongoDB credentials:
```toml
MONGODB_URI = "mongodb+srv://your-username:your-password@your-cluster.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "course_dss"
```

## Step 3: Test Your Deployment

1. Your app will be available at: `https://your-app-name.streamlit.app`
2. Test the database connection
3. Verify all features work correctly

## Troubleshooting

### Database Connection Issues
- Check MongoDB Atlas network access (allow all IPs: 0.0.0.0/0)
- Verify credentials in Streamlit secrets
- Check MongoDB Atlas cluster status

### Import Errors
- Ensure all dependencies are in `requirements.txt`
- Check Python version compatibility

### Performance Issues
- Consider adding database connection pooling
- Implement caching for frequently accessed data

## Security Best Practices

✅ **Implemented:**
- Environment variables for sensitive data
- Streamlit secrets management
- Connection error handling

🔒 **Additional Recommendations:**
- Use MongoDB Atlas IP whitelist for production
- Implement user authentication
- Add rate limiting
- Regular security updates

## Monitoring

- Streamlit Cloud provides basic analytics
- Monitor MongoDB Atlas metrics
- Set up alerts for connection failures
