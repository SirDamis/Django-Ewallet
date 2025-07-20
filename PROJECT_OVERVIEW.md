# WaPay Project Documentation

---

## 1. Discovery Phase

### 1.1 Primary Language(s) & Framework(s)
- **Language:** Python 3.8.10
- **Framework:** Django 4.0.3
- **Other:** Django REST Framework, pytest, Gunicorn, RQ, Anymail, Whitenoise

### 1.2 Package/Dependency Manager & Build System
- **Dependency Manager:** `pip` (via `requirements.txt`)
- **Build/Setup:** `build.sh` (installs dependencies, collects static files, runs migrations)
- **Test Runner:** `pytest` (with `pytest-django`)
- **Procfile:** For Heroku deployment (runs migrations, starts Gunicorn server)

### 1.3 Entry Points
- **Web Server:** `manage.py` (Django), `ewallet/wsgi.py` (WSGI), `ewallet/asgi.py` (ASGI)
- **CLI:** `manage.py`
- **Heroku:** `Procfile` (`web: gunicorn ewallet.wsgi --log-file -`)
- **Main App:** `ewallet` Django project

---

## 2. High-Level Architecture

### 2.1 Top-Level Folder Map

```
.
├── ewallet/         # Main Django project (settings, URLs, utils)
├── user/            # User management app (custom user model, auth, registration)
├── wallet/          # Wallet app (transactions, balance, fund/withdraw)
├── referral/        # Referral system app
├── static/          # Static assets (css, js, images)
├── templates/       # HTML and email templates
├── tests.py         # (in each app) - minimal test stubs
├── requirements.txt # Python dependencies
├── manage.py        # Django CLI entry point
├── build.sh         # Build/setup script
├── Procfile         # Heroku process types
├── pytest.ini       # Pytest configuration
├── runtime.txt      # Python version for deployment
└── README.md        # Project overview and setup
```

### 2.2 Top-Level Directory Purposes

- **ewallet/**: Django project configuration, settings, URLs, and shared utilities.
- **user/**: Custom user model, registration, authentication, signals, and user-related views.
- **wallet/**: Core wallet logic, transaction history, fund/withdraw, and wallet views.
- **referral/**: Referral code management, referral relationships, and related views.
- **static/**: CSS, JS, and image assets for the frontend.
- **templates/**: HTML and email templates for all user-facing pages and emails.

### 2.3 C4-Context Diagram (Mermaid)

```mermaid
graph TD
    User[User]
    Web[WaPay Django App]
    DB[(Database)]
    Email[Email Provider]
    Payment[Flutterwave API]
    Redis[Redis (RQ)]
    Heroku[Heroku Platform]

    User-->|HTTP/HTTPS|Web
    Web-->|ORM|DB
    Web-->|SMTP/Anymail|Email
    Web-->|API|Payment
    Web-->|RQ|Redis
    Web-->|WSGI/ASGI|Heroku
```

---

## 3. Module / Package Deep-Dive

### ewallet (Project Core)
- **Description:** Django project configuration, settings, URLs, and shared utilities.
- **Public API:** `ewallet/urls.py` (routes), `ewallet/settings.py` (config), `ewallet/utils.py` (tokens, payment setup)
- **Key Abstractions:** Settings, environment management, token generation, payment gateway setup.
- **External Dependencies:** Database, Email (Anymail), Payment API (Flutterwave), Redis (RQ)
- **Extension Points:** Settings, utility functions.
- **Test Coverage:** ❌ (no direct tests)

### user (User Management)
- **Description:** Custom user model, registration, authentication, signals, and user-related views.
- **Public API:** 
  - URLs: `/`, `/register/`, `/login/`, `/logout/`, `/password_change/`, `/password_reset/`, `/activate/<uidb64>/<token>/`
  - Views: `HomeView`, `RegisterView`, `AccountNotVerifiedView`, `ActivateAccount`
  - Forms: `RegisterForm`, `LoginForm`, `EmailValidationOnForgotPassword`
  - Model: `User` (custom, email-based)
- **Key Abstractions:** `UserManager`, `User`, signals for wallet/referral creation and email verification.
- **External Dependencies:** Email (Django/Anymail), Wallet (creates wallet on user creation), Referral (creates code)
- **Extension Points:** Custom user model, signals, forms.
- **Test Coverage:** ❌ (stub only)

### wallet (Wallet & Transactions)
- **Description:** Handles wallet creation, balance, transactions, funding, withdrawal, and transaction history.
- **Public API:** 
  - URLs: `/wallet/`, `/wallet/transactions/`, `/wallet/send-fund/`, `/wallet/receive-fund/`, `/wallet/fund-wallet/`, `/wallet/withdraw-wallet/`
  - Views: `WalletView`, `SendFundView`, `ReceiveFundView`, `FundWalletView`, `WithdrawWalletView`, `TransactionView`
  - Models: `Wallet`, `TransactionHistory`, `PendingWithdrawal`
- **Key Abstractions:** Transaction recording, pending withdrawals, payment gateway integration.
- **External Dependencies:** Payment API (Flutterwave), User, Redis (RQ)
- **Extension Points:** Views, models, payment integration.
- **Test Coverage:** ❌ (stub only)

### referral (Referral System)
- **Description:** Manages referral codes, relationships, and referral-based registration.
- **Public API:** 
  - URLs: `/referral/`, `/join-us/<code>`
  - Views: `ReferralView`, `ReferralRegistrationView`
  - Models: `ReferralCode`, `Referral`
- **Key Abstractions:** Referral code generation, referral relationships.
- **External Dependencies:** User
- **Extension Points:** Views, models, forms.
- **Test Coverage:** ❌ (stub only)

---

## 4. Configuration & Environment

### 4.1 Config Files

- **requirements.txt**: Python dependencies.
- **pytest.ini**: Pytest configuration (Django settings module, test file patterns).
- **Procfile**: Heroku process types (release: migrations, web: Gunicorn server).
- **build.sh**: Build/setup script (installs dependencies, collects static, migrates).
- **runtime.txt**: Python version for deployment.
- **ewallet/settings.py**: Django settings (env vars, DB, email, static, etc.).
- **.env** (ignored): Environment variables (not in repo, but referenced).

### 4.2 Non-Secret Environment Variables (from settings.py and code)

- `DEBUG` (bool, default: False)
- `SECRET_KEY` (required, secret)
- `FLWPUBK_TEST` (Flutterwave public key, secret)
- `FLWSECK_TEST` (Flutterwave secret key, secret)
- `REDIRECT_DOMAIN` (used for payment redirects)
- (Commented out, but possible): `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` (for Postgres)
- (Commented out, but possible): `DEFAULT_FROM_EMAIL`, `EMAIL_HOST`, `EMAIL_USE_TLS`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `SENDINBLUE_API_KEY`

**Note:** All secrets are referenced via environment variables and not hardcoded (except a default `SECRET_KEY` for dev).

### 4.3 Secret Placeholders

- `SECRET_KEY`
- `FLWPUBK_TEST`
- `FLWSECK_TEST`
- Email credentials (`EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `SENDINBLUE_API_KEY`)
- Database credentials (if using Postgres)

---

## 5. Static & Template Assets

- **static/css/style.css**: Main stylesheet.
- **static/js/script.js**: Main JS file.
- **static/images/**: Wallet, card, and UI images.
- **templates/html/auth/**: Auth-related pages (login, register, password reset, etc.).
- **templates/html/wallet/**: Wallet dashboard, fund, send, receive, transaction, etc.
- **templates/html/referral/**: Referral home, join-us.
- **templates/emails/**: Email templates for activation and password reset.

---

## 6. Test Coverage

- **user/tests.py**: Stub only (no real tests).
- **wallet/tests.py**: Stub only (no real tests).
- **referral/tests.py**: Stub only (no real tests).
- **pytest.ini**: Configured for Django, but actual coverage is ⚠️/❌ (minimal to none).

---

## 7. Extension & Integration Points

- **User model**: Custom, can be extended.
- **Signals**: For wallet and referral code creation, email verification.
- **Payment**: Easily switchable via `ewallet/utils.py` and environment.
- **Email**: Pluggable backend (console, Anymail, etc.).
- **RQ/Redis**: For background jobs (potential, not deeply used in code).
- **Settings**: All major config via environment variables.

---

# Reference Usage

- **@project-structure**: For top-level folder map and directory purposes.
- **@env-vars**: For all environment variables and config.
- **@public-api**: For all main routes, models, and extension points.
- **@test-coverage**: For current test status and recommendations.