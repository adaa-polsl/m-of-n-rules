# Classification, regression and survival rule induction with complex elementary conditions

This repository contains data sets and code base used for experimental evaluation of the proposed algorithm of rule induction with complex elementary conditions. 

## Configuring experiments

The experiment code is located in the `src/experiment/` directory and is divided into three subdirectories: `m_of_n_classification`, `m_of_n_regression` and `m_of_n_survival`, for each problem type analysed. 

Each experiment can be configured using the `config.py` file located in its directory (e.g. for the classification problem this will be `src/experiment/m_of_n_classification/config.py`). This file allows you to configure the running of the experiment. The parameters that can be configured are listed below:
* `M` - parameter M for M-of-N conditions,
* `N` - parameter N for M-of-N conditions,
* `MAX_CANDIDATES` - the maximum number of candidates among M of N conditions to be considered,
* `MIN_SUPP_FRACTION` - minimum support used for the FP-Growth frequent element search algorithm,
* `get_rulekit_params` - Function that returns the parameters of the RuleKit algorithm used for rule induction. It accepts one parameter **complex_condition_enabled**. If set to True, complex conditions (excluding M-of-N conditions) will be induced.
* `CV_ENABLED` - Enable/disable cross-validation,
* `DATASETS` - List of datasets (from the `datasets` directory) to be used during the experiment.

## Running experiment

To run experiments you first need a working distribution of Python installed on your machine (version 3). Then you have to install all required dependencies using following command:
```bash
pip install -r ./requirements.txt
```
To run selected experiment first move to its directory:
```bash
cd ./src/experiment/{SELECTED_EXPERIMENT_DIR}
```
Then run following command:
```
python3 ./main.py
```
or 
```bash
python ./main.py
```
Experiment results will be produced to directory: `./src/experiment/{SELECTED_EXPERIMENT_DIR}/results/`. 

## Results and their structure

Calculated results could be found in directory: `./results`. It four subdirectories:
* classifications - results for classification problem,
* regression - results for regression problem,
* survival - results for survival problem,
* notebooks - jupyter notebooks for easy analysis of the results.

In each of this directories there are subdirectories for:
* decision_tree - results of the baseline Decision Tree Model
* min_supp_X - results of experiments with specified minimal support value.

> Minimal support was used to found frequent item sets using FP Growth algorithm to search for possible M-of-N conditions candidates.

The directory structure of the collected results is as follows:
```
results/*/
├─ dataset_1/no_discretization/
│  ├─ plain/
│  │  ├─ cv/
│  │  │  ├─ 1
│  │  │  │  ├─ rules
|  |  |  |     ├─ rules.txt <-- rules for specific CV fold
│  │  │  │  ├─ metrics.csv <-- metrics for specific CV fold
|  |  |  ...
│  │  │  ├─ 10
│  │  ├─ full_dataset
|  |  |  ├─ rules
|  |  |  |  ├─ rules.txt <-- rules trained on whole data set
|  |  |  ├─ metrics.csv <-- metrics for model trained on whole data set
│  │  ├─ cv_metrics.csv <-- concatenated metrics for all CV folds
│  │  ├─ metrics.csv <-- metrics aggregated for all CV folds
│  ├─ complex/
│  ├─ excact_M-of-N/
│  ├─ at_least_M-of-N/
|  ...
├─ dataset_N/no_discretization/
├─ metrics.csv <-- aggregated metrics for all datasets
```

The root directory contains metrics.csv file with all datasets results suitable for easy analysis. It also contains directories with the results of every evaluated dataset. Those folders contain three subdirectories for every tested variant:

* plain - original RuleKit implementations with no complex conditions
* complex - complex conditions:
    * negated conditions e.g. `Color != {red}` or `Age != <18, 35)`
    * attributes relation conditions e.g. `NumberRows < NumberCols` or `NumberRows = NumberCols`
    * internal disjunctions e.g. `Color = {red, green, black}` or `(Age = <18, 34) OR Age = <45, 60))`
* excact_M-of-N - all previously mentioned complex conditions + exact M-of-N conditions (exact 2-of-3) e.g.  `2-of-3(Degree = {Bachelor's}, Age < 35, Gender = Male)`
* at_least_M-of-N - all previously mentioned complex conditions + at least M-of-N conditions (at least 2-of-3) e.g.  `2-of-3(Degree = {Bachelor's}, Age < 35, Gender = Male)`

## Data availability

### Classification datasets

* anneal: [https://archive.ics.uci.edu/ml/datasets/Annealing](https://archive.ics.uci.edu/ml/datasets/Annealing)
* auto-mpg: [https://archive.ics.uci.edu/ml/datasets/auto+mpg](https://archive.ics.uci.edu/ml/datasets/auto+mpg)
* autos: [https://archive.ics.uci.edu/ml/datasets/Automobile](https://archive.ics.uci.edu/ml/datasets/Automobile)
* balance-scale: [https://archive.ics.uci.edu/ml/datasets/balance+scale](https://archive.ics.uci.edu/ml/datasets/balance+scale)
* bupa-liver-disorders: [https://archive.ics.uci.edu/ml/datasets/liver+disorders](https://archive.ics.uci.edu/ml/datasets/liver+disorders)
* car: [https://archive.ics.uci.edu/ml/datasets/Car+Evaluation](https://archive.ics.uci.edu/ml/datasets/Car+Evaluation)
* cleveland: [https://archive.ics.uci.edu/ml/datasets/heart+disease](https://archive.ics.uci.edu/ml/datasets/heart+disease)
* cylinder-bands: [https://archive.ics.uci.edu/ml/datasets/Cylinder+Bands](https://archive.ics.uci.edu/ml/datasets/Cylinder+Bands)
* echocardiogram: [https://archive.ics.uci.edu/ml/datasets/Echocardiogram](https://archive.ics.uci.edu/ml/datasets/Echocardiogram)
* ecoli: [https://archive.ics.uci.edu/ml/datasets/ecoli](https://archive.ics.uci.edu/ml/datasets/ecoli)
* flag: [https://archive.ics.uci.edu/ml/datasets/Flags](https://archive.ics.uci.edu/ml/datasets/Flags)
* glass: [https://archive.ics.uci.edu/ml/datasets/glass+identification](https://archive.ics.uci.edu/ml/datasets/glass+identification)
* hayes-roth: [https://archive.ics.uci.edu/ml/datasets/Hayes-Roth](https://archive.ics.uci.edu/ml/datasets/Hayes-Roth)
* heart-c: [https://archive.ics.uci.edu/ml/datasets/Heart+Disease](https://archive.ics.uci.edu/ml/datasets/Heart+Disease)
* heart-statlog: [https://archive.ics.uci.edu/ml/datasets/statlog+(heart)](https://archive.ics.uci.edu/ml/datasets/statlog+(heart))
* hepatitis: [https://archive.ics.uci.edu/ml/datasets/hepatitis](https://archive.ics.uci.edu/ml/datasets/hepatitis)
* iris: [https://archive.ics.uci.edu/ml/datasets/iris](https://archive.ics.uci.edu/ml/datasets/iris)
* lymphography: [https://archive.ics.uci.edu/ml/datasets/Lymphograph](https://archive.ics.uci.edu/ml/datasets/Lymphograph)
* monk-1: [https://archive.ics.uci.edu/ml/datasets/MONK's+Problems](https://archive.ics.uci.edu/ml/datasets/MONK's+Problems)
* monk-2: [https://archive.ics.uci.edu/ml/datasets/MONK's+Problems](https://archive.ics.uci.edu/ml/datasets/MONK's+Problems)
* monk-3: [https://archive.ics.uci.edu/ml/datasets/MONK's+Problems](https://archive.ics.uci.edu/ml/datasets/MONK's+Problems)
* mushroom: [https://archive.ics.uci.edu/ml/datasets/mushroom](https://archive.ics.uci.edu/ml/datasets/mushroom)
* nursery: [https://archive.ics.uci.edu/ml/datasets/nursery](https://archive.ics.uci.edu/ml/datasets/nursery)
* sonar: [http://archive.ics.uci.edu/ml/datasets/connectionist+bench+(sonar,+mines+vs.+rocks)](http://archive.ics.uci.edu/ml/datasets/connectionist+bench+(sonar,+mines+vs.+rocks))
* tic-tac-toe: [https://archive.ics.uci.edu/ml/datasets/Tic-Tac-Toe+Endgame](https://archive.ics.uci.edu/ml/datasets/Tic-Tac-Toe+Endgame)
* titanic: [https://www.kaggle.com/c/titanic](https://www.kaggle.com/c/titanic)
* vote: [https://archive.ics.uci.edu/ml/datasets/congressional+voting+records](https://archive.ics.uci.edu/ml/datasets/congressional+voting+records)
* wine: [https://archive.ics.uci.edu/ml/datasets/wine](https://archive.ics.uci.edu/ml/datasets/wine)
* zoo: [https://archive.ics.uci.edu/ml/datasets/zoo][(https://archive.ics.uci.edu/ml/datasets/zoo)]


### Regression datasets

* auto-mpg: [https://archive.ics.uci.edu/dataset/9/auto+mpg](https://archive.ics.uci.edu/dataset/9/auto+mpg)
* auto-price: [https://archive.ics.uci.edu/dataset/10/automobile](https://archive.ics.uci.edu/dataset/10/automobile)
* auto93: 1993 New Car Data [https://www.openintro.org/data/index.php?data=cars93](https://www.openintro.org/data/index.php?data=cars93)
* bodyfat: [https://www.kaggle.com/datasets/fedesoriano/body-fat-prediction-dataset](https://www.kaggle.com/datasets/fedesoriano/body-fat-prediction-dataset)
* bolts: [https://lib.stat.cmu.edu/datasets/bolts](https://lib.stat.cmu.edu/datasets/bolts)
* breasttumor: [https://archive.ics.uci.edu/dataset/14/breast+cancer](https://archive.ics.uci.edu/dataset/14/breast+cancer)
* cholesterol: [https://www.openml.org/d/204](https://www.openml.org/d/204)
* cloud: [https://www.kaggle.com/datasets/mathurinache/cloud-dataset](https://www.kaggle.com/datasets/mathurinache/cloud-dataset)
* concrete: [https://archive.ics.uci.edu/dataset/165/concrete+compressive+strength](https://archive.ics.uci.edu/dataset/165/concrete+compressive+strength)
* cpu: [https://www.openml.org/d/561](https://www.openml.org/d/561)
* dee: [https://sci2s.ugr.es/keel/dataset/data/regression/dee-names.txt](https://sci2s.ugr.es/keel/dataset/data/regression/dee-names.txt)
* diabetes: [https://archive.ics.uci.edu/dataset/34/diabetes](https://archive.ics.uci.edu/dataset/34/diabetes)
* echomonths: [https://archive.ics.uci.edu/dataset/38/echocardiogram](https://archive.ics.uci.edu/dataset/38/echocardiogram)
* elusage: [https://pages.stern.nyu.edu/~jsimonof/SmoothMeth/Data/Tab/](https://pages.stern.nyu.edu/~jsimonof/SmoothMeth/Data/Tab/)
* fishcatch: [https://jse.amstat.org/datasets/fishcatch.txt](https://jse.amstat.org/datasets/fishcatch.txt)
* fruitfly: [https://www.tandfonline.com/doi/full/10.1080/10691898.1994.11910467](https://www.tandfonline.com/doi/full/10.1080/10691898.1994.11910467)
* gascons: [https://www.openml.org/d/226](https://www.openml.org/d/226)
* kidney: [https://archive.ics.uci.edu/dataset/336/chronic+kidney+disease](https://archive.ics.uci.edu/dataset/336/chronic+kidney+disease)
* lowbwt: [https://www.rdocumentation.org/packages/boot/versions/1.2-10/topics/birthwt](https://www.rdocumentation.org/packages/boot/versions/1.2-10/topics/birthwt)
* machine: [https://archive.ics.uci.edu/dataset/29/computer+hardware](https://archive.ics.uci.edu/dataset/29/computer+hardware)
* mbagrade: [https://www.openml.org/d/190](https://www.openml.org/d/190)
* ozone: [https://archive.ics.uci.edu/dataset/172/ozone+level+detection](https://archive.ics.uci.edu/dataset/172/ozone+level+detection)
* pharynx: [https://www.openml.org/d/213](https://www.openml.org/d/213)
* pollution: [https://www.openml.org/d/542](https://www.openml.org/d/542)
* pwlinear: [https://www.openml.org/search?type=data&id=721](https://www.openml.org/search?type=data&id=721)
* pyrim: The data are described in: King, Ross .D., Muggleton,
 Steven., Lewis, Richard. and Sternberg, Michael.J.E. Drug Design by
 machine learning: the use of inductive logic programming to model the
 structure-activity relationships of trimethoprim analogues binding to
 dihydrofolate reductase. Source: [http://www.ncc.up.pt/~ltorgo/Regression/DataSets.html](http://www.ncc.up.pt/~ltorgo/Regression/DataSets.html)
* servo [https://archive.ics.uci.edu/dataset/87/servo](https://archive.ics.uci.edu/dataset/87/servo)
* strike: [https://lib.stat.cmu.edu/datasets/strikes](https://lib.stat.cmu.edu/datasets/strikes) 
* veteran: [https://lib.stat.cmu.edu/datasets/veteran](https://lib.stat.cmu.edu/datasets/veteran)

### Survival datasets

* actg320 (HIV-infected patients): [ftp://ftp.wiley.com/public/sci_tech_med/survival](ftp://ftp.wiley.com/public/sci_tech_med/survival)
* bmt-ch (bone marrow transplant): https://github.com/adaa-polsl/GuideR/blob/master/datasets/bmt/bone-marrow.arff
* cancer (advanced lung cancer patients): survival R package
* follic (follicular cell lymphoma patients): randomForestSRC R package
* GBSG2 (node-positive breast cancer patients): TH.data R package
* hd (Hodgkin's disease patients): randomForestSRC R package
* lung (early detection of lung cancer): [​https://www.stats.ox.ac.uk/pub/datasets/csb](https://www.stats.ox.ac.uk/pub/datasets/csb)
* Melanoma (malignant melanoma patients after radical operation): riskRegression R package
* mgus (patients with monoclonal gammopathy of undetermined significance): survival R package
* pbc (primary biliary cirrhosis of the liver): survival R package
* std (occurrence of sexually transmitted diseases): KMsurv R package
* uis (drug abuse reduction): quantreg R package
* wcgs (occurrence of coronary heart disease): epitools R package
* whas1 (myocardial infarction patients, 1st book edition): [​ftp://ftp.wiley.com/public/sci_tech_med/survival](ftp://ftp.wiley.com/public/sci_tech_med/survival)
* whas500 (myocardial infarction patients, 2nd book edition): [​ftp://ftp.wiley.com/public/sci_tech_med/survival](ftp://ftp.wiley.com/public/sci_tech_med/survival)
* zinc (esophageal cancer): NestedCohort R package