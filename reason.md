### **Jira Story: Revert Changes in Production Using GitLab**  

**Project:** _[Your Project Name]_  
**Issue Type:** Story  
**Priority:** High  
**Assignee:** _[Your Name or Team]_  
**Reporter:** _[Your Name]_  
**Labels:** rollback, production, GitLab, CI/CD  

---

### **Summary:**  
Revert the recent changes in the production environment using GitLab to restore the last stable version.

---

### **Description:**  
A recent deployment introduced changes that need to be rolled back in the production environment. This story outlines the steps to revert the changes using GitLab.  

**Acceptance Criteria:**  
- The production branch (`prod` or `main`) is restored to the last stable version.  
- All impacted services are reverted and functional.  
- The rollback is tested to confirm stability.  
- CI/CD pipeline successfully deploys the reverted changes.  

---

### **Steps to Revert Changes:**  
1. **Identify the Problematic Commit or Version**  
   - Review the recent commit history in GitLab (`Repository > Commits`).  
   - Identify the commit hash or tag of the last stable deployment.  

2. **Revert Using GitLab UI (If Applicable)**  
   - Navigate to the commit.  
   - Click **Revert** and merge the changes back into `prod`.  
   - Verify the deployment.  

3. **Revert Using Git Commands (If Needed)**  
   - Checkout the `prod` branch:  
     ```bash
     git checkout prod
     ```  
   - Reset to the stable commit:  
     ```bash
     git reset --hard <commit-hash>
     git push --force
     ```  
   - Manually trigger the CI/CD pipeline if it doesn’t auto-deploy.  

4. **Rollback Using GitLab CI/CD (If Configured)**  
   - Navigate to **CI/CD > Pipelines** in GitLab.  
   - Identify the last successful deployment.  
   - Trigger a rollback job, if available.  

5. **Validate Production Environment**  
   - Test the application to confirm that the rollback was successful.  
   - Verify logs and monitoring dashboards for any issues.  
   - Confirm with stakeholders before closing the ticket.  

---

### **Dependencies:**  
- Access to GitLab repository and production environment.  
- Knowledge of the last stable commit or tag.  
- CI/CD pipeline configuration for deployment.  

---

### **Additional Notes:**  
- If the rollback causes any issues, consider restoring a backup or applying a hotfix.  
- Document lessons learned to prevent similar incidents in the future.  

---
