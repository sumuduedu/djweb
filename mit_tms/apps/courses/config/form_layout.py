COURSE_FORM_LAYOUT = [

    ("Basic Information", [
        "title",
        "code",
        "description",
        "status",
    ]),

    ("Academic Structure", [
        "level",
        "entry_qualification",
        "curriculum_category",
        "curriculum_availability",
        "equivalent_course",
        "industry",
        "ncs",
    ]),

    ("Delivery", [
        "delivery_mode",
        "course_mode",
        "medium",
    ]),

    ("Duration & Hours", [
        "duration_months",
        "theory_hours",
        "practical_hours",
        "assignment_hours",
        "ojt_months",
    ]),

    ("Capacity", [
        "batches_per_year",
        "students_per_batch",
    ]),

    ("Financial", [
        "is_free",
        "course_fee",
        "fee_includes",
    ]),

    ("Physical Resources", [
        "physical_resources",
    ]),

    ("Resource Details", [
        "tools_available",
        "equipment_available",
        "machinery_available",
    ]),

    ("NVQ Details", [
        "nvq_level",
        "qualification_code",
    ]),

    ("Pedagogy", [
        "prerequisite",
        "learning_outcomes",
    ]),
]

RELATION_LAYOUT = [
    {
        "name": "learning_resources",
        "label": "Learning Resources",
        "fields": ["name", "type", "file", "url", "description"],
        "allow_add": True
    }
]
