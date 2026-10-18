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

| Dataset version | Files in `data/` | Git commit |
|---|---|---|
| v1 | iris_v1.csv | `0e0a9e4` |
| v2 | iris_v1.csv + iris_v2.csv | `8ec6f2f` |

Because git and DVC work together, we can always answer the question:
"which exact dataset version produced this model?" - we look at the commit,
read the `data.dvc` pointer, and DVC knows the exact files.

## How DVC is used

- Git stores only the small pointer file `data.dvc`, not the csv files.
- The real csv files are stored in an Azure Blob Storage container
  (`azure://irisdata/data`, see `.dvc/config`).
- `dvc pull` downloads the data, `dvc push` uploads a new version.
- To connect to Azure, set `AZURE_STORAGE_ACCOUNT_NAME` and
  `AZURE_STORAGE_ACCOUNT_KEY` as environment variables on your computer.
  No password is stored inside git.
