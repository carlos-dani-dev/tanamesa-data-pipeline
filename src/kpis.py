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


@with_column_validation(
        kpi_name="difficulty of access",
        required_columns=(
            "Nos últimos meses, você teve medo da comida da sua casa acabar antes de ter dinheiro para comprar mais?",
            "Nos últimos meses, você sentiu fome e não comeu por falta de dinheiro?",    
            "Você mora na zona urbana da cidade ou na zona rural da cidade?",
            "Você sente que tipo de dificuldade para chegar ao restaurante?"
        )
)
def _local_access(df):

    cond_q6 = df[
        "Nos últimos meses, você teve medo da comida da sua casa acabar antes de ter dinheiro para comprar mais?"
        ].isin(["Sim, tive medo da comida acabar"])
    cond_q5 = df[
        "Nos últimos meses, você sentiu fome e não comeu por falta de dinheiro?"
        ].isin(["Sim, deixei de comer por falta de dinheiro"])

    vag = df[(cond_q5 & cond_q6)]

    vag_by_difficulty_of_access = vag.groupby(df[
        "Você sente dificuldade para chegar ao restaurante?"
        ]).size().sort_index()
    
    cond_q17 = df[
        "Você mora na zona urbana da cidade ou na zona rural da cidade?"
        ].isin(["Moro na zona urbana"])

    urban_df = df[cond_q17]
    rural_df = df[~cond_q17]

    acces_urban_region = urban_df.groupby(
        "Você sente que tipo de dificuldade para chegar ao restaurante?"
        ).size().sort_index()

    acces_rural_region = rural_df.groupby(
        "Você sente que tipo de dificuldade para chegar ao restaurante?"
        ).size().sort_index()

    return  {
        "beneficiaries on vag by difficulty of access": vag_by_difficulty_of_access,
        "difficulty of access by region (urban)": acces_urban_region,
        "difficulty of access by region (rural)": acces_rural_region
    }


@with_column_validation(
        kpi_name="beneficiaries queue awaiting",
        required_columns=(
            "Nos últimos meses, você teve medo da comida da sua casa acabar antes de ter dinheiro para comprar mais?",
            "Nos últimos meses, você sentiu fome e não comeu por falta de dinheiro?",    
            "Você já esperou na fila e mesmo assim ficou sem receber a refeição?"
        )
)
def _beneficiaries_not_eating(df):

    cond_q22 = df[
        "Você já esperou na fila e mesmo assim ficou sem receber a refeição?"
        ].isin(["Raramente entro na fila e não recebo a refeição", "Frequentemente entro na fila e não recebo a refeição"])

    eating = len(df[~(cond_q22)])
    not_eating = len(df[cond_q22])

    cond_q6 = df[
        "Nos últimos meses, você teve medo da comida da sua casa acabar antes de ter dinheiro para comprar mais?"
        ].isin(["Sim, tive medo da comida acabar"])
    cond_q5 = df[
        "Nos últimos meses, você sentiu fome e não comeu por falta de dinheiro?"
        ].isin(["Sim, deixei de comer por falta de dinheiro"])

    vag_not_eating = len(df[((cond_q5 & cond_q6) & (cond_q22))])
    not_vag_not_eating = len(df[( (~(cond_q5 & cond_q6)) & (cond_q22) )])

    return {
        "await and eat": eating,
        "await and NOT eat": not_eating,
        "await and NOT eat on vag": vag_not_eating,
        "await and NOT eat NOT on vag": not_vag_not_eating
    }


@with_column_validation(
        kpi_name="menu sugestion",
        required_columns=(
            "Você já tentou sugerir alguma mudança ao cardápio do restaurante?",
            "Quando você não gosta do cardápio do dia, o que você faz com a refeição?",
            "Você já deixou de comer alguma refeição do programa Tá Na Mesa por que não gostou do cardápio do dia?",
            "As refeições ofertadas diariamente são variadas?",
            "Em que momento você descobre o cardápio que será servido no dia?"
        )
)
def _restaurant_menu(df):

    menu_sugestion = df.groupby(df["Você já tentou sugerir alguma mudança ao cardápio do restaurante?"]).size().sort_index()

    daily_menu_realization = df.groupby(
        df["Em que momento você descobre o cardápio que será servido no dia?"]).size().sort_index()

    varied_menu = df.groupby(
        df["As refeições ofertadas diariamente são variadas?"]).size().sort_index()

    menu_satisfaction = df.groupby(
        df["Você já deixou de comer alguma refeição do programa Tá Na Mesa por que não gostou do cardápio do dia?"]
    ).size().sort_index()

    action_if_dont_like_food = df.groupby(
        "Quando você não gosta do cardápio do dia, o que você faz com a refeição?"
    ).size().sort_index()

    return {
        "menu change sugestions": menu_sugestion,
        "daily menu realization": daily_menu_realization,
        "menu variety": varied_menu,
        "menu satisfaction": menu_satisfaction,
        "when beneficiary didnt like the food served": action_if_dont_like_food
    }


@with_column_validation(
        kpi_name="restaurant operationalization",
        required_columns=(
            "Você sabe quantas refeições o restaurante pode servir todo dia?",
            "A pessoa que recebe o seu pagamento também entrega a sua refeição ao mesmo tempo?",
            "O restaurante é identificado como parte do programa Tá Na Mesa?"
        )
)
def _restaurant_op(df):

    bene_knows_food_qtt = df.groupby(df["Você sabe quantas refeições o restaurante pode servir todo dia?"]).size().sort_index

    payment_serving_separation = df.groupby(df[
        "A pessoa que recebe o seu pagamento também entrega a sua refeição ao mesmo tempo?"
        ]).size().sort_index()

    restaurant_program_signposted = df.groupby(df[
        "O restaurante é identificado como parte do programa Tá Na Mesa?"
    ]).size().sort_index()

    return {
        "Beneficiary knows maximun dairy food served": bene_knows_food_qtt,
        "Payment and serving separation": payment_serving_separation,
        "restaurant program signposted": restaurant_program_signposted
    }


@with_column_validation(
        kpi_name="restaurant cleaning",
        required_columns=(
            "Em relação à limpeza do restaurante, qual a sua opinião?"
        )
)
def _restaurant_cleaning(df):

    return {
        "restaurant cleaning":
        df.groupby(df["Em relação à limpeza do restaurante, qual a sua opinião?"]).size().sort_index()
    }


@with_column_validation(
        kpi_name="cold food",
        required_columns=(
            "Você já recebeu sua refeição fria?"
        )
)
def _cold_food(df):

    return {
        "cold food":
        df.groupby(df["Você já recebeu sua refeição fria?"]).size().sort_index()
    }


@with_column_validation(
        kpi_name="package integrity",
        required_columns=(
            "Você já recebeu refeições servidas em embalagens danificadas ou sujas?"
        )
)
def _packaging_integrity(df):

    return {
        "package integrity":
        df.groupby(df[
            "Você já recebeu refeições servidas em embalagens danificadas ou sujas?"
            ]).size().sort_index()
    }


@with_column_validation(
        kpi_name="food integrity",
        required_columns=(
            "Você já percebeu alguma refeição estragada?"
        )
)
def _food_integrity(df):
    
    return {
        "food integrity":
        df.groupby(df[
            "Você já percebeu alguma refeição estragada?"
        ]).size().sort_index()
    }


@with_column_validation(
        kpi_name="time on queue",
        required_columns=(
            "Nos últimos meses, você teve medo da comida da sua casa acabar antes de ter dinheiro para comprar mais?",
            "Nos últimos meses, você sentiu fome e não comeu por falta de dinheiro?",
            #"Quanto tempo você espera na fila para receber a sua refeição?"
        )
)
def _time_on_queue(df):

    time_on_queue = df.groupby(df["Quanto tempo você espera na fila para receber a sua refeição?"])

    sum = 0
    for name, group in time_on_queue:
        if "Não preciso" in name: sum += len(group)*0.25
        if "até 30" in name: sum += len(group)*0.5
        if "de 30" in name: sum += len(group)*0.75
        if "de 1(uma)" in name: sum += len(group)*1.5
        if "por mais de 2(duas)" in name: sum += len(group)

    cond_q20 = df[
        "Quanto tempo você espera na fila para receber a sua refeição?"
    ].isin(["Não preciso esperar, recebo a refeição rapidamente"])

    cond_q6 = df[
        "Nos últimos meses, você teve medo da comida da sua casa acabar antes de ter dinheiro para comprar mais?"
        ].isin(["Sim, tive medo da comida acabar"])
    cond_q5 = df[
        "Nos últimos meses, você sentiu fome e não comeu por falta de dinheiro?"
        ].isin(["Sim, deixei de comer por falta de dinheiro"])

    vag_not_waiting = len(df[((cond_q5 & cond_q6) & (cond_q20))])
    not_vag_not_waiting = len(df[( (~(cond_q5 & cond_q6)) & (cond_q20) )])

    return {
        "average time on queue": (sum/len(df))*60,
        "time on queue":
            time_on_queue.size().sort_index(),
        "beneficiaries not waiting on vag": vag_not_waiting,
        "beneficiaries not waiting not on vag": not_vag_not_waiting
    }

@with_column_validation(
        kpi_name="difficulty on waiting for food",
        required_columns=(
            "Você sente alguma dificuldade enquanto espera pela sua refeição?"
        )
)
def _difficulty_on_waiting(df):

    return {
        "difficulty on waiting":
            df.groupby(df["Você sente alguma dificuldade enquanto espera pela sua refeição?"]).size().sort_index()
    }


@with_column_validation(
        kpi_name="difficulty on waiting for food",
        required_columns=(
            "Para uma única pessoa, a quantidade de comida das refeições é suficiente?",
            "A quantidade de carne, frango ou peixe servida nas refeições é suficiente?",
            "Levando em conta todas as refeições que você já recebeu durante o programa Tá Na Mesa, como você avalia o sabor das refeições?",
            "Em relação a todo o programa Tá Na Mesa, qual o seu nível de satisfação?",
            "Na sua opinião, o programa Tá Na Mesa precisa ser continuado? "
        )
)
def _program_review(df):

    food_qtt = df.groupby(
        df["Para uma única pessoa, a quantidade de comida das refeições é suficiente?"]
    ).size().sort_index()
    protein_qtt = df.groupby(
        df["A quantidade de carne, frango ou peixe servida nas refeições é suficiente?"]
    ).size().sort_index()
    food_flavor = df.groupby(
        df["Levando em conta todas as refeições que você já recebeu durante o programa Tá Na Mesa, como você avalia o sabor das refeições?"]
    ).size().sort_index()
    program_satisfaction = df.groupby(
        df["Em relação a todo o programa Tá Na Mesa, qual o seu nível de satisfação?"]
    ).size().sort_index()
    program_continuity = df.groupby(
        df["Na sua opinião, o programa Tá Na Mesa precisa ser continuado? "]
    ).size().sort_index()

    return {
        "food quantity review": food_qtt,
        "protein quantity review": protein_qtt,
        "food flavor review": food_flavor,
        "program satisfaction review": program_satisfaction,
        "program_continuity": program_continuity
    }

if __name__ == "__main__":
    load_dotenv(override=True)
    df=pd.read_csv(os.getenv("CLEANED_DATA_PATH"))
    
    print(_time_on_queue(df))