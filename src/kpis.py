import os
from dotenv import load_dotenv

import datetime
import numpy as np
import pandas as pd

from functools import wraps
from typing import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class KPI:
    name: str
    description: str
    required_columns: tuple[str, ...]
    calculate: Callable


class KPIError(Exception):
    pass

def _validate_columns(kpi_name: str, df: pd.DataFrame, required_columns: tuple[str, ...]) -> None:
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise KPIError(
            f"KPI {kpi_name} requer {missing_columns}, que não foram encontradas no dataset."
        )

# decorator
def with_column_validation(kpi_name, required_columns):
    def decorator(fn):
        @wraps(fn)
        def wrapped(df):
            _validate_columns(kpi_name, df, required_columns)
            return fn(df)                                      
        return wrapped
    return decorator


@with_column_validation(
        kpi_name="time survey administration",
        required_columns=("Submitted at")
)
def _time_survey_administration(df):

    first_sub = pd.to_datetime(df["Submitted at"].min())
    today_day = datetime.datetime.now()

    days_till_now = (today_day-first_sub).days
    weeks_till_now = (today_day-first_sub).days//7 + 1

    day_submission = df["Submitted at"].apply(lambda x: (pd.to_datetime(x)-first_sub).days).values
    week_submission = df["Submitted at"].apply(lambda x: (pd.to_datetime(x)-first_sub).days//7 + 1).values

    day_group = df.groupby(day_submission).size().sort_index()
    day_group.index.name = "days"
    day_group.name = "submissions"

    week_group = df.groupby(week_submission).size().sort_index()
    week_group.index.name = "weeks"
    week_group.name = "submissions"

    return {
        "days untill now ": days_till_now, 
        "weeks untill now": weeks_till_now,
        "submissions by day": day_group,
        "submissions by weeks": week_group
        }


@with_column_validation(
        kpi_name="submissions groupped by city",
        required_columns=("Selecione o seu município")
)
def _survey_responses_by_city(df):
    
    city_group = df.groupby(df["Selecione o seu município"]).size().sort_index()
    city_group.index.name = "city"
    city_group.name = "submissions"

    return {"submissions by city": city_group}


@with_column_validation(
        kpi_name="vag and cadunico distribution",
        required_columns=(
            "Você é inscrito no programa CadÚnico?",
            "Nos últimos meses, você teve medo da comida da sua casa acabar antes de ter dinheiro para comprar mais?",
            "Nos últimos meses, você sentiu fome e não comeu por falta de dinheiro?"
            )
)
def _vag_cadunico(df):

    cond_q6 = df[
        'Nos últimos meses, você teve medo da comida da sua casa acabar antes de ter dinheiro para comprar mais?'
        ].isin(['Sim, tive medo da comida acabar'])
    cond_q5 = df[
        'Nos últimos meses, você sentiu fome e não comeu por falta de dinheiro?'
        ].isin(['Sim, deixei de comer por falta de dinheiro'])

    vag = (cond_q5 & cond_q6).sum()

    cond_q1 = df[
        'Você é inscrito no programa CadÚnico?'
    ].isin(['Sim, sou inscrito'])

    cadunico = cond_q1.sum()

    cadunico_vag = (cond_q1 & cond_q5 & cond_q6).sum()

    return {
        "beneficiaries on vag": int(vag),
        "beneficiaries registered on cadunico": int(cadunico),
        "beneficiaries registered on cadunico on vag": int(cadunico_vag)
    }


@with_column_validation(
        kpi_name="beneficiaries consistency of access",
        required_columns=(
            "Você é inscrito no programa CadÚnico?",
            "Nos últimos meses, você teve medo da comida da sua casa acabar antes de ter dinheiro para comprar mais?",
            "Nos últimos meses, você sentiu fome e não comeu por falta de dinheiro?",
            "Com que frequência você consegue receber alguma refeição do programa Tá Na Mesa?"
        )
)
def _consistenfy_of_access(df):

    cond_q6 = df[
        'Nos últimos meses, você teve medo da comida da sua casa acabar antes de ter dinheiro para comprar mais?'
        ].isin(['Sim, tive medo da comida acabar'])
    cond_q5 = df[
        'Nos últimos meses, você sentiu fome e não comeu por falta de dinheiro?'
        ].isin(['Sim, deixei de comer por falta de dinheiro'])

    vag_df = df[cond_q5 & cond_q6]
    not_vag_df = df[~(cond_q5 & cond_q6)]

    vag_consistency = vag_df.groupby(df[
        "Com que frequência você consegue receber alguma refeição do programa Tá Na Mesa?"
        ]).size().sort_index()

    not_vag_consistency = not_vag_df.groupby(df[
        "Com que frequência você consegue receber alguma refeição do programa Tá Na Mesa?"
        ]).size().sort_index()

    return {
        "beneficiaries on vag consistency of access": vag_consistency,
        "beneficiaries NOT on vag consistency of access": not_vag_consistency
    }


@with_column_validation(
        kpi_name="program dependency",
        required_columns=(
            "Sem o programa Tá Na Mesa, você continua se alimentando normalmente?",
            "Contando com a refeição distribuída pelo programa Tá Na Mesa, quantas refeições você faz por dia?"
        )
)
def _program_dependency(df):

    cond_q6 = df[
        "Nos últimos meses, você teve medo da comida da sua casa acabar antes de ter dinheiro para comprar mais?"
        ].isin(["Sim, tive medo da comida acabar"])
    cond_q5 = df[
        "Nos últimos meses, você sentiu fome e não comeu por falta de dinheiro?"
        ].isin(["Sim, deixei de comer por falta de dinheiro"])

    cond_q9 = df[
        "Sem o programa Tá Na Mesa, você continua se alimentando normalmente?"
        ].isin(["Não, dependo totalmente da refeição servida pelo programa"])
    cond_q10 = df[
        "Contando com a refeição distribuída pelo programa Tá Na Mesa, quantas refeições você faz por dia?"
        ].isin([
            "Faço apenas a refeição servida pelo programa",
            "Faço apenas 2(duas) refeições por dia, contando com a refeição servida pelo programa"
        ])

    dependents = (cond_q9 & cond_q10).sum()
    not_dependents = (~(cond_q9 & cond_q10)).sum()

    dependents_on_vag = ((cond_q9  & cond_q10) & (cond_q5 & cond_q6)).sum()
    
    return {
        "program dependents": int(dependents),
        "program NOT dependents": int(not_dependents),
        "program dependents on vag": int(dependents_on_vag)
    }


@with_column_validation(
        kpi_name="families dependency",
        required_columns=(
            "Quantas pessoas moram com você?",
            "As refeições do programa Tá Na Mesa servem todas as pessoas da sua casa?"
        )
)
def _assisted_families(df):

    family_serving = df.groupby(df[
        "As refeições do programa Tá Na Mesa servem todas as pessoas da sua casa?"
               ]).size().sort_index
    
    cond_q8 = df[
        "As refeições do programa Tá Na Mesa servem todas as pessoas da sua casa?"
        ].isin(["Sim, servem todas as pessoas"])
    
    families_tot_served_config = df[cond_q8].groupby(df[
        "Quantas pessoas moram com você?"
        ]).size().sort_index()

    return {
        "residence program serving": family_serving,
        "entire served family configurantion": families_tot_served_config
    }


if __name__ == "__main__":
    load_dotenv(override=True)
    df=pd.read_csv(os.getenv("CLEANED_DATA_PATH"))
    
    print(_assisted_families(df))