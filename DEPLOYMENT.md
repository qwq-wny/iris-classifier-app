# Deployment

The project uses GitHub Actions for CI (continuous integration) and CD
(continuous delivery).

## Branches

| Branch | Job | What happens |
|---|---|---|
| dev | CI | tests, code checks and Docker build run on every push |
| staging | CI + staging build | after a merge, a staging `.env` is created from secrets and the staging image is built |
| main | CI + production build | after a merge, a production `.env` is created from secrets and the production image is built |

## The full path of one change

1. A developer creates a `feature/...` branch and writes code.
2. A pull request is opened from `feature/...` to `dev`.
3. GitHub Actions runs the CI pipeline:
   - `ruff check` (code problems),
   - `ruff format --check` (code style),
   - `pytest` (all tests),
   - `docker build` (the image must build).
4. If CI fails, the pull request cannot be merged.
   If CI passes, the branch is merged into `dev`.
5. A pull request from `dev` to `staging` runs CI again.
   After the merge, the staging workflow creates a staging `.env`
   (from the GitHub secret `STAGING_MODEL_NAME`) and builds the image.
6. A pull request from `staging` to `main` runs CI again.
   After the merge, the production workflow creates a production `.env`
   (from the GitHub secret `PRODUCTION_MODEL_NAME`) and builds the image.

## GitHub secrets used by the pipelines

| Secret | Used by | Example value |
|---|---|---|
| STAGING_MODEL_NAME | staging build | model-v2 |
| PRODUCTION_MODEL_NAME | production build | model-v2 |

## Branch protection (recommended settings)

In GitHub: Settings -> Branches -> Add branch protection rule.

- Branch name pattern: `dev`, `staging` and `main` (one rule for each).
- Enable "Require a pull request before merging".
- Enable "Require status checks to pass before merging" and select the CI jobs.
- With these settings a branch cannot be merged when CI fails.

## DVC remote (Azure)

The data is pushed to Azure Blob Storage with DVC.
The connection does not store any password inside git.
You only need these two environment variables on your computer:

```
AZURE_STORAGE_ACCOUNT_NAME=your_account_name
AZURE_STORAGE_ACCOUNT_KEY=your_account_key
```

Then run:

```bash
dvc pull   # download the data
dvc push   # upload a new data version
```
