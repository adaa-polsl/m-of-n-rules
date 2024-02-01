from logging import getLogger
import os
from pandas.api.types import is_numeric_dtype
from experiments_utils import *
from experiments_utils.results.tables import *
from m_of_n_survival.helpers import *
from m_of_n_survival import config
import pandas as pd
from utils.rulekit.survival import SurvivalRules
from sklearn import metrics
from utils.helpers import (
    calculate_ruleset_conditions,
    ConditionsCounts,
)


def write_rules_to_file(clf: SurvivalRules, file_path: str):
    with open(os.path.join(file_path, 'rules.txt'), 'w+') as f:
        f.write(f'Rules qualities:\n')
        for i, rule in enumerate(clf.model.rules):
            f.write(f'r{i + 1}: {rule.weight}\n')
        f.write(f'________________________________\n')
        for i, rule in enumerate(clf.model.rules):
            f.write(
                f'r{i + 1}: {str(rule)} (p={rule.weighted_p}, n={rule.weighted_n}, P={rule.weighted_P}, N={rule.weighted_N})\n')
    os.makedirs(os.path.join(file_path, 'estimators'), exist_ok=True)
    for i, rule in  enumerate(clf.model.rules):
        times = list(rule._java_object.getEstimator().getTimes())
        probs = [
            rule._java_object.getEstimator().getProbabilityAt(t) for t in times
        ]
        estimator = pd.DataFrame({'time': times, 'probability': probs})
        estimator.to_csv(os.path.join(file_path, 'estimators', f'r{i + 1}.csv'), index=False)

def generate_results(
    experiment_config: ExperimentConfig,
    experiment_models: ExperimentModels,
    experiment_datasets: ExperimentDatasets,
    fold_index: int = None
):
    # zapisanie wyników
    def produce_model_results(
            model_type: str,
            clf: SurvivalRules,
            _X_train: pd.DataFrame,
            _y_train: pd.Series,
            _X_test: pd.DataFrame,
            _y_test: pd.DataFrame) -> dict:

        conditions_counts: ConditionsCounts = calculate_ruleset_conditions(
            clf.model)

        tmp = ' '.join(
            list(map(lambda r: str(r), clf.model.rules)))
        m_of_n_count = tmp.count(f'{config.M}-of-{config.N}')
        getLogger().info(
            f'\n\nWarunki M-of-N pojawiły się: {m_of_n_count} razy w zbiorze reguł'
        )
        if fold_index is not None:
            result_table: Table = Tables.get(
                experiment_config.dataset_name,
                experiment_config.variant,
                model_type,
                'cv',
                str(fold_index),
                'metrics'
            )
        else:
            result_table: Table = Tables.get(
                experiment_config.dataset_name,
                experiment_config.variant,
                model_type,
                'metrics'
            )

        result_table.rows = [
            {
                'model_type': model_type,
                'variant': experiment_config.variant,
                'dataset': experiment_config.dataset_name,
                'M-of-N count': m_of_n_count,

                'integrated_brier_score (train)': clf.score(_X_train, _y_train),
                'integrated_brier_score (test)': clf.score(_X_test, _y_test),

                'rules':  clf.model.stats.rules_count,
                'conditions_count': clf.model.stats.rules_count * clf.model.stats.conditions_per_rule,
                'plain conditions count': conditions_counts.plain / clf.model.stats.rules_count,
                'complex conditions count': conditions_counts.complex / clf.model.stats.rules_count,
                'avg conditions per rule': clf.model.stats.conditions_per_rule,
                'avg rule quality': clf.model.stats.avg_rule_quality,
                'avg rule precision': clf.model.stats.avg_rule_precision,
                'avg rule coverage': clf.model.stats.avg_rule_coverage,
                'training time total (s)': clf.model.stats.time_total_s,
                'training time growing (s)': clf.model.stats.time_growing_s,
                'training time pruning (s)': clf.model.stats.time_pruning_s,

                'pvalue significance fdr': clf.model.calculate_significance_fdr(alpha=0.05)['fraction'],
                'pvalue significance fwer': clf.model.calculate_significance_fwer(alpha=0.05)['fraction'],


                'induction measure': config.DEFAULT_PARAMS_VALUE['induction_measure'].value.replace('Measures.', ''),
                'pruning measure': config.DEFAULT_PARAMS_VALUE['pruning_measure'].value.replace('Measures.', ''),
                'voting measure': config.DEFAULT_PARAMS_VALUE['voting_measure'].value.replace('Measures.', ''),
            }
        ]
        result_table.save()
        rules_base_path: str = os.path.join(
            os.path.dirname(result_table._file_path), 'rules'
        )
        os.makedirs(rules_base_path, exist_ok=True)
        write_rules_to_file(
            clf, os.path.join(rules_base_path, 'rules.txt')
        )
        return result_table

    produce_model_results(
        'plain',
        experiment_models.plain_rules,
        experiment_datasets.X_train,
        experiment_datasets.y_train,
        experiment_datasets.X_test,
        experiment_datasets.y_test
    ),
    produce_model_results(
        'complex',
        experiment_models.complex_rules,
        experiment_datasets.X_train,
        experiment_datasets.y_train,
        experiment_datasets.X_test,
        experiment_datasets.y_test
    ),
    produce_model_results(
        'exact_M-of-N',
        experiment_models.exact_m_of_n_rules,
        experiment_datasets.X_exact_binary_train,
        experiment_datasets.y_train,
        experiment_datasets.X_exact_binary_test,
        experiment_datasets.y_test
    )
    produce_model_results(
        'at_least_M-of-N',
        experiment_models.at_least_m_of_n_rules,
        experiment_datasets.X_at_least_binary_train,
        experiment_datasets.y_train,
        experiment_datasets.X_at_least_binary_test,
        experiment_datasets.y_test
    )


def _string_supporting_mean(col):
    if is_numeric_dtype(col):
        return col.mean()
    else:
        return col.unique()[0] if col.nunique() == 1 else np.NaN


def _string_supporting_std(col):
    if is_numeric_dtype(col):
        return col.std()
    else:
        return col.unique()[0] if col.nunique() == 1 else np.NaN


def aggreage_cv_folds_results(
    dataset: str,
    variant: str,
):
    for model_type in ['plain', 'complex', 'exact_M-of-N', 'at_least_M-of-N']:
        df: pd.DataFrame = pd.concat(
            Tables.query(dataset, variant, model_type, 'cv',
                         '[!f]', 'metrics', as_pandas=True)
        )
        df_summary = df.groupby(['variant', 'model_type']).agg(
            _string_supporting_mean)
        df_std = df.groupby(['variant', 'model_type']).agg(
            _string_supporting_std).reset_index(drop=True)

        df_summary['variant'] = variant
        df_summary['model_type'] = model_type

        columns = []
        for column in df_std.columns.tolist():
            if is_numeric_dtype(df[column]):
                columns.append(column)
                columns.append(f'{column} (std)')
                df_summary[f'{column} (std)'] = df_std[column].tolist()

        summary_results_table = Tables.get(
            dataset, variant, model_type, 'metrics')
        summary_results_table.set_df(df_summary.reset_index(drop=True))
        summary_results_table.save()

        results_table = Tables.get(dataset, variant, model_type, 'cv_metrics')
        results_table.set_df(df)
        results_table.save()
