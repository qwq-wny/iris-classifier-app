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
- 1 row has a wrong `sepal_width` value of 50 cm (an impossible value).

### Version 2 (v2) - file `data/iris_v2.csv`

The cleaned version with exactly 150 rows:

- duplicates removed,
- the wrong `sepal_width` value fixed (the row was restored to the original
  value from the source dataset),
- no missing values.

## Which commit belongs to which version

| Dataset version | File | Git commit |
|---|---|---|
| v1 | data/iris_v1.csv | (filled after the git commits are made) |
| v2 | data/iris_v1.csv + data/iris_v2.csv | (filled after the git commits are made) |

## How DVC is used

- Git stores only the small pointer file `data.dvc`, not the csv files.
- The real csv files are stored in an Azure Blob Storage container.
- `dvc pull` downloads the data, `dvc push` uploads a new version.
