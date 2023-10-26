from tinydb import Query

from compaipair.templates.cli_functions import (
    new_template,
    edit_template,
    show_templates,
)
from compaipair.types.completion_template import CompletionTemplate
from compaipair.utils import get_db, close_db


def test_save_new_template_saves_template_to_db():
    new_template(
        name="Test template",
        priming="You know what's good for you",
        decorator="Don't forget the trash!",
    )

    template = Query()
    test_db = get_db()
    templates_table = test_db.table("templates")
    res = templates_table.get(template.name == "Test template")
    close_db()
    assert (
        res["name"] == "Test template"
        and res["priming"] == "You know what's good for you"
        and res["decorator"] == "Don't forget the trash!"
    )


def test_edit_template_changes_saved_template():
    old_template = CompletionTemplate(
        name="Test template",
        priming="You know what's good for you",
        decorator="Don't forget the trash!",
    )
    old_template.save()

    edit_template("Test template", priming="You don't know what's good for you")

    test_db = get_db()
    template = Query()
    templates_table = test_db.table("templates")
    res = templates_table.get(template.name == "Test template")
    close_db()
    assert (
        res["name"] == "Test template"
        and res["priming"] == "You don't know what's good for you"
        and res["decorator"] == "Don't forget the trash!"
    )


def test_show_templates_shows_available_templates(capsys):
    templates = [
        CompletionTemplate(
            name="test_template_1",
            priming="Test template 1 priming",
            decorator="Test template 2 decorator",
        ),
        CompletionTemplate(
            name="test_template_2",
            priming="Test template 2 priming",
            decorator="Test template 2 decorator",
        ),
    ]
    for template in templates:
        template.save()

    show_templates()

    captured = capsys.readouterr().out.strip()

    assert all(
        [
            expected_text in captured
            for expected_text in ["test_template_1", "test_template_2"]
        ]
    )


def test_show_templates_shows_available_templates(capsys):
    templates = [
        CompletionTemplate(
            name="test_template_1",
            priming="Test template 1 priming",
            decorator="Test template 2 decorator",
        ),
        CompletionTemplate(
            name="test_template_2",
            priming="Test template 2 priming",
            decorator="Test template 2 decorator",
        ),
    ]
    for template in templates:
        template.save()

    show_templates(verbose=True)

    captured = capsys.readouterr().out.strip()

    assert all(
        [
            expected_text in captured
            for expected_text in ["test_template_1", "test_template_2"]
        ]
    )
