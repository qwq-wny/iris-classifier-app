# Data documentation

## Where the data comes from

The data is the famous Iris dataset that comes inside scikit-learn
(`sklearn.datasets.load_iris`). It is a small public dataset, so it is safe
to use for a university project. It has 150 flowers. Each flower has 4
measurements (in cm) and a name: setosa, versicolor or virginica.

The script `ml/make_datasets.py` was used to create the csv files.

## The two dataset versions

### Version 1 (v1) - file `data/iris_v1.csv`

The first usable version. It has 152 rows, but with small problems:

- 2 rows are copies of other rows (duplicates),
- 1 row has a wrong `sepal_width` value of 50 cm (an impossible value),
- 6 rows have a wrong flower name (label mistakes).

### Version 2 (v2) - file `data/iris_v2.csv`

The cleaned version with exactly the 150 original flowers:

- duplicates removed,
- the impossible `sepal_width` value fixed,
- the 6 wrong flower names corrected.

## Which commit belongs to which version

| Dataset version | Files in `data/` | Git commit | DVC hash |
|---|---|---|---|
| v1 | iris_v1.csv | `0e0a9e4` | `c4f884dbd8910a355ec91c2672ecaa68.dir` |
| v2 | iris_v1.csv + iris_v2.csv | `8ec6f2f` | `0fba930d9fb57b40b64019e040011e66.dir` |

Because git and DVC work together, we can always answer the question:
"which exact dataset version produced this model?" - we look at the commit,
read the `data.dvc` pointer, and DVC knows the exact files.

## How DVC is used

- Git stores only the small pointer file `data.dvc`, not the csv files.
  `data/` is listed in `.gitignore`, so the csv files never enter git.
- The pointer stores the hash of the whole `data/` folder. Each dataset
  version above maps to one hash, and each MLflow run records that hash as
  the `dvc_data_hash` parameter.
- `dvc push` uploads the data to the remote, `dvc pull` downloads it.

## Azure remote status

The Azure remote is **not configured yet**: `.dvc/config` is still empty, so
`dvc remote list` prints nothing and `dvc pull` fails with
`No remote provided and no default remote set`.

Until the storage account is provided, rebuild the data locally (it is created
deterministically from scikit-learn):

```bash
python -m ml.make_datasets
```

Once the Azure account is available:

```bash
dvc remote add -d azure azure://<container>/<path>
export AZURE_STORAGE_ACCOUNT_NAME=<name>
export AZURE_STORAGE_ACCOUNT_KEY=<key>
dvc push
```

Credentials are kept in environment variables (or in `.dvc/config.local`,
which DVC ignores on purpose). No password is stored inside git.
