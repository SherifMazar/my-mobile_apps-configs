# my-mobile_apps-configs 🌐📱

Centralized, zero-cloud-cost remote configuration repository for mobile applications.

This repository serves lightweight, isolated JSON configurations for mobile applications (such as **Voxora** and future apps). Each mobile application consumes its own isolated configuration file (`<app_name>.json`), ensuring:
- **Zero Cross-App Blast Radius:** A syntax error or schema change in one app's configuration never impacts any other app.
- **Zero Server Costs:** Hosted entirely on free static CDNs (GitHub Pages, Cloudflare Pages, or static storage).
- **Instant Remote Control:** Developers can toggle early access trials, update support links, and manage minimum supported versions in seconds without releasing app updates.

---

## 📁 Repository Structure

```text
my-mobile_apps-configs/
├── .github/
│   └── workflows/
│       └── validate-and-deploy.yml   # (Optional) CI/CD schema validation and GitHub Pages deploy
├── schema.json                       # JSON Schema (Draft-07) defining strict contract
├── validate_configs.py               # Pre-commit & CI validation script
├── template_app.json                 # Boilerplate template for new mobile apps
├── voxora.json                       # Live configuration for Voxora: Voice TV Remote
└── README.md                         # Architecture and operational runbook
```

---

## ⚙️ Configuration Schema Overview

Every app configuration file must conform to `schema.json`. Below is the core schema structure:

```json
{
  "app_id": "dev.voxora",
  "app_name": "Voxora: Voice TV Remote",
  "schema_version": "1.0.0",
  "last_updated_utc": "2026-11-06T00:00:00Z",
  "early_access": {
    "active": true,
    "banner_message": "Early Access Trial: All premium voice features unlocked. Enjoy full access!",
    "banner_cta_url": "https://voxora.dev/feedback",
    "banner_dismissible": true
  },
  "trial": {
    "duration_days": 14,
    "grace_period_days": 14
  },
  "pricing": {
    "lifetime_product_id": "dev.voxora.lifetime",
    "price_usd_reference": 1.99,
    "currency": "USD"
  },
  "support": {
    "email": "support@voxora.dev",
    "feedback_url": "https://voxora.dev/feedback",
    "faq_url": "https://voxora.dev/faq"
  },
  "min_supported_version": "1.0.0"
}
```

### Key Fields & Behavior:

| Key | Type | Description |
| :--- | :--- | :--- |
| `early_access.active` | `boolean` | When `true`, all users have full, unrestricted access. A top banner displays `banner_message`. |
| `early_access.active = false` | `boolean` | **Early Access Ended:** Banner vanishes. Existing users enter the `trial.grace_period_days` (14 days). New installs receive `trial.duration_days` (14 days), after which the $1.99 Lifetime Purchase is required. |
| `trial.duration_days` | `integer` | Free trial period for new downloads once Early Access has ended (default: `14`). |
| `trial.grace_period_days` | `integer` | Grace period granted to legacy users who installed during Early Access when the flag is flipped (default: `14`). |
| `pricing.lifetime_product_id` | `string` | In-App Purchase SKU registered on Apple App Store Connect and Google Play Console. |
| `min_supported_version` | `string` | Semantic version string. Used by the app to show a forced update prompt if client version is lower. |

---

## 🚀 How to Host on GitHub Pages (Recommended)

1. **Create GitHub Repository:**
   - Create a new repository on GitHub named `my-mobile_apps-configs`.
   - Push this local directory to GitHub:
     ```bash
     git remote add origin git@github.com:<your-username>/my-mobile_apps-configs.git
     git branch -M main
     git push -u origin main
     ```

2. **Enable GitHub Pages:**
   - In GitHub, navigate to **Settings** > **Pages**.
   - Under **Build and deployment** > **Source**, choose **Deploy from a branch**.
   - Select branch: `main` / folder: `/ (root)` and click **Save**.

3. **Public URL Access:**
   Your configuration endpoints will be immediately available globally via CDN:
   - **Voxora:** `https://<your-username>.github.io/my-mobile_apps-configs/voxora.json`
   - **Template:** `https://<your-username>.github.io/my-mobile_apps-configs/template_app.json`

*(Alternatively, you can link this repo to Cloudflare Pages for instant edge caching with custom domains).*

---

## 🛠️ Operational Playbooks

### Playbook 1: How to Terminate Early Access Trial (Target User Count Reached)
When you monitor active devices in **Google Play Console** ("Installs on active devices") and **Apple App Store Connect** ("App Units") and hit your target (e.g., 5,000 active users):

1. Open `voxora.json`.
2. Flip `early_access.active` from `true` to `false`:
   ```json
   "early_access": {
     "active": false,
     "banner_message": "",
     "banner_cta_url": "",
     "banner_dismissible": true
   }
   ```
3. Update `last_updated_utc` to current ISO timestamp.
4. Run validation:
   ```bash
   python3 validate_configs.py
   ```
5. Commit and push:
   ```bash
   git add voxora.json
   git commit -m "chore(voxora): terminate early access trial period"
   git push origin main
   ```
Within minutes of CDN cache invalidation, app clients will fetch the updated flag:
- The Early Access banner disappears.
- Legacy users are automatically transitioned to the 14-day transition grace period.
- New downloads get the standard 14-day trial before the $1.99 paywall is shown.

---

### Playbook 2: Adding a New Mobile Application
When building your next mobile app:
1. Duplicate `template_app.json` and name it `<your_new_app_name>.json` (e.g. `soundflow.json`).
2. Update the `app_id`, `app_name`, and product IDs to match the new app's credentials.
3. Validate:
   ```bash
   python3 validate_configs.py
   ```
4. Commit and push. The new app's configuration is now live at:
   `https://<your-username>.github.io/my-mobile_apps-configs/<your_new_app_name>.json`

---

## 🧪 Local Validation

To test that all JSON configurations are syntactically valid and conform to `schema.json`:

```bash
python3 validate_configs.py
```

Expected output:
```text
============================================================
 Validating configs against schema.json...
============================================================
Checking: voxora.json
  -> VALID
Checking: template_app.json
  -> VALID

============================================================
 Summary: 2 passed, 0 failed.
============================================================
```
