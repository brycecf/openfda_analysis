from openfda.api import QuestionOneData
import click
from click.exceptions import BadArgumentUsage
import fire
import json


def cli(question_num):
    click.secho(f"Retrieving data for {question_num}...", fg="yellow")
    if question_num == 1:
        get_question_one_data()
    elif question_num == 2:
        get_question_two_data()
    elif question_num == 3:
        get_question_three_data()
    else:
        error_msg = (
            f"CLI arg for `question_num` must be >=1 and <=3. Received {question_num}"
        )
        raise BadArgumentUsage(error_msg)
        click.secho(error_msg, fg="red")
        raise click.Abort
    click.secho(f"Data retrieved for {question_num}", fg="green")


def get_question_one_data():
    q1_data = QuestionOneData()

    all_countries = q1_data.get_all_occur_countries()
    click.secho("Retrieved all occurring countries", fg="green")
    save_data_to_file(all_countries, "all_occur_countries.json")

    all_patient_reactions = q1_data.get_all_patient_reactions()
    click.secho("Retrieved all patient reactions", fg="green")
    save_data_to_file(all_patient_reactions, "all_patient_reactions.json")


def get_question_two_data():
    pass


def get_question_three_data():
    pass


def save_data_to_file(json_obj, output_path):
    click.secho(f"Writing JSON object to {output_path}", fg="yellow")
    with open(output_path, "w") as output_file:
        json.dump(json_obj, output_file)
    click.secho(f"Wrote JSON object to {output_path}", fg="green")


def main():
    fire.Fire(cli)
