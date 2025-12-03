# Deployment Checklist

Use this checklist to track your deployment progress.

## Pre-Deployment

### Local Testing
- [ ] Run setup script (`./setup.sh` or `setup.bat`)
- [ ] Backend starts successfully (http://localhost:8000)
- [ ] Frontend starts successfully (http://localhost:3000)
- [ ] Can create test project with sample_config.json
- [ ] HTML generation works
- [ ] PDF generation works
- [ ] Downloads work correctly

### Code Preparation
- [ ] All sensitive data removed from code
- [ ] Environment variables documented
- [ ] .gitignore properly configured
- [ ] README.md reviewed and updated
- [ ] All files committed to git

## GitHub Setup

- [ ] GitHub repository created
- [ ] Repository visibility set (Private/Public)
- [ ] Local code pushed to GitHub
- [ ] Repository URL noted: `_______________________`
- [ ] Collaborators added (if needed)

## Vercel Deployment

### Initial Setup
- [ ] Vercel account created
- [ ] GitHub account connected to Vercel
- [ ] Repository imported to Vercel
- [ ] Project name set: `_______________________`

### Configuration
- [ ] Framework preset: Auto-detected ✓
- [ ] Root directory: `./` ✓
- [ ] Build command: Auto-detected ✓
- [ ] Output directory: Auto-detected ✓
- [ ] Environment variable added: `PLAYWRIGHT_BROWSERS_PATH=/tmp/.cache/ms-playwright`

### Deployment
- [ ] First deployment initiated
- [ ] Build completed successfully
- [ ] Deployment URL received: `_______________________`
- [ ] Test URL works in browser

## Post-Deployment Testing

### Functionality Tests
- [ ] Homepage loads
- [ ] Can fill in film information form
- [ ] Can upload poster image
- [ ] Can upload production stills
- [ ] Can add team members
- [ ] Can add awards
- [ ] Can add reviews
- [ ] Project creation works
- [ ] Validation shows errors/warnings correctly
- [ ] EPK generation works
- [ ] HTML download works
- [ ] PDF download works
- [ ] PDF has correct formatting

### Cross-Browser Testing
- [ ] Works in Chrome
- [ ] Works in Firefox
- [ ] Works in Safari
- [ ] Works in Edge
- [ ] Works on mobile (responsive)

### Performance
- [ ] Page loads in < 3 seconds
- [ ] EPK generation completes in < 30 seconds
- [ ] Files download successfully
- [ ] No console errors

## Team Onboarding

### Access
- [ ] Deployment URL shared with team
- [ ] Access instructions provided
- [ ] Sample config shared for testing
- [ ] Quick start guide shared

### Training
- [ ] Demo completed with team
- [ ] Common workflows documented
- [ ] Support contact established
- [ ] Feedback process established

## Optional Enhancements

### Domain Setup (Optional)
- [ ] Custom domain purchased
- [ ] Domain added in Vercel
- [ ] DNS configured
- [ ] SSL certificate verified
- [ ] Old URL redirects to new domain

### Authentication (Recommended for Production)
- [ ] Authentication service chosen: `_______________________`
- [ ] Service configured
- [ ] Login page implemented
- [ ] Protected routes configured
- [ ] User roles defined
- [ ] Access control tested

### Storage (Recommended for Production)
- [ ] Storage service chosen: `_______________________`
- [ ] Service configured
- [ ] File upload to storage working
- [ ] File download from storage working
- [ ] Cleanup policy configured

### Monitoring (Recommended)
- [ ] Analytics enabled in Vercel
- [ ] Error tracking setup
- [ ] Uptime monitoring configured
- [ ] Alert notifications configured

## Documentation

- [ ] Internal wiki/docs updated
- [ ] Team training materials created
- [ ] Support process documented
- [ ] Backup procedures documented
- [ ] Recovery procedures documented

## Maintenance Plan

### Regular Tasks Scheduled
- [ ] Weekly: Check error logs
- [ ] Monthly: Review usage metrics
- [ ] Monthly: Update dependencies
- [ ] Quarterly: Security review
- [ ] Quarterly: Cost review
- [ ] Annually: Architecture review

### Contacts Documented
- [ ] Project lead: `_______________________`
- [ ] Technical contact: `_______________________`
- [ ] Vercel account owner: `_______________________`
- [ ] Domain registrar: `_______________________`
- [ ] Support email: `_______________________`

## Emergency Procedures

### Rollback Plan
- [ ] Previous deployment URL noted
- [ ] Rollback procedure documented
- [ ] Team trained on rollback

### Backup Plan
- [ ] Backup frequency defined: `_______________________`
- [ ] Backup location: `_______________________`
- [ ] Restore procedure tested
- [ ] Recovery time objective (RTO): `_______________________`

### Incident Response
- [ ] Incident contact list created
- [ ] Escalation process defined
- [ ] Status page setup (if needed)
- [ ] User communication plan defined

## Sign-Off

### Project Completion
- [ ] All critical items completed
- [ ] All team members trained
- [ ] Documentation complete
- [ ] Handoff to operations team (if applicable)

### Stakeholder Approval
- [ ] Technical lead approval: _____________ Date: _______
- [ ] Project manager approval: _____________ Date: _______
- [ ] End user acceptance: _____________ Date: _______

---

## Quick Reference

**Deployment URL**: `_______________________`

**GitHub Repo**: `_______________________`

**Vercel Project**: `_______________________`

**Deployed By**: `_______________________`

**Deployment Date**: `_______________________`

**Version**: `1.0.0`

---

## Notes

Use this space for deployment-specific notes, issues encountered, or special configurations:

```
[Your notes here]
```

---

**Status**: [ ] Planning  [ ] In Progress  [ ] Testing  [ ] Complete

**Next Review Date**: `_______________________`
