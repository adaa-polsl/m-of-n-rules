import pandas as pd
import plotly.express as px
from glob import glob
import os
from IPython.core.display import HTML
import plotly.graph_objects as go
from lifelines import KaplanMeierFitter

VARIANTS = [
    'plain',
    'complex',
    'at_least_M-of-N',
    'exact_M-of-N',
]


def _get_results_base_path(dataset_name: str, cv_fold: int, variant: str) -> str:
    return f'../../CASE_STUDY/{dataset_name}/no_discretization/{variant}/cv/{str(cv_fold)}'


def _get_rules_metrics(results_base_path: str) -> pd.DataFrame:
    return pd.read_csv(f'{results_base_path}/metrics.csv')


def _read_rules(results_base_path: str) -> list[str]:
    with open(f'{results_base_path}/rules/rules.txt', 'r') as file:
        lines = file.readlines()
        results = ''
        start_reading = False
        for line in lines:
            if '_____' in line:
                start_reading = True
            if start_reading:
                results += line
        return results


def _read_rules_estimators(results_base_path: str) -> list[tuple[str, pd.DataFrame]]:
    rules_estimators = []
    paths = glob(f'{results_base_path}/rules/estimators/r*.csv')
    n_rules = len(paths)
    for i in range(1, n_rules + 1):
        r_name = f'r{i}'
        rules_estimators.append((r_name, pd.read_csv(
            f'{results_base_path}/rules/estimators/r{i}.csv')))
    return rules_estimators


def _fit_kaplan_meier_on_full_dataset(dataset_name: str, cv_fold: int) -> pd.DataFrame:
    df = pd.read_parquet(
        f'../../datasets/survival/{dataset_name}/cv/{str(cv_fold)}/train.parquet'
    )
    kmf = KaplanMeierFitter()
    kmf.fit(df['survival_time'], df['survival_status'],
            label='Kaplan Meier Estimate')
    return kmf.survival_function_


def _make_plot(kaplan_meier: pd.DataFrame, rules_estimators: list):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=kaplan_meier.index,
        y=kaplan_meier['Kaplan Meier Estimate'],
        name='Kaplan Meier Estimate')
    )
    for rule_name, rule_estimator in rules_estimators:
        fig.add_trace(go.Scatter(
            x=rule_estimator['time'], y=rule_estimator['probability'],
            name=rule_name, line_shape='hv'
        ))
    fig.show()


def show_results_for_folds(dataset_name: str):
    for cv_fold in range(1, 11):
        display(HTML(f'<h3>Fold: {cv_fold}</h3>'))
        metrics = pd.concat([
            _get_rules_metrics(_get_results_base_path(
                dataset_name, cv_fold, variant))
            for variant in VARIANTS
        ])
        display(metrics)


def plot_survival_curves(dataset_name: str, cv_fold: int):
    kaplan_meier: pd.DataFrame = _fit_kaplan_meier_on_full_dataset(
        dataset_name, cv_fold
    )
    metrics = pd.concat([
        _get_rules_metrics(_get_results_base_path(
            dataset_name, cv_fold, variant))
        for variant in VARIANTS
    ])
    display(metrics)
    for variant in VARIANTS:
        display(HTML(f'<h3>{variant} fold: {cv_fold}</h3>'))
        results_base_path: str = _get_results_base_path(
            dataset_name, cv_fold, variant
        )
        rules_estimators = _read_rules_estimators(
            results_base_path
        )
        rules: str = _read_rules(
            results_base_path
        )
        _make_plot(kaplan_meier, rules_estimators)
        print(rules)
