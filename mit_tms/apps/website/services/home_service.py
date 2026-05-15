from website.models.page import Page


def get_home_page():

    return (
        Page.objects
        .prefetch_related("sections")
        .get(page_type="HOME")
    )
